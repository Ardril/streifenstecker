import logging
import datetime
import os

class MortieLogger(logging.Logger):

    def __init__(self, name="Mortie2", tofile=False):
        super().__init__(name)
        date_time_tuple = datetime.datetime.now().isoformat(timespec='seconds').replace("-", "_").replace(":", "_").split("T")
        if tofile and not os.path.exists(f"./logs/{date_time_tuple[0]}"):
            os.makedirs(f"./logs/{date_time_tuple[0]}")

        log_to_console = logging.StreamHandler()
        log_to_console.setLevel("INFO")
        self.addHandler(log_to_console)
        log_to_console.setFormatter(logging.Formatter(
                "{asctime} - {levelname} - {funcName} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M",
        ))

        if tofile:
            filepath = f"./logs/{date_time_tuple[0]}/{date_time_tuple[1]}_{name}.txt"
            try:
                open(filepath,"x").close()
            except FileExistsError:
                pass

            log_to_logfile = logging.FileHandler(filepath, encoding="utf-8-sig")
            log_to_logfile.setLevel("DEBUG")
            log_to_logfile.setFormatter(logging.Formatter(
                "{asctime} - {levelname} - {funcName} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M",
            ))
            self.addHandler(log_to_logfile)
            self.warning("Hello")
