import asyncio

from streifenstecker.communication.serialConnection import MessboxConnectionHandler
from streifenstecker.communication.modbusCommunication import ModbusConnectionHandler
from streifenstecker.logging.mortielogger import MortieLogger

#serConn = MessboxConnectionHandler()
#conf_path =  os.path.join(os.path.join(os.path.dirname(__file__), "..", ".."), "config", "serial_config.yaml")
#config = yaml.safe_load(open(conf_path))

sps = ModbusConnectionHandler(
    logger=MortieLogger(name="SPS_Connection"),
)
messboxen = MessboxConnectionHandler(
    logger=MortieLogger(name="Messboxen_Connection"),
)
async def open_connections():

    await sps.connect()



async def mainloop():

    #advance_foil()
    #stick_probes()
    #get_measurements()
    #remove_probes()




if __name__ == "__main__":
    asyncio.run(
        mainloop(),
        debug=True)

