import pyfirmata
import time
from SimConnect import *
import logging
from SimConnect.Enum import *
from time import sleep
import json
from types import SimpleNamespace

def get_setting():

    # f = open('data.json')
    # data = json.load(f)

    return json.loads(open('settings.json.json'), object_hook=lambda d: SimpleNamespace(**d))


def valideteinput(prompt):
    try:
        trt = float(prompt) * 1000
        return trt
        # there is no need to use another variable here, just return the conversion,
        # if it fail it will try again because it is inside this infinite loop
    except:
        print("Return 600")
        return 600


if __name__ == "__main__":


    print("Program Start Up")

    logging.basicConfig(level=logging.DEBUG)
    LOGGER = logging.getLogger(__name__)
    LOGGER.info("START")
    # time holder for inline commands
    ct_g = millis()


    board = pyfirmata.Arduino("COM3")
    it = pyfirmata.util.Iterator(board)
    it.start()
    # creat simconnection and pass used user classes
    sm = SimConnect()
    ae = AircraftEvents(sm)
    aq = AircraftRequests(sm)


    print("Board Initialized")
    SpeedBluePot = board.get_pin("a:0:i")
    HeadingWhitePot = board.get_pin("a:1:i")
    AltitudeGreenPot = board.get_pin("a:2:i")
    VerticalSpeedBlackPot = board.get_pin("a:3:i")
    xAxis = board.get_pin("a:4:i")
    yAxis = board.get_pin("a:5:i")

    BL = board.get_pin('d:5:i')
    BML = board.get_pin('d:4:i')
    BMR = board.get_pin('d:3:i')
    BR = board.get_pin('d:2:i')

    # PARKING_BRAKES = Event(b'PARKING_BRAKES', sm)
    # long path
    PARKING_BRAKES = ae.Miscellaneous_Systems.PARKING_BRAKES
    # using get
    GEAR_TOGGLE = ae.Miscellaneous_Systems.get("GEAR_TOGGLE")

    # Increase Heading
    INC_HEADING = ae.Autopilot.HEADING_BUG_INC
    DEC_HEADING = ae.Autopilot.HEADING_BUG_DEC
    # Increase Speed
    INC_SPEED = ae.Autopilot.AP_SPD_VAR_INC
    DEC_SPEED = ae.Autopilot.AP_SPD_VAR_DEC
    # Increase Altitude
    INC_ALT = ae.Autopilot.AP_ALT_VAR_INC
    DEC_ALT = ae.Autopilot.AP_ALT_VAR_DEC
    # Increase VerticalSpeed
    INC_VES = ae.Autopilot.AP_VS_VAR_INC
    DEC_VES = ae.Autopilot.AP_VS_VAR_DEC

    time.sleep(1)

    print("Started")

    while not sm.quit:
        print("Reading")
        # Speed Start
        if valideteinput(SpeedBluePot.read()) > 750:
            INC_SPEED()
            print("Speed Increase")
        elif valideteinput(SpeedBluePot.read()) < 550:
            DEC_SPEED()
            print("Speed Decrease")
        # Speed End

        # Heading Start
        if valideteinput(HeadingWhitePot.read()) > 750:
            INC_HEADING()
            print("Heading Increase")
        elif valideteinput(HeadingWhitePot.read()) < 550:
            DEC_HEADING()
            print("Heading Decrease")
        # Heading End

        # Altitude Start
        if valideteinput(AltitudeGreenPot.read()) > 750:
            INC_ALT()
            print("Altitude Increase")
        elif valideteinput(AltitudeGreenPot.read()) < 550:
            DEC_ALT()
            print("Altitude Decrease")
        # Altitude End

        # VerticalSpeed Start
        if valideteinput(VerticalSpeedBlackPot.read()) > 750:
            INC_VES()
            print("VerticalSpeed Increase")
        elif valideteinput(VerticalSpeedBlackPot.read()) < 550:
            DEC_VES()
            print("VerticalSpeed Decrease")
        # VerticalSpeed End
        print("Read End")
        time.sleep(0.1)
