import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from AppList import app_ip
drivers = []
driver = webdriver.Chrome()

show_more_class_tag = "RveJvd"
all_reviews_tag = "UD7Dzf"
full_reviews_tag = "OzU4dc"
users_tag = "kx8XBd"
users_name_tag = "X43Kjb"
dates_tag = "p2TkOb"
stars_tag = "nt2Cld"
solid_star_tag = "vQhuPe"
scroll_to_bottom = "window.scrollTo(0, document.body.scrollHeight);"

click_show_more = "var a = document.getElementsByClassName(\""+show_more_class_tag+"\"); a[0].click();"
full_reviews_len = '0'

app_num = 0
def search_show_more():
    count = 0
    while(len(driver.find_elements_by_class_name(show_more_class_tag)) == 0 and count < 10):
        driver.execute_script(scroll_to_bottom)
        time.sleep(3)
        count += 1
    return len(driver.find_elements_by_class_name(show_more_class_tag))

def is_crash_exist(review):
    crash_words = ["crash"]#, "freeze"]
    for word in crash_words:
        if word in review.lower():
            return True
    return False


while app_num < len(app_ip):
    url = "https://play.google.com/store/apps/details?id="+ app_ip[app_num]+"&showAllReviews=true&hl=en"
    page_num = 0
    driver.get(url)
    show_more_exist = 1

    #show all reviews


    while show_more_exist:
        show_more_exist = search_show_more()
        if show_more_exist:
            print("app name %s page %d:" % (app_ip[app_num], page_num))
            page_num += 1
            driver.execute_script(click_show_more)

    #click all full review buttons
    full_reviews_len = len(driver.find_elements_by_class_name(full_reviews_tag))
    if (full_reviews_len > 0):
        for i in range(0, full_reviews_len):
            click_full_reviews = "var a = document.getElementsByClassName(\"" + full_reviews_tag + "\"); a[" + str(
                i) + "].click();"
            driver.execute_script(click_full_reviews)
    print("start to match result")

    count = 0

    reviews = driver.find_elements_by_class_name(all_reviews_tag)
    users = driver.find_elements_by_class_name(users_tag)
    dates = []
    user_name = []
    stars = driver.find_elements_by_class_name(stars_tag)
    for user in users:
        dates.append(user.find_elements_by_class_name(dates_tag)[0])
        user_name.append(user.find_elements_by_class_name(users_name_tag)[0])
        #stars.append(user.find_elements_by_class_name(star_tag)[0])

    final_json = []
    print("start to build json for "+app_ip[app_num])
    for review, date, name in zip(reviews,dates,user_name):
        if is_crash_exist(review.text):
            count += 1
            result = {"Content": review.text, "Numbers": str(count), "Date": date.text}
            print(date.text)
            print(review.text)
            final_json.append(result)
    if len(final_json) > 0:
        output = json.dumps(final_json)
        fp = open("json_file/"+app_ip[app_num]+".json", "w")
        fp.write(output)
        fp.close()
    app_num += 1

driver.quit()

