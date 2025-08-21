from matplotlib import pyplot as plt
from PIL import Image
import datetime


# Calculation is a container of methods, upon instantiation it does all the math for the weight and balance.
# check_wb is where the information is checked for airworthiness, and a dictionary created for other classes to
# use later on. Fuel is converted to pounds in the math, and re-changed to gallons only for user viewing later.
# images also created in this class
class CalculationP:
    def __init__(self, data):
        self.data = data

        if self.data['ident'] == "C-GLVO":
            self.fuel_arm = 48
            self.empty_weight = 1503.8
            self.empty_arm = 39.14
        if self.data['ident'] == "C-GMRB":
            self.fuel_arm = 48
            self.empty_weight = 1492.7
            self.empty_arm = 39.48
        if self.data['ident'] == "C-GIQB":
            self.fuel_arm = 48
            self.empty_weight = 1477.78
            self.empty_arm = 39.53
        if self.data['ident'] == "C-GMKR":
            self.fuel_arm = 48
            self.empty_weight = 1494
            self.empty_arm = 39.1

        self.ident = self.data['ident']
        self.fuel_load = round(self.data['fuel_load'] * 6, 2)  # 6 pounds per gallon
        self.fuel_taxi = round(self.data['fuel_taxi'] * -6, 2)  # negative to represent fuel being burned from tanks
        self.fuel_flight = round(self.data['fuel_flight'] * -6, 2)
        self.pax1 = self.data['pax1']
        self.pax2 = self.data['pax2']
        self.bag1 = self.data['bag1']
        self.bag2 = self.data['bag2']

        self.pax1_moment = round(self.pax1 * 37, 2)
        self.pax2_moment = round(self.pax2 * 73, 2)
        self.bag1_moment = round(self.bag1 * 95, 2)
        self.bag2_moment = round(self.bag2 * 123, 2)
        self.empty_moment = round(self.empty_weight * self.empty_arm, 2)

        self.zero_fuel_weight = round(self.empty_weight + self.pax1 + self.pax2 + self.bag1 + self.bag2, 2)
        self.zero_fuel_moment = round(self.empty_moment + self.pax1_moment + self.pax2_moment +
                                      self.bag1_moment + self.bag2_moment, 2)
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

        # these will check the category the plane will be in from t/o to landing. 1 is normal, 0 is utility
        to_category = 1
        ldg_category = 1

        if self.ramp_weight > 2407:
            ramp_weight_good = False
        if self.takeoff_weight > 2400:
            to_weight_good = False

        zfw_arm_good = self.check_in_limits(self.zero_fuel_weight, self.zero_fuel_arm)
        ldg_arm_good = self.check_in_limits(self.landing_weight, self.landing_arm)
        to_arm_good = self.check_in_limits(self.takeoff_weight, self.takeoff_arm)

        if to_weight_good and to_arm_good == 1:
            to_category = self.check_category(self.takeoff_weight, self.takeoff_arm)
        if to_weight_good and ldg_arm_good == 1:
            ldg_category = self.check_category(self.landing_weight, self.landing_arm)

        # fuel reserves in gallons and hours calculated here using 10 GPH
        reserve_gallons = round((self.landing_weight - self.zero_fuel_weight) / 6, 1)
        reserve_hours = round(reserve_gallons / 10, 1)

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
        if to_category == 1:
            self.data["to_category"] = "Normal Category"
        else:
            self.data["to_category"] = "Utility Category"
        if ldg_category == 1:
            self.data["ldg_category"] = "Normal Category"
        else:
            self.data["ldg_category"] = "Utility Category"
        # time_util is 0 if both takeoff and landing categories are the same. If they switch in flight, it becomes the
        # minutes until that happens.
        if to_category == 1 and ldg_category == 0:
            self.data["time_util"] = self.time_util([self.takeoff_weight, self.takeoff_arm],
                                                    [self.landing_weight, self.landing_arm])
        else:
            self.data["time_util"] = 0
        return self.data

    # re-usable function to check if a given point on the wb graph are in limits using limitations for the Cessna 152.
    # carves the polygon of the loading limits chart into multiple sections of squares and triangle to calculate if
    # in limits or not
    def check_in_limits(self, weight, arm):
        weight = round(weight, 2)
        arm = round(arm, 2)
        if weight < 1950 and 35 <= arm <= 47.3:
            return 1
        if weight < 1950 and arm < 35:
            return 0
        if (1950 <= weight <= 2400) and 39.5 <= arm <= 47.3:
            return 1
        if arm > 47.3:
            return 2
        # the below is the top-left area on the graph, uses the bottom left as origin of the graph and diagonal line
        # has a slope of 193.939393
        if (1950 <= weight <= 2400) and arm < 39.5:
            a = weight - 1950
            b = arm - 35
            c = 100 * b
            if a <= c:
                return 1
            if a > c:
                return 0

    # 0 is utility. 1 is normal.
    def check_category(self, weight, arm):
        weight = round(weight, 2)
        arm = round(arm, 2)
        if (weight <= 2100) and (arm <= 40.5):
            return 0
        else:
            return 1  # less complex function needed here, as check_category only executes if the wb is valid.

    # takes a weight and arm pair in [2105, 40.7] format, and returns how many minutes into the flight the cat switches
    # to util. Only gets run if to is normal and ldg is utility
    def time_util(self, to, ldg):
        to_wt = to[0]
        to_arm = to[1]
        ldg_wt = ldg[0]
        ldg_arm = ldg[1]

        slope = ((to_wt - ldg_wt) / (to_arm - ldg_arm))  # making linear equation, this is slope
        y_int = (ldg_wt - (ldg_arm * slope))  # b of equation
        top_int = (2100 - y_int) / slope  # the arm when weight is the upper limit of the utility category
        if top_int <= 40.5:  # this goes if line crosses through the top edge of utility cat
            ratio = (to_arm - top_int) / (to_arm - ldg_arm)
            fuel_elapsed = to_wt - ldg_wt
            # /6/10*60 is redundant, but brackets finds how many pounds of gas into the flight the category changes.
            # then /6 to gallons, /10 to time in hours for 10GPH, and *60 for minutes.
            return int((fuel_elapsed * ratio) / 6 / 10 * 60)
        if top_int > 40.5:  # goes if line crosses through the right edge. In this case it crosses through 40.5 always
            ratio = (to_arm - 40.5) / (to_arm - ldg_arm)
            fuel_elapsed = to_wt - ldg_wt
            return int((fuel_elapsed * ratio) / 6 / 10 * 60)
        return None

    def create_graph(self, mod_title=None):
        # if mod_title is passed in an arg, it will allow the title to be changed to display the name of instructor
        # and student flying this. This func creates the wb graph, similar to one student is used to using
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d")  # used for the title datestamp

        x_range = [34, 48.5]
        y_range = [1500, 2500]

        fig, ax = plt.subplots()
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)  # drawing the visible area of the graph

        left_x = [35, 35]
        left_y = [1500, 1950]
        dia_x = [35, 39.5]
        dia_y = [1950, 2400]
        top_x = [39.5, 47.3]
        top_y = [2400, 2400]
        right_x = [47.3, 47.3]
        right_y = [1500, 2400]
        top_util_x = [36.5, 40.5]
        top_util_y = [2100, 2100]
        right_util_x = [40.5, 40.5]
        right_util_y = [1500, 2100]

        ax.plot(left_x, left_y, color='black', linestyle='--', linewidth=1)
        ax.plot(dia_x, dia_y, color='black', linestyle='--', linewidth=1)
        ax.plot(top_x, top_y, color='black', linestyle='--', linewidth=1)
        ax.plot(right_x, right_y, color='black', linestyle='--', linewidth=1)  # draws the lines on graph
        ax.plot(top_util_x, top_util_y, color='black', linestyle='--', linewidth=1)
        ax.plot(right_util_x, right_util_y, color='black', linestyle='--', linewidth=1)

        dots = [(self.ramp_arm, self.ramp_weight, "red", "Ramp"),
                (self.takeoff_arm, self.takeoff_weight, 'orange', 'Takeoff'),
                (self.landing_arm, self.landing_weight, 'green', 'Landing'),
                (self.zero_fuel_arm, self.zero_fuel_weight, 'blue', 'Zero-Fuel')]

        for x, y, c, d in dots:
            ax.scatter(x, y, color=c, label=d)  # puts the weights on the graphs

        if mod_title is not None:  # goes through adding the names to the title once names are known to program
            if len(mod_title) == 2:
                ax.set_title(
                    f"Student: {mod_title[0]} - Instructor: {mod_title[1]}\nCessna 172 - {self.ident} - {date}")
            else:
                ax.set_title(f"Pilot: {mod_title[0]}\nCessna 172 - {self.ident} - {date}")
        else:
            ax.set_title(f"Cessna 172 - {self.ident} - {date}")

        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0), ncol=4)  # puts the legend for the dots on the screen
        ax.set_xlabel("Arm")
        ax.set_ylabel("Weight (Lbs)")  # axis labels

        fig.savefig('./WB/Photos/graph.jpeg', format='jpeg', dpi=300)  # saves the pic in the hard drive

    def create_sheet(self):
        # manually inputs all the fields from the class variables. Very straight forward
        column1 = ["Front Seats", "Rear Seats", "Baggage Area 1", "Baggage Area 2", "Basic Empty Weight",
                   "Zero Fuel Weight", "Fuel - Wing Tanks", "Ramp Weight", "Less Fuel for Taxi", "Takeoff Weight",
                   "Less Fuel for Flight", "Landing Weight"]
        column2 = [37, 73, 95, 123, self.empty_arm, self.zero_fuel_arm, self.fuel_arm, self.ramp_arm, self.fuel_arm,
                   self.takeoff_arm, self.fuel_arm, self.landing_arm]
        column3 = [self.pax1, self.pax2, self.bag1, self.bag2, self.empty_weight, self.zero_fuel_weight, self.fuel_load,
                   self.ramp_weight, self.fuel_taxi, self.takeoff_weight, self.fuel_flight, self.landing_weight]
        column4 = [self.pax1_moment, self.pax2_moment, self.bag1_moment, self.bag2_moment, self.empty_moment,
                   self.zero_fuel_moment, self.fuel_load_moment, self.ramp_moment, self.fuel_taxi_moment,
                   self.takeoff_moment,self.fuel_flight_moment, self.landing_moment]

        rows = list(zip(column1, column2, column3, column4))  # zip() turns each equal index position eg [2] into one
        # list item

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.axis('tight')
        ax.axis('off')

        table = ax.table(cellText=rows, colLabels=["Item", "Arm", "Weight", "Moment"], loc='center')  # ignore warning.
        # table is the spreadsheet object

        # the following will shade some cells on the wb table for readability
        zf_weight_cell = table.get_celld()[(6, 0)]
        zf_weight_cell.set_facecolor("dodgerblue")

        ramp_weight_cell = table.get_celld()[(8, 0)]
        ramp_weight_cell.set_facecolor("darkorange")

        to_weight_cell = table.get_celld()[(10, 0)]
        to_weight_cell.set_facecolor("gray")

        ldg_weight_cell = table.get_celld()[(12, 0)]
        ldg_weight_cell.set_facecolor("gold")

        table.auto_set_column_width(col=list(range(len(rows[0]))))  # sets the column width
        table.scale(1, 1.75)  # scaling of cell sizes

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
