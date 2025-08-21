import customtkinter as tk
from customtkinter import CTkImage
from PIL import Image


# Image is the middle frame on the screen, only used to pull the image from the file in the program, and put it on
# the screen.
class ImageWindow(tk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # below are the image files belonging to the frame
        self.two_photo = CTkImage(dark_image=Image.open("WB/Photos/two.png"), size=(48, 48))
        self.wb_image = CTkImage(dark_image=Image.open("WB/Photos/combinedshrink.jpeg"), size=(500, 780))

        self.configure(fg_color="#353535", width=533, height=900)

        self.two_icon = tk.CTkButton(self, image=self.two_photo, height=48, width=48, state="disabled",
                                     fg_color="#353535", text="")
        self.two_icon.grid(column=0, row=0, padx=(12, 460), pady=(20, 0))

        self.image_button = tk.CTkButton(self, image=self.wb_image, height=780, width=500, state="disabled",
                                         fg_color="#353535", text="")
        self.image_button.grid(column=0, row=1, pady=(20, 20))
