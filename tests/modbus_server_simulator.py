from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock,ModbusDeviceContext,ModbusServerContext
from argparse import Namespace
from pymodbus import ModbusDeviceIdentification
import asyncio
import time

#------------------------------ Coils ------------------------------
# Folie_Ready 1001  
# Folie_Error 1002
# Folie_Ende  1003
#
# Steck_Ready 2001
# Steck_Error 2002
#
# ------------------------------ Discrete Inputs ------------------------------
# Förderer_Alive 3001
# Förderer_Ready 3002
# Stecker_Ready  3003
#
# ------------------------------ Request From Client ------------------------------
# 
# Folie_Request 101
# Steck_Request 201
# Steck_Lösung_Request 301
#
#

class CallbackModbusSequentialDataBlock(ModbusSequentialDataBlock):
    """
    A custom overload of the ModbusSequentialDataBlock to allow for callback functions to be executed when values change within the datablock
    """
    def __init__(self, address, values, callback):
        super().__init__(address, values)
        self.callback = callback

    def setValues(self, address, values):
        super().setValues(address, values)
        print(f"Change at {address} with values {values}")
        self.callback(self,address, values)

def on_change(datablock:CallbackModbusSequentialDataBlock,address, values):
    # Main behavior method of the server

    if address == 101 and values[0]:
        # Folie_Request; Set Folie Ready to False
        datablock.setValues(3002,[0])
        print("Moving foil")
        # Wait 5 sec to simulate foil movement; Set Ready to True
        time.sleep(5)
        print("Foil ready")
        datablock.setValues(3002,[1])

    elif address == 201 and values[0]:
        # Steck_Request; Set Steck Ready to False
        datablock.setValues(2001,[0])
        print("Moving probes")
        # Wait 3 sec to simulate stecker movement; Set Ready to True
        time.sleep(3)
        print("Probes connected")
        datablock.setValues(2001,[1])

    elif address == 301 and values[0]:
        # Steck_Loesungs_Request
        datablock.setValues(2001,[0])
        print("Moving probes")
        # Wait 3 sec to simulate stecker movement; Set Ready to True
        time.sleep(3)
        print("Probes disconnected")
        datablock.setValues(2001,[1])
    
    return

class ModbusServerSimulator:


    def setup_server(self):
        """Run server setup."""
        
        args = Namespace(host="127.0.0.1",port=502,framer="socket")

        callback_datablock = lambda : CallbackModbusSequentialDataBlock(0x00, [17] * 100, on_change)  
                
        context = ModbusDeviceContext(
                    di=callback_datablock(), 
                    co=callback_datablock(), 
                    hr=callback_datablock(), 
                    ir=callback_datablock()
                )
        
        ## Set ready and alive coils to true



        context.setValues(1,1001,[1])   # Folie_Ready
        context.setValues(1,1002,[0])   # Folie_Error
        context.setValues(1,1003,[0])   # Folie_Ende

        context.setValues(1,2001,[1])   # Steck_Ready
        context.setValues(1,2002,[0])   # Steck_Error

        context.setValues(1,3001,[1])   # Förderer_Alive
        context.setValues(1,3002,[1])   # Förderer_Ready
        context.setValues(1,3003,[1])   # Stecker_Ready

        single = True

        # Build data storage
        args.context = ModbusServerContext(devices=context, single=single)

        args.identity = ModbusDeviceIdentification(
            info_name={"VendorName": "Pymodbus","ProductCode": "PM","VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
                "ProductName": "Pymodbus Server","ModelName": "Pymodbus Server",
            }
        )
        return args
    

    async def run_async_server(self,args) -> None:
        """Run server."""
        
    
        await StartAsyncTcpServer(
                context=args.context,  
                identity=args.identity,  
                address=("",5020),
                # custom_functions=[],  # allow custom handling
                framer=args.framer,  # The framer strategy to use
                # ignore_missing_devices=True,  # ignore request to a missing device
                # broadcast_enable=False,  # treat device 0 as broadcast address,
                # timeout=1,  # waiting time for request to complete
        )
    


    async def async_helper(self) -> None:
        run_args = self.setup_server()
        await self.run_async_server(run_args)

if __name__ == "__main__":
    mbss = ModbusServerSimulator()
    print("Starting server...")
    asyncio.run(mbss.async_helper(), debug=False)