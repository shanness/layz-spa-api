"""Authenticates with Lay-Z-Spa"""
import asyncio
from datetime import datetime
from .api import Api
class Spa:
    """The class to handle authenticating with the API"""
    def __init__(self, api, did):
        """
        constructor
        """
        self.api = Api({"did": did, "api_token":api})                  

    async def is_online(self):
        """
        Indicates if the device is currently online
        """
        result = await self.api.send_command("is_online")
        return result["data"] == "true"        

    async def update_status(self):        
        """
        Fetches the Status of the Spa
        """
        result = await self.api.send_command("status")
        
        data = result["data"]                              
        """self.updated_at = datetime.fromtimestamp(data["updated_at"])"""
        attr = data["attr"]
        
        self.wave_appm_min = 0
        self.heat_timer_min = attr["timer_delay"]
        self.earth = 0
        self.wave_timer_min = 0

        self.filter_timer_min = 0
        self.heat_appm_min = attr["timer_duration"]
        self.filter_appm_min = 0

        self.locked = 0

        self.power = attr["power"] == 1
        self.heat_power = attr["heat"] == 1
        self.wave_power = attr["airjet"] == 1
        self.filter_power = attr["filter"] == 1

        self.temp_now = attr["temp_now"]
        self.temp_set = attr["temp_set"]
        self.temp_set_unit ="°C" if attr["temp_set_unit"]=="1" else "°F"
        self.heat_temp_reach = 0

        self.system_err1 = attr["e01"]
        self.system_err2 = attr["e02"]
        self.system_err3 = attr["e03"]
        self.system_err4 = attr["e04"]
        self.system_err5 = attr["e05"]
        self.system_err6 = attr["e06"]
        self.system_err7 = attr["e07"]
        self.system_err8 = attr["e08"]
        self.system_err9 = attr["e09"]            

    async def set_power(self, power):
        """
        Turn the spa on or off
        """
        if power:
            await self.api.send_command("turn_on")
            power=True
        else:
            await self.api.send_command("turn_off")
            power=False

    async def set_filter_power(self, power):
        """
        Turn the filter on or off
        """
        if power:
            await self.api.send_command("turn_filter_on")
            filter_power=True
        else:
            await self.api.send_command("turn_filter_off")
            filter_power=False

    async def set_heat_power(self, power):
        """
        Turn the heater on or off
        """
        if power:
            await self.api.send_command("turn_heat_on")
            heat_power=True
        else:
            await self.api.send_command("turn_heat_off")
            heat_power=False

    async def set_wave_power(self, power):
        """
        Turn the bubbles on and off
        """
        if power:
            await self.api.send_command("turn_wave_on")
            wave_power=True
        else:
            await self.api.send_command("turn_wave_off")
            wave_power=False

    async def set_target_temperature(self, temperature):
        """
        Set the target temperature for the spa
        """
        await self.api.send_command("temp_set", {"temperature": temperature})
        target=temperature