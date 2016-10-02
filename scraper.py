import re
from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from shapely.geometry.point import Point

from utils import clean_dict

__author__ = 'antonin'

# Disable insecure request warnings because we don't care about these here
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



RESULT_PAGE_URL = "https://www.civiweb.com/FR/offre-liste/page/{page}.aspx"
OFFER_PAGE_URL = "https://www.civiweb.com/FR/offre/{id}.aspx"


class Scraper:
    @staticmethod
    def scrap_offers_list_max_page():
        response = requests.get(RESULT_PAGE_URL.format(page=1), verify=False)
        max_page, = re.search(r"<a href='/FR/offre-liste/page/(\d+).aspx'><img src='/images/puce-derniere-page.gif' alt='Derni&egrave;re page' /></a>", response.text).groups()
        return int(max_page)

    @staticmethod
    def scrap_offers_list_page(page):
        page_response = requests.get(RESULT_PAGE_URL.format(page=page), verify=False)
        offer_ids = [int(offer_id) for offer_id in re.findall(r'<a class="xt_offrelink" href="/FR/offre/(\d+).aspx">', page_response.text)]
        print("Page %d parsed" % page)
        return offer_ids

    @staticmethod
    def scrap_offer_details_page(offer_id):
        page_response = requests.get(OFFER_PAGE_URL.format(id=offer_id), verify=False)
        if page_response.status_code != 200:  # Some offers have 500 errors
            print("Skip %d because of status code %d" % (offer_id, page_response.status_code))
            return

        bs = BeautifulSoup(page_response.text, "html.parser")

        print("Parse offer %d..." % offer_id)
        offer = dict(
            id=offer_id,
            title=bs.find(id='ContenuPrincipal_BlocA1_m_oTitle').text,
            country=bs.find(id='ContenuPrincipal_BlocA1_m_oContry').text,
            city=bs.find(id='ContenuPrincipal_BlocA1_m_oCity').text,
            start_date=bs.find(id='ContenuPrincipal_BlocA1_m_oStartDate').text,
            end_date=bs.find(id='ContenuPrincipal_BlocA1_m_oEndDate').text,
            duration_months=bs.find(id='ContenuPrincipal_BlocA1_m_oNumberOfMonths').text,
            organization=bs.find(id='ContenuPrincipal_BlocA1_m_oOrganization').text,
            salary=bs.find(id='ContenuPrincipal_BlocA1_m_oIndemnite').text,
            description=bs.find(id='ContenuPrincipal_BlocA1_m_oDescription').text,
            publication_date=bs.find(id='ContenuPrincipal_BlocB1_m_oPublicationDate').text,
            mission_type=bs.find(id='ContenuPrincipal_BlocB1_m_oTypeMission').text,
            jobs_availables=bs.find(id='ContenuPrincipal_BlocB1_m_oNumberOfJobs').text,
            required_experience_months=bs.find(id='ContenuPrincipal_BlocB1_m_oDesiredExperience').text,
            required_education_level=bs.find(id='ContenuPrincipal_BlocB1_m_oEducation').text,
            required_languages=bs.find(id='ContenuPrincipal_BlocB1_m_oLanguages').text,
            required_skills=bs.find(id='ContenuPrincipal_BlocB1_m_oCompetence').text,
            required_education_type=bs.find(id='ContenuPrincipal_BlocB1_m_oEducationLevel').text,

            active=True,
        )
        print("Offer %d parsed" % offer_id)

        if offer['title'] == "L'offre n'est plus disponible.":
            print('skip')
            return

        clean_dict(offer)

        Scraper.scrap_or_fetch_location(offer, bs)
        return offer

    @staticmethod
    def scrap_or_fetch_location(offer, bs):
        """
        Find data contained in a <script> tag this way:
            var Longitude = "";
            var Latitude = "";
        """
        map_script_code = bs.find(id='contentMap').parent.findNext('script').findNext('script').text
        result = re.search('var Longitude = "(.*)";\s*var Latitude = "(.*)";', map_script_code)

        try:
            longitude, latitude = result.group(1), result.group(2)
            longitude, latitude = float(longitude), float(latitude)
            offer.location = Point(longitude, latitude).wkt
        except ValueError:
            pass


if __name__ == "__main__":
    print("TESTING SCRAP")
    import pprint
    pprint.pprint(Scraper.scrap_offer_details_page(73288))
    pprint.pprint(Scraper.scrap_offer_details_page(87101))



