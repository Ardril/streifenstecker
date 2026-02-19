import time
from argparse import ArgumentError
import serial
from serial.tools.list_ports import comports


class MessboxConnectionHandler():

    
    def __init__(self,port,logger):
        for prt in comports():
            print(prt.device)
        self.serCon1 = serial.Serial()
        self.logger = logger
        self.serCon1.port = port

    def __del__(self):
        self.serCon1.close()

    def is_open(self):
        return self.serCon1.is_open

    def open_connection(self):
        try:
            self.serCon1.open()
            self.serCon1.write(b"a")
            #todo Remove this
            if ".ino" not in str(self.serCon1.readline()):
                self.logger.debug(f"Port {self.serCon1.port} opened, but the device is not a messbox")
                return -1
            self.serCon1.reset_input_buffer()
            self.serCon1.reset_output_buffer()
            self.logger.debug(f"Port {self.serCon1.port} opened")
            return 1
        except serial.SerialException as e:
            raise e
        
             
    def get_measurements(self):
        if not self.serCon1.is_open:
            return -1
        self.logger.debug("Measuring resistance...")
        self.serCon1.write(b"t")
        time.sleep(0.2)
        response = str(self.serCon1.readline()).replace("b","").replace("'","")
        self.logger.debug(f"Got {len(response.split("  "))-1} values")
        self.logger.debug(response)
        # b'1207.20 1216.12 1226.48 330.91
        # 1206.95 1216.12 1226.42 330.93
        # 1206.64 1215.99 1226.38 330.99
        # 1206.69 1216.00 1226.34 330.90
        # 1206.61 1215.98 1226.39 331.10
        # 1206.42 1215.94 1226.41 331.09
        # 1206.12 1215.93 1226.39 330.92
        # 1206.72 1216.01 1226.43 331.00
        # 1207.57 1216.33 1226.63 331.16
        # 0.559s\r\n'

        retval = {
            "contact1":response.split("  ")[0].split(" "),
            "contact2":response.split("  ")[1].split(" "),
            "contact3":response.split("  ")[2].split(" "),
            "contact4":response.split("  ")[3].split(" "),
            "contact5":response.split("  ")[4].split(" "),
            "contact6":response.split("  ")[5].split(" "),
            "contact7":response.split("  ")[6].split(" "),
            "contact8":response.split("  ")[7].split(" "),
            "contact9":response.split("  ")[8].split(" "),
            "time":    response.split("  ")[-1].replace("\\r","").replace("\\n","")

        }

        return retval



