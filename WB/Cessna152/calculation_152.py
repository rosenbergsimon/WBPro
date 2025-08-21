from matplotlib import pyplot as plt
from PIL import Image
import datetime


# Calculation is a container of methods, upon instantiation it does all the math for the weight and balance.
# check_wb is where the information is checked for airworthiness, and a dictionary created for other classes to
# use later on. Fuel is converted to pounds in the math, and re-changed to gallons only for user viewing later.
# images also created in this class
class Calculation152:
    def __init__(self, data):
        self.data = data

        if self.data['ident'] == "C-GZHL":
            self.fuel_arm = 42
            self.empty_weight = 1138.4
            self.empty_arm = 30.33
        elif self.data['ident'] == "C-GYBI":
            self.fuel_arm = 42
            self.empty_weight = 1141.28
            self.empty_arm = 30.11
        elif self.data['ident'] == "C-GOLK":
            self.fuel_arm = 39.5
            self.empty_weight = 1146.42
            self.empty_arm = 29.65
        elif self.data['ident'] == "C-GGKH":
            self.fuel_arm = 39.5
            self.empty_weight = 1166.07
            self.empty_arm = 29.79

        self.ident = self.data['ident']
        self.fuel_load = round(self.data['fuel_load'] * 6, 2)   # 6 pounds per gallon
        self.fuel_taxi = round(self.data['fuel_taxi'] * -6, 2)  # negative to represent fuel being burned from tanks
        self.fuel_flight = round(self.data['fuel_flight'] * -6, 2)
        self.pax = self.data['pax1']
        self.bag1 = self.data['bag1']
        self.bag2 = self.data['bag2']

        self.pax_moment = round(self.pax * 39, 2)
        self.bag1_moment = round(self.bag1 * 64, 2)
        self.bag2_moment = round(self.bag2 * 84, 2)
        self.empty_moment = round(self.empty_weight * self.empty_arm, 2)

        self.zero_fuel_weight = round(self.empty_weight + self.pax + self.bag1 + self.bag2, 2)
        self.zero_fuel_moment = round(self.empty_moment + self.pax_moment + self.bag1_moment + self.bag2_moment, 2)
        self.zero_fuel_arm = round(self.zero_fuel_moment / self.zero_fuel_weight, 2)

        self.fuel_load_moment = round(self.fuel_load * self.fuel_arm, 2)
        self.ramp_weight = round(self.zero_fuel_weight + self.fuel_load, 2)
        self.ramp_moment = round(self.zero_fuel_moment + self.fuel_load_moment, 2)
        self.ramp_arm = round(self.ramp_moment / self.ramp_weight, 2)

        self.fuel_taxi_moment = round(self.fuel_taxi * self.fuel_arm, 2)
        self.takeoff_weight = round(self.ramp_weight + self.fuel_taxi, 2)
        self.takeoff_moment = round(self.ramp_moment + self.fuel_taxi_moment, 2)
        self.takeoff_arm = round(self.takeoff_moment / self.takeoff_weight, 2)

        self.fuel_flight_moment = round(self.fuel_flight * self.fuel_arm, 2)
        self.landing_weight = round(self.takeoff_weight + self.fuel_flight, 2)
        self.landing_moment = round(self.takeoff_moment + self.fuel_flight_moment, 2)
        self.landing_arm = round(self.landing_moment / self.landing_weight, 2)

    def check_wb(self):
        # weight_good is a boolean to be changed, if overweight becomes False. arm_good: 0 is forward, 1 is in limits,
        # 2 is aft.
        ramp_weight_good = True
        to_weight_good = True
        zfw_arm_good = 1
        ldg_arm_good = 1
        to_arm_good = 1

        if self.ramp_weight > 1675:
            ramp_weight_good = False
        if self.takeoff_weight > 1670:
            to_weight_good = False

        zfw_arm_good = self.check_in_limits(self.zero_fuel_weight, self.zero_fuel_arm)
        ldg_arm_good = self.check_in_limits(self.landing_weight, self.landing_arm)
        to_arm_good = self.check_in_limits(self.takeoff_weight, self.takeoff_arm)

        # fuel reserves in gallons and hours calculated here using 7 GPH
        reserve_gallons = round((self.landing_weight - self.zero_fuel_weight) / 6, 1)
        reserve_hours = round(reserve_gallons / 7, 1)

        self.create_graph()
        self.create_sheet()
        self.combine_images()  # these all make the image, and combine them all for viewing/uploading

        # returns all the relevant information that the upload class will need to display.
        self.data["ramp_weight_good"] = ramp_weight_good
        self.data["to_weight_good"] = to_weight_good
        self.data["zfw_arm_good"] = zfw_arm_good
        self.data["ldg_arm_good"] = ldg_arm_good
        self.data["to_arm_good"] = to_arm_good
        self.data["reserve_gallons"] = reserve_gallons
        self.data["reserve_hours"] = reserve_hours
        self.data["takeoff_weight"] = self.takeoff_weight
        self.data["landing_weight"] = self.landing_weight

        return self.data

    # re-usable function to check if a given point on the wb graph are in limits using limitations for the Cessna 152.
    # carves the polygon of the loading limits chart into multiple sections of squares and triangle to calculate if
    # in limits or not
    def check_in_limits(self, weight, arm):
        weight = round(weight, 2)
        arm = round(arm, 2)
        if weight < 1350 and 31 <= arm <= 36.5:
            return 1
        if weight < 1350 and arm < 31:
            return 0
        if (1350 <= weight <= 1670) and 32.65 <= arm <= 36.5:
            return 1
        if arm > 36.5:
            return 2
        # the below is the top-left area on the graph, uses the bottom left as origin of the graph and diagonal line
        # has a slope of 193.939393
        if (1350 <= weight <= 1670) and arm < 32.65:
            a = weight - 1350
            b = arm - 31
            c = 193.9393939393 * b
            if a <= c:
                return 1
            if a > c:
                return 0

    def create_graph(self, mod_title=None):
        # if mod_title is passed in an arg, it will allow the title to be changed to display the name of instructor
        # and student flying this. This func creates the wb graph, similar to one student is used to using
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d")  # used for the title datestamp

        x_range = [30, 38]
        y_range = [1100, 1750]

        fig, ax = plt.subplots()
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)  # drawing the visible area of the graph

        left_x = [31, 31]
        left_y = [1100, 1350]
        dia_x = [31, 32.65]
        dia_y = [1350, 1670]
        top_x = [32.65, 36.5]
        top_y = [1670, 1670]
        right_x = [36.5, 36.5]
        right_y = [1100, 1670]

        ax.plot(left_x, left_y, color='black', linestyle='--', linewidth=1)
        ax.plot(dia_x, dia_y, color='black', linestyle='--', linewidth=1)
        ax.plot(top_x, top_y, color='black', linestyle='--', linewidth=1)
        ax.plot(right_x, right_y, color='black', linestyle='--', linewidth=1)  # draws the lines on graph

        dots = [(self.ramp_arm, self.ramp_weight, "red", "Ramp"),
                (self.takeoff_arm, self.takeoff_weight, 'orange', 'Takeoff'),
                (self.landing_arm, self.landing_weight, 'green', 'Landing'),
                (self.zero_fuel_arm, self.zero_fuel_weight, 'blue', 'Zero-Fuel')]

        for x, y, c, d in dots:
            ax.scatter(x, y, color=c, label=d)  # puts the weights on the graphs

        if mod_title is not None:  # goes through adding the names to the title once names are known to program
            if len(mod_title) == 2:
                ax.set_title(
                    f"Student: {mod_title[0]} - Instructor: {mod_title[1]}\nCessna 152 - {self.ident} - {date}")
            else:
                ax.set_title(f"Pilot: {mod_title[0]}\nCessna 152 - {self.ident} - {date}")
        else:
            ax.set_title(f"Cessna 152 - {self.ident} - {date}")

        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0), ncol=4)  # puts the legend for the dots on the screen
        ax.set_xlabel("Arm")
        ax.set_ylabel("Weight (Lbs)")  # axis labels

        fig.savefig('./WB/Photos/graph.jpeg', format='jpeg', dpi=300)  # saves the pic in the hard drive

    def create_sheet(self):
        # manually inputs all the fields from the class variables
        column1 = ["Front Seats", "Baggage Area 1", "Baggage Area 2", "Basic Empty Weight", "Zero Fuel Weight",
                   "Fuel - Wing Tanks", "Ramp Weight", "Less Fuel for Taxi", "Takeoff Weight", "Less Fuel for Flight",
                   "Landing Weight"]
        column2 = [39, 64, 84, self.empty_arm, self.zero_fuel_arm, self.fuel_arm, self.ramp_arm, self.fuel_arm,
                   self.takeoff_arm, self.fuel_arm, self.landing_arm]
        column3 = [self.pax, self.bag1, self.bag2, self.empty_weight, self.zero_fuel_weight, self.fuel_load,
                   self.ramp_weight, self.fuel_taxi, self.takeoff_weight, self.fuel_flight, self.landing_weight]
        column4 = [self.pax_moment, self.bag1_moment, self.bag2_moment, self.empty_moment, self.zero_fuel_moment,
                   self.fuel_load_moment, self.ramp_moment, self.fuel_taxi_moment, self.takeoff_moment,
                   self.fuel_flight_moment, self.landing_moment]

        rows = list(zip(column1, column2, column3, column4))  # zip() turns each equal index position eg [2] into one
        # list item

        fig, ax = plt.subplots(figsize=(4, 5))
        ax.axis('tight')
        ax.axis('off')

        table = ax.table(cellText=rows, colLabels=["Item", "Arm", "Weight", "Moment"], loc='center')  # ignore warning.
        # table is the spreadsheet object

        # the following will shade some cells on the wb table for readability
        zf_weight_cell = table.get_celld()[(5, 0)]
        zf_weight_cell.set_facecolor("dodgerblue")

        ramp_weight_cell = table.get_celld()[(7, 0)]
        ramp_weight_cell.set_facecolor("darkorange")

        to_weight_cell = table.get_celld()[(9, 0)]
        to_weight_cell.set_facecolor("gray")

        ldg_weight_cell = table.get_celld()[(11, 0)]
        ldg_weight_cell.set_facecolor("gold")

        table.auto_set_column_width(col=list(range(len(rows[0]))))  # sets the column width
        table.scale(1, 2)  # scaling of cell sizes

        fig.savefig('./WB/Photos/sheet.jpeg', format='jpeg', dpi=300)  # saves on the hard drive

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
