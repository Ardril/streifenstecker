import time
from argparse import ArgumentError
import serial




class MessboxConnectionHandler():

    
    def __init__(self,ports,logger):
        if len(ports) > 2 or len(ports) < 1:
            raise ArgumentError("2 Ports for the Messboxen must be supplied")

        self.serCon1 = serial.Serial()
        self.serCon2 = serial.Serial()
        
        self.serCon1.port = ports[0]
        self.serCon2.port = ports[1]
        self.serCon1.open()
        self.serCon2.open()
        
             
    def get_measurements(self):
        retval = {
            "con1":"",
            "con2":"",
        }
        self.serCon1.write(b"T")
        time.sleep(0.2)
        response = str(self.serCon1.readline())
        retval["con1"] = response.replace(".",",")

        self.serCon2.write(b"T")
        time.sleep(0.2)
        response = str(self.serCon2.readline())
        retval["con2"] = response.replace(".", ",")

        return retval



