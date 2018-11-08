from app import app
import json
from bs4 import BeautifulSoup
import urllib2

# lakeshore_apartment=urllib2.urlopen("http://129.213.131.176/lakeshore-pearl")
lakeshore_apartment=urllib2.urlopen("http://129.213.84.36/lakeshore-pearl")


apartment_list = json.loads(lakeshore_apartment.read())

class LakeshoreApartmentInfo:

    def __init__(self, url):
        ''' Initializing Parameters for URL '''
        self.url = url
        page = urllib2.urlopen(self.url)
        self.soup = BeautifulSoup(page, "html.parser")

    def apartment_amenities(self):
        '''Fetching apartment amenities'''
        amenities = self.soup.find_all('div', id='amenities')
        p = amenities[0].find_all("p")
        p1 = json.dumps([elem.get_text() for elem in p])
        return p1

    def apartment_floorplan(self):
        '''Fetching apartment floorplan'''
        floorplans = []
        images = self.soup.findAll('img')
        for image in images:
            if "floorplans" in image['src']:
                floorplans.append(image['src'])
        return floorplans[0]

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/lakeshore')
def lakeshore():
    for apartment in apartment_list:
        apartment_info = LakeshoreApartmentInfo(apartment["url"])
        apartment_amenities = apartment_info.apartment_amenities()
        apartment.update({"amenities": apartment_amenities})
        apartment_floorplan = apartment_info.apartment_floorplan()
        apartment.update({"floorplan": apartment_floorplan})

    return json.dumps(apartment_list)