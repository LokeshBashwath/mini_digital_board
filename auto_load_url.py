# selenium script to load url using from file

import datetime, time, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import configparser
config = configparser.ConfigParser(inline_comment_prefixes="#")

urls = current_url = None
service = Service(r"C:\selenium_driver\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.implicitly_wait(5)

config.read('variables.ini')
url_load_interval = int(config.get('timers','url_load_interval'))*3600  # convert hour to seconds
url_file_read_interval = int(config.get('timers','url_file_read_interval'))*60  #convert minutes to seconds
refresh_url_interval = int(config.get('timers','url_load_interval'))*60     #convert minutes to seconds
last_modified_time = os.stat('url_file.txt').st_mtime   # get last modified time of url file
retain_last_url = (config.get('settings','retain_last_url'))


def load_url(rx_url):
    #driver.get(rx_url)     # Loads the url
    print('URL loaded : ', rx_url)


def get_urls():
    if os.stat('url_file.txt').st_size == 0:
        SystemExit('The url file is empty')

    fd = open("url_file.txt", "r")
    latest_urls = []
    for ele in fd.readlines():
        latest_urls.append(ele.strip('\n'))
    print("latest_urls ", latest_urls)
    fd.close()
    return latest_urls


def check_for_file_update():
    latest_modified_time = os.stat('url_file.txt').st_mtime
    print("last modified time ", last_modified_time)
    print("latest modified time ", latest_modified_time)
    if last_modified_time == latest_modified_time:
        return False     # url_file not updated
    else:
        return True     # file got update


while True:
    try:
        with open("url_file.txt") as fd:
            url_list = fd.readlines()
            print(url_list)
        for line_num, url in enumerate(url_list):
            print(line_num+1, "->", url.strip('\n'))
            driver.get(url.strip('\n'))  # Loads the url
            time.sleep(url_load_interval)
            if url == url_list[-1]:
                if retain_last_url:
                    driver.get(url.strip('\n'))  # Loads the url
                    while True:
                        pass
        # for url in urls:
        #     load_url(url.strip('\n'))
        #     time.sleep(url_file_read_interval)
        #     if check_for_file_update():
        #         pass
        #     if url == urls[-1]:     # check is last url from url_file
        #         if check_for_file_update():
        #             print("File updated")
        #             last_modified_time = os.stat('url_file.txt').st_mtime
        #             list1 = urls
        #             list2 = get_urls()
        #             urls = [item for item in list2 if item not in list1]
        #             for url in urls:
        #                 load_url(url.strip('\n'))
        #             break
        #         else:
        #             print("File not updated ")
        #
        # urls = None

    except Exception as err:
        print("script end time : ", datetime.datetime.now())
        print("ERROR :", err)


