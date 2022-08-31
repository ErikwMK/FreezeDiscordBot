import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

import cogs.SetupBot as SetupBot

# import time
import asyncio
import json

from cogs.StaticMethods import StaticMethods


with open("config.json") as f:
    config = json.load(f)

class Stats(commands.Cog, StaticMethods):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.map_dic = {
            "mks": {"track_long": "Mario Kart Stadium (MKS)", "track_short": "MKS", "link": "https://images-ext-2.discordapp.net/external/_Uf097v5rOGaoLyt0D_ZbcHesmnH70Mz67ZcIxw5l0g/https/i.imgur.com/x2KufpY.png", "difference": []},
            "wp": {"track_long": "Water Park (WP)", "track_short": "WP", "link": "https://images-ext-2.discordapp.net/external/_0RyxvSKHHkFbHGozhD0sDQulInS1Z7gw6lQQTvG8-k/https/i.imgur.com/oRKjkU4.png", "difference": []},
            "ssc": {"track_long": "Sweet Sweet Canyon (SSC)", "track_short": "SSC", "link": "https://images-ext-2.discordapp.net/external/g4TCl2kB9i1rEaD4qvrYXliFE-GSVYPbmsdSkgz7oOA/https/i.imgur.com/FNd8cqL.png", "difference": []},
            "tr": {"track_long": "Thwomp Ruins (TR)", "track_short": "TR", "link": "https://images-ext-1.discordapp.net/external/2KKxkZBNG8xoKO_B8mWcOHYBelqOo9WMFaRdDgK7GPU/https/i.imgur.com/CqWeTRF.png", "difference": []},
            "mc": {"track_long": "Mario Circuit (MC)", "track_short": "MC", "link": "https://images-ext-2.discordapp.net/external/78-ECGwrSxMPxV1BkWV78WI1j2mbZg79sJ44r5wtyHc/https/i.imgur.com/kLWQ3PG.png", "difference": []},
            "th": {"track_long": "Toad Harbor (TH)", "track_short": "TH", "link": "https://images-ext-2.discordapp.net/external/suCjE8V-YTtHy-ExuM9QdnCb7GjtYGuiqavldN562XE/https/i.imgur.com/FYu4brr.png", "difference": []},
            "tm": {"track_long": "Twisted Mansion (TM)", "track_short": "TM", "link": "https://images-ext-2.discordapp.net/external/EtxNCLxssibCTu3BJYpGG2xf7CIcoj8yWjPK5o_WgDk/https/i.imgur.com/gDqTSTK.png", "difference": []},
            "sgf": {"track_long": "Shy Guy Falls (SGF)", "track_short": "SGF", "link": "https://images-ext-1.discordapp.net/external/dp8q5kNo0Qha9niqqF2VVmfT-zUGFmce9LLaxWPd3NY/https/i.imgur.com/u1DldtB.png", "difference": []},
            "sa": {"track_long": "Sunshine Airport (SA)", "track_short": "SA", "link": "https://images-ext-2.discordapp.net/external/A63KGCm3QCeMWPkOcjn8uRmZAKkXdTsKs01nGAhmIUU/https/i.imgur.com/AHMg0iD.png", "difference": []},
            "ds": {"track_long": "Dolphin Shoals (DS)", "track_short": "DS", "link": "https://images-ext-1.discordapp.net/external/vMhKuI5Z9rheJfsouyE3eFBlr_djUfwLestWNACtZIg/https/i.imgur.com/S8bSb2i.png", "difference": []},
            "ed": {"track_long": "Electrodrome (ED)", "track_short": "ED", "link": "https://images-ext-1.discordapp.net/external/ypTysMD6l4RLJQFS9CWdTyMG9JCWvKGGhAhkGlfdQIo/https/i.imgur.com/IzFL0Wy.png", "difference": []},
            "mw": {"track_long": "Mount Wario (MW)", "track_short": "MW", "link": "https://images-ext-2.discordapp.net/external/RRMPB_7_4pZaGJuZKgBFjoRDOY22LxUh1u8sprJXGOE/https/i.imgur.com/D5AGGZk.png", "difference": []},
            "cc": {"track_long": "Cloudtop Cruise (CC)", "track_short": "CC", "link": "https://images-ext-1.discordapp.net/external/tO7Vgf2YcJ5B7167z6kAaux5fATh-FrG3UrkoNwNtpE/https/i.imgur.com/kocoKcq.png", "difference": []},
            "bdd": {"track_long": "Bone-Dry Dunes (BDD)", "track_short": "BDD", "link": "https://images-ext-1.discordapp.net/external/9RGtZleR5Cv8nyHXHb42XjmER1DJ6JABFFA4aVgplKU/https/i.imgur.com/ChMkdXy.png", "difference": []},
            "bc": {"track_long": "Bowser\'s Castle (BC)", "track_short": "BC", "link": "https://images-ext-1.discordapp.net/external/uCV-JqA-L-A844wlDRE0c0ArwroeljE93H4ZKN3PMt8/https/i.imgur.com/F4i4OTB.png", "difference": []},
            "rr": {"track_long": "Rainbow Road (RR)", "track_short": "RR", "link": "https://images-ext-2.discordapp.net/external/sK75OxBy4beSnFuiQ9b82XwSWQqDKSVJwW4JsozKnao/https/i.imgur.com/Gq8ynLF.png", "difference": []},
            "rmmm": {"track_long": "Wii Moo Moo Meadows (rMMM)", "track_short": "rMMM", "link": "https://images-ext-2.discordapp.net/external/CY4j84Z_l_hwubdZUBaOfLfK3-LsxieU12kfi3Wjz8Q/https/i.imgur.com/bAhUGdN.png", "difference": []},
            "rmc": {"track_long": "GBA Mario Circuit (rMC)", "track_short": "rMC", "link": "https://images-ext-2.discordapp.net/external/zxpBNNQV9bnWHfewm9-PvHmhDlxa6yVtlfoHiA0tHjo/https/i.imgur.com/gB4c69G.png", "difference": []},
            "rccb": {"track_long": "DS Cheep Cheep Beach (rCCB)", "track_short": "rCCB", "link": "https://images-ext-2.discordapp.net/external/YHueaD-VXA8HnAM1ZZZGm1aoQJWMiYUilC2h8V_UxJA/https/i.imgur.com/pTmv1ng.png", "difference": []},
            "rtt": {"track_long": "N64 Toad\'s Turnpike (rTT)", "track_short": "rTT", "link": "https://images-ext-1.discordapp.net/external/MHNzqb2vzIVWa-pyfqfCKb1HEfBEZWcCseawmfk1XHQ/https/i.imgur.com/NshE4yu.png", "difference": []},
            "rddd": {"track_long": "GCN Dry Dry Desert (rDDD)", "track_short": "rDDD", "link": "https://images-ext-1.discordapp.net/external/NC00hiaM6uAoZHWKsYt9mbJwUpUl82e1DbyhtJxGdCA/https/i.imgur.com/QAuzvJB.png", "difference": []},
            "rdp3": {"track_long": "SNES Donut Plains 3 (rDP3)", "track_short": "rDP3", "link": "https://images-ext-2.discordapp.net/external/j6zV5qDXkSw1EFbfuzj8brNU0AyWkGr5e9er0cuqzj0/https/i.imgur.com/rELdEcJ.png", "difference": []},
            "rrry": {"track_long": "N64 Royal Raceway (rRRy)", "track_short": "rRRy", "link": "https://images-ext-1.discordapp.net/external/6YFo1w8HmpDkZ9wM-Wm2AmuAK78ltDdiwVp5cexXvpU/https/i.imgur.com/wF0P4L0.png", "difference": []},
            "rdkj": {"track_long": "3DS DK Jungle (rDKJ)", "track_short": "rDKJ", "link": "https://images-ext-1.discordapp.net/external/Og1SD2Dua1mZoJ6IQW6ItVejVZg2E99xUy9R6aYwF8c/https/i.imgur.com/vcGy5bY.png", "difference": []},
            "rws": {"track_long": "DS Wario Stadium (rWS)", "track_short": "rWS", "link": "https://images-ext-2.discordapp.net/external/mGhG3ws0QSDtgpYmc2cDzquDYyRDcfTQ7RKGG5WhwTs/https/i.imgur.com/l0fXw5q.png", "difference": []},
            "rsl": {"track_long": "GCN Sherbet Land (rSL)", "track_short": "rSL", "link": "https://images-ext-2.discordapp.net/external/uagElNkQI2PWMn7DBASIo840_kyLWb0JyLNGKxmCptk/https/i.imgur.com/KR5hpqy.png", "difference": []},
            "rmp": {"track_long": "3DS Music Park (rMP)", "track_short": "rMP", "link": "https://images-ext-2.discordapp.net/external/hbR_5RK75W5lojtUKFArnOxjeuMv4V0gefNm8UQIbxw/https/i.imgur.com/mo37kKo.png", "difference": []},
            "ryv": {"track_long": "N64 Yoshi Valley (rYV)", "track_short": "rYV", "link": "https://images-ext-2.discordapp.net/external/UrrtZSdKG4VOr-2z6S1YS-mpqd22SLXJrf4SlHlPZZs/https/i.imgur.com/uymaWqK.png", "difference": []},
            "rttc": {"track_long": "DS Tick-Tock Clock (rTTC)", "track_short": "rTTC", "link": "https://images-ext-2.discordapp.net/external/hg-WVUyn5PcCb88tbjuFkcr6epfSPPZkhUgkz1jxBKc/https/i.imgur.com/2JituCs.png", "difference": []},
            "rpps": {"track_long": "3DS Piranha Plant Slide (rPPS)", "track_short": "rPPS", "link": "https://images-ext-1.discordapp.net/external/z99OC5pWBJ7Xc4nkhNqWj4VxqwgBEfsjgAfnMd21-ZI/https/i.imgur.com/5i6A3II.png", "difference": []},
            "rgv": {"track_long": "Wii Grumble Volcano (rGV)", "track_short": "rGV", "link": "https://images-ext-2.discordapp.net/external/pTxGnePtu5UhGCmSipCLmXw8ebH1dzsf9_3jv-55hos/https/i.imgur.com/WGS2ojx.png", "difference": []},
            "rrrd": {"track_long": "N64 Rainbow Road (rRRd)", "track_short": "rRRd", "link": "https://images-ext-1.discordapp.net/external/aKzWCsYyPFkc6gjNPBXYn6E0z5AgIbJq8UFDC3o1RQk/https/i.imgur.com/qflI1QP.png", "difference": []},
            "dyc": {"track_long": "GCN Yoshi Circuit (dYC)", "track_short": "dYC", "link": "https://images-ext-2.discordapp.net/external/SN3a5jdlADWK5hKeg7r-eTJaNAQhTct6d6rlSNNjlFg/https/i.imgur.com/bvkqGEL.png", "difference": []},
            "dea": {"track_long": "Excite Bike Arena (dEA)", "track_short": "dEA", "link": "https://images-ext-1.discordapp.net/external/5_cJ92ZV6-wqKig2fSV2NJaQYoPtV5hcPij8AtEW1H4/https/i.imgur.com/H3h3JT0.png", "difference": []},
            "ddd": {"track_long": "Dragon Driftway (dDD)", "track_short": "dDD", "link": "https://images-ext-2.discordapp.net/external/KLR6fC8Cbdu5grOaKsG8EQSsSgu3eHXyJuxnt2XptEo/https/i.imgur.com/LeYOzs1.png", "difference": []},
            "dmc": {"track_long": "Mute City (dMC)", "track_short": "dMC", "link": "https://images-ext-1.discordapp.net/external/2gmyNfyyePllHR1ewdKKUOY9l5RoVoxsTkQO--zrvDA/https/i.imgur.com/224DyTF.png", "difference": []},
            "dwgm": {"track_long": "Wii Wario\'s Gold Mine (dWGM)", "track_short": "dWGM", "link": "https://images-ext-1.discordapp.net/external/GddNL-hmWbENA4AUCAnHhJQHB_bMl1s-s1gUvnQ6th0/https/i.imgur.com/Pjyewat.png", "difference": []},
            "drr": {"track_long": "SNES Rainbow Road (dRR)", "track_short": "dRR", "link": "https://images-ext-1.discordapp.net/external/WW8spbvRLUfFlDVg-lQwn-Q_z82clCSpDkRZ-5n3pzI/https/i.imgur.com/ogwuCwZ.png", "difference": []},
            "diio": {"track_long": "Ice Ice Outpost (dIIO)", "track_short": "dIIO", "link": "https://images-ext-1.discordapp.net/external/0ITvNvoUoWUTv-HifmeCYmReqCrzi8lZ4Eoh0haj5zU/https/i.imgur.com/X4QD87f.png", "difference": []},
            "dhc": {"track_long": "Hyrule Circuit (dHC)", "track_short": "dHC", "link": "https://images-ext-2.discordapp.net/external/KzNks7dOoO6oicnGvZOB5OPzCkC8Hsvlqg89RYBu-xE/https/i.imgur.com/eM2YHQw.png", "difference": []},
            "dbp": {"track_long": "GCN Baby Park (dBP)", "track_short": "dBP", "link": "https://images-ext-1.discordapp.net/external/NVdasyrMIZinw_6s10wcNFY28r6i4PEg6WUtf7xXBvc/https/i.imgur.com/DKAXxiW.png", "difference": []},
            "dcl": {"track_long": "GBA Cheese Land (dCL)", "track_short": "dCL", "link": "https://images-ext-2.discordapp.net/external/Be5wTkv0wHiv97u7esFLCWzE45SCbi4pgg8AV_XA5zs/https/i.imgur.com/JVPSAtV.png", "difference": []},
            "dww": {"track_long": "Wild Woods (dWW)", "track_short": "dWW", "link": "https://images-ext-2.discordapp.net/external/ZHmmOS6kC5Cr4vxdHImdrrPVJ77VkN7Pi81oEM3RF30/https/i.imgur.com/5TZg4kh.png", "difference": []},
            "dac": {"track_long": "Animal Crossing (dAC)", "track_short": "dAC", "link": "https://images-ext-1.discordapp.net/external/DyYiBqof494_j66puFOelfoiVQCtAWok0cgLLpvl8KA/https/i.imgur.com/cjNpw2m.png", "difference": []},
            "dnbc": {"track_long": "3DS Neo Bowser City (dNBC)", "track_short": "dNBC", "link": "https://images-ext-1.discordapp.net/external/44MHipqSAqyFYjKjjyF8vcJaFVjlL9nncM9MDXmk9WU/https/i.imgur.com/dfvv1Uw.png", "difference": []},
            "drir": {"track_long": "GBA Ribbon Road (dRiR)", "track_short": "dRiR", "link": "https://images-ext-2.discordapp.net/external/DKwFQv8GNOLv9kq2TD5jgmucCIcF4aeT1RElsL0zRcY/https/i.imgur.com/Uc597hp.png", "difference": []},
            "dsbs": {"track_long": "Super Bell Subway (dSBS)", "track_short": "dSBS", "link": "https://images-ext-1.discordapp.net/external/3gG88U2Xvu428zmDd1YxxIyzU1iMURCVBBqJSAHZjA0/https/i.imgur.com/spI2tsr.png", "difference": []},
            "dbb": {"track_long": "Big Blue (dBB)", "track_short": "dBB", "link": "https://images-ext-1.discordapp.net/external/frpsxwFnrLz-kYwCZbwZ5-XO7B8Xe_oMfR2bUohAA2Y/https/i.imgur.com/C1YYKFH.png", "difference": []},
            "bpp": {"track_long": "Tour Paris Promenade (bPP)", "track_short": "bPP", "link": "https://images-ext-2.discordapp.net/external/bLVril6oc46zUNEkZ8Nz18ZtW5M854ZNmW0CMsIbwvY/https/i.imgur.com/rrwvSjq.png", "difference": []},
            "btc": {"track_long": "3DS Toad Circuit (bTC)", "track_short": "bTC", "link": "https://images-ext-1.discordapp.net/external/ekilPteazkHz4Vy5l0rquDSwpwOQHlMoMzJHpCH-YGk/https/i.imgur.com/bK9csi6.png", "difference": []},
            "bcmo": {"track_long": "N64 Choco Mountain (bCMo)", "track_short": "bCMo", "link": "https://images-ext-1.discordapp.net/external/BJAbSbZ6eSuoYu7dfD01ePL6l-ec2Igj29y-w6AGpTw/https/i.imgur.com/ktqlNP7.png", "difference": []},
            "bcma": {"track_long": "Wii Coconut Mall (bCMa)", "track_short": "bCMa", "link": "https://images-ext-1.discordapp.net/external/EHTZ0Is0L_gfqF_yoB44-PuOqnWKtMZJOECSRdBlsDI/https/i.imgur.com/EUXlLQ6.png", "difference": []},
            "btb": {"track_long": "Tour Tokyo Blur (bTB)", "track_short": "bTB", "link": "https://images-ext-2.discordapp.net/external/mshUVNu-AtQJbeim02rP6dnUtudPKsv0fUuULeMKbRQ/https/i.imgur.com/bIHXjVC.png", "difference": []},
            "bsr": {"track_long": "DS Shroom Ridge (bSR)", "track_short": "bSR", "link": "https://images-ext-2.discordapp.net/external/IdtY222Uizlw0X2erPq5D46FB2d-Aek_PRHTCotMa3c/https/i.imgur.com/4XTF56w.png", "difference": []},
            "bsg": {"track_long": "GBA Sky Garden (bSG)", "track_short": "bSG", "link": "https://images-ext-2.discordapp.net/external/47avJT2DLdC15DMGYI26JEFsZ6eJjy6jTf0wvP_hkd4/https/i.imgur.com/efMObR1.png", "difference": []},
            "bnh": {"track_long": "Tour Ninja Hideaway (bNH)", "track_short": "bNH", "link": "https://images-ext-1.discordapp.net/external/RKcMfdqHd3dC0d7x2IZktDtO40zjTTEn2z2VufOHefo/https/i.imgur.com/o9RWZ0t.png", "difference": []},
            "bnym": {"track_long": "Tour New York Minute (bNYM)", "track_short": "bNYM",  "link": "https://images-ext-1.discordapp.net/external/m12mq1pmY_tDhW1llgUCeIy5xCwKib0aDyhP8iVJkwY/https/i.imgur.com/jijGEl3.png",  "difference": []},
            "bmc3": {"track_long": "SNES Mario Circuit 3 (bMC3)", "track_short": "bCM3",  "link": "https://images-ext-1.discordapp.net/external/eWcvDZ-BbT6y8MOY-0yBz0CN1mBQT3_iiDSupoCoVhk/https/i.imgur.com/hCXv3gu.png",  "difference": []},
            "bkd": {"track_long": "N64 Kalimari Desert (bKD)", "track_short": "bKD", "link": "https://images-ext-2.discordapp.net/external/y4axN6gv5ltNBsfi9oBCqz1LqKXzqU8Wq-d_sQAbaxY/https/i.imgur.com/9JrvdNA.png", "difference": []},
            "bwp": {"track_long": "DS Waluigi Pinball (bWP)", "track_short": "bWP", "link": "https://images-ext-2.discordapp.net/external/2Y1wosOW6_-pSqsVX8IGXEJ-YDmE28PqtbCmErIEjHs/https/i.imgur.com/BcpdnWU.png", "difference": []},
            "bss": {"track_long": "Tour Sydney Sprint (bSS)", "track_short": "bSS", "link": "https://images-ext-1.discordapp.net/external/v06DDixqLwUwIyKiUFlgiTJGIs5RuVHMxvjw2ePSVhE/https/i.imgur.com/IOHbb5k.png", "difference": []},
            "bsl": {"track_long": "GBA Snow Land (bSL)", "track_short": "bSL", "link": "https://images-ext-2.discordapp.net/external/ZUuz-pJfMi_95YXuQrvQkBqOm7Z6F1Y1s0mMN6DmIxw/https/i.imgur.com/h3Hsz06.png", "difference": []},
            "bmg": {"track_long": "Wii Mushroom Gorge (bMG)", "track_short": "bMG", "link": "https://images-ext-1.discordapp.net/external/1Ce6L4ll4i-861ifITFVwO9TDRcmPoD4ujPsjHzkoyQ/https/i.imgur.com/om5Sz3C.png", "difference": []},
            "bshs": {"track_long": "Sky-High Sundae (bSHS)", "track_short": "bSHS", "link": "https://images-ext-1.discordapp.net/external/wFIO61w1VZoNVs43mmnp75smt1rPDyW01IINTxe7WP4/https/i.imgur.com/TnDR4UG.png", "difference": []}}
        self.maps = [
            "mks", "wp", "ssc", "tr", "mc", "th", "tm", "sgf",
            "sa", "ds", "ed", "mw", "cc", "bdd", "bc", "rr",
            "rmmm", "rmc", "rccb", "rtt", "rddd", "rdp3", "rrry", "rdkj",
            "rws", "rsl", "rmp", "ryv", "rttc", "rpps", "rgv", "rrrd",
            "dyc", "dea", "ddd", "dmc", "dwgm", "drr", "diio", "dhc",
            "dbp", "dcl", "dww", "dac", "dnbc", "drir", "dsbs", "dbb",
            "bpp", "btc", "bcmo", "bcma", "btb", "bsr", "bsg", "bnh",
            "bnym", "bmc3", "bkd", "bwp", "bss", "bsl", "bmg", "bshs"]
        self.maps_long = [
            "Mario Kart Stadium", "Water Park", "Sweet Sweet Canyon", "Thwomp Ruins",
            "Mario Circuit", "Toad Harbor", "Twisted Mansion", "Shy Guy Falls",
            "Sunshine Airport", "Dolphin Shoals", "Electrodrome", "Mount Wario",
            "Cloudtop Cruise", "Bone-Dry Dunes", "Bowser\'s Castle", "Rainbow Road",
            "Wii Moo Moo Meadows", "GBA Mario Circuit", "DS Cheep Cheep Beach", "N64 Toad\'s Turnpike",
            "GCN Dry Dry Desert", "SNES Donut Plains 3", "N64 Royal Raceway", "3DS DK Jungle",
            "DS Wario Stadium", "GCN Sherbet Land", "3DS Music Park", "N64 Yoshi Valley",
            "DS Tick-Tock Clock", "3DS Piranha Plant Slide", "Wii Grumble Volcano", "N64 Rainbow Road",
            "GCN Yoshi Circuit", "Excite Bike Arena", "Dragon Driftway", "Mute City",
            "SNES Rainbow Road", "Ice Ice Outpost", "Hyrule Circuit", "Wii Wario\'s Gold Mine",
            "GCN Baby Park", "GBA Cheese Land", "Wild Woods", "Animal Crossing",
            "3DS Neo Bowser City", "GBA Ribbon Road", "Super Bell Subway", "Big Blue",
            "Tour Paris Promenade", "3DS Toad Circuit", "N64 Choco Mountain", "Wii Coconut Mall",
            "Tour Tokyo Blur", "DS Shroom Ridge", "GBA Sky Garden", "Tour Ninja Hideaway",
            "Tour New York Minute", "SNES Mario Circuit 3", "N64 Kalimari Desert", "DS Waluigi Pinball",
            "Tour Sydney Sprint", "GBA Snow Land", "Wii Mushroom Gorge", "Sky-High Sundae"]


    async def checkmap(self, map):
        output = map.lower() in self.maps
        return output

    async def convert_to_short_map(self, map):
        return self.maps[self.maps_long.index(map)]

    @staticmethod  # deletes the process_message if neccessary
    async def delete_process_message_func(msg, boolean):
        if boolean is True:
            await msg.delete()
        return

    async def CalculateStatsData(self, differences, not_last):
        avg_difference = await self.addplus(round(sum(differences) / len(differences), 2))
        max_difference = await self.addplus(max(differences))
        min_difference = await self.addplus(min(differences))
        data = {"avg_difference": avg_difference, "max_difference": max_difference, "min_difference": min_difference}
        if not_last is False:
            last_difference = await self.addplus(differences[-1])
            data["last_difference"] = last_difference
        return data


    @app_commands.command(name="mapstats", description="Analyse your toadbot channel of a specific map")
    @app_commands.describe(map="The map you want to analyse, e. g. MKS, rmmm, bNH", amount_of_wars="The amount of wars you want to have analysed, either an integer or 'all'", toadchannel="Overwrites the default toadchannel from the setup commands")
    @app_commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def mapstats(self, interaction: discord.Interaction, map: str, amount_of_wars: str,
                       toadchannel: discord.TextChannel = None):
        # time1 = time.time()
        map = map.lower()  # checks if every parameter is correct
        if await self.checkmap(await self.specialmaps(map.lower())) is False:
            return await interaction.response.send_message("This map doesn't exist!", ephemeral=True)
        try:
            amount_of_wars = int(amount_of_wars)
            if int(amount_of_wars) < 0:
                return await interaction.response.send_message("The number of wars is invalid! Use numbers `> 0` or type all", ephemeral=True)
            limit = await self.calculate_limit(amount_of_wars, interaction.guild.id)
        except ValueError:
            if amount_of_wars == "all" or amount_of_wars is None:
                amount_of_wars = None
                limit = None
            else:
                return await interaction.response.send_message("The number of wars is invalid! Use numbers `> 0` or type all", ephemeral=True)
        if toadchannel is None:
            toadchannel_id = SetupBot.GetToadbot(str(interaction.guild.id))
            if toadchannel_id is None:
                return await interaction.response.send_message("No default toadbot channel is set! Either use the optional toadbot parameter or contact a leader to set a default toadbot channel!", ephemeral=True)
            toadchannel = self.bot.get_channel(int(toadchannel_id))

        delete_process_message = False
        process_msg = None
        try:
            if amount_of_wars > 10:
                process_msg = await interaction.channel.send("The process of the analysation might take a bit! Please be patient and don't add another command when it's not working in a few seconds!")
                delete_process_message = True
        except TypeError:
            process_msg = await interaction.channel.send("The process of the analysation might take a bit! Please be patient and don't add another command when it's not working in a few seconds!")
            delete_process_message = True

        await interaction.response.defer(ephemeral=False)
        all_differences = []
        not_toadbot = 0
        amount_of_races = 0
        track_to_search = self.map_dic[map]["track_long"].rsplit(" (")[0]
        async for i in toadchannel.history(limit=limit):  # goes through the channel and collects data
            while not_toadbot <= 200:
                not_toadbot += 1
                embeds = i.embeds
                for embed in embeds:
                    try:
                        if embed.title.startswith("Score"):
                            amount_of_races += 1
                            not_toadbot = 0
                            if embed.fields[4].value.startswith(track_to_search):
                                all_differences.append(int(embed.fields[3].value))
                    except IndexError:
                        pass
                break
            else:
                await self.delete_process_message_func(process_msg, delete_process_message)
                await asyncio.sleep(0.2)
                return await interaction.followup.send("This isn't an toadbot channel! Set the default toadbot channel or the toadbot channel in your command to a valid toadbot channel!", ephemeral=True)
        # time2 = time.time()
        await self.delete_process_message_func(process_msg, delete_process_message)
        await asyncio.sleep(0.3)
        if amount_of_wars == 0:
            embed = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])), title="Mapstats")
            embed.set_thumbnail(url=self.map_dic[map]["link"])
            embed.add_field(name=f"This map wasn't played in the amount of wars, you entered!", value="Enter a higher amount!", inline=False)
            return embed

        data = await self.CalculateStatsData(all_differences, False)
        embed_name = f"In the last {amount_of_wars} wars, "  # creates the embed
        if amount_of_wars is None:
            embed_name = f"In all ({round(amount_of_races / 12)}) wars, "
        embed = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])))
        embed.set_thumbnail(url=self.map_dic[map]["link"])
        embed.add_field(
            name=f"{embed_name}**{self.map_dic[map]['track_long']}** was played **{len(all_differences)}** times.",
            value="Here the stats:", inline=False)
        embed.add_field(name=f"Average score: ", value=f"{data['avg_difference']}", inline=False)
        embed.add_field(name=f"Last score: ", value=f"{data['last_difference']}", inline=False)
        embed.add_field(name=f"Maximum score: ", value=f"{data['max_difference']}", inline=False)
        embed.add_field(name=f"Minimum score: ", value=f"{data['min_difference']}", inline=False)
        # await interaction.channel.send(f"This took** {int((time2 - time1) / 60)} minutes and {round((time2 - time1) % 60, 1)} seconds**", delete_after=5)
        return await interaction.followup.send(embed=embed)

    @app_commands.command(name="map", description="All Races of a map and their opponent & data")
    @app_commands.describe(map="The map you want to analyse, e. g. MKS, rmmm, bNH", amount_of_wars="The amount of wars you want to have analysed, either an integer or 'all'", toadchannel="Overwrites the default toadchannel from the setup commands")
    @app_commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def map(self, interaction: discord.Interaction, map: str, amount_of_wars: str,
                  toadchannel: discord.TextChannel = None):
        map = map.lower()
        if await self.checkmap(await self.specialmaps(map.lower())) is False:
            return await interaction.response.send_message("This map doesn't exist!", ephemeral=True)
        try:
            amount_of_wars = int(amount_of_wars)
            if int(amount_of_wars) < 0:
                return await interaction.response.send_message("The number of wars is invalid! Use numbers `> 0` or type all", ephemeral=True)
            limit = await self.calculate_limit(amount_of_wars, interaction.guild.id)
        except ValueError:
            if amount_of_wars == "all" or amount_of_wars is None:
                amount_of_wars = None
                limit = None
            else:
                return await interaction.response.send_message("The number of wars is invalid! Use numbers `> 0` or type all", ephemeral=True)
        if toadchannel is None:
            toadchannel_id = SetupBot.GetToadbot(str(interaction.guild.id))
            if toadchannel_id is None:
                return await interaction.response.send_message("No default toadbot channel is set! Either use the optional toadbot parameter or contact a leader to set a default toadbot channel!", ephemeral=True)
            toadchannel = self.bot.get_channel(int(toadchannel_id))

        delete_process_message = False
        process_msg = None
        try:
            if amount_of_wars > 10:
                process_msg = await interaction.channel.send("The process of the analysation might take a bit! Please be patient and don't add another command when it's not working in a few seconds!")
                delete_process_message = True
        except TypeError:
            process_msg = await interaction.channel.send("The process of the analysation might take a bit! Please be patient and don't add another command when it's not working in a few seconds!")
            delete_process_message = True

        await interaction.response.defer(ephemeral=False)
        all_differences = []
        not_toadbot = 0
        amount_of_races = 0
        track_to_search = self.map_dic[map]["track_long"].rsplit(" (")[0]
        async for i in toadchannel.history(limit=limit):
            while not_toadbot <= 200:
                not_toadbot += 1
                embeds = i.embeds
                for embed in embeds:
                    try:
                        if embed.title.startswith("Score") and embed.fields[3].name == "Difference":
                            amount_of_races += 1
                            not_toadbot = 0
                            if embed.fields[4].value.startswith(track_to_search):
                                all_differences.append({"difference": await self.addplus(int(embed.fields[3].value)), "opponent": embed.fields[2].name, "date": i.created_at.strftime("%d-%m-%Y")})
                    except IndexError:
                        pass
                break
            else:
                await self.delete_process_message_func(process_msg, delete_process_message)
                await asyncio.sleep(0.2)
                return await interaction.followup.send("This isn't an toadbot channel! Set the default toadbot channel or the toadbot channel in your command to a valid toadbot channel!", ephemeral=True)

        if len(all_differences) == 0:
            embed = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])), title="Map")
            embed.set_thumbnail(url=self.map_dic[map]["link"])
            embed.add_field(name=f"This map wasn't played in the amount of wars, you entered!", value="Enter a higher amount!", inline=False)
            await self.delete_process_message_func(process_msg, delete_process_message)
            await asyncio.sleep(0.2)
            return await interaction.followup.send(embed=embed)

        embed_name = f"In the last {amount_of_wars} wars, "
        if amount_of_wars is None:
            embed_name = f"In all ({round(amount_of_races / 12)}) wars, "

        embed = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])))
        embed.set_thumbnail(url=self.map_dic[map]["link"])
        embed.add_field(name=f"{embed_name}**{self.map_dic[map]['track_long']}** was played **{len(all_differences)}** times.", value="Here the stats:", inline=False)
        for i, n in zip(all_differences, range(len(all_differences))):  # adds a field for every map and its data
            embed.add_field(name=f"{n + 1}.", value=f"`Difference:` {i['difference']}\n`Opponent:` {i['opponent']}\n`Date:` {i['date']}")

        await self.delete_process_message_func(process_msg, delete_process_message)
        return await interaction.followup.send(embed=embed)

    @app_commands.choices(
        order_by=[
            Choice(name="In-game order", value="default"),
            Choice(name="Best average", value="best"),
            Choice(name="Worst average", value="worst"),
            Choice(name="Most played", value="most")
        ]
    )
    @app_commands.command(name="stats64", description="The stats of all maps in the game! This is a spammy command!")
    @app_commands.describe(amount_of_wars="The amount of wars you want to have analysed, either an integer or 'all'", order_by="Order the analysation messages", toadchannel="Overwrites the default toadchannel from the setup command")
    @app_commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def stats64(self, interaction: discord.Interaction, amount_of_wars: str, order_by: Choice[str], toadchannel: discord.TextChannel = None):
        # time1 = time.time()
        if SetupBot.GetPermsStats56(str(interaction.guild.id)) is True:
            if "manage_messages" not in [perm[0] for perm in interaction.user.guild_permissions if perm[1]]:
                return await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
        try:
            amount_of_wars = int(amount_of_wars)
            if int(amount_of_wars) < 0:
                await interaction.response.send_message("The number of wars is invalid! Use numbers `> 0` or type all", ephemeral=True)
                return
            limit = await self.calculate_limit(amount_of_wars, interaction.guild.id)
        except ValueError:
            if amount_of_wars == "all" or amount_of_wars is None:
                amount_of_wars = None
                limit = None
            else:
                return await interaction.response.send_message("The number of wars is invalid! Use numbers `> 0` or type all", ephemeral=True)
        if toadchannel is None:
            toadchannel_id = SetupBot.GetToadbot(str(interaction.guild.id))
            if toadchannel_id is None:
                return await interaction.response.send_message("No default toadbot channel is set! Either use the optional toadbot parameter or contact a leader to set a default toadbot channel!", ephemeral=True)
            toadchannel = self.bot.get_channel(int(toadchannel_id))
        delete_process_message = False
        process_msg = None
        try:
            if amount_of_wars > 10:
                process_msg = await interaction.channel.send("The process of the analysation might take a bit! Please be patient and don't add another command when it's not working in a few seconds!")
                delete_process_message = True
        except TypeError:
            process_msg = await interaction.channel.send("The process of the analysation might take a bit! Please be patient and don't add another command when it's not working in a few seconds!")
            delete_process_message = True

        await interaction.response.defer(ephemeral=False)
        all_differences = []
        not_toadbot = 0
        amount_of_races = 0
        async for i in toadchannel.history(limit=limit):
            while not_toadbot <= 200:
                embeds = i.embeds
                for embed in embeds:
                    try:
                        if embed.title.startswith("Score"):
                            not_toadbot = 0
                            amount_of_races += 1
                            all_differences.append(int(embed.fields[3].value))
                            if embed.fields[4].name == "Track" and embed.fields[3].name == "Difference":
                                map_embed = embed.fields[4].value
                                difference = embed.fields[3].value
                            else:
                                continue
                            self.map_dic[await self.convert_to_short_map(map_embed)]["difference"].append(
                                int(difference))
                    except IndexError:
                        continue
                    except AttributeError:
                        pass
                break
            else:
                await self.delete_process_message_func(process_msg, delete_process_message)
                return await interaction.followup.send("This isn't an toadbot channel! Set the default toadbot channel or the toadbot channel in your command to a valid toadbot channel!", ephemeral=True)

        embed_list = []
        if len(all_differences) == 0:
            embed_not_played = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])), title="Stats64")
            embed_not_played.set_thumbnail(url="https://media.discordapp.net/attachments/932023933392285706/932024135041814528/reFRZtransparent.png")
            embed_not_played.add_field(name=f"There was no map played in the amount of wars you entered!", value="Enter a higher amount!", inline=False)
            return await interaction.followup.send(embed=embed_not_played)
        data = await self.CalculateStatsData(all_differences, True)
        if amount_of_wars is None:
            embed_name = f"of all wars, "
        else:
            embed_name = f"of the last {amount_of_wars} wars, "
        embed = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/932023933392285706/932024135041814528/reFRZtransparent.png")
        embed.add_field(name=f"Overall stats from {embed_name}and of every map.", value="Here the stats:", inline=False)
        embed.add_field(name=f"Average score: ", value=f"{data['avg_difference']}", inline=False)
        embed.add_field(name=f"Maximum score: ", value=f"{data['max_difference']}", inline=False)
        embed.add_field(name=f"Minimum score: ", value=f"{data['min_difference']}", inline=False)
        embed_list.append(embed)

        stats64_map_dic = list(self.map_dic.items())

        def SortByAvg(lst):
            return sum(lst[1]["difference"]) / len(lst[1]["difference"])

        def SortByLen(lst):
            return len(lst[1]["difference"])

        do_order = None
        reverse = None
        if order_by.value == "default":
            do_order = False
        elif order_by.value == "best":
            do_order = True
            reverse = True
            key = SortByAvg
        elif order_by.value == "worst":
            do_order = True
            reverse = False
            key = SortByAvg
        elif order_by.value == "most":
            do_order = True
            reverse = True
            key = SortByLen

        if do_order is True:
            to_sort = []
            for i in stats64_map_dic:
                if i[1]["difference"]:
                    to_sort.append(i)

            stats64_map_dic = sorted(to_sort, key=key, reverse=reverse)

        for i in stats64_map_dic:
            map = i[1]["difference"]
            link = i[1]["link"]
            track_shown = i[1]["track_long"]
            if len(map) == 0:
                embed_not_played_map = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])))
                embed_not_played_map.set_thumbnail(url=link)
                embed_not_played_map.add_field(
                    name=f"{track_shown} wasn't played in the amount of wars, you entered!",
                    value="Enter a higher amount!", inline=False)
                embed_list.append(embed_not_played_map)
            else:
                embed_name = f"In the last {amount_of_wars} wars, "
                if amount_of_wars is None:
                    embed_name = f"In all ({round(amount_of_races / 12)}) wars, "
                amount_played = f"{len(map)} times"
                if len(map) == 1:
                    amount_played = "once"

                avg_difference = await self.addplus(round(sum(map) / len(map), 2))
                max_difference = await self.addplus(max(map))
                min_difference = await self.addplus(min(map))
                last_difference = await self.addplus(map[-1])
                embed_played_map = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])))
                embed_played_map.set_thumbnail(url=str(link))
                embed_played_map.add_field(name=f"{embed_name}{track_shown} was played {amount_played}.", value="Here the stats:", inline=False)
                embed_played_map.add_field(name=f"Average score: ", value=f"{avg_difference}", inline=False)
                embed_played_map.add_field(name=f"Last score: ", value=f"{last_difference}", inline=False)
                embed_played_map.add_field(name=f"Maximum score: ", value=f"{max_difference}", inline=False)
                embed_played_map.add_field(name=f"Minimum score: ", value=f"{min_difference}", inline=False)
                embed_list.append(embed_played_map)
            # time2 = time.time()

        stats64_msg1, stats64_msg2, stats64_msg3, stats64_msg4, stats64_msg5, stats64_msg6, stats64_msg7, stats64_msg8, stats64_msg9 = None, None, None, None, None, None, None, None, None
        try:
            stats64_msg1 = await interaction.followup.send(embed=embed_list[0])  # more messages because limit of embeds/message == 10
            await asyncio.sleep(1.2)
            stats64_msg2 = await interaction.channel.send(embeds=embed_list[1:9])
            await asyncio.sleep(1.2)
            stats64_msg3 = await interaction.channel.send(embeds=embed_list[9:17])
            await asyncio.sleep(1.2)
            stats64_msg4 = await interaction.channel.send(embeds=embed_list[17:25])
            await asyncio.sleep(1.2)
            stats64_msg5 = await interaction.channel.send(embeds=embed_list[25:33])
            await asyncio.sleep(1.2)
            stats64_msg6 = await interaction.channel.send(embeds=embed_list[33:41])
            await asyncio.sleep(1.2)
            stats64_msg7 = await interaction.channel.send(embeds=embed_list[41:49])
            await asyncio.sleep(1.2)
            stats64_msg8 = await interaction.channel.send(embeds=embed_list[49:57])
            await asyncio.sleep(1.2)
            stats64_msg9 = await interaction.channel.send(embeds=embed_list[57:])
        except discord.HTTPException:
            pass
        await self.delete_process_message_func(process_msg, delete_process_message)
        # await interaction.channel.send(f"This took** {int((time2 - time1) / 60)} minutes and {round((time2 - time1) % 60, 1)} seconds**", delete_after=5)
        delete_message = await interaction.channel.send("React to remove the messages again!", delete_after=60)
        await delete_message.add_reaction("❌")

        def CheckReaction(reaction, member):
            channel = reaction.message.channel.id == delete_message.channel.id
            user = member.id == interaction.user.id
            staff = "manage_messages" in [perm[0] for perm in interaction.user.guild_permissions if perm[1]]
            emoji = reaction.emoji == "❌"
            return channel and (user or staff) and emoji

        try:
            await self.bot.wait_for("reaction_add", check=CheckReaction, timeout=61)  # waits for reaction, in case the messages should be removed again
        except asyncio.exceptions.TimeoutError:
            return

        try:  # deletes all sent messages, no for loop because defining not possible without error in some cases (if filter used)
            await stats64_msg2.delete()
            await asyncio.sleep(0.2)
            await stats64_msg3.delete()
            await asyncio.sleep(0.2)
            await stats64_msg4.delete()
            await asyncio.sleep(0.2)
            await stats64_msg5.delete()
            await asyncio.sleep(0.2)
            await stats64_msg6.delete()
            await asyncio.sleep(0.2)
            await stats64_msg7.delete()
            await asyncio.sleep(0.2)
            await stats64_msg8.delete()
            await asyncio.sleep(0.2)
            await stats64_msg9.delete()
            await asyncio.sleep(0.2)
        except discord.app_commands.CommandInvokeError:
            await stats64_msg1.delete()
        except AttributeError:
            await stats64_msg1.delete()
        except discord.errors.NotFound:
            pass
        try:
            await delete_message.delete()
        except discord.errors.NotFound:
            pass
        return

    @app_commands.command(name="overallstats", description="Shows the stats of every map!")
    @app_commands.describe(amount_of_wars="The amount of wars you want to have analysed, either an integer or 'all'", toadchannel="Overwrites the default toadchannel from the setup command")
    @app_commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def overallstats(self, interaction: discord.Interaction, amount_of_wars: str, toadchannel: discord.TextChannel = None):
        try:
            amount_of_wars = int(amount_of_wars)
            if int(amount_of_wars) < 0:
                return await interaction.response.send_message("The number of wars is invalid! Use numbers `> 0` or type all", ephemeral=True)
            limit = await self.calculate_limit(amount_of_wars, interaction.guild.id)
        except ValueError:
            if amount_of_wars == "all" or amount_of_wars is None:
                amount_of_wars = None
                limit = None
            else:
                return await interaction.response.send_message("The number of wars is invalid! Use numbers `> 0` or type all", ephemeral=True)
        if toadchannel is None:
            toadchannel_id = SetupBot.GetToadbot(str(interaction.guild.id))
            if toadchannel_id is None:
                return await interaction.response.send_message("No default toadbot channel is set! Either use the optional toadbot parameter or contact a leader to set a default toadbot channel!", ephemeral=True)
            toadchannel = self.bot.get_channel(int(toadchannel_id))

        delete_process_message = False
        process_msg = None
        try:
            if amount_of_wars > 10:
                process_msg = await interaction.channel.send("The process of the analysation might take a bit! Please be patient and don't add another command when it's not working in a few seconds!")
                delete_process_message = True
        except TypeError:
            process_msg = await interaction.channel.send("The process of the analysation might take a bit! Please be patient and don't add another command when it's not working in a few seconds!")
            delete_process_message = True

        await interaction.response.defer(ephemeral=False)
        all_differences = []
        not_toadbot = 0
        amount_of_races = 0
        async for i in toadchannel.history(limit=limit):
            while not_toadbot <= 200:
                not_toadbot += 1
                embeds = i.embeds
                for embed in embeds:
                    try:
                        if embed.title.startswith("Score") and embed.fields[3].name == "Difference":
                            amount_of_races += 1
                            all_differences.append(int(embed.fields[3].value))
                            not_toadbot = 0
                    except IndexError:
                        continue
                break
            else:
                await self.delete_process_message_func(process_msg, delete_process_message)
                await asyncio.sleep(0.2)
                return await interaction.followup.send("This isn't an toadbot channel! Set the default toadbot channel or the toadbot channel in your command to a valid toadbot channel!", ephemeral=True)

        if len(all_differences) == 0:
            embed = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])), title="Overallstats")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/932023933392285706/932024135041814528/reFRZtransparent.png")
            embed.add_field(name=f"There was no map played in the amount of wars you entered!", value="Enter a higher amount!", inline=False)
        else:
            if amount_of_wars is None:
                embed_name = f"of all ({round(amount_of_races / 12)}( wars, "
            else:
                embed_name = f"of the last {amount_of_wars} wars, "
            avg_difference = await self.addplus(round(sum(all_differences) / len(all_differences), 2))
            max_difference = await self.addplus(max(all_differences))
            min_difference = await self.addplus(min(all_differences))
            embed = discord.Embed(colour=discord.Colour((config["MAIN_COLOR"])))
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/932023933392285706/932024135041814528/reFRZtransparent.png")
            embed.add_field(name=f"Overall stats from {embed_name}and of every map.", value="Here the stats:", inline=False)
            embed.add_field(name=f"Average score: ", value=f"{avg_difference}", inline=False)
            embed.add_field(name=f"Maximum score: ", value=f"{max_difference}", inline=False)
            embed.add_field(name=f"Minimum score: ", value=f"{min_difference}", inline=False)

        await interaction.followup.send(embed=embed)
        return await self.delete_process_message_func(process_msg, delete_process_message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Stats(bot),
    )
