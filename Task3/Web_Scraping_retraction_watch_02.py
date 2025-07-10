import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, NoSuchElementException
import time
import pandas as pd
import math

s = Service(r"chromedriver.exe")
file_path = r"Task_3_Annotation-MU-dependent_gpt_gemini.csv"
new_file_path = r"Task_3_Annotation-MU-dependent_gpt_gemini.csv"
df = pd.read_csv(file_path)
# print(df)
df['CitingID'] = df['CitingID'].astype(str)
# df['pmcid'] = df['pmcid'].astype(str)
# df['Title'] = df['Title'].astype(str)
# df['Retraction_Watch'] = df['Retraction_Watch'].astype(str)

driver = webdriver.Chrome(service = s)
driver.get("https://retractiondatabase.org/RetractionSearch.aspx")

# df['Retraction_Watch_citing'] = df['Retraction_Watch_citing'].astype(str)
Retraction_Watch_citing = []

for index, row in df.iterrows():

    # print(row['Title'])
    # if pd.isnull(row['Title']):
        # print(row['CitedID'])
    text_in_watch = ''
    try:
        driver.find_element(By.NAME, 'txtOriginalPubMedID').clear()
        driver.find_element(By.NAME, 'txtOriginalPubMedID').send_keys(row['CitingID'])
        driver.find_element(By.XPATH, '//*[@id="btnSearch"]').click()

        reason_elements = driver.find_elements(By.CLASS_NAME, 'rReason')
        # title_element = driver.find_element(By.CLASS_NAME, 'rTitleNotIE')

        for i, element in enumerate(reason_elements):
            text_in_watch = element.text  + '\n' + text_in_watch
        # title = title_element.text

        Retraction_Watch_citing.append(text_in_watch)

        time.sleep(1)

    except Exception as e:
        print(f"No result for {row['CitingID']}")
        title = ''
        Retraction_Watch_citing.append("")



df['Retraction_Watch_citing'] = Retraction_Watch_citing

driver.quit()

df.to_csv(new_file_path, index=False)


