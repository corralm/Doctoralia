import json
import scrapy


class Doctoralia(scrapy.Spider):
    """Recursively crawls doctoralia.com.br and extracts doctor data."""
    name = 'DoctoraliaScraper'
    # start_urls = ['https://www.doctoralia.com.br/psicologo']
    start_urls = ['https://www.doctoralia.com.br/raquel-navarro/psicologo/manaus']

    def parse(self, response):
        """Recursively follows links to all Doctoralia doctors and extracts data from them."""

        rx = response.xpath
        # ZLApp.AppConfig
        zr = response.css("script")[6]
        # Google Tag Manager
        gr = response.xpath("//script")[8]
        yield {
            'doctor_id': zr.re_first("DOCTOR_ID:\s(\d+)"),
            'name': zr.re_first("FULLNAME:\s'(.*?)'"),
            'city': zr.re_first("NAME:\s'(.*?)'").strip(),
            'specialization': zr.re_first("SPECIALIZATION[\s\S]*?NAME:\s'(.*?)'").strip(),
            'reviews': rx("//div/meta[@itemprop='reviewCount']/@content").get(),
            'telemedicine': gr.re_first("virtual\-consultation\-profile'\]\s=\s'(.*?)'"),
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
