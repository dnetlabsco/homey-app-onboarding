from homey.device import Device
import asyncio
import random

SENSOR_INTERVAL = 10   # sensor updates
MODE_INTERVAL = 60     # weather mode changes
MODES = ['sunny', 'cloudy', 'rainy']


class MyDevice(Device):

    async def on_init(self):
        await super().on_init()

       
        self._trigger = self.homey.flow.get_device_trigger_card('weather-changed')

        self._tasks = [
            asyncio.ensure_future(self.sensor_loop()),
            asyncio.ensure_future(self.mmode_loop()),
        ]

    async def update_sensors(self):
        await self.set_capability_value('measure_temperature', round(random.uniform(15, 25), 1))
        await self.set_capability_value('measure_humidity', round(random.uniform(30, 70), 1))
        await self.set_capability_value('measure_pressure', round(random.uniform(1000, 1025), 1))

    async def update_mode(self):
        new_mode = random.choice(MODES)
        if new_mode == self.get_capability_value('mode'):
            return  

        await self.set_capability_value('mode', new_mode)
        #token
        temperature = self.get_capability_value('measure_temperature')
        await self._trigger.trigger(self, {'temperature': temperature}, mode=new_mode)

    async def sensor_loop(self):
        while True:
            try:
                await self.update_sensors()
            except Exception as err:
                self.error('Sensor update failed:', err)
            await asyncio.sleep(SENSOR_INTERVAL)

    async def mmode_loop(self):
        while True:
            try:
                await self.update_mode()
            except Exception as err:
                self.error('Mode update failed:', err)
            await asyncio.sleep(MODE_INTERVAL)

    async def on_deleted(self):
        for task in self._tasks:
            task.cancel()


homey_export = MyDevice