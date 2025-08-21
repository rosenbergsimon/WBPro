import customtkinter as tk
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkImage
from PIL import Image


# Input allows for the user to input the numbers, the program will check for typos/major errors from entry. Then will
# proceed to calculation upon success in another file/class.
class Input(tk.CTkFrame):
    def __init__(self, master, calculate, data):
        super().__init__(master)
        self.calculate = calculate
        self.configure(fg_color="#353535", width=533, height=900)
        self.grid_propagate(False)
        self.data = data
        self.label_font = tk.CTkFont(family="ebrima", size=14)
        self.title_font = tk.CTkFont(family="ebrima", size=18)
        self.title_u_font = tk.CTkFont(family="ebrima", size=18, underline=True)

        self.one_photo = CTkImage(dark_image=Image.open("WB/Photos/one.png"), size=(48, 48))

        # specific options to the RG's here
        self.ac_options = ["C-GIQJ"]
        # sets a StringVar to represent value of the aircraft selected, and to call functions
        self.ac_option = tk.StringVar()  # This code will change the fuel max number on the fuel label (24.5 or 37.5)
        self.ac_option.set("C-GIQJ")  # when the box is clicked to new plane selection
        self.ac_option.trace("w", self.ac_change)

        # below are all the items on the screen.
        self.one_icon = tk.CTkButton(self, image=self.one_photo, height=48, width=48, state="disabled",
                                     fg_color="#353535", text="")
        self.one_icon.grid(column=0, columnspan=2, row=0, padx=(12, 460), pady=(20, 5))

        self.title_label = tk.CTkLabel(self, text="Enter the aircraft and loading/fuel information below:",
                                       font=self.title_u_font, width=494)
        self.title_label.grid(column=0, columnspan=2, row=1, padx=20, pady=20)

        self.ac_label = tk.CTkLabel(self, text="Select an Airplane from the menu:", font=self.label_font,
                                    width=354, anchor="w")
        self.ac_label.grid(column=0, row=2, padx=20, pady=20)
        self.ac_box = tk.CTkOptionMenu(self, variable=self.ac_option, width=50, height=35, values=self.ac_options,
                                       font=self.label_font, fg_color="#3EA216", button_color="#2B750E")
        self.ac_box.grid(column=1, row=2, padx=20, pady=20)

        self.front_label = tk.CTkLabel(self, text="Enter the weight (lbs) in the front seats", font=self.label_font,
                                       width=354, anchor="w")
        self.front_label.grid(column=0, row=3, padx=20, pady=20)
        self.front_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.front_entry.grid(column=1, row=3, padx=20, pady=20)

        self.back_label = tk.CTkLabel(self, text="Enter the weight (lbs) in the back seats", font=self.label_font,
                                      width=354, anchor="w")
        self.back_label.grid(column=0, row=4, padx=20, pady=20)
        self.back_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.back_entry.grid(column=1, row=4, padx=20, pady=20)

        self.bag1_label = tk.CTkLabel(self, text="Enter the weight (lbs) in Baggage Area #1 (max 200)",
                                      width=354, font=self.label_font, anchor="w")
        self.bag1_label.grid(column=0, row=5, padx=20, pady=20)
        self.bag1_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.bag1_entry.grid(column=1, row=5, padx=20, pady=20)

        self.bag2_label = tk.CTkLabel(self, text="Enter the weight (lbs) in Baggage Area #2 (max 50)",
                                      width=354, font=self.label_font, anchor="w")
        self.bag2_label.grid(column=0, row=6, padx=20, pady=20)
        self.bag2_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.bag2_entry.grid(column=1, row=6, padx=20, pady=20)

        self.bag_note = tk.CTkLabel(self, text="Note: Baggage area 1 and 2 combined limit = 200lbs.",
                                    width=494, font=self.label_font, anchor="w")
        self.bag_note.grid(column=0, row=7, columnspan=2, padx=20, pady=20)

        self.fuel_start_label = tk.CTkLabel(self, text="Enter the US gallons of fuel on board (max 62)",
                                            width=354, font=self.label_font, anchor="w")
        self.fuel_start_label.grid(column=0, row=8, padx=20, pady=20)
        self.fuel_start_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.fuel_start_entry.grid(column=1, row=8, padx=20, pady=20)

        self.fuel_taxi_label = tk.CTkLabel(self, text="Enter the planned fuel burned (in US gallons) for taxi",
                                           width=354, font=self.label_font, anchor="w")
        self.fuel_taxi_label.grid(column=0, row=9, padx=20, pady=20)
        self.fuel_taxi_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.fuel_taxi_entry.grid(column=1, row=9, padx=20, pady=20)

        self.fuel_flight_label = tk.CTkLabel(self, text="Enter the planned fuel burned (in US gallons) for the flight",
                                             width=354, font=self.label_font, anchor="w")
        self.fuel_flight_label.grid(column=0, row=10, padx=20, pady=20)
        self.fuel_flight_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.fuel_flight_entry.grid(column=1, row=10, padx=20, pady=20)

        self.calculate_button = tk.CTkButton(self, width=400, height=60, text="Calculate", font=self.title_font,
                                             command=lambda: self.check_valid(), fg_color="#3EA216")
        self.calculate_button.grid(column=0, columnspan=2, row=11, padx=20, pady=(30, 20))

    # part of the StringVar system, changes the fuel capacity label. Not needed now.
    def ac_change(self, *args):
        pass

    # check_valid ensures the information entered are valid, and can be sent for processing. Catching things like typos
    # and invalid entries that aircraft cannot handle
    def check_valid(self):
        # self.data is a dict that can be sent away for processing wb with
        self.data = {}  # literal on one line is harder to read
        self.data['pax1'] = self.front_entry.get()
        self.data['pax2'] = self.back_entry.get()
        self.data['bag1'] = self.bag1_entry.get()
        self.data['bag2'] = self.bag2_entry.get()
        self.data['fuel_load'] = self.fuel_start_entry.get()
        self.data['fuel_taxi'] = self.fuel_taxi_entry.get()
        self.data['fuel_flight'] = self.fuel_flight_entry.get()
        # if nothing entered, turns it into 0. Also turns everything into absolute value. Student may be tempted to
        # enter fuel burn in negative.
        self.data = {i: ((abs(float(j))) if j != '' else 0.0) for i, j in self.data.items()}
        self.data["type"] = "Cessna 72R"
        self.data['ident'] = self.ac_box.get()  # ignore

        # checking validity of entries by user for obvious error or un-airworthy ex. Baggage limits. The user should be
        # corrected on those errors, but program still needs to allow for out-of-cg or gw calculations to assist in
        # learning
        if self.data['pax1'] == 0:
            CTkMessagebox(title="Error",
                          message="Please enter a valid weight for the front seats.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")

            return
        if (self.data['bag1'] + self.data['bag2']) > 200:
            CTkMessagebox(title="Error",
                          message="Baggage compartment is overweight.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if (self.data['bag2']) > 50:
            CTkMessagebox(title="Error",
                          message="Baggage compartment is overweight.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if (self.data['fuel_load']) > 62:
            CTkMessagebox(title="Error",
                          message="Please enter a fuel capacity under the maximum limit for this aircraft.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if (self.data['fuel_load'] - (self.data['fuel_taxi'] + self.data['fuel_flight'])) < 6:
            CTkMessagebox(title="Error",
                          message="Warning: Less than 6 gallons of fuel will remian after landing. Please recalculate.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if (self.data['fuel_load'] - (self.data['fuel_taxi'] + self.data['fuel_flight'])) < 12:
            a = self.data['fuel_load'] - (self.data['fuel_taxi'] + self.data['fuel_flight'])
            CTkMessagebox(title="Error",
                          message=f"Caution: {a} gallons of fuel will remain after landing. (Under 1 hour of "
                                  f"flight time. Proceed at your own risk.)",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")

        # if function has not early returned, proceeds with calculation
        self.calculate(self.data)
