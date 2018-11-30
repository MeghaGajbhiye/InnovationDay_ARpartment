from app import app
import json
from bs4 import BeautifulSoup
import urllib2

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
        p1_list = json.loads(p1)
        return p1_list

    def apartment_floorplan(self):
        '''Fetching apartment floorplan'''
        floorplans = []
        images = self.soup.findAll('img')
        for image in images:
            if "floorplans" in image['src']:
                floorplans.append(image['src'])
        return floorplans[0]

    def apartment_title(self, apartment):
        '''Fetching bathroom, bedroom and sqrft'''
        apartment_title= apartment["title"]
        my_string= apartment_title.split()
        print my_string[0],my_string[2], my_string[4]
        apartment.update({"Bed": int(my_string[0])})
        apartment.update({"Bath": int(my_string[2])})
        apartment.update({"Space": int(my_string[4])})

    def apartment_price(self, apartment):
        '''Fetching minimum and maximum price'''
        apartment_price = apartment["price"]
        my_string = apartment_price.split()
        apartment.update({"Min_price": float(my_string[1].replace("$", "").replace(",",""))})
        apartment.update({"Max_price": float(my_string[3].replace("$", "").replace(",",""))})

class AzulApartmentInfo:
    def __init__(self, url):
        ''' Initializing Parameters for URL '''
        self.url = url
        page = urllib2.urlopen(self.url)
        self.soup = BeautifulSoup(page, "html.parser")

    def apartment_floorplan(self):
        '''Fetching apartment floorplan'''
        floorplans = []
        images = self.soup.findAll('img')
        for image in images:
            if "assets" in image['src']:
                floorplans.append(image['src'])
        return floorplans[0]

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/lakeshore')
def lakeshore():
    lakeshore_apartment = urllib2.urlopen("http://129.213.86.83/lakeshore-pearl")
    lakeshore_apartment_list = json.loads(lakeshore_apartment.read())
    for apartment in lakeshore_apartment_list:
        apartment_info = LakeshoreApartmentInfo(apartment["url"])
        apartment_amenities = apartment_info.apartment_amenities()
        apartment.update({"amenities": apartment_amenities})
        apartment_floorplan = apartment_info.apartment_floorplan()
        apartment.update({"floorplan": apartment_floorplan})
        apartment_info.apartment_title(apartment)
        apartment_info.apartment_price(apartment)

    return json.dumps(lakeshore_apartment_list)

@app.route('/azulapartments')
def azulapartments():
    azulapartments = urllib2.urlopen("http://129.213.86.83/azulapartments")
    azule_apartment_list = json.loads(azulapartments.read())
    for apartment in azule_apartment_list:
        apartment_info = AzulApartmentInfo(apartment["url"])
        apartment_floorplan = apartment_info.apartment_floorplan()
        apartment.update({"floorplan": apartment_floorplan})

    return json.dumps(azule_apartment_list)

if __name__ =='__main__':
    app.debug= True
    app.run(host='0.0.0.0', port=5000)