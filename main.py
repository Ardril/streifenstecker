import asyncio
import time
import threading
from streifenstecker.ui.stecktestgui import SteckerApp
from streifenstecker.communication.serialConnection import MessboxConnectionHandler
from streifenstecker.communication.modbusCommunication import ModbusConnectionHandler
from streifenstecker.logging.mortielogger import MortieLogger


log_entry = {
    "timestamp":0,
    "box1":{},
    "box2":{}
}



app = SteckerApp()

sps = ModbusConnectionHandler(
    logger=MortieLogger(name="SPS_Connection",tofile=True),
)
mb1 = MessboxConnectionHandler(
    port="COM7",
    logger=MortieLogger(name="MB_Connection1",tofile=True),
)
mb2 = MessboxConnectionHandler(
    port="COM6",
    logger=MortieLogger(name="MB_Connection2",tofile=True),
)
async def open_connections():

    await sps.connect()


async def meas_by_type(meas_type:str,times):

    if not sps.client.connected:
        raise AttributeError("SPS is not connected!")

    match meas_type:

        case "n":   #normal
            await sps.advance_foil()
            await sps.connect_probes()
            mb1.get_measurements()
            mb2.get_measurements()
            await sps.disconnect_probes()

        case "r":   #repeat
            if not times > 0:
                raise AttributeError("The number of repeats can't be 0 when using 'repeat' measurement type")

            for i in range(times):
                await sps.advance_foil()
                await sps.connect_probes()
                mb1.get_measurements()
                mb2.get_measurements()
                await sps.disconnect_probes()

        case "s":   #short to ground

            await sps.disconnect_probes()
            mb1.get_measurements()
            mb2.get_measurements()

async def mainloop(logger):

    app.update_state_display("Ready")
    mb1.open_connection()
    await open_connections()

    for i in range(12):
        app.update_state_display("Working")
        ret = await sps.advance_foil()
        if ret != 1:
            if ret == 10:
                logger.warning("An error occurred while advancing the foil")
            elif ret == 0:
                logger.warning("Foil is empty")
                app.update_state_display("FoilEmpty")
                app.request_foil_change()
                while not app.get_foil_state():
                    time.sleep(0.5)


        if await sps.connect_probes() > 0:
            measurements = mb1.get_measurements()
            app.update_measurement_fields(measurements)
            logger.info(f"{measurements}")
    #advance_foil()
    #stick_probes()
    #get_measurements()
    #remove_probes()


def sim_util():
    from tests import modbus_server_simulator
    mbss = modbus_server_simulator.ModbusServerSimulator()
    asyncio.run(mbss.async_helper(), debug=False)



if __name__ == "__main__":
    sim_thread = threading.Thread(target=sim_util)
    sim_thread.start()


    def run_manager():
        _logger = MortieLogger(name="Main", tofile=True)
        asyncio.run(mainloop(_logger), debug=False)

    core_thread = threading.Thread(target=run_manager)
    core_thread.start()


    app.mainloop()
    print("APP CLOSED")
    core_thread.join()
    sim_thread.join()
