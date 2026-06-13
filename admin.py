from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
import sys
import psutil

# the cookie path below is in the python file network. This script will launch a browser using selenium, and use the
# same cookie file that the actual program will use. That way, if you log in to an account with this script, the login
# info will save for future uses.

url_school = os.environ.get("URL_SCHOOL")

def find_browser_instances(profile_path, browser_name="msedge.exe"):  # runs under msedge.exe
    if sys.platform == "linux":
        browser_name = "firefox-bin"
    for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]): # finds all processes running in os
        try:
            if browser_name.lower() in proc.info["name"].lower():  # true if process matches name with browser_name
                cmd_args = proc.info["cmdline"]  # holds a list of args, including the user-data-dir arg.
                # below runs through all cmd_args, checks for profile_path match.
                if cmd_args and any(profile_path in arg for arg in cmd_args):
                    proc.kill()  # ends process.
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):  # null case
            pass

if sys.platform == "linux":
    options = FirefoxOptions()
    profile_path = f"/home/{os.getlogin()}/.cache/mozilla/firefox/folder.selenium_profile"
    options.add_argument("-profile")
    options.add_argument(profile_path)
    find_browser_instances(profile_path)
    driver = webdriver.Firefox(options=options)
if sys.platform == "win32":
    options = EdgeOptions()
    profile_path = f"user-data-dir:C:/Users/{os.getlogin()}/AppData/Local/Programs/Python/Python312/Lib/site-packages/selenium/profiles/wpp"
    options.add_argument(profile_path)
    options.add_experimental_option("detach", True)
    driver = webdriver.Edge(options=options)

driver.get(f"https://{url_school}.flightlogger.net/")
