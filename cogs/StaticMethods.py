import time
from datetime import date

class StaticMethods:

    @staticmethod
    async def specialmaps(map):
        output = map
        if map in ["bcm64", "bcmo", "bchm"]:
            output = "bcmo"
        elif map in ["bcmw", "bcma", "bcom"]:
            output = "bcma"
        return output

    @staticmethod
    async def addplus(s):
        output = s
        if s > 0:
            output = f"+{s}"
        return output

    @staticmethod  # calculates the limit for the message-history
    async def calculate_limit(count, guild_id):
        maps_per_war = 12
        messages_per_map = 1
        if guild_id == 746014047866191932:
            messages_per_map = 2
        messages_per_war = 2

        limit = count * maps_per_war * messages_per_map + messages_per_war
        return limit

    @staticmethod
    async def create_timestamp(hour: int, timestamp_format: str):
        warday = date.today()
        day = warday.day
        month = warday.strftime("%b")
        year = warday.strftime("%Y")
        time_obj = time.localtime()
        local_time = time.strftime("%a " + str(month) + " " + str(day) + " " + str(hour) + ":00:00 " + str(year),
                                   time_obj)
        time_sting = time.strptime(local_time)
        war_time = str(time.mktime(time_sting)).split(".")[0]
        war_time_timestamp = f"<t:{war_time}:{timestamp_format}>"
        return war_time_timestamp

    @staticmethod
    async def ToTextNumber(n):
        n = str(n)
        if n[-1] in ["1", "01"] and n not in ["11"]:
            return f"{n[:-1]}1st"
        elif n[-1] in ["2", "02"] and n not in ["12"]:
            return f"{n[:-1]}2nd"
        elif n[-1] in ["3", "03"] and n not in ["13"]:
            return f"{n[:-1]}3rd"
        return f"{str(n)}th"

    @staticmethod
    async def AddNull(n):
        if n in range(1, 10):
            return "0" + str(n)
        return str(n)
