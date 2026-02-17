import asyncio
import threading
from streifenstecker.communication.serialConnection import MessboxConnectionHandler
from streifenstecker.communication.modbusCommunication import ModbusConnectionHandler
from streifenstecker.logging.mortielogger import MortieLogger
from streifenstecker.ui.stecktestgui import SteckerApp


class WorkflowManager:

    sps:ModbusConnectionHandler
    mb1:MessboxConnectionHandler
    mb2:MessboxConnectionHandler
    logger:MortieLogger
    ui:SteckerApp

    def __init__(self,mess_before_repeat,repeat_count,stg_after_x, ui=False):
        self.logger = MortieLogger("WorkFlowManager",True)

        # --- --- --- --- --- --- --- --- --- --- ---
        self.sps = ModbusConnectionHandler(
            logger=MortieLogger(name="SPS_Connection", tofile=True),
        )
        self.mb1 = MessboxConnectionHandler(
            port="COM7",
            logger=MortieLogger(name="MB_Connection1", tofile=True),
        )
        self.mb2 = MessboxConnectionHandler(
            port="COM3",
            logger=MortieLogger(name="MB_Connection2", tofile=True),
        )
        if ui:
            self.ui = SteckerApp()
        # --- --- --- --- --- --- --- --- --- --- ---
        self.measurements_before_repeat = mess_before_repeat
        self.repeat_per_repeat_measurement = repeat_count
        self.short_measurement_after_x = stg_after_x
        self.cycle_n = 1

    async def open_connections(self):

        self.logger.info("Opening connection to messbox 1")
        if self.mb1.open_connection() < 0 :
            self.logger.error("The connection to messbox 1 is closed")
            return -1
        self.logger.info("Messbox 1 opened")

        self.logger.info("Opening connection to messbox 2")
        if self.mb2.open_connection() < 0 :
            self.logger.error("The connection to messbox 2 is closed")
            return -1
        self.logger.info("Messbox 2 opened")

        self.logger.info("Opening modbus connection")
        await self.sps.connect()
        return 0

    async def meas_by_type(self,meas_type: str, times=0):

        # Todo Werte loggen !


        if not self.sps.client.connected:
            raise AttributeError("SPS is not connected!")

        if not self.mb1.is_open():
            raise AttributeError("MB1 is not open!")
        if not self.mb2.is_open():
            raise AttributeError("MB2 is not open!")

        meas1 = 0
        meas2 = 0

        match meas_type:

            case "n":  # normal
                ret = await self.sps.advance_foil()

                await self.sps.connect_probes()
                meas1 = self.mb1.get_measurements()
                meas2 = self.mb2.get_measurements()
                self.ui.update_measurement_fields(
                    measurements1=meas1,
                    measurements2=meas2,
                )
                await self.sps.disconnect_probes()
                self.cycle_n += 1

            case "r":  # repeat
                if not times > 0:
                    raise AttributeError("The number of repeats can't be 0 when using 'repeat' measurement type")

                for i in range(times):
                    await self.sps.connect_probes()
                    meas1 = self.mb1.get_measurements()
                    meas2 = self.mb2.get_measurements()
                    self.ui.update_measurement_fields(
                        measurements1=meas1,
                        measurements2=meas2,
                    )
                    await self.sps.disconnect_probes()
                    self.cycle_n += 1

            case "s":  # short to ground

                await self.sps.disconnect_probes()
                meas1 = self.mb1.get_measurements()
                meas2 = self.mb2.get_measurements()
                self.ui.update_measurement_fields(
                    measurements1=meas1,
                    measurements2=meas2,
                )
                self.cycle_n += 1

        print(self.cycle_n)
        self.ui.update_cycle_count(self.cycle_n)

    async def mainloop(self):
        if await self.open_connections() == 0:
            while True:
                if self.cycle_n % self.measurements_before_repeat == 0:
                    # Trigger repeat
                    self.logger.info(f"Performing {self.repeat_per_repeat_measurement} repeat measurements")
                    await self.meas_by_type("r",self.repeat_per_repeat_measurement)

                elif self.cycle_n % self.short_measurement_after_x == 0:
                    # Trigger short_to_ground
                    self.logger.info("Performing short_to_ground measurement")
                    await self.meas_by_type("s")

                else:
                    self.logger.info("Performing normal measurement")
                    await self.meas_by_type("n")



if __name__ == "__main__":

    def sim_util():
        from tests import modbus_server_simulator
        mbss = modbus_server_simulator.ModbusServerSimulator()
        asyncio.run(mbss.async_helper(), debug=False)

    sim_thread = threading.Thread(target=sim_util)
    sim_thread.start()
    wfm = WorkflowManager(
        mess_before_repeat=7,
        repeat_count=3,
        stg_after_x=10,
        ui = True
    )
    def run_manager():
        asyncio.run(wfm.mainloop())


    core_thread = threading.Thread(target=run_manager)
    core_thread.start()

    wfm.ui.mainloop()