
from streifenstecker.communication.serialConnection import MessboxConnectionHandler
import mock_serial


try: 
    serial = MessboxConnectionHandler("COM3")
    values = serial.getMeasurements()
    if str(values) == "5.29 4.82 5.02 4.77 4.53 5.14 4.93 4.87 7.01":
        print("Passed")
except:
    print("Exception occurred")

