from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count

import joblib

import geocoder
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import update, func

import settings
from database import Database
from models import Offer
from scraper import Scraper
from settings import PATH_CACHE_GEOCODER

__author__ = 'Antonin'


# Initialization: load the disk-backed geocaching cache data
memory = joblib.Memory(cachedir=PATH_CACHE_GEOCODER, verbose=0)

# Initialization: Connect to the database and create a transaction
engine, _ = Database().connect()
Session = sessionmaker(bind=engine)
session = Session()

current_total = session.query(func.count(Offer.id)).scalar()
active_total = session.query(func.count(Offer.id)).filter(Offer.active==True).scalar()

# Set all current offers to active=False
update(Offer).where(Offer.active==True).values(active=False)


def fetch_and_process_offer(offer_id):
    offer = Scraper.scrap_offer_details_page(offer_id)
    if not offer:
        return
    if not offer.get('location'):
        location = geocode_city_country(offer['city'].lower(), offer['country'].lower())  # Lower for better cache
        offer['location'] = location or None
    Offer.upsert(session, offer)


@memory.cache()
def geocode_city_country(city, country):
    location = '{city}, {country}'.format(city=city, country=country)
    return geocoder.google(location, key=settings.API_KEY_GOOGLE_GEOCODER).wkt


# 1) Fetch the number of pages of offers
print("Fetching total info...")
max_page = Scraper.scrap_offers_list_max_page()
print("Total %d pages to fetch" % max_page)

# 2) Fetch the list of offer ids
thread_pool = ThreadPool(processes=cpu_count())
offer_ids = thread_pool.map(Scraper.scrap_offers_list_page, range(1, max_page+1))
thread_pool.close()
thread_pool.join()

offer_ids = list(sum(offer_ids, []))
print("OFFER IDS", len(offer_ids), offer_ids)

# 3) Fetcb all the offers
thread_pool = ThreadPool(processes=cpu_count())
offers = thread_pool.map(fetch_and_process_offer, offer_ids)
thread_pool.close()
thread_pool.join()

print(offers)

new_total = session.query(func.count(Offer.id)).scalar()
new_active_total = session.query(func.count(Offer.id)).filter(Offer.active==True).scalar()


session.commit()


print("Before", current_total, "now", new_total)
print("Active count was", active_total, "now", new_active_total)
