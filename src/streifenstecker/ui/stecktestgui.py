import logging

import customtkinter as ctk
from streifenstecker.ui.CtkLogHandler import CtkLogHandler
from streifenstecker.ui.ProbeBoxFrame import ProbeBoxFrame
ctk.set_appearance_mode("system")

BG_GREY = "#B1AAAA"


class SteckerApp(ctk.CTk):

    state_color = {
        "Ready":    "#93FF8A",
        "Working":  "#FBFF8A",
        "Error":    "#FF0000",
        "FoilEmpty":"#8E8AFF",
    }

    def __init__(self):
        super().__init__()
        self.foil_state = True
        self.geometry("1900x1000")
        self.title("Streifenstecker XS")
        self.resizable(False,False)

        self.grid_columnconfigure([0,1,2],weight=1)
        self.rowconfigure([8,9,10],weight=1)

        # --- --- ---  --- --- ---  Widget Definition --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        self.box1Frame = ProbeBoxFrame(self,"Box1")
        self.box2Frame = ProbeBoxFrame(self,"Box2")
        self.foilBtn = ctk.CTkButton(self, text="Folie getauscht", state="disabled", command=self.button_callback)


        # --- --- ---  --- --- ---  --- --- ---  --- --- --- --- --- ---  --- --- ---  --- --- ---  --- --- ---

        self.targetCycles = ctk.IntVar(value=600)
        self.currentCycles = ctk.IntVar(value=0)

        self.targetCyclesFrame = ctk.CTkFrame(self)
        self.targetCyclesField = ctk.CTkLabel( self.targetCyclesFrame, textvariable=self.targetCycles)
        self.targetCyclesLabel = ctk.CTkLabel( self.targetCyclesFrame,text="Soll-Zyklen:")
        self.currentCyclesFrame = ctk.CTkFrame(self)
        self.currentCyclesField = ctk.CTkLabel(self.currentCyclesFrame, textvariable=self.currentCycles)
        self.currentCyclesLabel = ctk.CTkLabel(self.currentCyclesFrame,text="Ist-Zyklen:")

        self.mTime = ctk.StringVar(value="8")
        self.timeField = ctk.CTkLabel(self, textvariable=self.mTime, bg_color="#EDDADA",text_color="#000000")
        self.timeLabel = ctk.CTkLabel(self, text="Messungsdauer")

        self.sys_state = ctk.StringVar(value="Working")
        self.stateField = ctk.CTkLabel(self, textvariable=self.sys_state, bg_color=BG_GREY,text_color="#000000")
        self.stateLabel = ctk.CTkLabel(self, text="Zustand")

        self.logField = ctk.CTkTextbox(self)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(CtkLogHandler(self.logField))
        self.logger.info("UI logger up and running")
        self.logField.tag_config("WARNING", foreground="yellow")
        self.logField.tag_config("INFO", foreground="white")
        self.logField.tag_config("ERROR", foreground="red")

        # --- --- ---  --- --- ---  UI Layout --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


        self.box1Frame.grid(column=0, columnspan=3, row=0, rowspan=6, pady=5, padx=5, sticky="new")
        self.box2Frame.grid(column=0, columnspan=3, row=7, rowspan=6, pady=5, padx=5, sticky="new")

        self.currentCyclesFrame.grid(row=11, column=0, padx=20,sticky="ew")
        self.targetCyclesFrame.grid(row=12, column=0, padx=20,sticky="ew")

        self.targetCyclesField.grid(row=0,column=1,padx=5,sticky="e")
        self.targetCyclesLabel.grid(row=0,column=0,padx=5,sticky="w")

        self.currentCyclesField.grid(row=0,column=1,padx=5,sticky="e")
        self.currentCyclesLabel.grid(row=0,column=0,padx=5,sticky="w")



        self.logField.grid(row=15, column=0, columnspan=3, pady=15, sticky="nesw")
        self.foilBtn.grid(row=14, column=2, pady=5, padx=5, sticky="ew")

        self.timeLabel.grid(row=13, column=0, pady=5, padx=20, sticky="ew")
        self.timeField.grid(row=14, column=0, pady=5, padx=20, sticky="ew")

        self.stateLabel.grid(row=13, column=1, pady=5, padx=20, sticky="ew")
        self.stateField.grid(row=14, column=1, pady=5, padx=20, sticky="ew")



    def update_measurement_fields(self,measurements1,measurements2):
        self.after(15, self.box1Frame.update_measurement_fields,measurements1)
        self.after(15, self.box2Frame.update_measurement_fields, measurements2)
        self.mTime.set(measurements1["time"])

    def update_state_display(self,state):
        if state not in self.state_color.keys():
            return -1
        color = self.state_color[state]
        self.stateField.configure(bg_color=color)
        self.sys_state.set(state)
        return 1

    def get_foil_state(self):
        return self.foil_state

    def update_cycle_count(self,value):
        self.after(20,self.currentCycles.set,value)



    def log_to_output(self,text) -> None:
        self.logger.info(text)

    def request_foil_change(self):
        self.foil_state = False
        self.foilBtn.configure(state="normal")
        self.logger.warning("Die Folie ist leer. Bitte die Folienrolle tauschen und dann mit dem Schalter bestätigen")
        return

    def button_callback(self):
        self.foil_state = True
        self.foilBtn.configure(state="disabled")
        self.logger.info("Folie getauscht. Der Zyklus wird weiter durchgeführt")

if __name__ == "__main__":
    app = SteckerApp()
    app.mainloop()