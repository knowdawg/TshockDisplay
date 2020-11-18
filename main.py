import requests
import time

from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010

def get_team_color(team_num):
    team_colors = { 0: "none", 1: "Red", 2: "Green", 3: "Blue", 4: "Yellow", 5: "Pink"}
    return "Team:" + team_colors[team_num]

def main():
    # rev.1 users set port=0
    # substitute spi(device=0, port=0) below if using that interface
    # substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
    serial = i2c(port=1, address=0x3C)

    # substitute ssd1331(...) or sh1106(...) below if using that device
    device = ssd1306(serial)

    while True:
        resp = requests.get('http://192.168.1.14:7878/v2/server/status?players=true')
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /server/status/ {}'.format(resp.status_code))
        results = resp.json()

        if True:
            players = results['players']
        else:
            players = [
                {"nickname": "Knowdawg",
                "username": "",
                "group": "guest",
                "active": true,
                "state": 10,
                "team": 0},
                {"nickname": "Bob",
                "username": "",
                "group": "guest",
                "active": true,
                "state": 10,
                "team": 0},
            ]


        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            for i, player in enumerate(players):
                draw.text((5, 5 + (i*10)), f'{player["nickname"]} {get_team_color(player["team"])}', fill="white")
        time.sleep(1)

if __name__ == "__main__":
    main()