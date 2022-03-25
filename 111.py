import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import math

url = pd.DataFrame(columns=['URL', 'City Key'])

url_data = pd.read_csv('WalkinJobs-Input.csv', dtype=str)
print(url_data.head())
url_data['URL'] = url_data['URL'].astype(str)
print(url_data.dtypes)
options = webdriver.ChromeOptions()
options.add_argument('--disable-software-rasterizer')
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
for index, row in url_data.iterrows():
    firstpage = str(row['URL'])
    url = url.append({'URL': firstpage, 'City Key': str(row['City Key'])}, ignore_index=True)

    driver.get(str(row['URL']))
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    soup.prettify()
    results = soup.find(class_='sortAndH1Cont')
    # jobs_subtext =  results.find(class_ ='fleft grey-text mr-5 fs12')
    jobs_text = results.text
    print(jobs_text)
    job_count = jobs_text.split('of')[1].strip()
    job_count = job_count.split(' ')[0]
    # print(job_count)
    pages = math.ceil(int(job_count) / 20)
    # print(pages)
    for page in range(2, pages + 1):
        site = firstpage.split('?')
        site.insert(1, '-' + str(page))
        site.insert(2, '?')
        # print(site)
        nextpage = ''.join(site)
        # print(nextpage)
        url = url.append({'URL': nextpage, 'City Key': str(row['City Key'])}, ignore_index=True)
print(url)
driver.close()
url.to_csv('url_input_pages.csv')

import time

for index, row in url.iterrows():
    u = row['URL']
    import time

    status = pd.DataFrame(columns=['URL', 'City Key', 'Status'])
    driver = webdriver.Chrome('chromedriver.exe')
    driver2 = webdriver.Chrome('chromedriver.exe')
    df = pd.DataFrame(columns=['Title', 'Company', 'Time', 'URL', 'Location', 'Job_Desc', 'City Key'])
    try:
        driver.get(str(u))
    except:
        print("url is error")
        driver.refresh()
    time.sleep(5)
    try:
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        # print(driver.current_url)
        soup.prettify()

        results = soup.find(class_='list')
        # df = pd.DataFrame(columns=['Title','Company','Time','URL', 'Location'])
        job_elems = results.find_all('article', class_='jobTuple bgWhite br4 mb-8')
        try:
            for job in job_elems:
                URL = job.find('a', class_='title fw500 ellipsis').get('href')
                Title = job.find('a', class_='title fw500 ellipsis')
                print(Title.text)
                Company = job.find('a', class_='subTitle ellipsis fleft')
                print(Company.text)

                driver2.get(URL)
                import time

                time.sleep(3)
                soup2 = BeautifulSoup(driver2.page_source, 'html5lib')
                soup2.prettify()
                # driver2.close()
                results2 = soup2.find(class_='venue')
                location = results2.text
                results2 = soup2.find(class_='walkin')
                time = results2.text
                results2 = soup2.find(class_='job-desc')
                jd = results2.text
                df = df.append(
                    {'Title': Title.text, 'Company': Company.text, 'URL': URL, 'Location': location, 'Time': time,
                     'Job_Desc': jd, 'City Key': row['City Key']}, ignore_index=True)
                status = status.append({'URL': u, 'City Key': row['City Key'], 'Status': 'success'}, ignore_index=True)
        except:
            print('Item extraction Error')
            status = status.append({'URL': URL, 'City Key': row['City Key'], 'Status': 'error'}, ignore_index=True)
    except:
        print('page Error')
        status = status.append({'URL': u, 'City Key': row['City Key'], 'Status': 'error'}, ignore_index=True)

    df.to_csv("Extract_op.csv", mode='a', header=False)
    status.to_csv('Extraction_status.csv', mode='a', header=False)
    driver.close()
    driver2.close()
