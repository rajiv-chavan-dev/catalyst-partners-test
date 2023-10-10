import time
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def scrape_website(url, webdriver_path):
    try:
        all_list = []
        for i in range(0,9):
            final_url = url + str(i)
            response = requests.get(final_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                all_teachers = soup.find_all('div',{'class':'views-row'})
                school_name = soup.find('div',{'class':'site-name'}).text
                address = soup.find("p",{"class":"address"}).text
                state = address.split(",")[-1].replace("55387","")
                zip_code = address.split(",")[-1].replace("MN","").replace("Directions","")
                for teacher in all_teachers:
                    # import ipdb;ipdb.set_trace()
                    data_dict = {}
                    data_dict['school_name'] = school_name.strip()
                    add = re.sub(r"\s+", " ", address)
                    data_dict['address'] = add
                    st = re.sub(r"\s+", "", state)
                    data_dict['state'] = st.replace("Directions","")
                    z = re.sub(r"\s+", "", zip_code)
                    data_dict['zip_code'] = z
                    name = teacher.find('h2',{'class':'title'}).text
                    last_name = name.split(",")[0]
                    data_dict['last_name'] = last_name
                    first_name = name.split(",")[1]
                    data_dict['first_name'] = first_name
                    title = teacher.find("div",{'class':'field job-title'}).text
                    data_dict['title'] = title.strip()
                    phone_number = teacher.find('div',{'class':'field phone'}).text
                    data_dict['phone_number'] = phone_number.strip()
                    email = teacher.find('div',{'class':'field email'}).text
                    data_dict['email'] = email.strip()
                    all_list.append(data_dict)

    except Exception as e:
        print("Error:", str(e))

    finally:
        df = pd.DataFrame(all_list)
        df.to_csv("list_of_dict_to_csv.csv")

# Example usage of the function
if __name__ == "__main__":
    #main url
    url_to_scrape = "https://isd110.org/our-schools/laketown-elementary/staff-directory?s=&page="
     # Replace with the actual path to Chrome WebDriver
    chrome_webdriver_path = "/Users/work/python/chromedriver_mac64/chromedriver"  

    scrape_website(url_to_scrape, chrome_webdriver_path)
