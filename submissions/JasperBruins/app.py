from homey.app import App


class MyApp(App):
    async def on_init(self):
        await super().on_init()
        self.log("Initialized MyApp")
        
        self.weather_changed_card = self.homey.flow.get_device_trigger_card("weather_changed")

        card = self.homey.flow.get_action_card("set_weather_mode")
        card.register_run_listener(self.set_weather_mode)

        condition_card = self.homey.flow.get_condition_card("is_it_raining")
        condition_card.register_run_listener(self.is_it_raining)
    async def is_it_raining(self, args):

        device = args["device"]

        current_mode = device.get_capability_value("mode")

        return current_mode == "rainy"
        
    async def set_weather_mode(self, args):
        device = args["device"]
        mode = args["mode"]
        await device.set_capability_value("mode", mode)
        self.log(f"Set weather mode to: {mode} for device: {device.name}")
        return True
        

        
homey_export = MyApp
