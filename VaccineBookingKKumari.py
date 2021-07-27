import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import threading

SECONDS_TO_WAIT = 3
URL = 'https://bookmyvaccine.kumaricovidcare.in'
OUTPUT = 'result.csv'
HEADERS = ['vaccine', 'qty', 'time']


def notify(vaccine, qty):
    print('Hurry up {} is available in {} qty'.format(vaccine, qty))


def do_something(vaccine, qty):
    threading.Thread(target=notify, args=(vaccine, qty)).start()


def crawl():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(URL)

    time.sleep(SECONDS_TO_WAIT)  # this need because results captured using ajax with jwt tokens

    elements = browser.find_elements_by_xpath("//button[contains(@class,'availability-btn')]")

    out = []

    for e in elements:
        vaccine = e.find_element_by_xpath("preceding-sibling::p").text
        qty = 0 if e.text == 'Not Available' else int(e.text)
        if qty > 0:
            do_something(vaccine, qty)

        out.append({'vaccine': vaccine, 'qty': qty, 'time': int(time.time())})

    return out


def store_result(result):
    with open(OUTPUT, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        for r in result:
            writer.writerow(r)


if __name__ == '__main__':
    result = crawl()
    store_result(result)
