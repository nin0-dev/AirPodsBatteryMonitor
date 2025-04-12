#!/usr/bin/python
import sys
from bt.service import Service
from aap.watchers.battery_watcher import BatteryWatcher
from aap.enums.enums import BatteryType
import asyncio
import json
from datetime import datetime

address = sys.argv[1]
psm = 0x1001
service = Service(address, psm)
battery = BatteryWatcher()

def handle_battery(b):
    data = {
        "charge": {},
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # [type, percent, status]
    for item in battery.battery: 
        match item[0]:
            case BatteryType.Left:
                data["charge"]["left"] = item[1]
                data["charging_left"] = item[2] == "Charging"
            case BatteryType.Right:
                data["charge"]["right"] = item[1]
                data["charging_right"] = item[2] == "Charging"
            case BatteryType.Case:
                data["charge"]["case"] = item[1]
                data["charging_case"] = item[2] == "Charging"
                
    with open("/tmp/airpods.json", "w") as f:
        json.dump(data, f)

    

service.subscribe(battery.process_response)
battery.subscribe(handle_battery)

if __name__ == "__main__":
    def run_service():
        try:
            asyncio.run(service.start())
        except Exception as e:
            print(e)
            run_service()

    run_service()