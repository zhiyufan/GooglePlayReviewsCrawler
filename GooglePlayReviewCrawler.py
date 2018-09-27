import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

wait = WebDriverWait( driver, 10 )

app_ip = ['com.owncloud.android']

show_more_class_tag = "n9lfJ"
all_reviews_tag = "UD7Dzf"

scroll_to_bottom = "window.scrollTo(0, document.body.scrollHeight);"

click_show_more = "var a = document.getElementsByClassName(\""+show_more_class_tag+"\"); a[0].click();"

app_num = 0
while app_num < len(app_ip):
    url = "https://play.google.com/store/apps/details?id="+ app_ip[app_num]+"&showAllReviews=true&hl=en"

    f = open(app_ip[app_num]+'.txt', 'w')

    page_num = 0

    driver.get(url)

    driver.execute_script(scroll_to_bottom)

    time.sleep(10)



    while len(driver.find_elements_by_class_name(show_more_class_tag)) > 0:
        print("page %d:" % page_num)
        page_num += 1
        driver.execute_script(scroll_to_bottom)
        button = driver.execute_script(click_show_more)
        time.sleep(10)
        driver.execute_script(scroll_to_bottom)


    count = 1
    reviews = driver.find_elements_by_class_name(all_reviews_tag)
    print("App name: %s" % app_ip, file = f)
    for review in reviews:
        count += 1
        print("Review %d" % count, file = f)
        print(review.text, file = f)
        print(file = f)
    app_num += 1
driver.quit()

