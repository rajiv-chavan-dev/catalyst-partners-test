from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from bs4 import BeautifulSoup


def scrape_website(url, webdriver_path):
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options = option)
    # Initialize the Chrome WebDriver
    # driver = webdriver.Chrome(executable_path=webdriver_path)

    try:
        # Open the URL in the browser
        driver.get(url)

        # Wait for the page to load (you may need to adjust the waiting time)
        time.sleep(5)

        # Create an empty list to store scraped data
        scraped_data = []

        # Locate and click the "Next" button to navigate through the pages (if available)
        i=0
        while i<2:
            soup=BeautifulSoup(driver.page_source)
            # import ipdb;ipdb.set_trace()
            all_tr = soup.find_all('tr',{'role':'row'})
            for each_tr in all_tr:
                all_td = each_tr.find_all('td')
                data_dict = {}
                for each_td in all_td:
                    span_text = each_td.find('span').text 
                    if span_text == "Bid Solicitation #":
                        if "Bid Number" in data_dict.keys():
                            pass 
                        data_dict['Bid Number'] = each_td.text.replace("Bid Solicitation #","")
                    elif span_text == "Buyer":
                       data_dict['Buyer'] = each_td.text.replace("Buyer","")
                    elif span_text == "Description":
                        data_dict['Description'] = each_td.text.replace("Description","")
                    elif span_text == "Bid Opening Date":
                        data_dict['Bid Opening Date'] = each_td.text.replace("Bid Opening Date","")
                if data_dict:
                    scraped_data.append(data_dict)
            # # Locate and click the "Next" button to navigate to the next page
            # import ipdb;ipdb.set_trace()
            next_button = driver.find_element(By.XPATH, '//*[@id="bidSearchResultsForm:bidResultId_paginator_bottom"]/span[4]/span[2]')
            next_button.click()
            time.sleep(5)  # Adjust the waiting time as needed
            i += 1

    except Exception as e:
        print("Error:", str(e))

    finally:
        # Close the WebDriver when done
        driver.quit()
        with open("mydata.json", "w") as final:
            json.dump(scraped_data, final)

# Example usage of the function
if __name__ == "__main__":

    url_to_scrape = "https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true"
    chrome_webdriver_path = "/Users/work/python/chromedriver_mac64/chromedriver"  # Replace with the actual path to Chrome WebDriver

    scrape_website(url_to_scrape, chrome_webdriver_path)
