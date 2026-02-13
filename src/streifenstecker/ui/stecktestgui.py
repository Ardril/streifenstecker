import customtkinter as ctk
from customtkinter import ThemeManager
ctk.set_appearance_mode("system")

BG_GREY = "#B1AAAA"

class SteckerApp(ctk.CTk):

    state_color = {
        "Ready":"#93FF8A",
        "Working":"#FBFF8A",
        "Error":"#FF0000",
        "FoilEmpty":"#8E8AFF",
    }

    def __init__(self):
        super().__init__()
        self.geometry("1500x600")
        self.title("Streifenstecker XS")
        
        self.grid_columnconfigure([0,1,2,3,4,5,8],weight=1)
        self.rowconfigure(8,weight=1)
        # Row 1
        # --- --- ---  --- --- ---  --- --- ---  --- --- --- --- --- ---  --- --- ---  --- --- ---  --- --- ---
        self.meas1 = ctk.StringVar(value="0")
        self.measField1 = ctk.CTkLabel(self, textvariable=self.meas1, bg_color=BG_GREY)
        self.measLabel1 = ctk.CTkLabel(self, text="Kontakt 1")

        self.meas2 = ctk.StringVar(value="1")
        self.measField2 = ctk.CTkLabel(self, textvariable=self.meas2, bg_color=BG_GREY)
        self.measLabel2 = ctk.CTkLabel(self, text="Kontakt 2")

        self.meas3 = ctk.StringVar(value="2")
        self.measField3 = ctk.CTkLabel(self, textvariable=self.meas3, bg_color=BG_GREY)
        self.measLabel3 = ctk.CTkLabel(self, text="Kontakt 3")

        # Row 2
        # --- --- ---  --- --- ---  --- --- ---  --- --- --- --- --- ---  --- --- ---  --- --- ---  --- --- ---

        self.meas4 = ctk.StringVar(value="3")
        self.measField4 = ctk.CTkLabel(self, textvariable=self.meas4, bg_color=BG_GREY)
        self.measLabel4 = ctk.CTkLabel(self, text="Kontakt 4")

        self.meas5 = ctk.StringVar(value="4")
        self.measField5 = ctk.CTkLabel(self, textvariable=self.meas5, bg_color=BG_GREY)
        self.measLabel5 = ctk.CTkLabel(self, text="Kontakt 5")

        self.meas6 = ctk.StringVar(value="5")
        self.measField6 = ctk.CTkLabel(self, textvariable=self.meas6, bg_color=BG_GREY)
        self.measLabel6 = ctk.CTkLabel(self, text="Kontakt 6")

        # Row 3
        # --- --- ---  --- --- ---  --- --- ---  --- --- --- --- --- ---  --- --- ---  --- --- ---  --- --- ---

        self.meas7 = ctk.StringVar(value="6")
        self.measField7 = ctk.CTkLabel(self, textvariable=self.meas7, bg_color=BG_GREY)
        self.measLabel7 = ctk.CTkLabel(self, text="Kontakt 7")

        self.meas8 = ctk.StringVar(value="7")
        self.measField8 = ctk.CTkLabel(self, textvariable=self.meas8, bg_color=BG_GREY)
        self.measLabel8 = ctk.CTkLabel(self, text="Kontakt 8")

        self.meas9 = ctk.StringVar(value="8")
        self.measField9 = ctk.CTkLabel(self, textvariable=self.meas9, bg_color=BG_GREY)
        self.measLabel9 = ctk.CTkLabel(self, text="Kontakt 9")

        # --- --- ---  --- --- ---  --- --- ---  --- --- --- --- --- ---  --- --- ---  --- --- ---  --- --- ---

        self.mTime = ctk.StringVar(value="8")
        self.timeField = ctk.CTkLabel(self, textvariable=self.mTime, bg_color="#EDDADA",text_color="#000000")
        self.timeLabel = ctk.CTkLabel(self, text="Messungsdauer")

        self.sys_state = ctk.StringVar(value="Working")
        self.stateField = ctk.CTkLabel(self, textvariable=self.sys_state, bg_color=BG_GREY,text_color="#000000")
        self.timeLabel = ctk.CTkLabel(self, text="Zustand")

        self.measField1.grid(row=2, column=0, padx=20, sticky="ew")
        self.measLabel1.grid(row=1, column=0, padx=20, sticky="ew")

        self.measField2.grid(row=2, column=1, padx=20, sticky="ew")
        self.measLabel2.grid(row=1, column=1, padx=20, sticky="ew")

        self.measField3.grid(row=2, column=2, padx=20, sticky="ew")
        self.measLabel3.grid(row=1, column=2, padx=20, sticky="ew")


        self.measField4.grid(row=4, column=0, padx=20, sticky="ew")
        self.measLabel4.grid(row=3, column=0, padx=20, sticky="ew")

        self.measField5.grid(row=4, column=1, padx=20, sticky="ew")
        self.measLabel5.grid(row=3, column=1, padx=20, sticky="ew")

        self.measField6.grid(row=4, column=2, padx=20, sticky="ew")
        self.measLabel6.grid(row=3, column=2, padx=20, sticky="ew")


        self.measField7.grid(row=6, column=0, padx=20, sticky="ew")
        self.measLabel7.grid(row=5, column=0, padx=20, sticky="ew")

        self.measField8.grid(row=6, column=1, padx=20, sticky="ew")
        self.measLabel8.grid(row=5, column=1, padx=20, sticky="ew")

        self.measField9.grid(row=6, column=2, padx=20, sticky="ew")
        self.measLabel9.grid(row=5, column=2, padx=20, sticky="ew")

        self.timeField.grid(row=8, column=0, pady=15, padx=20, sticky="ew")
        self.stateField.grid(row=8, column=2, pady=15, padx=20, sticky="ew")

    def update_measurement_fields(self,measurements):

        self.meas1.set(measurements["contact1"])
        self.meas2.set(measurements["contact1"])
        self.meas3.set(measurements["contact1"])
        self.meas4.set(measurements["contact1"])
        self.meas5.set(measurements["contact1"])
        self.meas6.set(measurements["contact1"])
        self.meas7.set(measurements["contact1"])
        self.meas8.set(measurements["contact1"])
        self.meas9.set(measurements["contact1"])

        self.mTime.set(measurements["time"])

    def update_state_display(self,state):
        if state not in self.state_color.keys():
            return -1
        color = self.state_color[state]
        self.stateField.configure(bg_color=color)
        self.sys_state.set(state)
        return 1

if __name__ == "__main__":
    app = SteckerApp()
    app.mainloop()