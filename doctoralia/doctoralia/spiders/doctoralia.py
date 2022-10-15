from statistics import StatisticsError, mode
import json
import scrapy


class Doctoralia(scrapy.Spider):
    """Recursively crawls doctoralia.com.br and extracts doctor data."""
    name = 'DoctoraliaScraper'
    # start_urls = ['https://www.doctoralia.com.br/psicologo']
    start_urls = [
        'https://www.doctoralia.com.br/raquel-navarro/psicologo/manaus',
        'https://www.doctoralia.com.br/fabiana-fuchs/psicologo-psicanalista/rio-de-janeiro',
        'https://www.doctoralia.com.br/pamella-lima/psicologo/sao-paulo',
        'https://www.doctoralia.com.br/ivana-andrade/psicologo/belo-horizonte',
        'https://www.doctoralia.com.br/isabella-gutierres/psicologo/sorocaba',
        'https://www.doctoralia.com.br/anna-gabryella-lopes-coelho/psicologo/goiania',
        ]

    def parse(self, response):
        """Recursively follows links to all Doctoralia doctors and extracts data from them."""

        rx = response.xpath
        # ZLApp.AppConfig
        zr = rx("//script")[6]
        # Google Tag Manager
        gr = rx("//script")[8]
        def parse_price(self, response):
            """Returns most common price from services provided."""
            # get numerical price list
            pl = rx("//div[@class='media m-0']//span[@data-id='service-price']").re('\$\\xa0(.*)')
            pg = (int(p) for p in pl)
            # get alternate price list
            vl = rx("//span[@data-id='service-price']/span/text()").getall()
            # get most common price value, giving precedence to numerical price
            try:
                return mode(pg)
            except StatisticsError:
                try:
                    return mode(vl)
                except StatisticsError:
                    return None

        yield {
            'doctor_id': zr.re_first("DOCTOR_ID:\s(\d+)"),
            'name1': zr.re_first("FULLNAME:\s'(.*?)'"),
            'name2': gr.re_first("doctor\-name'\]\s=\s'(.*?)'"),
            'city': zr.re_first("NAME:\s'(.*?)'").strip(),
            'region': gr.re_first("region'\]\s=\s'(.*?)'"),
            'specialization': zr.re_first("SPECIALIZATION[\s\S]*?NAME:\s'(.*?)'").strip(),
            'reviews': rx("//div/meta[@itemprop='reviewCount']/@content").get(),
            'telemedicine': gr.re_first("virtual\-consultation\-profile'\]\s=\s'(.*?)'"),
            'price': parse_price(self, response),
            'url': gr.re_first("\['gtm\-url'\]\s=\s'(.*?)'"),

        }

        # follow all the links to each talk on the page calling the parse_doctor callback for each of them
        # doctor_page_links = response.xpath("//span[@data-ga-event='click']")
        # yield from response.follow_all(doctor_page_links, self.parse_doctor)

        # looks for the link to the next page, builds a URL and yields a new request to the next page
        # pagination_links = response.xpath("//a[@aria-label='next']")
        # yield from response.follow_all(pagination_links, self.parse)

    
    # def parse_doctor(self, response):
        """Parses the response, extracting the scraped psychologist data as dicts."""
