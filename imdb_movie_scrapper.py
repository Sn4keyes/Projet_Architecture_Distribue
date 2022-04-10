#!/usr/bin/python

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

NB_MOVIE = 25 # Nombre de film a boucler
URL = 'https://www.imdb.com/chart/top/'
PATH_DRIVER = "C:\Program Files\Chromedriver\chromedriver.exe" # A modifier ! Mettre votre PATH

def get_nb_com(driver):
    comment_tot = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[2]/div[1]/div/span')
    tot_text = comment_tot.text
    nb_com = int("".join(filter(str.isdigit, tot_text)))
    print("NB COMM  == ", nb_com)
    nb_com = nb_com - 50
    return nb_com

def click_review(driver):
    review_button = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[1]/a')
    review_button.click()
    time.sleep(2)
    return driver

def open_movie(driver, y):
    movie_selected = driver.find_element(By.XPATH, '//*[@class="lister-list"]/tr[{}]/td[2]/a'.format(y))
    movie_selected.click()
    time.sleep(2)
    return driver

def manage_scrapper(driver, dict_comment):
    for y in range(1, NB_MOVIE):
        driver = open_movie(driver, y)
        driver = click_review(driver)
        nb_com = get_nb_com(driver)
        df = driver.find_element(By.CLASS_NAME, 'lister')
        for i in range(0, nb_com): 
            if ((i % 25) == 0):
                load_more = driver.find_element(By.XPATH, '//*[@class="ipl-load-more__button"]')
                load_more.click()
                time.sleep(2)
            else:
                try:
                    star = df.find_element(By.XPATH, "//div[{}]/div[1]/div[1]/div[1]/span[contains(@class, 'rating-other-user-rating')]/span[1]".format(i)).text
                    comment = df.find_element(By.XPATH, "//div[{}]/div[1]/div[1]/div[contains(@class, 'content')]/div[contains(@class, 'text show-more__control')]".format(i)).text
                    nb_star = int(star)
                    if nb_star == 10:
                        dict_comment['Rate'].append(nb_star)
                        dict_comment['Comment'].append(comment)
                    elif nb_star <= 4:
                        dict_comment['Rate'].append(nb_star)
                        dict_comment['Comment'].append(comment)
                except:
                    print("! PAS DE NOTE !")
        driver.get(URL)
    return driver, dict_comment

def setup_scrapper():
    service = Service(executable_path=PATH_DRIVER)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(URL)
    return driver

def main():
    dict_comment = {'Rate': [], 'Comment': []}
    driver = setup_scrapper()
    driver, dict_comment = manage_scrapper(driver, dict_comment)
    df_movies = pd.DataFrame(dict_comment, columns=['Rate', 'Comment'])
    df_movies.to_json(r'work\DataSet\Movie_dataframe.json')
    print(df_movies)
    print("####################")
    return driver

if __name__ == "__main__":
    driver = main()