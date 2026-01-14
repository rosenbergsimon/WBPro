import customtkinter as tk
from customtkinter import CTkImage
from CTkMessagebox import CTkMessagebox
from PIL import Image
from WB.api_call import return_students
from WB.lesson_uploader import LessonWB
from WB.booking_uploader import BookingWB
import datetime as dt


# holds the objects on the screen for the right-most upload frame. The buttons that hold the student names link to two
# external functions, one for booking uploads, one for lesson uploads.
class Upload(tk.CTkFrame):
    def __init__(self, master, data, update_image, root, close):
        super().__init__(master)
        self.root = root
        self.quit_app = close
        self.three_photo = CTkImage(dark_image=Image.open("WB/Photos/three.png"), size=(48, 48))
        self.configure(fg_color="#353535", width=533, height=900)
        self.label_font = tk.CTkFont(family="ebrima", size=16)
        self.title_font = tk.CTkFont(family="ebrima", size=18)
        self.label_u_font = tk.CTkFont(family="ebrima", size=14, underline=True)
        self.title_u_font = tk.CTkFont(family="ebrima", size=18, underline=True)

        self.update_image = update_image
        self.data = data

        # widgets on the screen are as below.
        self.three_icon = tk.CTkButton(self, image=self.three_photo, height=48, width=48, state="disabled",
                                       fg_color="#353535", text="")
        self.three_icon.grid(column=0, row=0, columnspan=2, padx=(12, 460), pady=(20, 5))

        self.title_label = tk.CTkLabel(self, text="Review the Weight and Balance Information Below:",
                                       font=self.title_u_font, width=494)
        self.title_label.grid(column=0, columnspan=2, row=1, padx=20, pady=20)

        if self.data["type"] == "Cessna 172":
            self.to_weight = tk.CTkLabel(self, text=f"Takeoff Weight: {int(self.data["takeoff_weight"])} pounds. "
                                                    f"({self.data["to_category"]})", font=self.label_font,
                                         width=494, anchor="w")
            self.to_weight.grid(column=0, row=2, padx=20, pady=(20, 10))

            self.landing_weight = tk.CTkLabel(self, text=f"Landing Weight: {int(self.data["landing_weight"])} pounds. "
                                                         f"({self.data["ldg_category"]})", font=self.label_font,
                                              width=494, anchor="w")
            self.landing_weight.grid(column=0, row=3, padx=20, pady=10)

            if self.data["time_util"] == 0:
                self.transfer_util = tk.CTkLabel(self, text="", font=self.label_font, width=494, anchor="w")
                self.transfer_util.grid(column=0, row=4, padx=20, pady=10)
            else:
                self.transfer_util = tk.CTkLabel(self, text=f"The aircraft will enter the utility category "
                                                            f"{self.data["time_util"]} minutes after takeoff.",
                                                 font=self.label_font, width=494, anchor="w")
                self.transfer_util.grid(column=0, row=4, padx=20, pady=10)

        else:
            self.to_weight = tk.CTkLabel(self, text=f"Takeoff Weight: {int(self.data["takeoff_weight"])} pounds.",
                                         font=self.label_font, width=494, anchor="w")
            self.to_weight.grid(column=0, row=2, padx=20, pady=20)

            self.landing_weight = tk.CTkLabel(self, text=f"Landing Weight: {int(self.data["landing_weight"])} pounds.",
                                              font=self.label_font, width=494, anchor="w")
            self.landing_weight.grid(column=0, row=3, padx=20, pady=(15, 0))

            self.transfer_util = tk.CTkLabel(self, text="", font=self.label_font, width=494, anchor="w")
            self.transfer_util.grid(column=0, row=4, padx=20, pady=0)

        if self.data["type"] == "Cessna 152":
            self.fuel_reserve = tk.CTkLabel(self, text=f"Fuel Reserve on Landing: {self.data["reserve_gallons"]} "
                                                       f"gallons ({self.data["reserve_hours"]} hours @ 7 GPH)",
                                            font=self.title_font, width=494, anchor="w")
            self.fuel_reserve.grid(column=0, columnspan=2, row=5, padx=20, pady=(10, 15))
        elif self.data["type"] == "Cessna 172":
            self.fuel_reserve = tk.CTkLabel(self, text=f"Fuel Reserve on Landing: {self.data["reserve_gallons"]} "
                                                       f"gallons ({self.data["reserve_hours"]} hours @ 10 GPH)",
                                            font=self.title_font, width=494, anchor="w")
            self.fuel_reserve.grid(column=0, columnspan=2, row=5, padx=20, pady=(10, 15))
        elif self.data["type"] == "Cessna 72R":
            self.fuel_reserve = tk.CTkLabel(self, text=f"Fuel Reserve on Landing: {self.data["reserve_gallons"]} "
                                                       f"gallons ({self.data["reserve_hours"]} hours @ 12 GPH)",
                                            font=self.title_font, width=494, anchor="w")
            self.fuel_reserve.grid(column=0, columnspan=2, row=5, padx=20, pady=(10, 15))
        elif self.data['type'] == "Cessna 182":
            self.fuel_reserve = tk.CTkLabel(self, text=f"Fuel Reserve on Landing: {self.data["reserve_gallons"]} "
                                                       f"gallons ({self.data["reserve_hours"]} hours @ 15 GPH)",
                                            font=self.title_font, width=494, anchor="w")
            self.fuel_reserve.grid(column=0, columnspan=2, row=5, padx=20, pady=(10, 15))
        elif self.data['type'] == "Cessna 310":
            self.fuel_reserve = tk.CTkLabel(self, text=f"Fuel Reserve on Landing: {self.data["reserve_gallons"]} "
                                                       f"pounds ({self.data["reserve_hours"]} hours @ 180 PPH)",
                                            font=self.title_font, width=494, anchor="w")
            self.fuel_reserve.grid(column=0, columnspan=2, row=5, padx=20, pady=(10, 15))

        self.go_no_go_icon = tk.CTkButton(self, text="", font=self.title_font, height=40, width=400, hover=False)
        self.go_no_go_icon.grid(column=0, columnspan=2, row=6, padx=20, pady=15)

        self.upload_button = tk.CTkButton(self, text="Upload", font=self.title_font, height=40, width=400,
                                          fg_color="#3EA216", command=self.show_names_box)
        self.upload_button.grid(column=0, columnspan=2, row=7, padx=20, pady=15)

        self.upload_title = tk.CTkLabel(self, text="", width=494, font=self.title_u_font)
        self.upload_title.grid(column=0, columnspan=2, row=8, padx=20, pady=20)

        self.names_frame = None  # the below are set to None, as the object needs to be constructed

        self.upload_status_bar = None

        self.update_buttons()

    def update_buttons(self):
        # this checks if wb is in limits, and sets upload to enabled/disabled
        if self.data['type'] != "Cessna 310" and self.data['type'] != "Cessna 182":
            self.data['ldg_weight_good'] = True
            self.data['zfw_weight_good'] = True
        if self.data['type'] == "Cessna 182":
            self.data['zfw_weight_good'] = True

        if self.data['type'] == "Cessna 310" and not self.data['to_weight_good']:
            self.go_no_go_icon.configure(text="Takeoff weight is overweight. Please redo.", fg_color="red")
            self.upload_button.configure(state="disabled")
        elif self.data['type'] == "Cessna 310" and not self.data['ramp_weight_good']:
            self.go_no_go_icon.configure(text="Ramp weight is overweight. Please redo.", fg_color="red")
            self.upload_button.configure(state="disabled")
        elif self.data['type'] == "Cessna 310" and not self.data['ldg_weight_good']:
            self.go_no_go_icon.configure(text="Landing weight is overweight. Please redo.", fg_color="red")
            self.upload_button.configure(state="disabled")
        elif self.data['type'] == "Cessna 310" and not self.data['zfw_weight_good']:
            self.go_no_go_icon.configure(text="Zero-fuel weight is overweight. Please redo.", fg_color="red")
            self.upload_button.configure(state="disabled")
        elif self.data['type'] != "Cessna 310" and not self.data['to_weight_good']:
            self.go_no_go_icon.configure(text="Takeoff weight is overweight. Please redo.", fg_color="red")
            self.upload_button.configure(state="disabled")
        elif self.data['type'] != "Cessna 310" and not self.data['ramp_weight_good']:
            self.go_no_go_icon.configure(text="Ramp weight is overweight. Please redo.", fg_color="red")
            self.upload_button.configure(state="disabled")
        elif self.data['type'] == "Cessna 182" and not self.data['ldg_weight_good']:
            self.go_no_go_icon.configure(text="Landing weight is overweight. Please redo.", fg_color="red")
            self.upload_button.configure(state="disabled")
        elif self.data["zfw_arm_good"] == 0:
            self.go_no_go_icon.configure(fg_color="red", text="Zero-fuel weight is too far forward. Please redo.")
            self.upload_button.configure(state="disabled")
        elif self.data["ldg_arm_good"] == 0:
            self.go_no_go_icon.configure(fg_color="red", text="Landing weight is too far forward. Please redo.")
            self.upload_button.configure(state="disabled")
        elif self.data["to_arm_good"] == 0:
            self.go_no_go_icon.configure(fg_color="red", text="Takeoff weight is too far forward. Please redo.")
            self.upload_button.configure(state="disabled")
        elif self.data["zfw_arm_good"] == 2:
            self.go_no_go_icon.configure(fg_color="red", text="Zero-fuel weight is too far aft. Please redo.")
            self.upload_button.configure(state="disabled")
        elif self.data["ldg_arm_good"] == 2:
            self.go_no_go_icon.configure(fg_color="red", text="Landing weight is too far aft. Please redo.")
            self.upload_button.configure(state="disabled")
        elif self.data["to_arm_good"] == 2:
            self.go_no_go_icon.configure(fg_color="red", text="Takeoff weight is too far aft. Please redo.")
            self.upload_button.configure(state="disabled")
        else:
            self.go_no_go_icon.configure(fg_color="#006300", text="Aircraft is within Weight and Balance Limits.")
            self.upload_button.configure(state="normal")

    def show_names_box(self):
        self.upload_title.configure(text="Select your name below to upload to FlightLogger:")
        if self.names_frame is not None:
            self.names_frame.destroy()
            self.names_frame = None
        self.names_frame = tk.CTkFrame(self, height=180, width=394, fg_color="#606060")

        if self.upload_status_bar is not None:
            self.upload_status_bar.destroy()
            self.upload_status_bar = None
        self.upload_status_bar = tk.CTkButton(self, text="Select your Name", fg_color="#606060", width=394, height=70,
                                              font=self.title_font, hover=False)

        self.names_frame.grid(column=0, columnspan=2, row=9, padx=70, pady=20)
        self.upload_status_bar.grid(column=0, columnspan=2, row=10, padx=70, pady=20)

        # runs the api call
        students = return_students(self.data['ident'])
        student_buttons = []

        for i in students: 
            i['time'] = dt.datetime.fromisoformat(i['time'])
        students.sort(key=lambda x: x['time'])

        students = students[0:3]

        for i in students:
            local_time = i['time'].astimezone(dt.timezone(dt.timedelta(hours=-6)))
            time_needed = local_time.strftime("%H:%M")

            if i['flight_type'] == "SingleStudentBooking" or i['flight_type'] == "MultiStudentBooking":
                student_buttons.append(tk.CTkButton(self.names_frame, text=f"{i['student']} ({time_needed})",
                                                    width=354, height=40, fg_color="#3EA216", font=self.title_font))
                student_buttons[-1].configure(command=lambda idx=len(student_buttons):
                                              LessonWB(students[idx - 1], self.upload_button, student_buttons,
                                                       self.upload_status_bar, self.root, self.quit_app,
                                                       self.update_image))

                # will be 0 if no lesson attached.
                if i['codes'][1] == '0' or i['codes'][2] == '0':
                    student_buttons[-1].configure(command=lambda idx=len(student_buttons):
                                                  self.remind_instructor_lesson(students[idx - 1]['flight_type']))
                student_buttons[-1].grid(column=0, row=len(student_buttons) - 1, padx=20, pady=10)

            if i['flight_type'] == "RentalBooking" or i['flight_type'] == "OperationBooking":
                student_buttons.append(tk.CTkButton(self.names_frame, text=f"{i['student']} ({time_needed})",
                                                    width=354, height=40, fg_color="#3EA216", font=self.title_font))
                student_buttons[-1].configure(command=lambda idx=len(student_buttons):
                                              BookingWB(students[idx - 1], self.upload_button, student_buttons,
                                                        self.upload_status_bar, self.root, self.quit_app,
                                                        self.update_image))
                student_buttons[-1].grid(column=0, row=len(student_buttons) - 1, padx=20, pady=10)

    def remind_instructor_lesson(self, flight_type):
        if flight_type == "SingleStudentBooking":
            CTkMessagebox(title="Error",
                          message="Please ensure your instructor has attached a valid lesson\n to the booking in "
                                  "FlightLogger, then re-click the Upload button.",
                          font=("ebrima", 14), fg_color="#353535", button_color="#3EA216")
        if flight_type == "MultiStudentBooking":
            CTkMessagebox(title="Error",
                          message="Please ensure your instructor has attached a valid lesson\n to both students' "
                                  "booking in FlightLogger, then re-click the Upload button.",
                          font=("ebrima", 14), fg_color="#353535", button_color="#3EA216")

    def update_image(self, names):
        self.update_image(names)
