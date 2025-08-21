import customtkinter as tk
from WB.wbhome import WBHome
import os
import webbrowser

tk.set_appearance_mode("dark")

# This file is the main menu, with the options to click on. Options execute various commands.


class Homepage(tk.CTkToplevel):
    def __init__(self, launch_page, close_app, root, home):
        super().__init__()
        self.root = root
        self.launch_page = launch_page
        self.close_app = close_app
        self.protocol("WM_DELETE_WINDOW", self.close_app)  # top right x closes application, close_app in main.py
        self.title("WBPro")
        self.geometry("450x620")
        self.configure(fg_color="#353535")
        self.font = tk.CTkFont(family="ebrima", size=18)
        self.footer_font = tk.CTkFont(family="ebrima", size=16)
        self.loop_count = 0

        # below are each item on the screen. Functions are lambda to prevent execution on launch of toplevel.
        self.welcome_label = tk.CTkLabel(self, text="Welcome! \nSelect an option:", font=self.font)
        self.welcome_label.grid(column=0, row=0, padx=50, pady=(35, 20))

        self.wb_btn = tk.CTkButton(self, text="Weight and Balance", font=self.font, height=50, width=350,
                                   command=lambda x="WB": self.launch(x), fg_color="#3EA216")
        self.wb_btn.grid(column=0, row=1, padx=50, pady=20)

        self.itinerary_btn = tk.CTkButton(self, text="Flight Itinerary", font=self.font, height=50, width=350,
                                          command=lambda x="172": self.launch(x), fg_color="#606060")
        self.itinerary_btn.grid(column=0, row=2, padx=50, pady=20)

        self.ofp_v_btn = tk.CTkButton(self, text="VFR OFP", font=self.font, height=50, width=350,
                                      command=lambda x="RG": self.launch(x), fg_color="#606060")
        self.ofp_v_btn.grid(column=0, row=3, padx=50, pady=20)

        self.ofp_i_btn = tk.CTkButton(self, text="IFR OFP", font=self.font, height=50,
                                      width=350, fg_color="#606060")
        self.ofp_i_btn.grid(column=0, row=4, padx=50, pady=20)

        self.instructions_btn = tk.CTkButton(self, text="Instructions/Program Info", font=self.font, height=50,
                                             width=350, fg_color="#3EA216", command=lambda: self.open_html())
        self.instructions_btn.grid(column=0, row=5, padx=50, pady=20)

        self.footer = tk.CTkLabel(self, text="https://github.com/rosenbergsimon", font=self.footer_font,
                                  text_color="#A2A2A2")
        self.footer.grid(column=0, row=6, padx=50, pady=10)

    # uses str parameter from above func to open the appropriate toplevel window
    def launch(self, plane):
        if plane == "WB":
            self.launch_page(WBHome)

    # opens the instructions in the pc browser
    def open_html(self):
        file_path = "./information.html"
        webbrowser.open_new_tab(f"file://{os.path.realpath(file_path)}")
