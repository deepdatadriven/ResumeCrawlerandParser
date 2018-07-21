# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
## Author: Lin Tang
## Email:  niurenjob@hotmail.com
## Description: this is used to crawl all the information of every applicant from http://www.****.com/career/Admin/
## Date: 07/18/2018


import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import random


def save_csv(info_dict, page, index):
    df = pd.DataFrame.from_dict(info_dict, orient='index')
    df.index.name = 'id'
    df.columns = ["email", "name", "phone_number", "location", "skills", "resume_name"]
    output_name = "page_" + str(page) + "_" + str(index) + '.csv'
    df.to_csv('resume_info//' + output_name)
    print("---------------------------------------------")
    print(output_name + ' is done')
    print("---------------------------------------------")

class Spider(object):
    """
    crawl class
    """
    def __init__(self):
        self.browser = webdriver.Chrome(self._getdriverpath())
        self.browser.implicitly_wait(60) # Implicit waiting, up to 30 seconds
        self.browser.maximize_window()
        self.login()

        self.wait = WebDriverWait(self.browser, 10)

    def login(self):
        username = <UserName>
        password = <Password>
        # login url
        url = 'http://www.*****.com/career/Admin/'
        #self.browser.set_window_size(480, 760)
        self.browser.get(url)
        # next page after login
        # use xpath to get the login button
        elem = self.browser.find_element_by_id("txtUserName")
        elem.send_keys(username)
        elem = self.browser.find_element_by_id("txtPassword")
        elem.send_keys(password)
        elem = self.browser.find_element_by_xpath('//*[@id="btnLogin"]')
        elem.send_keys(Keys.ENTER)
        time.sleep(2)
        self.cookie2 = self.browser.get_cookies()
        # print cookie's information
        print(self.cookie2)

    def get_data(self):
        time.sleep(random.random() * random.choice([3,4,5]))
        page = 1
        page_total = 1
        index = 0
        start = True
        while page_total < 252:
            try:
                soup = BeautifulSoup(self.browser.page_source, "html.parser")
                tr_list = soup.select("table#ContentPlaceHolder1_datagridShowCandidate > tbody > tr")

                table = PrettyTable(["id", "email", "name", "phone_number", "location", "skills", "resume_name"])
                info_dict = {}
                for item in tr_list[1:-1]:
                    try:
                        results = []
                        td_list = item.select("td > table > tbody > tr > td")
                        results.append(str(index))
                        email = td_list[0].find('span').text.replace("\n", "").replace(" ", "")
                        results.append(email)
                        name = td_list[1].select("span")[0].text.replace("\n", "").replace("  ", " ") + " " + td_list[1].select("span")[1].text.replace("\n", "").replace(" ", "")
                        results.append(name)
                        phone_number = td_list[2].select("span")[0].text.replace("\n", "").replace(" ", "")
                        results.append(phone_number)
                        location = td_list[3].select("span")[0].text.replace("\n", "").replace(" ", "").strip()
                        results.append(location)
                        skills_temp = td_list[4]
                        skills = ""
                        for i, skill in enumerate(skills_temp.findAll('br')):
                            if i == 0:
                                skills = skills + skill.previous_sibling + "\n"
                                skills = skills + skill.next_sibling + "\n"
                            else:
                                skills = skills + skill.next_sibling + "\n"
                        skills = skills.strip()
                        results.append(skills)
                        if len(td_list[6].select("input")) < 2:
                            link_doc_name = "None"
                        else:
                            link_doc_name = td_list[6].select("input")[1].attrs["value"]
                        results.append(link_doc_name)
                        # link_id = td_list[6].select("input")[0].attrs["id"]
                        # link = self.browser.find_element_by_id(link_id)
                        # link.click()
                        table.add_row(results)
                        info_dict[index] = results[1:]
                        index += 1
                    except Exception as e:
                        print(e)

                print("=====================================page: %s=================================" % page_total)
                print(table)
                save_csv(info_dict, page_total, index)
                # self.login()
                xpath = '//*[@id="ContentPlaceHolder1_datagridShowCandidate"]/tbody/tr[12]/td/a[%s]' % page
                elem = self.browser.find_element_by_xpath(xpath)
                elem.click()

                if start == True:
                    if int(page_total) == 10 or int(page_total) == 11:
                        start = False
                        page = 2
                    else:
                        page += 1
                else:
                    if page == 11:
                        page = 2
                    else:
                        page += 1

                page_total += 1
                time.sleep(random.random() * random.choice([3, 4, 5]))
            except Exception as e:
                print(e)

    def quit(self):
        self.browser.close()

    def _getdriverpath(self):
        path = "chromedriver.exe"
        return path

if __name__ == '__main__':
    Spider().get_data()