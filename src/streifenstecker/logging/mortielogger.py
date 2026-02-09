import logging
import datetime

class MortieLogger(logging.Logger):

    def __init__(self, name="Mortie2", tofile=False):

        super().__init__(name)
        log_to_console = logging.StreamHandler()
        log_to_console.setLevel("INFO")
        if not tofile:
            self.addHandler(log_to_console)
            log_to_console.setFormatter(logging.Formatter(
                "{asctime} - {levelname} - {filename} -{funcName} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M",
            ))
        else:
            log_to_logfile = logging.FileHandler("errorlog.txt", encoding="utf-8-sig")
            log_to_logfile.setLevel("DEBUG")
            log_to_logfile.setFormatter(logging.Formatter(
                "{asctime} - {levelname} - {filename} -{funcName} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M",
            ))
            self.addHandler(log_to_logfile)


