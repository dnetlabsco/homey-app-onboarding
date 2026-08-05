from homey.device import Device
import random
import asyncio

class MyDevice(Device):
    async def on_init(self):
        await super().on_init()
        self.log("Initialized MyDevice")
        asyncio.create_task(self.update_value())
        asyncio.create_task(self.update_mode())


    async def update_value(self):
            
        while True:
            freeze = self.homey.settings.get("freeze") or False

            if freeze:
                await asyncio.sleep(10)
                continue

            temperature = round(random.uniform(15, 25), 1)
            humidity = round(random.uniform(30, 70), 1)
            pressure = round(random.uniform(1000, 1025), 1)

            await self.set_capability_value("measure_temperature", temperature)
            await self.set_capability_value("measure_humidity", humidity)
            await self.set_capability_value("measure_pressure", pressure)
            self.log(f"Values updated: {temperature}°C, {humidity}%, {pressure} mbar")

            
            await asyncio.sleep(10)

    async def update_mode(self):
        modes = ["sunny", "cloudy", "rainy"]
        mode = random.choice(modes)
        await self.set_capability_value("mode", mode)
        self.log(f"Mode updated: {mode}")

        await self.weather_changed_trigger()


        await asyncio.sleep(60)
        asyncio.create_task(self.update_mode())
    

    async def weather_changed_trigger(self):
        card = self.homey.app.weather_changed_card

        current_mode = self.get_capability_value("mode")
        temperature = self.get_capability_value("measure_temperature")

        await card.trigger(self,{"temperature" : temperature},)

homey_export = MyDevice
