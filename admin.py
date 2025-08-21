from selenium import webdriver
import os

# the cookie path below is in the python file network. This script will launch a browser using selenium, and use the
# same cookie file that the actual program will use. That way, if you log in to an account with this script, the login
# info will save for future uses.

url_school = os.environ.get("URL_SCHOOL")

cookie_path = rf"user-data-dir=C:\Users\{os.getlogin()}\AppData\Local\Programs\Python\Python312\Lib\site-packages\selenium\profile\wpp"

options = webdriver.EdgeOptions()

options.add_argument(cookie_path)

options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)

driver.get(f"https://{url_school}.flightlogger.net/")