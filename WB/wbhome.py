import customtkinter as tk
from WB.Cessna152.cessna152 import C152
from WB.Cessna172.cessna172 import C172
from WB.Cessna72R.cessna72r import C72R
from WB.Cessna310.cessna310 import C310
from WB.Cessna182.cessna182 import C182
tk.set_appearance_mode("dark")


# Identical to homepage, launch functions work with main in same way.


class WBHome(tk.CTkToplevel):
    def __init__(self, launch_page, close_app, root, home):
        super().__init__()
        self.root = root
        self.home = home  # goes to main menu page
        self.launch_page = launch_page
        self.close_app = close_app
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.title("WBPro")
        self.geometry("450x680")
        self.configure(fg_color="#353535")
        self.font = tk.CTkFont(family="ebrima", size=18)
        self.loop_count = 0

        # below are each item on the screen. Functions are lambda to prevent execution on launch of toplevel.
        self.welcome_label = tk.CTkLabel(self, text="Welcome! \nSelect an aircraft or option:", font=self.font)
        self.welcome_label.grid(column=0, row=0, padx=50, pady=(35, 20))

        self.c152_btn = tk.CTkButton(self, text="Cessna 152", font=self.font, height=50, width=350,
                                     command=lambda x="152": self.launch(x), fg_color="#3EA216")
        self.c152_btn.grid(column=0, row=1, padx=50, pady=20)

        self.c172_btn = tk.CTkButton(self, text="Cessna 172", font=self.font, height=50, width=350,
                                     command=lambda x="172": self.launch(x), fg_color="#3EA216")
        self.c172_btn.grid(column=0, row=2, padx=50, pady=20)

        self.c72r_btn = tk.CTkButton(self, text="Cessna 172RG", font=self.font, height=50, width=350,
                                     command=lambda x="RG": self.launch(x), fg_color="#3EA216")
        self.c72r_btn.grid(column=0, row=3, padx=50, pady=20)

        self.c182_btn = tk.CTkButton(self, text="Cessna 182", font=self.font, height=50, width=350,
                                     command=lambda x="182": self.launch(x), fg_color="#3EA216")
        self.c182_btn.grid(column=0, row=4, padx=50, pady=20)

        self.c310_btn = tk.CTkButton(self, text="Cessna 310", font=self.font, height=50, width=350,
                                     command=lambda x="310": self.launch(x), fg_color="#3EA216")
        self.c310_btn.grid(column=0, row=5, padx=50, pady=20)

        self.back_btn = tk.CTkButton(self, text="Go Back", font=self.font, height=50,
                                     width=350, fg_color="#3EA216", command=lambda x="Home": self.launch(x))
        self.back_btn.grid(column=0, row=6, padx=50, pady=20)

    def launch(self, plane):
        if plane == "152":
            self.launch_page(C152)
        elif plane == "172":
            self.launch_page(C172)
        elif plane == "RG":
            self.launch_page(C72R)
        elif plane == "Home":
            self.home()
        elif plane == "310":
            self.launch_page(C310)
        elif plane == "182":
            self.launch_page(C182)
