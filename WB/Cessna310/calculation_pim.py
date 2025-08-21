from matplotlib import pyplot as plt
from PIL import Image
import datetime


# Calculation is a container of methods, upon instantiation it does all the math for the weight and balance.
# check_wb is where the information is checked for airworthiness, and a dictionary created for other classes to
# use later on. Fuel is converted to pounds in the math, and re-changed to gallons only for user viewing later.
# images also created in this class
class CalculationPim:
    def __init__(self, data):
        self.data = data
        if self.data['ident'] == "C-GPIM (3 Seats)":
            self.empty_weight = 3834.13
            self.empty_arm = 34.22
        elif self.data['ident'] == "C-GPIM (4 Seats)":
            self.empty_weight = 3853.13
            self.empty_arm = 34.41
        elif self.data['ident'] == "C-GPIM (5 Seats)":
            self.empty_weight = 3868.33
            self.empty_arm = 34.71
        elif self.data['ident'] == "C-GPIM (6 Seats)":
            self.empty_weight = 3883.53
            self.empty_arm = 34.99

        self.data['ident'] = self.data['ident'][0:6]

        self.ident = self.data['ident']
        self.fuel_mains_arm = 35
        self.fuel_aux_arm = 47
        self.fuel_load_main = round(self.data['fuel_load_main'], 2)   # fuel already in pounds
        self.fuel_load_aux = round(self.data['fuel_load_aux'], 2)
        self.fuel_taxi = round(self.data['fuel_taxi'] * -1, 2)  # negative to represent fuel being burned from tanks
        self.fuel_flight_main = round(self.data['fuel_flight_main'] * -1, 2)
        self.fuel_flight_aux = round(self.data['fuel_flight_aux'] * -1, 2)
        self.pax1 = self.data['pax1']
        self.pax2 = self.data['pax2']
        self.pax3 = self.data['pax3']
        self.bag1 = self.data['bag1']
        self.bag2 = self.data['bag2']
        self.bag3 = self.data['bag3']

        self.pax1_moment = round(self.pax1 * 34.2, 2)
        self.pax2_moment = round(self.pax2 * 68, 2)
        self.pax3_moment = round(self.pax3 * 102, 2)
        self.bag1_moment = round(self.bag1 * -31, 2)
        self.bag2_moment = round(self.bag2 * 63, 2)
        self.bag3_moment = round(self.bag3 * 126, 2)
        self.empty_moment = round(self.empty_weight * self.empty_arm, 2)

        self.zero_fuel_weight = round(self.empty_weight + self.pax1 + self.pax2 + self.pax3 + self.bag1 + self.bag2
                                      + self.bag3, 2)
        self.zero_fuel_moment = round(self.empty_moment + self.pax1_moment + self.pax2_moment + self.pax3_moment +
                                      self.bag1_moment + self.bag2_moment + self.bag3_moment, 2)
        self.zero_fuel_arm = round(self.zero_fuel_moment / self.zero_fuel_weight, 2)

        self.fuel_load_main_moment = round(self.fuel_load_main * self.fuel_mains_arm, 2)
        self.fuel_load_aux_moment = round(self.fuel_load_aux * self.fuel_aux_arm, 2)
        self.ramp_weight = round(self.zero_fuel_weight + self.fuel_load_main + self.fuel_load_aux, 2)
        self.ramp_moment = round(self.zero_fuel_moment + self.fuel_load_main_moment + self.fuel_load_aux_moment, 2)
        self.ramp_arm = round(self.ramp_moment / self.ramp_weight, 2)

        self.fuel_taxi_moment = round(self.fuel_taxi * self.fuel_mains_arm, 2)
        self.takeoff_weight = round(self.ramp_weight + self.fuel_taxi, 2)
        self.takeoff_moment = round(self.ramp_moment + self.fuel_taxi_moment, 2)
        self.takeoff_arm = round(self.takeoff_moment / self.takeoff_weight, 2)

        self.fuel_flight_main_moment = round(self.fuel_flight_main * self.fuel_mains_arm, 2)
        self.fuel_flight_aux_moment = round(self.fuel_flight_aux * self.fuel_aux_arm, 2)
        self.landing_weight = round(self.takeoff_weight + self.fuel_flight_main + self.fuel_flight_aux, 2)
        self.landing_moment = round(self.takeoff_moment + self.fuel_flight_main_moment + self.fuel_flight_aux_moment, 2)
        self.landing_arm = round(self.landing_moment / self.landing_weight, 2)

    def check_wb(self):
        # weight_good is a boolean to be changed, if overweight becomes False. arm_good: 0 is forward, 1 is in limits,
        # 2 is aft.
        ramp_weight_good = True
        to_weight_good = True
        ldg_weight_good = True
        zfw_weight_good = True
        zfw_arm_good = 1
        ldg_arm_good = 1
        to_arm_good = 1

        if self.ramp_weight > 5725:
            ramp_weight_good = False
        if self.takeoff_weight > 5680:
            to_weight_good = False
        if self.landing_weight > 5400:
            ldg_weight_good = False

        zfw_arm_good = self.check_in_limits(self.zero_fuel_weight, self.zero_fuel_arm)
        ldg_arm_good = self.check_in_limits(self.landing_weight, self.landing_arm)
        to_arm_good = self.check_in_limits(self.takeoff_weight, self.takeoff_arm)

        if zfw_arm_good == 1:
            if self.zero_fuel_arm >= 41.3:
                if self.zero_fuel_weight > 5300:
                    zfw_weight_good = False
            elif self.zero_fuel_arm < 41.3:
                if self.zero_fuel_weight > (59.375 * self.zero_fuel_arm + 2847.8125):
                    zfw_weight_good = False

        # fuel reserves in pounds, use gallons var name for consistency
        reserve_gallons = round((self.landing_weight - self.zero_fuel_weight), 0)
        reserve_hours = round(reserve_gallons / 180, 1)

        self.create_graph()
        self.create_sheet()
        self.combine_images()  # these all make the image, and combine them all for viewing/uploading

        # returns all the relevant information that the upload class will need to display.
        self.data["ramp_weight_good"] = ramp_weight_good
        self.data["to_weight_good"] = to_weight_good
        self.data["ldg_weight_good"] = ldg_weight_good
        self.data['zfw_weight_good'] = zfw_weight_good
        self.data["zfw_arm_good"] = zfw_arm_good
        self.data["ldg_arm_good"] = ldg_arm_good
        self.data["to_arm_good"] = to_arm_good
        self.data["reserve_gallons"] = reserve_gallons
        self.data["reserve_hours"] = reserve_hours
        self.data["takeoff_weight"] = self.takeoff_weight
        self.data["landing_weight"] = self.landing_weight
        self.data['weight_good'] = True

        return self.data

    # re-usable function to check if a given point on the wb graph are in limits using limitations for the Cessna 310.
    # carves the polygon of the loading limits chart into multiple sections of squares and triangle to calculate if
    # in limits or not. There are 9 sections to check.
    def check_in_limits(self, weight, arm):
        weight = round(weight, 2)
        arm = round(arm, 2)
        # section one
        if weight <= 5680 and 39.3 <= arm <= 42.9:
            return 1
        # section two
        if weight <= 4500 and 32 <= arm <= 39.3:
            return 1
        # section three
        if 4500 <= weight <= 5500 and 32 <= arm <= 38.7:
            if weight <= (149.25373 * arm - 276.11936):
                return 1
        # section four
        if 4500 <= weight <= 5500 and 38.7 <= arm <= 39.3:
            return 1
        # section five
        if 5500 <= weight <= 5680 and 38.7 <= arm <= 39.3:
            if weight <= (300 * arm - 6110):
                return 1
        # section six
        if weight <= 5100 and 42.9 <= arm <= 43.6:
            return 1
        # section seven
        if 5100 <= weight <= 5500 and 43.1 <= arm <= 43.6:
            if weight <= (-800 * arm + 39980):
                return 1
        # section eight
        if 5100 <= weight <= 5500 and 42.9 <= arm <= 43.1:
            return 1
        # section nine
        if 5500 <= weight <= 5680 and 42.9 <= arm <= 43.1:
            if weight <= (-900 * arm + 44290):
                return 1
        # out of limits scenarios: if out of limits it had not returned in the above functions
        if arm < 39.3:
            return 0
        if arm > 42.9:
            return 2

    def create_graph(self, mod_title=None):
        # if mod_title is passed in an arg, it will allow the title to be changed to display the name of instructor
        # and student flying this. This func creates the wb graph, similar to one student is used to using
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d")  # used for the title datestamp

        x_range = [30, 45]
        y_range = [3900, 5800]

        fig, ax = plt.subplots()
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)  # drawing the visible area of the graph

        left_x = [32, 32]
        left_y = [3900, 4500]
        l_d_1_x = [32, 38.7]
        l_d_1_y = [4500, 5500]
        l_d_2_x = [38.7, 39.3]
        l_d_2_y = [5500, 5680]
        top_x = [39.3, 42.9]
        top_y = [5680, 5680]
        right_x = [43.6, 43.6]
        right_y = [3900, 5100]
        r_d_1_x = [43.1, 43.6]
        r_d_1_y = [5500, 5100]
        r_d_2_x = [42.9, 43.1]
        r_d_2_y = [5680, 5500]
        lw_line_x = [38.03, 43.23]
        lw_line_y = [5400, 5400]
        zfw_line1_x = [34.76, 41.3]
        zfw_line1_y = [4911, 5300]
        zfw_line2_x = [41.3, 43.36]
        zfw_line2_y = [5300, 5300]

        ax.plot(left_x, left_y, color='black', linestyle='--', linewidth=1)
        ax.plot(l_d_1_x, l_d_1_y, color='black', linestyle='--', linewidth=1)
        ax.plot(l_d_2_x, l_d_2_y, color='black', linestyle='--', linewidth=1)
        ax.plot(right_x, right_y, color='black', linestyle='--', linewidth=1)  # draws the lines on graph
        ax.plot(top_x, top_y, color='black', linestyle='--', linewidth=1)
        ax.plot(r_d_1_x, r_d_1_y, color='black', linestyle='--', linewidth=1)
        ax.plot(r_d_2_x, r_d_2_y, color='black', linestyle='--', linewidth=1)
        ax.plot(lw_line_x, lw_line_y, color='black', linestyle='--', linewidth=1)
        ax.plot(zfw_line1_x, zfw_line1_y, color='black', linestyle='--', linewidth=1)
        ax.plot(zfw_line2_x, zfw_line2_y, color='black', linestyle='--', linewidth=1)

        dots = [(self.ramp_arm, self.ramp_weight, "red", "Ramp"),
                (self.takeoff_arm, self.takeoff_weight, 'orange', 'Takeoff'),
                (self.landing_arm, self.landing_weight, 'green', 'Landing'),
                (self.zero_fuel_arm, self.zero_fuel_weight, 'blue', 'Zero-Fuel')]

        for x, y, c, d in dots:
            ax.scatter(x, y, color=c, label=d)  # puts the weights on the graphs

        if mod_title is not None:  # goes through adding the names to the title once names are known to program
            if len(mod_title) == 2:
                ax.set_title(
                    f"Student: {mod_title[0]} - Instructor: {mod_title[1]}\nCessna 310 - {self.ident} - {date}")
            else:
                ax.set_title(f"Pilot: {mod_title[0]}\nCessna 310 - {self.ident} - {date}")
        else:
            ax.set_title(f"Cessna 310 - {self.ident} - {date}")

        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0), ncol=4)  # puts the legend for the dots on the screen
        ax.set_xlabel("Arm")
        ax.set_ylabel("Weight (Lbs)")  # axis labels

        fig.savefig('./WB/Photos/graph.jpeg', format='jpeg', dpi=300)  # saves the pic in the hard drive

    def create_sheet(self):
        # manually inputs all the fields from the class variables
        column1 = ["Seats 1+2", "Seats 3+4", "Seats 5+6", "Nose Baggage", "Wing Baggage", "Aft Baggage",
                   "Basic Empty Weight", "Zero-Fuel Weight", "Main Tanks", "Aux Tanks", "Ramp Weight", "Taxi Fuel",
                   "Takeoff Weight", "Main Fuel Burn", "Aux Fuel Burn", "Landing Weight"]
        column2 = [34.2, 68, 102, -31, 63, 126, self.empty_arm, self.zero_fuel_arm, self.fuel_mains_arm,
                   self.fuel_aux_arm, self.ramp_arm, self.fuel_mains_arm, self.takeoff_arm, self.fuel_mains_arm,
                   self.fuel_aux_arm, self.landing_arm]
        column3 = [self.pax1, self.pax2, self.pax3, self.bag1, self.bag2, self.bag3, self.empty_weight,
                   self.zero_fuel_weight, self.fuel_load_main, self.fuel_load_aux, self.ramp_weight, self.fuel_taxi,
                   self.takeoff_weight, self.fuel_flight_main, self.fuel_flight_aux, self.landing_weight]
        column4 = [self.pax1_moment, self.pax2_moment, self.pax3_moment, self.bag1_moment, self.bag2_moment,
                   self.bag3_moment, self.empty_moment, self.zero_fuel_moment, self.fuel_flight_main_moment,
                   self.fuel_flight_aux_moment, self.ramp_moment, self.fuel_taxi_moment, self.takeoff_moment,
                   self.fuel_flight_main_moment, self.fuel_flight_aux_moment, self.landing_moment]

        rows = list(zip(column1, column2, column3, column4))  # zip() turns each equal index position eg [2] into one
        # list item

        fig, ax = plt.subplots(figsize=(4, 4.2))
        ax.axis('tight')
        ax.axis('off')

        table = ax.table(cellText=rows, colLabels=["Item", "Arm", "Weight", "Moment"], loc='center')  # ignore warning.
        # table is the spreadsheet object

        # the following will shade some cells on the wb table for readability
        zf_weight_cell = table.get_celld()[(8, 0)]
        zf_weight_cell.set_facecolor("dodgerblue")

        ramp_weight_cell = table.get_celld()[(11, 0)]
        ramp_weight_cell.set_facecolor("darkorange")

        to_weight_cell = table.get_celld()[(13, 0)]
        to_weight_cell.set_facecolor("gray")

        ldg_weight_cell = table.get_celld()[(16, 0)]
        ldg_weight_cell.set_facecolor("gold")

        table.auto_set_column_width(col=list(range(len(rows[0]))))  # sets the column width
        table.scale(1, 1.3)  # scaling of cell sizes

        fig.savefig('./WB/Photos/sheet.jpeg', format='jpeg', dpi=300)  # saves on the hard drive

        with Image.open('WB/Photos/sheet.jpeg') as img:
            img = img.resize((1555, 1555))
            img.save('WB/Photos/sheet.jpeg', "JPEG")

    def combine_images(self):
        # this combines the two jpeg into one jpeg for readability. This method also shrinks the previously created
        # image to fit on the GUI screen for the actual program. The better quality will get uploaded to flight logger
        image1 = Image.open("WB/Photos/graph.jpeg")
        image2 = Image.open("WB/Photos/sheet.jpeg")

        if image1.width != image2.width:
            image2 = image2.resize((image1.width, image2.height))

        total_height = image1.height + image2.height

        combined_image = Image.new("RGB", (image1.width, total_height))

        combined_image.paste(image1, (0, 0))
        combined_image.paste(image2, (0, image1.height))

        combined_image.save("./WB/Photos/combined.jpeg")

        # makes a smaller copy to be displayed on the monitor. The high quality one goes on flight logger.
        with Image.open('WB/Photos/combined.jpeg') as img:
            img = img.resize((500, 780))
            img.save('./WB/Photos/combinedshrink.jpeg', "JPEG")
