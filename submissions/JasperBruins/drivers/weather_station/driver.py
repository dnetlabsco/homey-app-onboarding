from homey.driver import Driver, ListDeviceProperties


class MyDriver(Driver):
    async def on_init(self):
        await super().on_init()
        self.log("Initialized MyDriver")

        card = self.homey.flow.get_device_trigger_card("weather_changed")
        
        async def on_run_listener(args, state):
            return args.get("mode") == state.get("mode")
        card.register_run_listener(on_run_listener)
    async def on_pair_list_devices(self, view_data):
        device: ListDeviceProperties = {
            "store": {
                "address": "127.0.0.1",
            },
            "name": "My Device",
            "data": {"id": "my-device"},
        }
        return [device]


homey_export = MyDriver
