from customtkinter import CTkFrame,StringVar,CTkLabel

class SplitFrame(CTkFrame):

    def __init__(self,master,text_in="EMPTY",child_bg_color="#0f0f0f",labeltext="Test"):
        super().__init__(master=master)
        val_list = text_in.split(" ")
        self.meas1 = StringVar(value=val_list[0])
        self.meas2 = StringVar(value=val_list[1])
        self.meas3 = StringVar(value=val_list[2])
        self.meas4 = StringVar(value=val_list[3])

        self.measField1_1 = CTkLabel(self, textvariable=self.meas1, bg_color=child_bg_color,text_color="#000000")
        self.measField1_2 = CTkLabel(self, textvariable=self.meas2, bg_color=child_bg_color,text_color="#000000")
        self.measField1_3 = CTkLabel(self, textvariable=self.meas3, bg_color=child_bg_color,text_color="#000000")
        self.measField1_4 = CTkLabel(self, textvariable=self.meas4, bg_color=child_bg_color,text_color="#000000")
        self.label = CTkLabel(self,text=labeltext)

        self.grid_columnconfigure([0,1,2,3],weight=1)

        self.label.grid(column=0, columnspan=4,row=0)
        self.measField1_1.grid(column=0, row=1, padx=5, sticky="ew")
        self.measField1_2.grid(column=1, row=1, padx=5, sticky="ew")
        self.measField1_3.grid(column=2, row=1, padx=5, sticky="ew")
        self.measField1_4.grid(column=3, row=1, padx=5, sticky="ew")

    def update_children(self, val_list):
        if len(val_list) < 4 or len(val_list) > 5:
            raise AttributeError("val_list must be 4 items long")

        self.meas1.set(value=val_list[0])
        self.meas2.set(value=val_list[1])
        self.meas3.set(value=val_list[2])
        self.meas4.set(value=val_list[3])


