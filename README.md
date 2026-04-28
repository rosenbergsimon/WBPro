# WBPro

<!-- rewrite all of this to be just a personal project. Selenium limitations. Just go over what it does, not how someone else could run the program. put the prockill in the termination of the program to add safety -->

WBPro is an end-user-focused Python program I made for the fligth school I attend, designed to integrate the weight-and-balance control system with FlightLogger's web-based flight school scheduling and management service. It allows for electronic creation of completed weight-and-balance forms, and subsequent uploading to the FlightLogger website. The completed form is stored on a students' "lesson", or on a flight booking, in the case of a non-school flight. 

Run from the python3 main.py file. The program incorporates a User Interface built with the CustomTkinter module, weight-and-balance form creation built with MatPlotLib, an API call using FlightLogger's GraphQL API to retrieve upcoming flight information, and an automated web browser component with Selenium to do the uploading to the FlightLogger website. An API function does not exist for uploading documents to lessons or bookings on FlightLogger. Error handling is only sufficient for the use cases at my school. 

# Information

This program will only work on Windows 10+ systems with Edge installed. I may try to figure out Linux/firefox eventually.  

The admin.py script is used to login to FlightLogger, and then save the login information to the data that selenium uses.

# Environment Variables

Two environment variables are required. The names for these are below. 

FlightLogger GraphQL API Key (Obtained from my.flightlogger.net): 

    WBPRO_CODE

School's FlightLogger web URL code (the letters between https:// and .flightlogger.net in the URL of FlightLogger)

    URL_SCHOOL

# Further Development

I could make the program better by building a settings menu that allows for the adding of specific aircraft types and profiles, and adding specific ident's empty weights and arms. Instead of hard-coding the weight and balance calculations, and on-screen menus, a more constructive approach could be made to allow for anything to be created. (Similar to ForeFlight). 

I only made this for one certain school. The code quality isn't very good, but it works for it's intended purpose.