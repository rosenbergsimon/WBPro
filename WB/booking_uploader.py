import customtkinter as tk
from CTkMessagebox import CTkMessagebox
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import psutil
import threading
import time
import os
import shutil


# this contains the methods needed to upload a booking to a flight logger booking (rental/ops flights)
class BookingWB:
    def __init__(self, info, upload_button, student_buttons, status_bar, root, close, update_image):
        self.info = info
        self.upload_button = upload_button
        self.student_buttons = student_buttons
        self.status_bar = status_bar
        self.root = root
        self.close = close
        self.update_image = update_image
        self.cookie_path = rf"user-data-dir=C:\Users\{os.getlogin()}\AppData\Local\Programs\Python\Python312\Lib\site-packages\selenium\profile\wpp"
        self.school_code = os.environ.get("URL_SCHOOL")
        self.url = f"https://{self.school_code}.flightlogger.net/bookings/overview"
        self.file_window = FileName(self.prepare, self.info)

    # prepares the program for the upload, and structures the threads to do it
    def prepare(self, info):
        self.file_window.destroy()
        self.info = info

        self.start_upload()

        self.find_browser_instances(self.cookie_path)

        thread = threading.Thread(target=lambda: self.execute_selenium(), daemon=True)
        thread.start()

    # does the browser automation script for the upload
    def execute_selenium(self):
        options = webdriver.EdgeOptions()

        options.add_argument(self.cookie_path)
        options.add_experimental_option("detach", True)
        options.add_argument('headless=new')  # makes it occur in the background

        driver = webdriver.Edge(options=options)

        driver.get(self.url)

        try:
            WebDriverWait(driver, 15).until(ec.presence_of_element_located((By.ID, f"bookingBlock{self.info['id']}")))
        except TimeoutException:
            # if the cookie is out of date, and FlightLogger logs itself out, the student cannot log back in themselves
            # so this element (the login box) will show up, and message box is issued.
            login_element = driver.find_elements(By.CSS_SELECTOR, ".email.required.control-label")
            # will proceed if logged out.
            if len(login_element) >= 1:
                CTkMessagebox(title="Error",
                              message="FlightLogger has logged out. Please contact dispatch. \n"
                                      "Use paper weight and balance for now.",
                              font=("ebrima", 14), fg_color="#353535", button_color="#3EA216")
                driver.quit()
            else:
                driver.quit()
                self.timeout_error()
                self.failed_reset_icons()
            return

        time.sleep(0.5)
        lock_btn = driver.find_elements(By.CSS_SELECTOR, "[title='Toggle create mode on']")
        if len(lock_btn) >= 1:
            lock_click = driver.find_element(By.ID, "toggleCreate")
            lock_click.click()
            time.sleep(0.25)

        brick = driver.find_element(By.CSS_SELECTOR, f"#bookingBlock{self.info['id']}")
        brick.click()

        try:
            WebDriverWait(driver, 15).until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        except TimeoutException:
            driver.quit()
            self.timeout_error()
            self.failed_reset_icons()
            return

        file_drag = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_drag.send_keys(rf"{os.getcwd()}\WB\Photos\temp\{self.info['file_name']}.jpeg")

        # makes sure the button has had time to actually disable, before running the next detector which checks if it
        # has become enabled
        time.sleep(2)

        button_wait = WebDriverWait(driver, 20)

        add_button = button_wait.until(lambda d: d.find_element(By.CSS_SELECTOR, ".StandardButton__StyledButton-jnuff8-"
                                                                                 "0.loMqZX.btn.btn-submit.Styles__Style"
                                                                                 "dActionButton-m00sx1-0.dXqePM"))
        button_wait.until(lambda d: not add_button.get_attribute("disabled"))

        add_button.click()

        time.sleep(2)

        no_instructor_avail = driver.find_elements(By.CSS_SELECTOR, ".StandardButton__StyledButton-jnuff8-0.loMqZ"
                                                                    "X.btn.btn-default.Styles__StyledActionButton-m00sx"
                                                                    "1-0.dXqePM")
        if len(no_instructor_avail) >= 1:
            no_instructor_avail[1].click()
            time.sleep(2)
            driver.quit()
            time.sleep(0.2)
            # below is to make sure the specially named file gets deleted since it is not needed anymore
            self.root.update()
            self.finish_upload()
        else:
            time.sleep(2)
            driver.quit()
            time.sleep(0.2)
            self.root.update()
            self.finish_upload()

    # grays out some buttons and changes some colours. Also clears the temp folder and adds the combined.jpeg to it
    def start_upload(self):
        self.update_image([self.info['student']])

        prohibited_chars = ['/', '\\', '?', '<', '>', ':', '"', '|', '*']
        for i in prohibited_chars:
            if i in self.info['file_name']:
                self.info['file_name'] = self.info['file_name'].replace(i, "")

        if os.path.isdir("WB/Photos/temp"):
            pass
        else:
            os.mkdir("WB/Photos/temp")

        for i in os.listdir("WB/Photos/temp"):
            file_path = os.path.join("WB/Photos/temp", i)
            if os.path.isfile(file_path):
                os.remove(file_path)
        new_file = os.path.join("WB/Photos/temp", f"{self.info['file_name']}.jpeg")
        shutil.copy2("WB/Photos/combined.jpeg", new_file)

        self.status_bar.configure(text="Upload in Progress.\n This may take over 30 seconds.", fg_color="#A08000")
        self.upload_button.configure(state="disabled", fg_color="#606060")
        self.root.update_idletasks()  # tkinter needs to finish all tasks before the webdriver will hog the thread.

    # returns the buttons
    def finish_upload(self):
        self.upload_button.configure(state="normal", fg_color="#3EA216")
        self.status_bar.configure(text="Upload Completed Successfully!", fg_color="#006300")
        msg = CTkMessagebox(title="Success!", message="Your Weight-and-Balance has been uploaded to FlightLogger.\n\n"
                                                      "Would you like to upload another W/B? (eg. multiple xc legs)",
                            icon="check", option_1="Upload Another", option_2="Close Program", button_width=150,
                            font=("ebrima", 14), fg_color="#353535", button_color="#3EA216", width=420)
        rsp = msg.get()
        if rsp == "Close Program":
            self.close()

    # if upload fails, will run
    def failed_reset_icons(self):
        self.upload_button.configure(state="normal", fg_color="#3EA216")
        self.status_bar.configure(text="Select your Name", fg_color="#606060")

    # also failed upload, messagebox pop up
    def timeout_error(self):
        CTkMessagebox(title="Error",
                      message="FlightLogger connection has timed out. Please retry, \n"
                              "check the internet connection, or contact dispatch.",
                      font=("ebrima", 14), fg_color="#353535", button_color="#3EA216")

    # the below function is required to fix a bug that is reoccurring in testbed. When using headless selenium, and the
    # program is interrupted, the msedge.exe instance will not close out in the os and leak mem. This function ensures
    # that no other
    # instances of msedge.exe, using the same cookie path, or user-data-dir, are open. If so, it will close all the
    # processes with it. Which with chromium, is many, hence the loop. This will not close unrelated, public browser
    # tabs that are open.

    def find_browser_instances(self, cookie_path, browser_name="msedge.exe"):  # runs under msedge.exe
        for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):  # finds all processes running in os
            try:
                if browser_name.lower() in proc.info["name"].lower():  # true if process matches name with browser_name
                    cmd_args = proc.info["cmdline"]  # holds a list of args, including the user-data-dir arg.
                    # below runs through all cmd_args, checks for cookie_path match.
                    if cmd_args and any(cookie_path in arg for arg in cmd_args):
                        proc.kill()  # ends process.
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):  # null case
                pass


# gathers a file name, to rename the actual file on the program's computer in order to make it recognizable on FL
class FileName(tk.CTkToplevel):
    def __init__(self, launch, info):
        super().__init__()
        self.launch = launch
        self.info = info
        self.geometry("800x260")
        self.title("File Name")
        self.attributes('-topmost', True)
        self.update()

        self.title_label = tk.CTkLabel(self, text="Enter a file name to be used in flightlogger: "
                                                  "(eg. W/B, CYXE-CYPA, Leg 1, etc)",
                                       font=tk.CTkFont(family="ebrima", size=18), width=700)
        self.title_label.grid(column=0, row=0, padx=50, pady=20)

        self.name_entry = tk.CTkEntry(self, width=500, font=tk.CTkFont(family="ebrima", size=14))
        self.name_entry.grid(column=0, row=1, padx=150, pady=20)

        self.btn = tk.CTkButton(self, width=300, height=60, text="Proceed",
                                font=tk.CTkFont(family="ebrima", size=18),
                                command=lambda: self.proceed(), fg_color="#3EA216")
        self.btn.grid(column=0, row=2, padx=50, pady=20)

    def proceed(self):
        if len(self.name_entry.get()) == 0:
            CTkMessagebox(title="Error",
                          message="Please enter a file name.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if len(self.name_entry.get()) > 20:
            CTkMessagebox(title="Error",
                          message="Please enter a file name under 20 characters.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        self.info['file_name'] = self.name_entry.get()
        self.launch(self.info)
        