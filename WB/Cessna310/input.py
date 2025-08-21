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
        self.label_font = tk.CTkFont(family="ebrima", size=16)
        self.title_font = tk.CTkFont(family="ebrima", size=18)
        self.title_u_font = tk.CTkFont(family="ebrima", size=18, underline=True)

        self.one_photo = CTkImage(dark_image=Image.open("./WB/Photos/one.png"), size=(48, 48))

        # specific options to the 152's here
        self.ac_options = ["C-GPIM (3 Seats)", "C-GPIM (4 Seats)", "C-GPIM (5 Seats)", "C-GPIM (6 Seats)"]

        # below are all the items on the screen.
        self.one_icon = tk.CTkButton(self, image=self.one_photo, height=48, width=48, state="disabled",
                                     fg_color="#353535", text="")
        self.one_icon.grid(column=0, columnspan=2, row=0, padx=(12, 460), pady=(20, 5))

        self.title_label = tk.CTkLabel(self, text="Enter the weights/fuel in pounds for both.",
                                       font=self.title_u_font, width=494)
        self.title_label.grid(column=0, columnspan=2, row=1, padx=10, pady=20)

        self.ac_label = tk.CTkLabel(self, text="Select an Airplane:", font=self.label_font,
                                    width=354, anchor="w")
        self.ac_label.grid(column=0, row=2, padx=20, pady=12)
        self.ac_box = tk.CTkOptionMenu(self, width=100, height=35, values=self.ac_options,
                                       font=self.label_font, fg_color="#3EA216", button_color="#2B750E")
        self.ac_box.grid(column=0, columnspan=2, row=2, padx=(350, 20), pady=12)

        self.front_label = tk.CTkLabel(self, text="Seats 1+2", font=self.label_font,
                                       width=354, anchor="w")
        self.front_label.grid(column=0, row=3, padx=20, pady=12)
        self.front_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.front_entry.grid(column=1, row=3, padx=20, pady=12)

        self.mid_label = tk.CTkLabel(self, text="Seats 3+4", font=self.label_font,
                                     width=354, anchor="w")
        self.mid_label.grid(column=0, row=4, padx=20, pady=12)
        self.mid_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.mid_entry.grid(column=1, row=4, padx=20, pady=12)

        self.back_label = tk.CTkLabel(self, text="Seats 5+6", font=self.label_font,
                                      width=354, anchor="w")
        self.back_label.grid(column=0, row=5, padx=20, pady=12)
        self.back_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.back_entry.grid(column=1, row=5, padx=20, pady=12)

        self.bag_nose_label = tk.CTkLabel(self, text="Nose Baggage (Max 347)",
                                          width=354, font=self.label_font, anchor="w")
        self.bag_nose_label.grid(column=0, row=6, padx=20, pady=12)
        self.bag_nose_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.bag_nose_entry.grid(column=1, row=6, padx=20, pady=12)

        self.bag_wing_label = tk.CTkLabel(self, text="Wing Baggage (Max 240)",
                                          width=354, font=self.label_font, anchor="w")
        self.bag_wing_label.grid(column=0, row=7, padx=20, pady=12)
        self.bag_wing_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.bag_wing_entry.grid(column=1, row=7, padx=20, pady=12)

        self.bag_aft_label = tk.CTkLabel(self, text="Aft Bags Station 126 (Max 160)",
                                         width=354, font=self.label_font, anchor="w")
        self.bag_aft_label.grid(column=0, row=8, padx=20, pady=12)
        self.bag_aft_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.bag_aft_entry.grid(column=1, row=8, padx=20, pady=12)

        self.fuel_mains_start_label = tk.CTkLabel(self, text="Fuel in mains at startup (Max 600)",
                                                  width=354, font=self.label_font, anchor="w")
        self.fuel_mains_start_label.grid(column=0, row=9, padx=20, pady=12)
        self.fuel_mains_start_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.fuel_mains_start_entry.grid(column=1, row=9, padx=20, pady=12)

        self.fuel_aux_start_label = tk.CTkLabel(self, text="Fuel in aux's at startup (Max 378)",
                                                width=354, font=self.label_font, anchor="w")
        self.fuel_aux_start_label.grid(column=0, row=10, padx=20, pady=12)
        self.fuel_aux_start_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.fuel_aux_start_entry.grid(column=1, row=10, padx=20, pady=12)

        self.fuel_taxi_label = tk.CTkLabel(self, text="Fuel burn during taxi (Taken from the mains)",
                                           width=354, font=self.label_font, anchor="w")
        self.fuel_taxi_label.grid(column=0, row=11, padx=20, pady=12)
        self.fuel_taxi_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.fuel_taxi_entry.grid(column=1, row=11, padx=20, pady=12)

        self.fuel_mains_flight_label = tk.CTkLabel(self, text="Fuel burned from mains in flight",
                                                   width=354, font=self.label_font, anchor="w")
        self.fuel_mains_flight_label.grid(column=0, row=12, padx=20, pady=12)
        self.fuel_mains_flight_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.fuel_mains_flight_entry.grid(column=1, row=12, padx=20, pady=12)

        self.fuel_aux_flight_label = tk.CTkLabel(self, text="Fuel burned from aux's in flight",
                                                 width=354, font=self.label_font, anchor="w")
        self.fuel_aux_flight_label.grid(column=0, row=13, padx=20, pady=12)
        self.fuel_aux_flight_entry = tk.CTkEntry(self, width=100, font=self.label_font)
        self.fuel_aux_flight_entry.grid(column=1, row=13, padx=20, pady=12)

        self.calculate_button = tk.CTkButton(self, width=400, height=60, text="Calculate", font=self.title_font,
                                             command=lambda: self.check_valid(), fg_color="#3EA216")
        self.calculate_button.grid(column=0, columnspan=2, row=14, padx=20, pady=20)

    # check_valid ensures the information entered are valid, and can be sent for processing. Catching things like typos
    # and invalid entries that aircraft cannot handle
    def check_valid(self):
        # self.data is a dict that can be sent away for processing wb with
        self.data = {}  # ignore
        self.data['pax1'] = self.front_entry.get()
        self.data['pax2'] = self.mid_entry.get()
        self.data['pax3'] = self.back_entry.get()
        self.data['bag1'] = self.bag_nose_entry.get()
        self.data['bag2'] = self.bag_wing_entry.get()
        self.data['bag3'] = self.bag_aft_entry.get()
        self.data['fuel_load_main'] = self.fuel_mains_start_entry.get()
        self.data['fuel_load_aux'] = self.fuel_aux_start_entry.get()
        self.data['fuel_taxi'] = self.fuel_taxi_entry.get()
        self.data['fuel_flight_main'] = self.fuel_mains_flight_entry.get()
        self.data['fuel_flight_aux'] = self.fuel_aux_flight_entry.get()
        # if nothing entered, turns it into 0. Also turns everything into absolute value. Student may be tempted to
        # enter fuel burn in negative.
        self.data = {i: ((abs(float(j))) if j != '' else 0.0) for i, j in self.data.items()}
        self.data["type"] = "Cessna 310"  # ignore these
        self.data['ident'] = self.ac_box.get()

        self.data['fuel_load'] = (self.data['fuel_load_main'] + self.data['fuel_load_aux'])
        self.data['fuel_flight'] = (self.data['fuel_flight_main'] + self.data['fuel_flight_aux'])

        # checking validity of entries by user for obvious error or un-airworthy ex. Baggage limits. The user should be
        # corrected on those errors, but program still needs to allow for out-of-cg or gw calculations to assist in
        # learning
        if self.data['pax1'] == 0:
            CTkMessagebox(title="Error",
                          message="Please enter a valid weight for the front seats.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")

            return
        if self.data['bag1'] > 347:
            CTkMessagebox(title="Error",
                          message="Baggage compartment is overweight.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if self.data['bag2'] > 240:
            CTkMessagebox(title="Error",
                          message="Baggage compartment is overweight.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if self.data['bag3'] > 160:
            CTkMessagebox(title="Error",
                          message="Baggage compartment is overweight.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if self.data['fuel_load_main'] > 600:
            CTkMessagebox(title="Error",
                          message="Please enter a fuel capacity under the maximum limit for this aircraft.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if self.data['fuel_load_aux'] > 378:
            CTkMessagebox(title="Error",
                          message="Please enter a fuel capacity under the maximum limit for this aircraft.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if self.data['fuel_load_main'] - self.data['fuel_taxi'] - self.data['fuel_flight_main'] < 0:
            CTkMessagebox(title="Error",
                          message="You burned more fuel than you have from the main tanks.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if self.data['fuel_load_aux'] - self.data['fuel_flight_aux'] < 0:
            CTkMessagebox(title="Error",
                          message="You burned more fuel than you have from the aux tanks.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if (self.data['fuel_load'] - (self.data['fuel_taxi'] + self.data['fuel_flight'])) < 90:
            CTkMessagebox(title="Error",
                          message="Warning: Less than 90 pounds of fuel will remian after landing. Please recalculate.",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")
            return
        if (self.data['fuel_load'] - (self.data['fuel_taxi'] + self.data['fuel_flight'])) < 180:
            a = self.data['fuel_load'] - (self.data['fuel_taxi'] + self.data['fuel_flight'])
            CTkMessagebox(title="Error",
                          message=f"Caution: {a} pounds of fuel will remain after landing. (Under 1 hour of "
                                  f"flight time. Proceed at your own risk.)",
                          font=("ebrima", 14), fg_color="#353535",
                          button_color="#3EA216")

        # if function has not early returned, proceeds with calculation
        self.calculate(self.data)
