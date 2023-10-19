from datetime import datetime
from statistics import StatisticsError, mode

from scrapy.spiders import Spider


class Doctoralia(Spider):
    """Recursively crawls doctoralia.com.br and extracts doctor data."""
    name = 'DoctoraliaScraper'
    allowed_domains = ['doctoralia.com.br']
    start_urls = [
        'https://www.doctoralia.com.br/especializacoes-medicas',  # all specializations
        # 'https://www.doctoralia.com.br/ginecologista',  # one specialization
    ]

    def parse(self, response):
        """Recursively follows links to all Doctoralia doctors and extracts data from them."""
        rx, rc, rf = response.xpath, response.css, response.follow_all

        # Looks for the link to each specialization, builds a URL and yields a new
        # request to the pagination links.
        spec_links = rc('.align-items-center .text-muted::attr(href)')
        yield from rf(spec_links, self.parse)

       # Looks for the link to the next page, builds a URL and yields a new
       # request to the next page.
        pagination_links = rx('//a[@aria-label="next"]')
        yield from rf(pagination_links, self.parse)

        # Follow all the links to each talk on the page calling the
        # parse_doctor callback for each of them.
        dr_page_links = rx('//div[@class="media"]/div[@class="pr-1"]//@href')
        links = [l for l in dr_page_links.getall() if '/clinicas/' not in l]
        yield from rf(links, self.parse_doctor)

    def parse_doctor(self, response):
        """Parses the response, extracting the scraped psychologist data as dicts."""
        rx = response.xpath
        # ZLApp.AppConfig
        zr = rx('//script')[6]
        # Google Tag Manager
        gr = rx('//script')[8]

        def parse_price(self, response):
            """Returns most common price from services provided."""
            # get numerical price list
            sp = '//span[@data-id="service-price"]'
            pl = rx(f'//div[@class="media m-0"]{sp}').re("\$\\xa0(.*)")
            pg = (int(p.replace('.', '')) for p in pl)
            # get alternate price list
            vl = rx(f"{sp}/span/text()").getall()
            # get most common price value, giving precedence to numerical price
            try:
                return mode(pg)
            except StatisticsError:
                try:
                    return mode(vl)
                except StatisticsError:
                    return ''

        yield {
            'doctor_id': zr.re_first("DOCTOR_ID:\s(\d+)"),
            'name1': zr.re_first("FULLNAME:\s'(.*?)'"),
            'name2': gr.re_first("doctor\-name'\]\s=\s'(.*?)'"),
            'city1': zr.re_first("NAME:\s'(.*?)'").strip(),
            'city2': gr.re_first("city'\]\s=\s'(.*?)'"),
            'region': gr.re_first("region'\]\s=\s'(.*?)'"),
            'specialization': gr.re_first("specialization'\]\s=\s'(.*?)'"),
            'reviews': rx('//div/meta[@itemprop="reviewCount"]/@content').get(),
            # 'oldest_review_date': min(rx('//time/@datetime').getall(), default=''),
            'newest_review_date': max(rx('//time/@datetime').getall(), default=''),
            'telemedicine': gr.re_first("virtual\-consultation\-profile'\]\s=\s'(.*?)'"),
            'price': parse_price(self, response),
            'url': gr.re_first("\['gtm\-url'\]\s=\s'(.*?)'"),
            'fetch_time': f'{datetime.now():%Y-%m-%dT%H:%M:%S}',
        }
