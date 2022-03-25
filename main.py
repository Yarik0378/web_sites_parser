import pandas as pd
from template_requests import Build_Scrapers_Requests
# from template_requests import Build_Scrapers_Selenium


scraper = Build_Scrapers_Requests() # Instantiate scraper object

# Call methods
scraper.packardjc_com()
scraper.packardjc_com()
scraper.packardjc_com()
scraper.save_csv()
# scraper.df2.to_csv('output.csv')

# dataset.to_csv('output.csv') # Save dataframe
