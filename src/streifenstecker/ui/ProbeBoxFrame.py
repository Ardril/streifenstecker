from customtkinter import CTkFrame, CTkLabel
from streifenstecker.ui.SplitFrame import SplitFrame

class ProbeBoxFrame(CTkFrame):

    def __init__(self,master,title):
        super().__init__(master,border_width=3,border_color="#000000")
        self.fields: list[SplitFrame] = []
        self.grid_columnconfigure([0,1,2], weight=1)
        self.grid_rowconfigure([0,1,2],weight=1)
        self.label = CTkLabel(self,text=title)
        for i in range(9):
            self.fields.append(
                SplitFrame(
                    self,
                    text_in="1_1 1_2 1_3 1_4",
                    child_bg_color="#B1AAAA",
                    labeltext=f"Kontakt {i+1}"
                )
            )
        self.label.grid(row=0, column=1, pady=10, padx=10, sticky="new")
        index = 0
        for c in range(3):
            for r in range(3):
                field = self.fields[index]
                field.grid(row=c+1,column=r, padx=10, pady=10, sticky="ew")
                index += 1

    def update_measurement_fields(self, measurements:dict):
        for i in range(len(self.fields)):
            updated_val = measurements[f"contact{i+1}"]
            self.fields[i].update_children(updated_val)
