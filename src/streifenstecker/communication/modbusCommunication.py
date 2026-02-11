import asyncio
import time

from pymodbus.client import AsyncModbusTcpClient as ModbusClient


coil_addresses ={
    "Folie_Ready": 1001,
    "Folie_Error": 1002,
    "Folie_Ende": 1003,
    "Steck_Ready": 2001,
    "Steck_Error": 2002,
    "Foerderer_Alive": 3001,
    "Foerderer_Ready": 3002,
    "Stecker_Ready":  3003,
    "Folie_Request": 101,
    "Steck_Request": 201,
    "Steck_Disconnect_Request": 301
}

class ModbusConnectionHandler:

    client:ModbusClient
    def __init__(self,logger,host=None,port=5020):
        self.logger = logger
        self.host = "127.0.0.1" if not host else host
        self.port = port

    async def connect(self):
        self.client = ModbusClient(
            host=self.host,
            port=self.port,
            timeout=10,
        )

        await self.client.connect()

    async def disconnect(self):
        self.client.close()

    async def read_coils(self,address,count):
        return await self.client.read_coils(address=address,count=count)

    async def write_coil(self,address,value):
        return await self.client.write_coil(address=address-1,value=value)

    async def advance_foil(self):
        await self.write_coil(address=coil_addresses["Folie_Request"],value=1)
        start_time = time.time()
        while time.time() - start_time < 5:
            response = await self.read_coils(address=coil_addresses["Folie_Ready"],count=1)
            if response.bits[0]:
                return 1
            time.sleep(0.1)
        return -1

    async def connect_probes(self):
        await self.write_coil(address=coil_addresses["Steck_Request"], value=1)
        start_time = time.time()
        while time.time() - start_time < 5:
            response = await self.read_coils(address=coil_addresses["Stecker_Ready"], count=1)
            if response.bits[0]:
                return 1
            time.sleep(0.1)
        return -1

    async def disconnect_probes(self):
        await self.write_coil(address=coil_addresses["Steck_Disconnect_Request"], value=1)
        start_time = time.time()
        while time.time() - start_time < 5:
            response = await self.read_coils(address=coil_addresses["Stecker_Ready"], count=1)
            if response.bits[0]:
                return 1
            time.sleep(0.1)
        return -1