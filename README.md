# WBPro

WBPro is an end-user-focused Python program designed for Windows 10+ that facilitates the integration of a flight school's weight-and-balance control system with FlightLogger's web-based flight school scheduling and management service. It allows for electronic creation of completed weight-and-balance forms, and subsequent uploading to the FlightLogger website. The completed form is stored on a students' "lesson", or on a flight booking, in the case of a non-student flight. 

This program can be easily run from running the main.py file. The program incorporates a User Interface built with the CustomTkinter module, weight-and-balance form creation built with MatPlotLib, an API call using FlightLogger's GraphQL API to retrieve upcoming flight information, and an automated web browser component with Selenium to do the uploading to the FlightLogger website. An API function does not exist for uploading documents to lessons or bookings on FlightLogger. The WBPro program utilizes many other libraries and incorporates a small amount of basic error-handling to increase suitability for end-user use. 

# Getting Started

This program will only work on Windows 10+ systems. 

Please ensure all the necessary libraries/packages needed from the requirements.txt file are installed with the environment/Venv.

In order to properly run the program, it is likely you will need to have user permissions within FlightLogger that allow for the reading of information on the flight schedule. You will also need the ability to modify bookings on the schedule if using WBPro to upload WB's to a rental or operation flight. 

A minimum screen resolution of 1680x1050 (with 1x Windows zoom scaling applied) is currently required to function properly. 

Running admin.py will open a Selenium browser with the homepage of FlightLogger. This is required on initial use to login to FlightLogger, for the Selenium web browser to use for later. The login cookies for selenium are stored in C:\Users\ <username>\AppData\Local\Programs\Python\ <python version>\Lib\site-packages\selenium\profile\wpp.

If any issues are encountered with storing login information, deleting wpp may solve this.

# Selenium Implementation

Selenium is implemented to manually "click" on items on the screen the same way a user would in order to upload the weight-and-balance form. This is the only way I have found to accomplish this task. It leads to occasional errors in completing the upload process. With an ideal computer, it takes approximately 10-12 seconds for the program to upload the weight-and-balance form. 

# Environment Variables

Two environment variables are required. The names for these are below. 

On Windows, use the following PowerShell command to set environment variables. A system restart is required to use them afterwards. Use the quotation marks for the value. 

    setx VARIABLE_NAME "VALUE"

FlightLogger GraphQL API Key (Obtained from my.flightlogger.net): 

    WBPRO_CODE

School's FlightLogger web URL code (the letters between https:// and .flightlogger.net in the URL of FlightLogger)

    URL_SCHOOL

# Further Development

I could make the program better by building a settings menu that allows for the adding of specific aircraft types and profiles, and adding specific ident's empty weights and arms. Instead of hard-coding the weight and balance calculations, and on-screen menus, a more constructive approach could be made to allow for anything to be created. (Similar to ForeFlight). 

If any actual flight schools other than my own are interested in using this, please send an email to the address on my github page, and I can look at making changes. I realized halfway through building this that the above would be a much better way to make the program. 
