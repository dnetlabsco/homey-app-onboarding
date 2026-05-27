from homey.app import App


class MyApp(App):
    async def on_init(self):
        await super().on_init()
        self.register_flow_cards()

    def register_flow_cards(self):
        flow = self.homey.flow
        
        #run listener handles the given methods
        flow.get_action_card('set-weather-mode').register_run_listener(self.set_mode)
        flow.get_condition_card('is-it-raining').register_run_listener(self.is_raining)
        flow.get_device_trigger_card('weather-changed').register_run_listener(self.weather_changed)

    async def set_mode(self, args, **kwargs):
        await args['device'].set_capability_value('mode', args['mode'])
        return True

    async def is_raining(self, args, **kwargs):
        return args['device'].get_capability_value('mode') == 'rainy'

    async def weather_changed(self, args, **kwargs):
        return args['mode'] == kwargs.get('mode')


homey_export = MyApp