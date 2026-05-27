from homey.driver import Driver, ListDeviceProperties
import uuid


class MyDriver(Driver):
    async def on_init(self):
        await super().on_init()
        self.log("MyDriver.on_init: start")

    async def on_pair_list_devices(self, view_data):
        device: ListDeviceProperties = {
            "name": "Weather Station",
            "data": {"id": str(uuid.uuid4())},
        }
        return [device]


homey_export = MyDriver