import json
import scrapy


class Doctoralia(scrapy.Spider):
    """Recursively crawls doctoralia.com.br and extracts doctor data."""
    name = 'DoctoraliaScraper'
    # start_urls = ['https://www.doctoralia.com.br/psicologo']
    start_urls = ['https://www.doctoralia.com.br/raquel-navarro/psicologo/manaus']

    def parse(self, response):
        """Recursively follows links to all Doctoralia doctors and extracts data from them."""

        # follow all the links to each talk on the page calling the parse_doctor callback for each of them
        # doctor_page_links = response.xpath("//span[@data-ga-event='click']")
        # yield from response.follow_all(doctor_page_links, self.parse_doctor)

        # looks for the link to the next page, builds a URL and yields a new request to the next page
        # pagination_links = response.xpath("//a[@aria-label='next']")
        # yield from response.follow_all(pagination_links, self.parse)
        yield {
            'doctor_id': response.css("script")[6].re_first("DOCTOR_ID:\s(\d+)"),
            'name': response.css("script").re_first("FULLNAME:\s'(.*?)'").strip(),
            'location': response.css("script").re_first("NAME:\s'(.*?)'").strip(),  
            'specialization': response.css("script")[6].re_first("SPECIALIZATION[\s\S]*?NAME:\s'(.*?)'").strip(),
            'reviews': response.xpath("//div/meta[@itemprop='reviewCount']/@content").get(),
            # 'price': ,  # choose a specific service, likely 'Consulta Psicologia' or 'Telemedicina'
            'telemedicine': response.xpath("//script")[8].re_first("virtual\-consultation\-profile'\]\s=\s'(.*?)'"),
            'url': response.xpath("//script")[8].re_first("\['gtm\-url'\]\s=\s'(.*?)'"),
            # 'oldest_review_date': ,
            # 'date_joined': ,
            # 'education': ,
            # 'experience_in': ,
            # 'medical_conditions_treated': ,

        }
    
