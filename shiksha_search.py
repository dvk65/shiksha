from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import numpy as np
#importing libraries

#Taking the location of chromedriver as input. chromedriver is a standalone server that webdriver uses to automate our scraping
dri_loc=("chromedriver.exe")
driver=webdriver.Chrome(dri_loc)

#Accessing the URL
url="https://www.shiksha.com/b-tech/exams-pc-10" 
driver.get(url)

#creating empty lists to store the required results
search_res_tit=[]
search_res_stit=[]
search_res_dates=[]
search_res_url=[]
csv_url_list=[]
search_res_desc=[]

#Initiating a loop to scrape all the pages
while True:
    time.sleep(5)
    #Clicking "No Thanks" every time the pop-up appears
    try:
        driver.find_element_by_id("customDenyBtn").click()
    except:
        pass

    #Gathering all the classes having the required data in them
    sea_res=driver.find_elements_by_class_name("uilp_exam_card")

    #Each class containing the data blocks is scraped. All the data required is stored in tags with unique class names. 
    #So we scrape the required data using class name.
    for sr in sea_res: 
        #Title of block
        try:
            sea_res_t=sr.find_element_by_class_name("exam_title")
            search_res_tit.append(sea_res_t.text)
        except:
            search_res_tit.append(np.nan)
        
        #clicking "No Thanks" on pop-up if it shows up
        try:
            driver.find_element_by_id("customDenyBtn").click()
        except:
            pass

        #Sub-title just under title of block
        try:
            sea_res_st=sr.find_element_by_class_name("exam_flnm")
            search_res_stit.append(sea_res_st.text)
        except:
            search_res_stit.append(np.nan)

        #clicking "No Thanks" on pop-up if it shows up
        try:
            driver.find_element_by_id("customDenyBtn").click()
        except:
            pass

        #Links at the bottom of the block. If required the URLs these links point to can be scraped using the get_attribute method
        try:
            s_url=[]
            sea_url=sr.find_elements_by_class_name("quick-links")
            for srl in sea_url:
                s_url.append(srl.text)
            surl=' '.join(s_url)
            search_res_url.append(surl)
        except:
            search_res_url.append(np.nan)

        #clicking "No Thanks" on pop-up if it shows up
        try:
            driver.find_element_by_id("customDenyBtn").click()
        except:
            pass
        
        #The description in the table in the data block
        try:
            s_desc=[]
            sea_desc=sr.find_elements_by_class_name("fix-textlength")
            for sesc in sea_desc:
                s_desc.append(sesc.text)
            sdesc='::'.join(s_desc)     #Joining the descriptions if more than one row is present
            search_res_desc.append(sdesc)
        except:
            search_res_desc.append(np.nan)
        
        #clicking "No Thanks" on pop-up if it shows up
        try:
            driver.find_element_by_id("customDenyBtn").click()
        except:
            pass
        
        #The important dates mentioned in the table in the data block
        try:
            s_dates=[]
            s_datesn=[]
            sea_date=sr.find_elements_by_class_name("fix-tdwidth")
            for sate in sea_date:
                s_dates.append(sate.text)
            for sd in s_dates:
                sdn=sd.replace("\n","")    #complete data is not stored in csv in "\n" is present in the scraped data
                s_datesn.append(sdn)
            sdate='::'.join(s_datesn)      #Joining the dates if more than one row is present
            search_res_dates.append(sdate)
        except:
            search_res_dates.append(np.nan)
 
        #Creating a dictionary to store scraped values in a dataframe
        sea_dict={"Search_Result_Title":search_res_tit,"Search_Result_SubTitle":search_res_stit, "Search_Result_URL":search_res_url,"Search_Result_Dates":search_res_dates, "Search_Result_Description": search_res_desc}
        #Writing dataframe into a csv named "infigon_search_results.csv". It will be created in the same folder as the code.
        sea_csv=pd.DataFrame(sea_dict)
        sea_csv.to_csv("Results/search_results.csv")
    
    #clicking "No Thanks" on pop-up if it shows up
    try:
        driver.find_element_by_id("customDenyBtn").click()
    except:
        pass
    
    #Clicking the next arrow at the bottom to go to the next page
    try:
        driver.find_element_by_class_name("Rgt-arrw").click()
    except:
        break

driver.close()

#If any value is not present the list is appended by "nan" as arrays must be of same length for writing them into csv