import asyncio

from streifenstecker.communication.serialConnection import MessboxConnectionHandler
from streifenstecker.communication.modbusCommunication import ModbusConnectionHandler


#serConn = MessboxConnectionHandler()
#conf_path =  os.path.join(os.path.join(os.path.dirname(__file__), "..", ".."), "config", "serial_config.yaml")
#config = yaml.safe_load(open(conf_path))

async def mainloop():

    #advance_foil()
    #stick_probes()
    #get_measurements()
    #remove_probes()
    modbusclient = ModbusConnectionHandler()
    await modbusclient.connect()
    response = await modbusclient.client.read_coils(address=3001,count=1)
    response = await modbusclient.write_coil(
        address=101,
        value=True)
    return response


if __name__ == "__main__":
    asyncio.run(
        mainloop(),
        debug=True)

