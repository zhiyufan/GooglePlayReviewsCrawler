import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json

driver = webdriver.Chrome()

wait = WebDriverWait( driver, 10 )

app_ip = ['com.owncloud.android', 'com.facebook.orca', 'com.contextlogic.wish', 'com.whatsapp', 'org.telegram.messenger']

show_more_class_tag = "n9lfJ"
all_reviews_tag = "UD7Dzf"
full_reviews_tag = "OzU4dc"
users_tag = "X43Kjb"
dates_tag = "p2TkOb"
start_tag = "pf5lIe"
solid_start_tag = "vQhuPe"
scroll_to_bottom = "window.scrollTo(0, document.body.scrollHeight);"

click_show_more = "var a = document.getElementsByClassName(\""+show_more_class_tag+"\"); a[0].click();"
full_reviews_len = '0'
#click_full_reviews = "var a = document.getElementsByClassName(\""+full_reviews_tag+"\"); a["+full_reviews_len+"].click();"

app_num = 0
while app_num < len(app_ip):

    url = "https://play.google.com/store/apps/details?id="+ app_ip[app_num]+"&showAllReviews=true&hl=en"

    page_num = 0

    driver.get(url)

    driver.execute_script(scroll_to_bottom)

    time.sleep(10)

    driver.execute_script(scroll_to_bottom)

    #show all reviews
    while len(driver.find_elements_by_class_name(show_more_class_tag)) > 0:
        print("app name %s page %d:" % (app_ip[app_num], page_num))
        page_num += 1
        driver.execute_script(scroll_to_bottom)
        button = driver.execute_script(click_show_more)

        time.sleep(10)
        driver.execute_script(scroll_to_bottom)

    #click all full review buttons
    full_reviews_len = len(driver.find_elements_by_class_name(full_reviews_tag))
    if (full_reviews_len > 0):
        for i in range(0, full_reviews_len):
            click_full_reviews = "var a = document.getElementsByClassName(\"" + full_reviews_tag + "\"); a[" + str(
                i) + "].click();"
            driver.execute_script(click_full_reviews)

    count = 0

    reviews = driver.find_elements_by_class_name(all_reviews_tag)
    dates = driver.find_elements_by_class_name(dates_tag)
    users = driver.find_elements_by_class_name(users_tag)
    stars = driver.find_elements_by_class_name("pf5lIe");

    final_json = []
    print("start to build json")
    for review, date, user,star in zip(reviews,dates,users, stars):
        count += 1
        result = {"Content": review.text, "Star": len(star.find_elements_by_class_name("vQHuPe")), "Numbers": str(count), "Date": date.text, "Name": user.text}
        final_json.append(result)
    output = json.dumps(final_json)
    fp = open(app_ip[app_num]+".json", "w")
    fp.write(output)
    fp.close()
    app_num += 1

driver.quit()

