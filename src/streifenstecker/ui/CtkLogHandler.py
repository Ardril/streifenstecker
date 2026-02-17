import logging
import customtkinter as ctk

class CtkLogHandler(logging.Handler):
    def __init__(self,text_widget:ctk.CTkTextbox):
        super().__init__()
        self.text_widget = text_widget
        self.setFormatter(logging.Formatter(
                "{asctime} - {levelname} - {funcName} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M",
        ))

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg + "\n", tags=record.levelname)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

        self.text_widget.after(0, append)