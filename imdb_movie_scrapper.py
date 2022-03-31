#!/usr/bin/python

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

NB_MOVIE = 250
URL = 'https://www.imdb.com/chart/top/'
PATH_DRIVER = "C:\Program Files\Chromedriver\chromedriver.exe" # A modifier ! Mettre votre PATH

def get_nb_com(driver):
    comment_tot = driver.find_element(By.XPATH, '//*[@id="main"]/section/div[2]/div[1]/div/span')
    tot_text = comment_tot.text
    nb_com = int("".join(filter(str.isdigit, tot_text)))
    return nb_com

def click_review(driver):
    review_button = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[1]/a')
    review_button.click()
    time.sleep(2)
    return driver

def get_movie_types(driver):
    movie_types = []
    types = driver.find_elements(By.CLASS_NAME, 'sc-16ede01-3')
    for e in types:
        movie_types.append(e.text)
    print("MOVIE TYPES == ", movie_types)
    return movie_types

def get_movie_name(driver):
    movie = driver.find_element(By.CLASS_NAME, 'sc-b73cd867-0')
    movie_name = movie.text
    return movie_name

def open_movie(driver, y):
    movie_selected = driver.find_element(By.XPATH, '//*[@class="lister-list"]/tr[{}]/td[2]/a'.format(y))
    movie_selected.click()
    time.sleep(2)
    return driver

def manage_scrapper(driver, dict_movie, df_movies):
    comment_pos = []
    comment_neg = []
    for y in range(1, NB_MOVIE):
        driver = open_movie(driver, y)
        movie_name = get_movie_name(driver)
        dict_movie['Name'] = movie_name
        movie_types = get_movie_types(driver)
        dict_movie['Types'] = movie_types
        driver = click_review(driver)
        nb_com = get_nb_com(driver)
        df = driver.find_element(By.CLASS_NAME, 'lister')
        for i in range(1, nb_com): 
            if ((i % 25) == 0):
                load_more = driver.find_element(By.XPATH, '//*[@class="ipl-load-more__button"]')
                load_more.click()
                time.sleep(2)
            try:
                star = df.find_element(By.XPATH, '//div[{}]/div[1]/div[1]/div[1]/span/span[1]'.format(i)).text
                comment = df.find_element(By.XPATH, "//div[{}]/div[1]/div[1]/div[contains(@class, 'content')]/div".format(i)).text
                nb_star = int(star)
                if nb_star >= 8:
                    comment_pos.append(comment)
                elif nb_star <= 3:
                    comment_neg.append(comment)
            except:
                time.sleep(2)
        dict_movie['Comment_pos'] = comment_pos
        dict_movie['Comment_neg'] = comment_neg
        df_movies = df_movies.append(dict_movie, ignore_index=True)
        driver.get(URL)
    return driver, df_movies

def setup_scrapper():
    service = Service(executable_path=PATH_DRIVER)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(URL)
    return driver

def main():
    dict_movie = {'Name': "", 'Types': [], 'Comment_pos': [], 'Comment_neg': []}
    df_movies = pd.DataFrame()
    driver = setup_scrapper()
    driver, df_movies = manage_scrapper(driver, dict_movie, df_movies)
    df_movies.to_json(r'Movie_dataframe.json')
    print("DATAFRAME MOVIES == \n", df_movies)
    print("####################")
    return driver

if __name__ == "__main__":
    driver = main()