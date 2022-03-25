import os
from builtins import print

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import json


class Build_Scrapers_Requests():
    '''
    Class used for scraping each building listings using the Requests module.
    '''
    df2 = pd.DataFrame()

    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
        }
        # Read in Target_Websites.xlsx file which will be fed int class methods
        websites_file = "Target_Websites.xlsx"
        path = os.path.join(os.getcwd(), websites_file)
        self.websites = pd.read_excel(path)
        self.data = pd.DataFrame(self.websites)  # Create a DataFarme where we add the data

    def save_data(self, result):
        df_dict = pd.DataFrame(result)
        Build_Scrapers_Requests.df2 = pd.concat([Build_Scrapers_Requests.df2, df_dict], ignore_index=True, sort=False)

    def checking_if_file_exists(self):
        try:
            websites_file = "output.csv"
            path = os.path.join(os.getcwd(), websites_file)
            df = pd.read_csv(path)
            return df.iloc[0]['Created_at']
        except:
            return False

    def send_requests(self, url):
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def save_csv(self):
        Build_Scrapers_Requests.df2.to_csv('output.csv')

    def packardjc(self):  # Replace website_name with the name of the website (you can use acronym)
        bool_ = True
        # Select target website
        # Replace "website.com" with the appropriate website URL
        url = self.websites[self.websites['Website'].str.contains("https://packardjc.com/#availability") == True][
            'Website'].values[0]
        soup = self.send_requests(url)
        trs = soup.select('table#tablepress-2 tbody tr')
        result = []
        for tr in trs:
            td = tr.select('td')
            unit = td[0].text
            bed_bath = td[1].text
            bedroom = bed_bath[0]
            bathroom = bed_bath[2]
            net_price = ''
            price_ = td[7].text
            price = "".join(c for c in price_ if c.isdecimal())
            sqft = td[2].text.replace(',', '').replace(' ', '')
            try:
                description = td[4].text
            except:
                description = ''
            floor = ''
            status = 'For Sale'
            amenity = ''
            availability = ''
            try:
                image_source = td[6].select_one('a').get('href')
            except:
                image_source = ''

            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '142 Charles Street'
            building_name = 'The Packard'
            borough = 'The Heights'
            city = 'Jersey City'
            state = 'NJ'
            zip_code = '07307'
            # You can append data only what is available

            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })

        self.save_data(result)
        print(f"{url} scraped")

    def nine15broad(self):
        url = "https://nine15broad.com/floor"
        soup = self.send_requests(url)
        trs = soup.select('table thead tr')[1:]
        result = []
        for tr in trs:
            td = tr.select('td')
            try:
                unit_ = td[0].text
                if "One" in unit_:
                    unit = 1
                elif "Two" in unit_:
                    unit = 2
                else:
                    unit = '0'
            except:
                unit = ''
            try:
                bed_bath_ = td[1].text
                bed_bath = "".join(c for c in bed_bath_ if c.isdecimal())
                bedroom = bed_bath[0]
                bathroom = bed_bath[1]
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            gross_price = ''
            price = ''
            try:
                net_price = td[3].text.replace('$', '')
            except:
                net_price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = td[2].text.replace('Sq Ft', '')
            except:
                sqft = 'ERROR'
            try:
                description = ''
            except:
                description = ''
            floor = ''
            status = 'Rental'
            amenity = ''
            availability = ''
            try:
                image_source = td[4].select_one('a').get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '915 Broad St'
            city = 'Newark'
            state = 'NJ'
            building_name = '915 Broad'
            borough = ''
            zip_code = '07102'
            # You can append data only what is available

            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def housejc(self):
        url = "https://100housejc.com/availability/"
        soup = self.send_requests(url)
        trs = soup.select('table tbody tr')
        result = []
        try:
            amenity_ = self.send_requests('https://100housejc.com/amenities/').select("div.bulletareas li")
            amenity = ''
            for x in amenity_[1:]:
                amenity += x.text + '; '
        except:
            amenity = 'ERROR'
        for tr in trs:
            td = tr.select('td')
            try:
                unit = td[0].text
            except:
                unit = ''
            try:
                bed_bath_ = td[1].text
                if 'Studio' in bed_bath_:
                    bedroom = '0'
                    bed_bath = "".join(c for c in bed_bath_ if c.isdecimal())
                    bathroom = bed_bath[0]
                else:
                    bed_bath = "".join(c for c in bed_bath_ if c.isdecimal())
                    bedroom = bed_bath[0]
                    bathroom = bed_bath[1]

            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = td[2].text.replace('$', '').replace(',', '')
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = td[3].text
            except:
                sqft = 'ERROR'
            try:
                description = ''
            except:
                description = ''
            floor = ''
            status = 'Rental'
            availability = ''
            try:
                image_source = td[4].select_one('a').get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '100 Hoboken Ave'
            city = 'Jersey City'
            state = 'NJ'
            building_name = '100 House'
            borough = 'The Heights'
            zip_code = '07310'
            # You can append data only what is available

            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def hudson2400(self):
        url = "https://2400hudson.com/floor-plans/"
        soup = self.send_requests(url)
        trs = soup.select('table tbody tr')
        result = []
        try:
            amenity_ = self.send_requests('https://2400hudson.com/amenities/').select("h4.et_pb_module_header")
            amenity = ''
            for x in amenity_:
                amenity += x.text + '; '
        except:
            amenity = 'ERROR'
        for tr in trs:
            td = tr.select('td')
            try:
                unit = td[1].text[0]
            except:
                unit = ''
            try:
                bed_bath_ = td[2].text
                if 'Studio' in bed_bath_:
                    bedroom = '0'
                    # bed_bath = "".join(c for c in bed_bath_ if c.isdecimal())
                    bathroom = td[3].text
                else:
                    # bed_bath = "".join(c for c in bed_bath_ if c.isdecimal())
                    bedroom = td[2].text
                    bathroom = td[3].text
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price_ = td[5].text
                if 'Leased' in price_:
                    price = ''
                else:
                    price = td[5].text.replace('$', '')
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = td[4].text
            except:
                sqft = 'ERROR'
            try:
                description = ''
            except:
                description = ''
            floor = ''
            status = 'Rental'

            availability = ''
            try:
                image_source = td[0].select_one('a').get('href')
                if "https://2400hudson.com/" in image_source:
                    pass
                else:
                    image_source = "https://2400hudson.com" + image_source
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '2130 JFK Boulevard'
            building_name = '2400 Hudson'
            borough = 'Fort Lee'
            city = 'Bergen County'
            state = 'NJ'
            zip_code = '*07024'
            # You can append data only what is available

            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def senateplace(self):
        url = "https://25senateplace.com/available-luxury-rentals/"
        soup = self.send_requests(url)
        trs = soup.select('table tbody tr')
        divs = soup.select('div#listing_ajax_container div.col-md-3')
        result = []
        try:
            amenity_ = self.send_requests('https://25senateplace.com/building-amenities/')
            amenity_ = amenity_.select("div[class='wpb_column vc_column_container vc_col-sm-4 vc_column'] li")
            amenity = ''
            for x in amenity_:
                amenity += x.text.strip() + '; '
        except:
            amenity = ''
        for div in divs:
            link = div.select_one('a').get('href')
            r_soup = self.send_requests(link)
            try:
                unit = div.select_one('h4').text.strip().replace('Residence ', '')
            except:
                unit = ''
            try:
                bed_bath_ = div.find('div', class_='property_location')
                try:
                    bedroom = bed_bath_.find('span', class_='inforoom').text
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_.find('span', class_='infobath').text
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            price = ''
            try:
                net_price_ = div.select_one("div.property_location span[class='']").text
                net_price = "".join(c for c in net_price_ if c.isdecimal())
            except:
                net_price = 'ERROR'

            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = div.select_one('span.infosize').text.replace(' ft2', '')
            except:
                sqft = 'ERROR'
            try:
                description = r_soup.select_one('div.wpb_wrapper p').text
            except:
                description = ''
            floor = ''
            status = 'Rental'

            try:
                availability = div.select_one("div.property_location div").text.replace('Available Date: ', '')
            except:
                availability = ''

            try:
                image_source = r_soup.select_one('figure.wpb_wrapper img').get('data-src')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '25 Senate Place'
            city = 'Jersey City'
            state = 'NJ'
            building_name = '25 Senate Place'
            borough = 'Journal Square'
            zip_code = '07306'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def jfk2130(self):
        url = "https://greenpropertyllc.appfolio.com/listings"
        soup = self.send_requests(url)
        divs = soup.select('div#result_container div.listing-item.result.js-listing-item')
        result = []
        for div in divs:
            link = "https://greenpropertyllc.appfolio.com" + div.select_one('h2 a').get('href')
            r_soup = self.send_requests(link)
            dd = div.select('div.detail-box dd')
            try:
                pattern = ' [0-9][A-Z],'
                unit_ = div.select_one('p.u-space-an span').text
                try:
                    unit = re.search(pattern, unit_).group(0).replace(',', '').strip()
                except:
                    unit = re.search(r" [A-Z]\d+,", unit_).group(0).replace(',', '').strip()
            except:
                unit = ''
            try:
                bed_bath_ = dd[2].text
                try:
                    bedroom = bed_bath_[0]
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_[7]
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price_ = dd[0].text
                price = "".join(c for c in price_ if c.isdecimal())
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = dd[1].text.replace(',', '')
            except:
                sqft = 'ERROR'
            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''

            status = 'Rental'
            try:
                amenity = ''
                amenity_ = r_soup.select_one('div.grid__large-6.grid__medium-6.grid__small-12').select('li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = dd[3].text
                if availability == 'NOW':
                    availability = datetime.now().strftime('%d-%m-%Y')
            except:
                availability = ''
            try:
                image_source = ''
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '25 Senate Place'
            city = 'Jersey City'
            state = 'NJ'
            building_name = '2130 JFK'
            borough = 'West Side'
            zip_code = '07305'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": 'https://2130jfk.com/',
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def ninthjc372(self):
        url = "https://372ninthjc.com/"
        soup = self.send_requests(url)
        trs = soup.select('table.cf.desktop tbody#allbed0 tr')
        result = []
        for div in trs:
            link = "https://372ninthjc.com/" + div.select_one("td[data-title='Floorplan'] a").get('href')
            r_soup = self.send_requests(link)
            td = div.select('td')
            try:
                unit = td[1].text
            except:
                unit = ''
            try:
                bed_bath_ = td[0].text
                try:
                    bedroom = re.search("[1-9] BR", bed_bath_).group(0)[0]
                except:
                    bedroom = '0'
                try:
                    bathroom = re.search("[1-9] BA", bed_bath_).group(0)[0]
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = div.select_one("td[data-title='Price']").text.replace('$', '').replace('.00', '')
            except:
                price = 'ERROR'
            try:
                sqft = td[2].text.replace('sqft', '')
            except:
                sqft = 'ERROR'
            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''

            status = 'Rental'
            try:
                amenity = ''
                amenity_ = r_soup.select_one('div.grid__large-6.grid__medium-6.grid__small-12').select('li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = td[4].text
                if 'Available' in availability:
                    availability = datetime.now().strftime('%d-%m-%Y')
            except:
                availability = ''
            try:
                image_source = r_soup.select_one('div.middle a.fancybox').get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '372 9TH STREET'
            city = 'Jersey City'
            state = 'NJ'
            building_name = 'DVORA 372 9th'
            borough = 'Downtown'
            zip_code = '07302'

            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def acresjc3(self):
        url = "https://nestiolistings.com/api/v2/listings/residential/rentals/?key=f4c1c9c61efe41ec8e8f7bf08a64422c"
        json_ = requests.get(url, headers=self.headers).json()
        result = []
        try:
            soup = self.send_requests('https://3acresjc.com/amenities/')
            amenity_ = soup.select("div[class='ct-div-block box-inner text-box amenities'] li")
            amenity = [amenity.text + ';' for amenity in amenity_]
            amenity = ''.join(amenity)
        except:
            amenity = ''
        for json in json_['items']:
            try:
                unit = json['unit_number']
            except:
                unit = ''
            try:
                bedroom = json['bedrooms']
                bathroom = int(json['bathrooms'])
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            try:
                net_price = json['price'].replace('.00', '')
            except:
                net_price = ''
            try:
                price = ''
            except:
                price = 'ERROR'
            try:
                sqft = ''
            except:
                sqft = 'ERROR'
            try:
                description = ''
            except:
                description = ''
            try:
                floor = json['floor']
            except:
                floor = ''
            status = 'Rental'

            try:
                availability = json['status']
                if 'Available' in availability:
                    availability = datetime.now().strftime('%d-%m-%Y')
            except:
                availability = ''
            try:
                image_source = json['photos'][-1]['original']
            except:
                image_source = ''

            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '400 Claremont Ave'
            city = 'Jersey City'
            state = 'NJ'
            building_name = '3 Acres'
            borough = 'Waterfront'
            zip_code = '07304'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": 'https://3acresjc.com/availability/',
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print("https://3acresjc.com/availability/ scraped")

    def elm60(self):
        url = "https://60elm.com/floor-plans/"
        soup = self.send_requests(url)
        divs = soup.select('div.fusion-layout-column.fusion_builder_column')
        result = []
        try:
            soup = self.send_requests('https://60elm.com/amenities/')
            amenity_ = soup.select("li.fusion-li-item")
            amenity = [amenity.text + ';' for amenity in amenity_]
            amenity = ''.join(amenity).strip().replace('\n', '')
        except:
            amenity = ''
        for div in divs:
            try:
                unit = div.select_one('div.heading.icon-left h2').text
            except:
                unit = ''
            try:
                bed_bath_ = div.select_one('div.content-container').text
                try:
                    bedroom = re.search("[1-9] bed", bed_bath_).group(0)[0]
                except:
                    bedroom = '0'
                try:
                    bathroom = re.search("[1-9] bath", bed_bath_).group(0)[0]
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'

            net_price = ''
            try:
                price = ''
            except:
                price = 'ERROR'
            try:
                sqft = ''
            except:
                sqft = 'ERROR'
            try:
                description = ''
            except:
                description = ''
            floor = ''

            status = 'Rental'
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = div.select_one('a.fusion-read-more').get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '60 Elm Street'
            city = 'Newark'
            state = 'NJ'
            building_name = '60 Elm'
            borough = ''
            zip_code = '07105'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def baygrovearms(self):
        url = "https://www.baygrovearms.com/"
        soup = self.send_requests(url)
        a = soup.select_one("div#comp-izozrlwx a[data-testid='linkElement']").get('href')
        soup = self.send_requests(a)
        divs = soup.select('div#tab-tours div.col-sm-4')
        result = []
        for div in divs:
            link = div.select_one("a.tour-link").get('href')
            r_soup = self.send_requests(link)
            try:
                unit_ = div.select_one('div.address').text
                unit = re.search(r"Unit \d{1,10000}", unit_).group(0).replace('Unit ', '')
            except:
                unit = 'ERROR'
            try:
                bed_bath_ = r_soup.select('div.row.property-features-icons div.col-md-2')
                try:
                    bedroom = bed_bath_[0].select_one('div.feature-data').text
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_[1].select_one('div.feature-data').text[0]
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price_ = div.select_one('div.info.info-medium').text
                price = "".join(c for c in price_ if c.isdecimal())
            except:
                price = 'ERROR'
            try:
                sqft = r_soup.select('div.row.property-features-icons div.col-md-2')[3].select_one(
                    'div.feature-data').text
            except:
                sqft = 'ERROR'
            try:
                description = r_soup.select_one('div.tour-description p').text
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                amenity = ''
                amenity_ = r_soup.select_one('div.grid__large-6.grid__medium-6.grid__small-12').select('li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = r_soup.select('div.container.photo-gallery-container div.row div.col-xs-6 a')[-1].get(
                    'href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '225 Bay Street'
            city = 'Jersey City'
            building_name = 'Bay Grove Arms'
            borough = 'Downtown'
            state = 'NJ'
            zip_code = '07302'

            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def embankmenthouse(self):
        url = "https://www.embankmenthouse.com/pages/availability.asp"
        soup = self.send_requests(url)
        divs = soup.select('div.table__body div.table__body__row')
        result = []
        for div in divs:
            data = {
                'id': 'henemledi',
                'unit': div.get('data-unit')
            }
            content = requests.post('https://www.embankmenthouse.com/ajax/get-plan-details.asp',
                                    data=data, headers=self.headers).text
            r_soup = BeautifulSoup(content, 'lxml')
            try:
                unit = r_soup.select_one('div.header h2').text.replace('Unit ', '').strip()
            except:
                unit = 'ERROR'
            try:
                bed_bath_ = div.select_one('div.table__body__cell.bed').text
                try:
                    bedroom = re.search(r'\d{1,10000} Bedroom', bed_bath_).group(0).replace(' Bedroom', '')
                except:
                    bedroom = '0'
                try:
                    bathroom = re.search(r'\d{1,10000} Bathroom', bed_bath_).group(0).replace(' Bathroom', '')
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = div.select_one('div.table__body__cell.priceFrom span').text.replace('$', '')
            except:
                price = 'ERROR'
            try:
                sqft = div.select_one('div.table__body__cell.sf span').text
            except:
                sqft = 'ERROR'

            try:
                description = r_soup.select_one('div.tour-description p').text
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                amenity = ''
                amenity_ = r_soup.select('div.bldAmenities.listAmenities.active li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source_ = r_soup.select('div.PhotoGallery.test div img')
                image_source = ''
                for img in image_source_:
                    if 'unit_photos' in img.get('src'):
                        image_source = img.get('src')
                        break
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '270 Tenth Street'
            building_name = 'EMBANKMENT HOUSE'
            borough = 'Waterfront'
            city = 'Jersey City'
            state = 'NJ'
            zip_code = '07302'

            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code
            })
        self.save_data(result)
        print(f"{url} scraped")

    def halfmoonharbourapts(self):
        url = "https://www.halfmoonharbourapts.com/CmsSiteManager/callback.aspx?act=Proxy/GetFloorPlans&callback=" \
              "jQuery22401610043673149908_1647354978234&_=1647354978235"
        json_ = requests.get(url, headers=self.headers).text.replace('jQuery22401610043673149908_1647354978234(',
                                                                     '').replace('})', '}')
        json__ = json.loads(json_)['floorplans']
        result = []
        soup = self.send_requests('https://www.halfmoonharbourapts.com/floor-plans.aspx')
        divs = soup.select('div.floorplan-block.filtered-in')
        for jsons, div in zip(json__, divs):
            try:
                unit = div.select_one('div.content_area_top h2').text
            except:
                unit = ''
            try:
                try:
                    bedroom = jsons['bedRooms']
                except:
                    bedroom = '0'
                try:
                    bathroom = jsons['bathRooms']
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price_ = jsons['rentRange']
                price = "".join(c for c in price_ if c.isdecimal())
            except:
                price = 'ERROR'
            try:
                sqft = jsons['maximumSquareFeet']
            except:
                sqft = 'ERROR'
            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''

            status = 'Rental'
            try:
                amenity = ''
                amenity_ = div.select('div.amenities-container li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = div.select_one('span.floorplan-image a').get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '7912 River Road'
            city = 'North Bergen'
            building_name = 'Half Moon Harbour'
            borough = ''
            state = 'NJ'
            zip_code = '*07047'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code
            })
        self.save_data(result)
        print(f"{url} scraped")

    def hudsonlightsnj(self):
        url = "https://www.hudsonlightsnj.com/fort-lee/hudson-lights/conventional/"
        soup = self.send_requests(url)
        divs = soup.select('li.fp-group-item')
        result = []
        a_soup = self.send_requests('https://www.hudsonlightsnj.com/fort-lee/hudson-lights/amenities/')
        try:
            amenity = ''
            amenity_ = a_soup.select('li.amenity-item')
            for li in amenity_:
                amenity += li.text.strip() + '; '
        except:
            amenity = ''
        for div in divs:
            f_link = div.select_one('a.primary-action').get('href')
            pr_id_ = re.search(r'&property\[id\]=\d+&', f_link).group(0)
            pf_id_ = re.search(r'&property_floorplan\[id\]=\d+&', f_link).group(0)
            pr_id_ = "".join(c for c in pr_id_ if c.isdecimal())
            pf_id_ = "".join(c for c in pf_id_ if c.isdecimal())
            try:
                image_source = div.select_one('div.image-container.popover-holder.js-popover meta').get('content')
            except:
                image_source = ''
            try:
                bed_bath_ = div.select_one('li.fp-group-item div.fp-col.bed-bath span.fp-col-text').text
                try:
                    bedroom = re.search(r"\dbd", bed_bath_).group(0).replace('bd', '')
                except:
                    bedroom = '0'
                try:
                    bathroom = re.search(r"\dba", bed_bath_).group(0).replace('ba', '')
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            if div.select_one('div.fp-col.action a').text == 'Get Notified':
                sqft = div.select_one('div.fp-col.sq-feet span.fp-col-text').text
                unit = ''
                net_price = ''
                price = ''
                description = ''
                floor = ''
                status = 'Rental'
                availability = ''
                building_name = 'Hudson Lights'
                address = '2030 Hudson Street'
                borough = 'Fort Lee'
                city = 'Bergen County'
                state = 'NJ'
                zip_code = '*07024'
                if self.checking_if_file_exists() is False:
                    created_at = datetime.now().strftime('%d-%m-%Y')
                else:
                    created_at = self.checking_if_file_exists()
                update_ut = datetime.now().strftime('%d-%m-%Y')
                if availability == '':
                    data_present = 0
                else:
                    data_present = 1
                result.append({
                    "Unit": unit,
                    "Bedroom": bedroom,
                    "Bathroom": bathroom,
                    "Gross Price": price,
                    "Net price": net_price,
                    "Sqft": sqft,
                    "Floor": floor,
                    "Amenity": amenity,
                    "Description": description,
                    "Status": status,
                    "Availability": availability,
                    "Source": url,
                    "Floorplan_Image_URL": image_source,
                    "Created_at": created_at,
                    "Updated_at": update_ut,
                    "Date_present": data_present,
                    "Address": address,
                    "City": city,
                    "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "Borough": borough,
                    "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "ZIP Code": zip_code
                })

            content = requests.get(f'https://www.hudsonlightsnj.com/?module=check_availability&is_secure=1&property'
                                   f'[id]={pr_id_}&action=view_unit_spaces&property_floorplan[id]={pf_id_}&'
                                   f'move_in_date=true&term_month=26&occupancy_type=conventional#',
                                   headers=self.headers).text
            r_soup = BeautifulSoup(content, 'lxml')
            divs_ = r_soup.select('div.unit-row.js-unit-row')
            for div_ in divs_:
                try:
                    unit = div_.select_one('div.unit-col.unit span.unit-col-text').text.replace('Unit ', '')
                except:
                    unit = 'ERROR'
                net_price = ''
                try:
                    price_ = div_.select_one('div.unit-col.rent').text
                    price = "".join(c for c in price_ if c.isdecimal())
                except:
                    price = 'ERROR'
                try:
                    sqft = div_.select_one('div.unit-col.sqft span.unit-col-text').text
                except:
                    sqft = 'ERROR'

                try:
                    description = ''
                except:
                    description = ''
                floor = ''
                status = 'Rental'

                try:
                    availability = div_.select_one('div.unit-col.availability span.unit-col-text').text
                    if availability == 'Now':
                        availability = datetime.now().strftime('%d-%m-%Y')
                except:
                    availability = ''
                if self.checking_if_file_exists() is False:
                    created_at = datetime.now().strftime('%d-%m-%Y')
                else:
                    created_at = self.checking_if_file_exists()
                update_ut = datetime.now().strftime('%d-%m-%Y')
                if availability == '':
                    data_present = 0
                else:
                    data_present = 1
                building_name = 'Hudson Lights'
                address = '2030 Hudson Street'
                borough = 'Fort Lee'
                city = 'Bergen County'
                state = 'NJ'
                zip_code = '*07024'

                result.append({
                    "Unit": unit,
                    "Bedroom": bedroom,
                    "Bathroom": bathroom,
                    "Gross Price": price,
                    "Net price": net_price,
                    "Sqft": sqft,
                    "Floor": floor,
                    "Amenity": amenity,
                    "Description": description,
                    "Status": status,
                    "Availability": availability,
                    "Source": url,
                    "Floorplan_Image_URL": image_source,
                    "Created_at": created_at,
                    "Updated_at": update_ut,
                    "Date_present": data_present,
                    "Address": address,
                    "City": city,
                    "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "Borough": borough,
                    "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "ZIP Code": zip_code
                })
        self.save_data(result)
        print(f"{url} scraped")

    def liveatbarbarasplace(self):
        url = "https://www.liveatbarbarasplace.com/floor-plans.aspx"
        soup = self.send_requests(url)
        divs = soup.select('div.floorplan-block.filtered-in')
        result = []
        for div in divs:
            try:
                unit = div.select_one('div.content_area_top h2').text
            except:
                unit = ''
            try:
                bed_bath_ = div.select('div.specification span[id]')
                try:
                    bedroom = bed_bath_[0].text
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_[1].text
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = ''
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = div.select('div.specification span[id]')[2].text.replace(',', '')
            except:
                sqft = 'ERROR'

            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                amenity = ''
                amenity_ = div.select('div.amenities-container ul li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = div.select('div.img_area ul li a')[-1].get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '471 Pacific Avenue'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "Barbara's Place Apartments"
            borough = 'Downtown'
            zip_code = '07304'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def liveatglennviewtownhouses(self):
        url = "https://www.liveatglennviewtownhouses.com/floor-plans.aspx"
        soup = self.send_requests(url)
        divs = soup.select('div.floorplan-block.filtered-in')
        result = []
        for div in divs:
            try:
                unit = div.select_one('div.content_area_top h2').text
            except:
                unit = ''
            try:
                bed_bath_ = div.select('div.specification span[id]')
                try:
                    bedroom = bed_bath_[0].text
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_[1].text
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = ''
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = div.select('div.specification span[id]')[2].text.replace(',', '')
            except:
                sqft = 'ERROR'

            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                amenity = ''
                amenity_ = div.select('div.amenities-container ul li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = div.select('div.img_area ul li a')[-1].get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '463 Pacific Avenue'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "Glennview Townhouses"
            borough = 'Bergen-Lafayette'
            zip_code = '07304'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def liveatoceanstower(self):
        url = "https://www.liveatoceanstower.com/floor-plans.aspx"
        soup = self.send_requests(url)
        divs = soup.select('div.floorplan-block.filtered-in')
        result = []
        for div in divs:
            try:
                unit = div.select_one('div.content_area_top h2').text
            except:
                unit = ''
            try:
                bed_bath_ = div.select('div.specification span[id]')
                try:
                    bedroom = bed_bath_[0].text
                    if bedroom not in '1234567890':
                        bedroom = 0
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_[1].text
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = ''
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = div.select('div.specification span[id]')[2].text.replace(',', '')
            except:
                sqft = 'ERROR'

            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                amenity = ''
                amenity_ = div.select('div.amenities-container ul li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = div.select('div.img_area ul li a')[-1].get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '425 Ocean Avenue'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "Ocean Towers"
            borough = 'Greenville'
            zip_code = '07305'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def liveatpacificcourt(self):
        url = "https://www.liveatpacificcourt.com/floor-plans.aspx"
        soup = self.send_requests(url)
        divs = soup.select('div.floorplan-block.filtered-in')
        result = []
        for div in divs:
            try:
                unit = div.select_one('div.content_area_top h2').text
            except:
                unit = ''
            try:
                bed_bath_ = div.select('div.specification span[id]')
                try:
                    bedroom = bed_bath_[0].text
                    if bedroom not in '1234567890':
                        bedroom = 0
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_[1].text
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = ''
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = div.select('div.specification span[id]')[2].text.replace(',', '')
            except:
                sqft = 'ERROR'

            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                amenity = ''
                amenity_ = div.select('div.amenities-container ul li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = div.select('div.img_area ul li a')[-1].get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '148 Bramhall Avenue'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "Pacific Court Apartments"
            borough = 'Bergen-Lafayette'
            zip_code = '07304'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def livethemorgan(self):
        url = "https://www.livethemorgan.com/floor-plans/"
        j_link = 'https://sightmap.com/app/api/v1/910pd727p2z/sightmaps/14497'
        r_soup = self.send_requests('https://www.livethemorgan.com/amenities/')
        json_ = requests.get(j_link, headers=self.headers).json()
        json_units = json_['data']['units']
        json_floor_plans = json_['data']['floor_plans']
        json_floors = json_['data']['floors']
        result = []
        try:
            amenity = ''
            amenity_ = r_soup.select('section#main-section ul li ')
            for li in amenity_:
                amenity += li.text + '; '
        except:
            amenity = ''
        for json_u in json_units:
            try:
                unit = json_u['unit_number']
            except:
                unit = ''
            try:
                bedroom = ''
                bathroom = ''
                image_source = ''
                for j_f_p in json_floor_plans:
                    if j_f_p['id'] == json_u['floor_plan_id']:
                        try:
                            bedroom = j_f_p['bedroom_count']
                        except:
                            bedroom = '0'
                        try:
                            bathroom = j_f_p['bathroom_count']
                        except:
                            bathroom = '0'
                        try:
                            image_source = j_f_p['image_url']
                        except:
                            image_source = ''

            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
                image_source = 'ERROR'

            net_price = ''
            try:
                price = json_u['price']
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = json_u['area']
            except:
                sqft = 'ERROR'
            try:
                description = ''
            except:
                description = ''
            try:
                floor = ''
                for j_f in json_floors:
                    if j_f['id'] == json_u['floor_id']:
                        try:
                            floor = j_f['filter_short_label']
                        except:
                            image_source = ''

            except:
                floor = 'ERROR'
            status = 'Rental'
            try:
                availability = json_u['available_on']
            except:
                availability = 'ERROR'
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '160 Morgan St'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "The Morgan at Provost Square"
            borough = 'Waterfront'
            zip_code = '07302'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def lumberhousejc(self):
        url = "https://www.lumberhousejc.com/threebedrooms"
        s_url = self.send_requests(url)
        a = s_url.select("a[class='sqs-block-button-element--medium sqs-button-element--primary "
                         "sqs-block-button-element']")
        result = []
        am = self.send_requests('https://www.lumberhousejc.com/amenities')
        try:
            amenity = ''
            amenity_ = am.select('p.sqsrte-small')
            for li in amenity_:
                amenity += li.text + '; '
        except:
            amenity = ''
        print(amenity)
        for a_ in a:
            link = "https://www.lumberhousejc.com" + a_.get('href')
            if 'lightbox' in link:
                continue
            soup = self.send_requests(link)
            trs = soup.select('div.sqs-block.html-block.sqs-block-html div.sqs-block-content strong')
            others = soup.select('.row .row.sqs-row')
            units = soup.select('div.content div.sqs-block.html-block.sqs-block-html h4 strong')
            for unit, other in zip(units, others[1:]):
                u_n = ''
                units_ = []
                for u in unit.text:
                    if u in '0123456789':
                        u_n += u
                    if u == '|':
                        units_.append(u_n)
                        u_n = ''
                units_.append(u_n)
                for unit__ in units_:
                    try:
                        bed_bath_ = other.select(' p.sqsrte-large')
                        try:
                            bedroom = "".join(c for c in bed_bath_[0].text if c.isdecimal())
                        except:
                            bedroom = '0'
                        try:
                            bathroom = "".join(c for c in bed_bath_[1].text if c.isdecimal())
                            if len(bathroom) > 1:
                                bathroom = "".join(c for c in bed_bath_[2].text if c.isdecimal())
                        except:
                            bathroom = '0'
                    except:
                        bedroom = 'ERROR'
                        bathroom = 'ERROR'
                    net_price = ''
                    try:
                        price_ = soup.select_one(' h4')
                        price = "".join(c for c in price_.text if c.isdecimal()) + '+'
                    except:
                        price = 'ERROR'
                    # price = "".join(c for c in price_ if c.isdecimal())
                    try:
                        sqft = other.select('p.sqsrte-large')[2].text
                        if 'BATHS' in sqft:
                            sqft = other.select('p.sqsrte-large')[1].text
                    except:
                        sqft = 'ERROR'
                    try:
                        description = ''
                    except:
                        description = ''
                    floor = ''
                    status = 'Rental'

                    try:
                        availability = ''
                    except:
                        availability = ''
                    try:
                        image_source = ''
                        image_source_ = other.select_one('a').get('href')
                        image_link = re.search("residence\d+_", image_source_).group(0).replace('_', '')
                        i_m_g = self.send_requests(f'https://www.lumberhousejc.com/{image_link}?format=html')
                        image_source = i_m_g.select_one('img.thumb-image').get('data-src')

                    except:
                        image_source = ''
                    if self.checking_if_file_exists() is False:
                        created_at = datetime.now().strftime('%d-%m-%Y')
                    else:
                        created_at = self.checking_if_file_exists()
                    update_ut = datetime.now().strftime('%d-%m-%Y')
                    if availability == '':
                        data_present = 0
                    else:
                        data_present = 1
                    address = '430 PALISADE AVENUE'
                    city = 'Jersey City'
                    state = 'NJ'
                    building_name = "Lumber House"
                    borough = 'The Heights'
                    zip_code = '07307'
                    # You can append data only what is available
                    result.append({
                        "Unit": unit__,
                        "Bedroom": bedroom,
                        "Bathroom": bathroom,
                        "Gross Price": price,
                        "Net price": net_price,
                        "Sqft": sqft.replace(' SF', ''),
                        "Floor": floor,
                        "Amenity": amenity,
                        "Description": description,
                        "Status": status,
                        "Availability": availability,
                        "Source": url,
                        "Floorplan_Image_URL": image_source,
                        "Created_at": created_at,
                        "Updated_at": update_ut,
                        "Date_present": data_present,
                        "Address": address,
                        "City": city,
                        "Building Name": building_name,
                        # Get the corresponding address from "Target_Websites" spreadsheet
                        "Borough": borough,
                        "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                        "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
                    })
        self.save_data(result)
        print(f"{url} scraped")

    def thearthousejc(self):
        url = "https://www.thearthousejc.com/"
        soup = self.send_requests(url)
        trs = soup.select('tbody#artjcallbed0 tr')
        result = []
        for tr in trs:
            link = "https://www.thearthousejc.com/" + tr.select_one("td[data-title='Floorplan'] a").get('href')
            r_soup = self.send_requests(link)
            f_p = self.send_requests(tr.select_one("td[data-title='Apply Now'] a").get('href'))
            try:
                unit = tr.select_one("td[data-title='Unit Number']").text
            except:
                unit = ''
            try:
                bed_bath_ = f_p.select_one("span[data-selenium-id='TermsFPBedBath']").text
                bed_bath = "".join(c for c in bed_bath_ if c.isdecimal())
                try:
                    if len(bed_bath) == 1:
                        bedroom = '0'
                    else:
                        bedroom = bed_bath[0]

                except:
                    bedroom = '0'
                try:
                    if len(bed_bath) == 1:
                        bathroom = bed_bath[0]
                    else:
                        bathroom = bed_bath[1]
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = tr.select_one("td[data-title='Price']").text.replace('$', '').replace('.00', '')
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = tr.select_one("td[data-title='Indoor Sqft']").text.replace(' sqft', '')
            except:
                sqft = 'ERROR'
            try:
                description = ''
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                amenity = ''
                amenity_ = r_soup.select('div.bottomSec li')
                for li in amenity_[1:]:
                    amenity += li.text.replace('\n', '') + '; '
            except:
                amenity = ''
            print(amenity)
            try:
                availability = tr.select_one("td[data-title='Availability']").text.strip()
            except:
                availability = ''
            try:
                image_source = r_soup.select_one('a.fancybox').get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '148 1st St'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "DVORA Art House"
            borough = 'Waterfront'
            zip_code = '07302'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def threejournalsquare(self):
        url = "https://www.threejournalsquare.com/Floor-plans.aspx"
        soup = self.send_requests(url)
        divs = soup.select('div.floorplan-block.filtered-in')
        result = []
        for div in divs:
            try:
                unit = div.select_one('div.content_area_top h2').text
            except:
                unit = ''
            try:
                bed_bath_ = div.select('div.specification span[id]')
                try:
                    bedroom = bed_bath_[0].text
                    if bedroom not in '1234567890':
                        bedroom = 0
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_[1].text
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = ''
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = div.select('div.specification span[id]')[2].text.replace(',', '')
            except:
                sqft = 'ERROR'

            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                amenity = ''
                amenity_ = div.select('div.amenities-container ul li')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = div.select_one(
                    'span.floorplan-image span.floor-plan-full-size-thumbnail.floor-plan-thumbnail').get('data-src')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '2935 John F Kennedy Blvd'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "3 Journal Square"
            borough = 'Journal Square'
            zip_code = '07306'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def vantagejc(self):
        amenity_soup = self.send_requests('https://www.vantagejc.com/amenities/')

        url = "https://www.vantagejc.com/floor/?bedroom=&availability=&address="
        soup = self.send_requests(url)
        divs = soup.select('div.price.fp-list div.eltd-hrl-item-inner')
        result = []
        try:
            amenity = ''
            amenity_ = amenity_soup.select('li.li1')
            for li in amenity_:
                amenity += li.text + '; '
        except:
            amenity = ''
        for div in divs:
            try:
                unit_ = div.select_one('div.info h2').text
                unit = "".join(c for c in unit_ if c.isdecimal())
            except:
                unit = ''
            try:
                count = 0
                bed_bath_ = ''
                price = ''
                sqft = ''
                for x in div.select_one('div.info h4.eltd-hrl-item-title.okk').text.strip():
                    if x == '|':
                        count += 1
                        continue
                    if count == 0:
                        bed_bath_ += x
                    if count == 1:
                        sqft += x
                    if count == 2:
                        price += x
            except:
                bed_bath_ = 'ERROR'
                price = 'ERROR'
                sqft = 'ERROR'

            try:
                bed_bath_ = bed_bath_.strip()
                if bed_bath_.strip() == 'Studio':
                    bedroom = 0
                    bathroom = 1
                else:
                    bed_bath_ = "".join(c for c in bed_bath_ if c.isdecimal())
                    bedroom = bed_bath_[0]
                    bathroom = bed_bath_[1]
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            net_price = ''
            try:
                price = price.strip().replace('$', '').replace(',', '')
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = sqft.strip().replace(' SF', '')
            except:
                sqft = 'ERROR'

            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''
            status = 'Rental'
            try:
                availability = div.select('div.info h4.eltd-hrl-item-title.okk')[1].text.strip()
                if ' NOW' in availability:
                    availability = datetime.now().strftime('%d-%m-%Y')
                else:
                    availability = availability.replace('AVAILABLE ', '')
            except:
                availability = 'ERROR'
            print(availability)

            try:
                image_source = div.select_one('button.view').get('id')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '1-33 Park View Avenue'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "Downtown"
            borough = 'Journal Square'
            zip_code = '07302'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def parkandshore(self):
        url = "https://parkandshore.com/availability"
        soup = self.send_requests(url)
        divs = soup.select('div.card')
        result = []
        for div in divs:
            link = div.select_one('div.card a').get('href')
            r_soup = self.send_requests('https://parkandshore.com' + link)
            floor_image_link = re.findall('"url":"(.*?)"', str(r_soup))
            try:
                unit = div.select_one('div.card-title-price span').text.replace('Residence ', '')
            except:
                unit = ''
            try:
                count = 0
                bedroom = ''
                bathroom = ''
                sqft = ''
                for x in div.select_one('div.card-text span').text:
                    if x == '/':
                        count += 1
                        continue
                    if count == 0:
                        bedroom += x
                    if count == 1:
                        bathroom += x
                    if count == 2:
                        sqft += x
                bedroom = bedroom.replace(' BR', '')
                bathroom = bathroom.replace(' BA', '')
                sqft = sqft.replace('SF', '').strip()
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
                sqft = 'ERROR'
            net_price = ''
            try:
                price = div.select('div.card-title-price span')[1].text.replace('$', '')
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                description = r_soup.select_one('div.availabilty-row__content p').text
            except:
                description = ''
            try:
                floor = r_soup.select_one("div.card").get('data-floor')
            except:
                floor = ''
            status = 'For sale'
            try:
                amenity = ''
                amenity_ = r_soup.select('li.list-amenities')
                for li in amenity_:
                    amenity += li.text + '; '
            except:
                amenity = ''
            try:
                availability = datetime.now().strftime('%d-%m-%Y')
            except:
                availability = ''
            try:
                image_source = ''
                for link_ in floor_image_link:
                    if "unit" in link_:
                        image_source = "https://parkandshore.com/" + link_
                    else:
                        continue
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '75 PARK LANE'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "75 Park Lane"
            borough = 'Waterfront'
            zip_code = '07310'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def maxwellplace(self):
        url = "https://www.maxwellplace.com/availability"
        soup = self.send_requests(url)
        divs = soup.select('div.unit-listing.js-unitListing')
        a_soup = self.send_requests('https://www.maxwellplace.com/amenities')

        result = []
        try:
            amenity = ''
            amenity_ = a_soup.select('div.features li')[1:]
            for li in amenity_:
                amenity += li.text + '; '
        except:
            amenity = ''
        for div in divs:
            link = div.select_one('a.bottom-button').get('href')
            r_soup = self.send_requests('https://www.maxwellplace.com' + link)
            try:
                unit = div.get('data-name')
            except:
                unit = ''

            try:
                bedroom = div.get('data-beds')
            except:
                bedroom = '0'
            try:
                bathroom = div.get('data-baths')
            except:
                bathroom = '0'

            net_price = ''
            try:
                price = div.get('data-price')
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = div.get('data-sqft')
            except:
                sqft = 'ERROR'

            try:
                description = r_soup.select_one('article p').text
            except:
                description = ''
            floor = ''
            status = 'For sale'

            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = r_soup.select_one('div.unit-image a').get('href')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '1000 Maxwell Place'
            city = 'Hoboken'
            state = 'NJ'
            building_name = "1000 Maxwell"
            borough = ''
            zip_code = '07030'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def venturagardenstreetlofts(self):
        url = "https://www.venturagardenstreetlofts.com/floor-plans/"
        soup = self.send_requests(url)
        divs = soup.select('div.floorplan_item')
        result = []
        a_soup = self.send_requests('https://www.venturagardenstreetlofts.com/amenities/')
        try:
            amenity = ''
            amenity_ = a_soup.select('div.col-md-4.content_block_content li')
            for li in amenity_:
                amenity += li.text + '; '
        except:
            amenity = ''
        for div in divs:
            try:
                unit = div.select_one("h3[role='heading']").text
            except:
                unit = ''
            try:
                bed_bath_ = div.select_one('p')
                bed_bath_ = str(bed_bath_).replace('<br/>', '|')
                bed_bath_ = BeautifulSoup(bed_bath_, 'html.parser').text
                count = 0
                sqft = ''
                bedroom = ''
                bathroom = ''
                for x in bed_bath_:
                    if x == '|':
                        count += 1
                        continue
                    if count == 1:
                        sqft += x
                if 'Studio' in bed_bath_:
                    bedroom = '0'
                if 'One Bath' in bed_bath_:
                    bathroom = 1
                if 'One Bedroom' in bed_bath_:
                    bedroom = 1
                sqft = sqft.replace(' Sq. Ft.', '')
            except:
                sqft = 'ERROR'
                bedroom = 'ERROR'
                bathroom = 'ERROR'

            net_price = ''
            try:
                price = div.select_one("h4").text.replace('Starting at: $', '')
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''
            status = 'Rental'

            try:
                availability = ''
            except:
                availability = ''
            try:
                image_source = div.select_one('img').get('src')
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '1425 Garden St'
            city = 'Hoboken'
            state = 'NJ'
            building_name = "garden street lofts"
            borough = 'Downtown'
            zip_code = '07030'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def revetmenthouse(self):
        url = "https://www.revetmenthouse.com/availability/"
        soup = self.send_requests(url)
        divs = soup.select('div.search__body div.search__item')
        a_soup = self.send_requests('https://www.revetmenthouse.com/#amenities')
        result = []
        try:
            amenity = ''
            amenity_ = a_soup.select('div.photo-item-text-grid li')
            for li in amenity_:
                amenity += li.text.strip() + '; '
        except:
            amenity = ''
        for div in divs:
            data_unit_id = div.get('data-unit-id')
            try:
                unit = div.select_one('div.search__line.col-01').text.replace('Residence ', '')
            except:
                unit = ''
            j_link = f"https://www.revetmenthouse.com/ajax/getunitdetails.asp?u={data_unit_id}&l=Residence%20{unit}&ln=om"
            j_json = requests.get(j_link, self.headers).text

            try:
                bed_bath_ = div.select_one('div.search__size.col-02')
                try:
                    bedroom = bed_bath_.select_one('span.search__size__bed').text.replace(' Bedroom', '')
                except:
                    bedroom = '0'
                try:
                    bathroom = bed_bath_.select_one('span.search__size__bath').text.replace(' Bathroom', '')
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            try:
                net_price = div.select_one('div.search__price.col-04').text.replace('$', '')
            except:
                net_price = ''
            try:
                price = ''
            except:
                price = 'ERROR'
            # price = "".join(c for c in price_ if c.isdecimal())
            try:
                sqft = div.select_one('div.search__sqft.col-03').text.replace(' Sq Ft', '')
            except:
                sqft = 'ERROR'
            try:
                description = div.select_one('p.js-listing-description').text
            except:
                description = ''
            floor = ''
            status = 'Rental'

            try:
                availability = json.loads(j_json)['unit']['extra']['date_available']
            except:
                availability = ''
            try:
                image_source = 'https://adkast.messagekast.com' + json.loads(j_json)['unit']['extra']['floorplan_pdf']
            except:
                image_source = ''
            if self.checking_if_file_exists() is False:
                created_at = datetime.now().strftime('%d-%m-%Y')
            else:
                created_at = self.checking_if_file_exists()
            update_ut = datetime.now().strftime('%d-%m-%Y')
            if availability == '':
                data_present = 0
            else:
                data_present = 1
            address = '121 Town Square Place'
            city = 'Jersey City'
            state = 'NJ'
            building_name = "REVETMENT HOUSE"
            borough = 'Waterfront'
            zip_code = '07310'
            # You can append data only what is available
            result.append({
                "Unit": unit,
                "Bedroom": bedroom,
                "Bathroom": bathroom,
                "Gross Price": price,
                "Net price": net_price,
                "Sqft": sqft,
                "Floor": floor,
                "Amenity": amenity,
                "Description": description,
                "Status": status,
                "Availability": availability,
                "Source": url,
                "Floorplan_Image_URL": image_source,
                "Created_at": created_at,
                "Updated_at": update_ut,
                "Date_present": data_present,
                "Address": address,
                "City": city,
                "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                "Borough": borough,
                "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
            })
        self.save_data(result)
        print(f"{url} scraped")

    def moderlofts(self):
        url = "https://www.moderalofts.com/jersey-city/modera-lofts/conventional/"
        soup = self.send_requests(url)
        divs = soup.select('li.fp-group-item')
        result = []
        a_soup = self.send_requests('https://www.moderalofts.com/jersey-city-nj-apartments/modera-lofts/amenities/')
        try:
            amenity = ''
            amenity_ = a_soup.select('li.amenity-item')
            for li in amenity_:
                amenity += li.text.strip() + '; '
        except:
            amenity = ''
        for div in divs:
            f_link = div.select_one('a.primary-action').get('href')
            pr_id_ = re.search(r'&property\[id\]=\d+&', f_link).group(0)
            pf_id_ = re.search(r'&property_floorplan\[id\]=\d+&', f_link).group(0)
            pr_id_ = "".join(c for c in pr_id_ if c.isdecimal())
            pf_id_ = "".join(c for c in pf_id_ if c.isdecimal())
            try:
                image_source = div.select_one('div.image-container.popover-holder.js-popover meta').get('content')
            except:
                image_source = ''
            try:
                bed_bath_ = div.select_one('li.fp-group-item div.fp-col.bed-bath span.fp-col-text').text
                try:
                    bedroom = re.search(r"\dbd", bed_bath_).group(0).replace('bd', '')
                except:
                    bedroom = '0'
                try:
                    bathroom = re.search(r"\dba", bed_bath_).group(0).replace('ba', '')
                except:
                    bathroom = '0'
            except:
                bedroom = 'ERROR'
                bathroom = 'ERROR'
            if div.select_one('div.fp-col.action a').text == 'Get Notified':
                sqft = div.select_one('div.fp-col.sq-feet span.fp-col-text').text
                unit = ''
                net_price = ''
                price = ''
                description = ''
                floor = ''
                status = 'Rental'
                availability = ''
                building_name = 'Hudson Lights'
                address = '2030 Hudson Street'
                borough = 'Fort Lee'
                city = 'Bergen County'
                state = 'NJ'
                zip_code = '*07024'
                if self.checking_if_file_exists() is False:
                    created_at = datetime.now().strftime('%d-%m-%Y')
                else:
                    created_at = self.checking_if_file_exists()
                update_ut = datetime.now().strftime('%d-%m-%Y')
                if availability == '':
                    data_present = 0
                else:
                    data_present = 1
                result.append({
                    "Unit": unit,
                    "Bedroom": bedroom,
                    "Bathroom": bathroom,
                    "Gross Price": price,
                    "Net price": net_price,
                    "Sqft": sqft,
                    "Floor": floor,
                    "Amenity": amenity,
                    "Description": description,
                    "Status": status,
                    "Availability": availability,
                    "Source": url,
                    "Floorplan_Image_URL": image_source,
                    "Created_at": created_at,
                    "Updated_at": update_ut,
                    "Date_present": data_present,
                    "Address": address,
                    "City": city,
                    "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "Borough": borough,
                    "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "ZIP Code": zip_code
                })

            content = requests.get(f'https://www.moderalofts.com/?module=check_availability&is_secure=1&property'
                                   f'[id]={pr_id_}&action=view_unit_spaces&property_floorplan[id]={pf_id_}&'
                                   f'move_in_date=true&term_month=26&occupancy_type=conventional#',
                                   headers=self.headers).text
            r_soup = BeautifulSoup(content, 'lxml')
            divs_ = r_soup.select('div.unit-row.js-unit-row')
            for div_ in divs_:
                try:
                    unit = div_.select_one('div.unit-col.unit span.unit-col-text').text.replace('Unit ', '')
                except:
                    unit = 'ERROR'
                net_price = ''
                try:
                    price_ = div_.select_one('div.unit-col.rent').text
                    price = "".join(c for c in price_ if c.isdecimal())
                except:
                    price = 'ERROR'
                try:
                    sqft = div_.select_one('div.unit-col.sqft span.unit-col-text').text
                except:
                    sqft = 'ERROR'

                try:
                    description = ''
                except:
                    description = ''
                floor = ''
                status = 'Rental'

                try:
                    availability = div_.select_one('div.unit-col.availability span.unit-col-text').text
                    if availability == 'Now':
                        availability = datetime.now().strftime('%d-%m-%Y')
                except:
                    availability = ''
                if self.checking_if_file_exists() is False:
                    created_at = datetime.now().strftime('%d-%m-%Y')
                else:
                    created_at = self.checking_if_file_exists()
                update_ut = datetime.now().strftime('%d-%m-%Y')
                if availability == '':
                    data_present = 0
                else:
                    data_present = 1
                building_name = 'Modera Lofts'
                address = '350 Warren St'
                borough = 'Waterfront'
                city = 'Jersey City'
                state = 'NJ'
                zip_code = '07302'

                result.append({
                    "Unit": unit,
                    "Bedroom": bedroom,
                    "Bathroom": bathroom,
                    "Gross Price": price,
                    "Net price": net_price,
                    "Sqft": sqft,
                    "Floor": floor,
                    "Amenity": amenity,
                    "Description": description,
                    "Status": status,
                    "Availability": availability,
                    "Source": url,
                    "Floorplan_Image_URL": image_source,
                    "Created_at": created_at,
                    "Updated_at": update_ut,
                    "Date_present": data_present,
                    "Address": address,
                    "City": city,
                    "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "Borough": borough,
                    "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "ZIP Code": zip_code
                })
        self.save_data(result)
        print(f"{url} scraped")

    def hudsoncondominiums77(self):
        url = "https://77hudsoncondominiums.com/"
        soup = self.send_requests(url)
        links_ = soup.select('ul.navigation li.navigation__item.sub-nav-container li a')[:2]
        result = []
        for link in links_:
            soup = self.send_requests('https://77hudsoncondominiums.com' + link)
            divs = soup.select("div[class='item w-50-l w-100 db fl listing-card-wrapper']")
            for div in divs:
                fool_data_link = soup.select_one("a").get('href')
                print(fool_data_link)
                soup_two = self.send_requests('https://77hudsoncondominiums.com' + fool_data_link)
                try:
                    unit = div.select_one('div.content_area_top h2').text
                except:
                    unit = ''
                try:
                    bed_bath_ = div.select('div.specification span[id]')
                    try:
                        bedroom = bed_bath_[0].text
                    except:
                        bedroom = '0'
                    try:
                        bathroom = bed_bath_[1].text
                    except:
                        bathroom = '0'
                except:
                    bedroom = 'ERROR'
                    bathroom = 'ERROR'
                net_price = ''
                try:
                    price = ''
                except:
                    price = 'ERROR'
                # price = "".join(c for c in price_ if c.isdecimal())
                try:
                    sqft = div.select('div.specification span[id]')[2].text.replace(',', '')
                except:
                    sqft = 'ERROR'

                try:
                    description = div.select_one('p.js-listing-description').text
                except:
                    description = ''
                floor = ''
                status = 'Rental'
                try:
                    amenity = ''
                    amenity_ = div.select('div.amenities-container ul li')
                    for li in amenity_:
                        amenity += li.text + '; '
                except:
                    amenity = ''
                try:
                    availability = ''
                except:
                    availability = ''
                try:
                    image_source = div.select('div.img_area ul li a')[-1].get('href')
                except:
                    image_source = ''
                if self.checking_if_file_exists() is False:
                    created_at = datetime.now().strftime('%d-%m-%Y')
                else:
                    created_at = self.checking_if_file_exists()
                update_ut = datetime.now().strftime('%d-%m-%Y')
                if availability == '':
                    data_present = 0
                else:
                    data_present = 1
                address = '463 Pacific Avenue'
                city = 'Jersey City'
                state = 'NJ'
                building_name = "Glennview Townhouses"
                borough = 'Bergen-Lafayette'
                zip_code = '07304'
                # You can append data only what is available
                result.append({
                    "Unit": unit,
                    "Bedroom": bedroom,
                    "Bathroom": bathroom,
                    "Gross Price": price,
                    "Net price": net_price,
                    "Sqft": sqft,
                    "Floor": floor,
                    "Amenity": amenity,
                    "Description": description,
                    "Status": status,
                    "Availability": availability,
                    "Source": url,
                    "Floorplan_Image_URL": image_source,
                    "Created_at": created_at,
                    "Updated_at": update_ut,
                    "Date_present": data_present,
                    "Address": address,
                    "City": city,
                    "Building Name": building_name,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "Borough": borough,
                    "State": state,  # Get the corresponding address from "Target_Websites" spreadsheet
                    "ZIP Code": zip_code  # Get the corresponding address from "Target_Websites" spreadsheet
                })
            self.save_data(result)
            print(f"{url} scraped")
# Build_Scrapers_Requests().nine15broad()

bl = Build_Scrapers_Requests()
# bl.packardjc()
# bl.nine15broad()
# bl.housejc()
# bl.hudson2400()
# bl.senateplace()
# bl.jfk2130()
# bl.ninthjc372()
# bl.acresjc3()
# bl.elm60()
# bl.baygrovearms()
# bl.embankmenthouse()
# bl.halfmoonharbourapts()
# bl.hudsonlightsnj()
# bl.liveatbarbarasplace()
# bl.liveatglennviewtownhouses()
# bl.liveatoceanstower()
# bl.liveatpacificcourt()
# bl.livethemorgan()
# bl.lumberhousejc()
# bl.thearthousejc()
# bl.vantagejc()
# bl.parkandshore()
# bl.maxwellplace()
# bl.venturagardenstreetlofts()
# bl.revetmenthouse()
# bl.moderlofts()
bl.hudsoncondominiums77()
bl.save_csv()
# Build_Scrapers_Requests().next_website()
