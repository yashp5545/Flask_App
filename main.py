from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import cv2
from PIL import Image
import numpy as np
import requests
import json
import csv
import time

class Bot:
    def __init__(self):
        self.driver = None
        self.first_call = True
        self.flag=0
    
    def drive(self):
        if self.driver is None:
            self.options = uc.ChromeOptions()
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument('--disable-infobars')
            self.options.add_argument('--disable-extensions')
            self.options.add_argument('--start-maximized')
            self.options.add_argument('--disable-notifications')
            # self.options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=self.options)
            self.driver.maximize_window()
        return self.driver

    def voterdata(self,name,state):
        try:
            driver = self.drive()
            driver.get("https://electoralsearch.eci.gov.in/")
            time.sleep(5)
            
            
            driver.find_element('xpath','//*[@id="mobile"]/p').click()
            
            driver.find_element('css selector',"input[name='mobile']").send_keys(name)
            
            dropdown_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'stateID'))
            )
            select = Select(dropdown_element)
            select.select_by_value(state)
            
            htmldata = driver.page_source
            soup = BeautifulSoup(htmldata, 'html.parser')
            
            xpath = '/html/body/div/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/img'
            element = driver.find_element(By.XPATH, xpath)
            
            src_attribute = element.get_attribute('src')
            
            return src_attribute
            
        except Exception as e:
            print(f"Error occurred: {e}")

    def captchadata(self,captcha):
        driver = self.drive()
        time.sleep(5)
        driver.find_element('css selector',"input[name='captcha']").send_keys(captcha)
        driver.find_element('xpath','/html/body/div/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div[4]/button').click()
        return 'Done'
        
    def getcsv(self,otp):
        driver = self.drive()
        driver.find_element('css selector',"input[name='enterOTP']").send_keys(otp)
            
        driver.find_element('xpath','/html/body/div/div[2]/div/div[3]/div[3]/div/button[1]').click()
        time.sleep(10)
        htmldata = driver.page_source
        soup = BeautifulSoup(htmldata, 'html.parser')
        dd = soup.find('table',attrs={'class':'result-table'})
        
        table_data = []
        for row in dd.find_all('tr'):
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            table_data.append(row_data)

        csv_file_path = 'Data.csv'

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            for row in table_data:
                csv_writer.writerow(row)

        return f"CSV file '{csv_file_path}' created successfully."
    
    def stop(self):
        driver = self.drive()
        driver.quit()
