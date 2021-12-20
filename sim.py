import pyfirmata
import time
from SimConnect import *
import logging
from SimConnect.Enum import *
from time import sleep
import json
from types import SimpleNamespace

from Models.models import Pins
from Models.models import InputType


def get_settings():
    with open('settings.json.json', 'r') as f:
        return json.load(f)


def validateinput(prompt):
    try:
        trt = float(prompt) * 1000
        return trt
    except:
        print("Return 600")
        return 600


def get_pyfirmata(settings):
    return pyfirmata.util.Iterator(pyfirmata.Arduino(settings["comm_port"]))


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    LOGGER = logging.getLogger(__name__)
    LOGGER.info("Program Start")

    LOGGER.info("Simulation Setup")
    settings = get_settings()
    arduinoBoard = get_pyfirmata(settings)
    simulation = SimConnect()
    aircraftEvents = AircraftEvents(simulation)
    aircraftRequests = AircraftRequests(simulation)

    inputs = []

    LOGGER.info("Simulation Setup")
    for pin in settings["pins"]:
        inputs.append(
            Pins(
                arduinoBoard.get_pin(pin["input_type"] + ":" + pin["pin_number"] + ":" + "i"),
                pin["can_repeat"],
                pin["timeout"],
                pin["max_value"],
                pin["threshold"],
                pin["compare"],
                pin["min_value"],
                pin["starting_value"],
                aircraftEvents.find(pin["function"]),
                pin["inputType"]
            )
        )

    time.sleep(1)

    LOGGER.info("Simulation Loop")
    while not simulation.quit:

        for pin in inputs:
            if pin.inputType == InputType.ANALOG:
                if validateinput(pin.arduinoPin.read()) > pin.threshold and pin.compare:
                    pin.function()
                elif validateinput(pin.arduinoPin.read()) < pin.threshold and not pin.compare:
                    pin.function()
            elif pin.inputType == InputType.DIGITAL:
                if pin.arduinoPin.read():
                    if pin.canRepeat:
                        pin.function()
                    elif pin.lastState:
                        pin.function()
                        pin.lastState = True
                    else:
                        pin.lastState = False
        time.sleep(0.1)
