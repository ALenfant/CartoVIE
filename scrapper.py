import re
from bs4 import BeautifulSoup
import requests

__author__ = 'Antonin'

LAST_OFFERS_RSS = "https://www.civiweb.com/FR/rss/offre-liste.aspx"
OFFER_URL = "https://www.civiweb.com/FR/offre/{0}.aspx"

min_offer_id = 0

# Get last offers RSS feed
response = requests.get(LAST_OFFERS_RSS)
last_offers_ids = map(int, re.findall(r"https://www.civiweb.com/FR/offre/(\d+).aspx", response.text))
max_offer_id = max(last_offers_ids)



print("Getting offerts between {0} and {1}...".format(min_offer_id, max_offer_id))
for offer_id in range(max_offer_id, min_offer_id, -1):
    print(offer_id)
    response = requests.get(OFFER_URL.format(offer_id))
    bs = BeautifulSoup(response.text)
    offer = dict(
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
        required_exerience=bs.find(id='ContenuPrincipal_BlocB1_m_oDesiredExperience').text,
        required_education_level=bs.find(id='ContenuPrincipal_BlocB1_m_oEducation').text,
        required_languages=bs.find(id='ContenuPrincipal_BlocB1_m_oLanguages').text,
        required_skills=bs.find(id='ContenuPrincipal_BlocB1_m_oCompetence').text,
        required_education_type=bs.find(id='ContenuPrincipal_BlocB1_m_oEducationLevel').text,
    )

    if offer['title'] == "L'offre n'est plus disponible.":
        print('skip')
        continue

    print(offer)



    #exit()
