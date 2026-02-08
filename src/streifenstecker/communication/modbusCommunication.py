from pymodbus.client import AsyncModbusTcpClient as ModbusClient


class ModbusConnectionHandler:

    client:ModbusClient
    def __init__(self,host=None,port=5020):
        self.client = ModbusClient(
            host="127.0.0.1" if host is None else host,
            port=port,
            timeout=10,
        )
    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        self.client.close()

    async def read_coils(self,address,count):
        return await self.client.read_coils(address=address,count=count)

    async def write_coil(self,address,value):
        return await self.client.write_coil(address=address-1,value=value)

