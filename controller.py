from inputs import get_gamepad
import math
import threading

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.connected = True

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0
        self.home = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this method
        ly = self.LeftJoystickY
        ry = self.RightJoystickY
        lx = self.LeftJoystickX
        rx = self.RightJoystickX
        return [lx, ly, rx, ry]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    rawLY = (event.state * -1) + 32769
                    ly = (((rawLY - 1) * (0xfff - 0)) / (65536 - 1)) + 0
                    self.LeftJoystickY = ly
                elif event.code == 'ABS_X':
                    rawLX = event.state  + 32769
                    lx = (((rawLX - 1) * (0xfff - 0)) / (65536 - 1)) + 0
                    self.LeftJoystickX = lx
                elif event.code == 'ABS_RY':
                    rawRY = (event.state * -1) + 32769
                    ry = (((rawRY - 1) * (0xfff - 0)) / (65536 - 1)) + 0
                    self.RightJoystickY = ry
                elif event.code == 'ABS_RX':
                    rawRX = event.state + 32769
                    rx = (((rawRX - 1) * (0xfff - 0)) / (65536 - 1)) + 0
                    self.RightJoystickX = rx
                elif event.code == 'ABS_Z':
                    if event.state / XboxController.MAX_TRIG_VAL > 0.5:
                        self.LeftTrigger = 1 # normalize between 0 and 1
                    else:
                        self.LeftTrigger = 0
                elif event.code == 'ABS_RZ':
                    if event.state / XboxController.MAX_TRIG_VAL > 0.5:
                        self.RightTrigger = 1 # normalize between 0 and 1
                    else:
                        self.RightTrigger = 0
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state
                elif event.code == 'BTN_WEST':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'ABS_HAT0X' and event.state == -1:
                    self.LeftDPad = 1
                elif event.code == 'ABS_HAT0X' and event.state == 1:
                    self.RightDPad = 1
                elif event.code == 'ABS_HAT0Y' and event.state == -1:
                    self.UpDPad = 1
                elif event.code == 'ABS_HAT0Y' and event.state == 1:
                    self.DownDPad = 1
                elif event.code == 'ABS_HAT0Y' and event.state == 0:
                    if self.UpDPad == 1: self.UpDPad = 0
                    else: self.DownDPad = 0
                elif event.code == 'ABS_HAT0X' and event.state == 0:
                    if self.RightDPad == 1: self.RightDPad = 0
                    else: self.LeftDPad = 0
                elif event.code == 'BTN_MODE':
                    self.home = event.state
    def close(self):
        print("done")
        
#joy = XboxController()
#while True:
#   print(joy.read())
