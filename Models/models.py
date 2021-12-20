from enum import Enum


class Pins:
    def __init__(self, arduino_pin, repeat, timeout, maxvalue, threshold,
                 compare, minvalue, starting_value, function, input_type):
        self.arduinoPin = arduino_pin,
        self.canRepeat = repeat,
        self.timeout = timeout,
        self.maxValue = maxvalue,
        self.threshold = threshold,
        self.compare = compare,
        self.minValue = minvalue,
        self.startingValue = starting_value,
        self.function = function
        self.inputType = input_type
        self.lastState = False


class InputType(Enum):
    ANALOG = "a"
    DIGITAL = "d"
