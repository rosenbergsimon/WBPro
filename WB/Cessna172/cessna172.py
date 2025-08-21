import customtkinter as tk
from WB.Cessna172.input import Input
from WB.image import ImageWindow
from WB.upload import Upload
from WB.Cessna172.calculation_n import CalculationN
from WB.Cessna172.calculation_p import CalculationP
from WB.Cessna172.calculation_s import CalculationS
from customtkinter import CTkImage
from PIL import Image


class C172(tk.CTkToplevel):
    def __init__(self, launch_page, close_app, root, home):
        super().__init__()
        self.root = root
        self.launch_page = launch_page
        self.quit_app = close_app
        self.title("Cessna 172")
        self.data = {}  # will be used to hold everything about this wb use case.
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        # below are two images used on the background of the screen. The CTkImage class holds the picture, and
        # the button structure below in each frame hold the image.
        self.two_photo = CTkImage(dark_image=Image.open("WB/Photos/two.png"), size=(48, 48))
        self.three_photo = CTkImage(dark_image=Image.open("WB/Photos/three.png"), size=(48, 48))

        self.calculation = None  # will be used for the Calculation object and re-using the numbers there
        self.geometry("1600x900+0+0")  # +0+0 is the window will open on the same spot on the monitor every time.

        # each frame is one third of the screen. Left one will not change, so is instantiated. Others will be
        # instantiated later, placeholder needed now.
        self.left_frame = Input(self, self.calculate, self.data)
        self.left_frame.grid(column=0, row=0)

        self.mid_frame = tk.CTkFrame(self, fg_color="#353535", height=900, width=533)
        self.mid_frame.grid(column=1, row=0)
        self.two_icon = tk.CTkButton(self.mid_frame, image=self.two_photo, height=48, width=48, state="disabled",
                                     fg_color="#353535", text="")
        self.two_icon.grid(column=0, row=0, padx=(12, 460), pady=(20, 5))

        self.right_frame = tk.CTkFrame(self, fg_color="#353535", height=900, width=533)
        self.right_frame.grid(column=2, row=0)
        self.three_icon = tk.CTkButton(self.right_frame, image=self.three_photo, height=48, width=48, state="disabled",
                                       fg_color="#353535", text="")
        self.three_icon.grid(column=0, row=0, padx=(12, 460), pady=(20, 5))

        self.left_frame.grid_propagate(False)  # this ensures the frames will not resize and lock to chosen width/height
        self.mid_frame.grid_propagate(False)
        self.right_frame.grid_propagate(False)

    # this function point to calculation_172.py class, and does all the calculating work/making of the images. Also hold
    # functions for updating the wb images
    def calculate(self, data):
        self.data = data
        if data['ident'] == "C-GBGV":
            self.calculation = CalculationN(data)
        elif data['ident'] == "C-FARC":
            self.calculation = CalculationS(data)
        else:
            self.calculation = CalculationP(data)
        self.data = self.calculation.check_wb()
        self.new_right()

    # re-launches the new frames, creates instances of the objects, and then will call the appropriate methods.
    # right_data is where the relevant data will be copied to
    def new_right(self):
        # mid_frame is created first, as the methods that belong to it need to be accessed in right_frame.
        self.mid_frame.destroy()
        self.mid_frame = ImageWindow(self)  # only holds the wb image within it.
        self.mid_frame.grid(column=1, row=0)

        self.right_frame.destroy()
        self.right_frame = Upload(self, self.data, self.update_image, self.root, self.quit_app)
        self.right_frame.grid(column=2, row=0)

        self.mid_frame.grid_propagate(False)
        self.right_frame.grid_propagate(False)

    def update_image(self, names):  # will revise images to add student/instructor name
        self.calculation.create_graph(names)
        self.calculation.combine_images()
