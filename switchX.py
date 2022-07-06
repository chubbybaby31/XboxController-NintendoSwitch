import argparse
import asyncio
import logging
import os
from contextlib import contextmanager
import random
import time
import controller

from joycontrol import logging_default as log
from joycontrol.controller_state import ControllerState, button_push, StickState
from joycontrol.protocol import controller_protocol_factory, Controller
from joycontrol.server import create_hid_server

# For debugging:
#logger = logging.getLogger(__name__)
#log.configure()


# terminate any running instances of Xbobdrv
os.system("pkill xboxdrv")
j=controller.XboxController()
currentButton=""
controller = Controller.PRO_CONTROLLER
switchBTADDR=None
if not os.geteuid() == 0:
	raise PermissionError(' [-] Script must be run as root!')


async def _main(controller, reconnect_bt_addr, spi_flash):
	factory = controller_protocol_factory(controller, spi_flash=spi_flash)
	ctl_psm, itr_psm = 17, 19
	transport, protocol = await create_hid_server(factory, ctl_psm=17, itr_psm=19,  device_id=None, reconnect_bt_addr=reconnect_bt_addr)
	await letItRain(protocol.get_controller_state())
	await transport.close()

async def letItRain(controller_state: ControllerState):
	try:
		enabled=True
		calibration = None
		lstick = controller_state.l_stick_state
		rstick = controller_state.r_stick_state
		button_state = controller_state.button_state

		# Button status
		upStatus=False
		downStatus=False
		leftStatus=False
		rightStatus=False
		homeStatus=False
		minusStatus=False
		plusStatus=False
		l_stickStatus=False
		r_stickStatus=False
		aStatus=False
		bStatus=False
		xStatus=False
		yStatus=False
		lStatus=False
		rStatus=False
		zlStatus=False
		zrStatus=False
		waitTime=0

		await controller_state.connect()
		print(" [+] Connected to Switch!")
		while enabled:
			if j.connected:
				# Analog sticks are our priority
				leftX = j.LeftJoystickX
				leftY = j.LeftJoystickY
				rightX = j.RightJoystickX
				rightY = j.RightJoystickY
				rstick.set_h(int(rightX))
				rstick.set_v(int(rightY))
				lstick.set_h(int(leftX))
				lstick.set_v(int(leftY))
				await asyncio.sleep(0)

				if j.UpDPad == 1:
					upStatus=True
					button_state.set_button('up')
					await controller_state.send()
				elif j.UpDPad == 0 and upStatus:
					upStatus=False
					button_state.set_button('up', pushed=False)
					await controller_state.send()
				if j.DownDPad == 1:
					downStatus=True
					button_state.set_button('down')
					await controller_state.send()
				elif j.DownDPad == 0 and downStatus:
					downStatus=False
					button_state.set_button('down', pushed=False)
					await controller_state.send()

				if j.LeftDPad == 1:
					leftStatus=True
					button_state.set_button('left')
					await controller_state.send()
				elif j.LeftDPad == 0 and leftStatus:
					leftStatus=False
					button_state.set_button('left', pushed=False)
					await controller_state.send()
				if j.RightDPad == 1:
					rightStatus=True
					button_state.set_button('right')
					await controller_state.send()
				elif j.RightDPad == 0 and rightStatus:
					rightStatus=False
					button_state.set_button('right', pushed=False)
					await controller_state.send()
				if j.home == 1:
					waitTime = waitTime+1
					homeStatus=True
					button_state.set_button('home')
					await controller_state.send()
				elif j.home == 0 and homeStatus:
					homeStatus=False
					waitStatus=waitTime
					waitTime=0
					button_state.set_button('home', pushed=False)
					await controller_state.send()
					if(waitStatus > 20):
						await button_push(controller_state,'b')
						await button_push(controller_state,'capture')

				if j.Back == 1:
					minusStatus=True
					button_state.set_button('minus')
					await controller_state.send()
				elif j.Back == 0 and minusStatus:
					minusStatus=False
					button_state.set_button('minus', pushed=False)
					await controller_state.send()

				if j.Start == 1:
					plusStatus=True
					button_state.set_button('plus')
					await controller_state.send()
				elif j.Start == 0 and plusStatus:
					plusStatus=False
					button_state.set_button('plus', pushed=False)
					await controller_state.send()

				if j.LeftThumb == 1:
					l_stickStatus=True
					button_state.set_button('l_stick')
					await controller_state.send()
				elif j.LeftThumb == 0 and l_stickStatus:
					l_stickStatus=False
					button_state.set_button('l_stick', pushed=False)
					await controller_state.send()

				if j.RightThumb == 1:
					r_stickStatus=True
					button_state.set_button('r_stick')
					await controller_state.send()
				elif j.RightThumb == 0 and r_stickStatus:
					r_stickStatus=False
					button_state.set_button('r_stick', pushed=False)
					await controller_state.send()

				if j.A == 1:
					bStatus=True
					button_state.set_button('b')
					await controller_state.send()
				elif j.A == 0 and bStatus:
					bStatus=False
					button_state.set_button('b', pushed=False)
					await controller_state.send()

				if j.B == 1:
					aStatus=True
					button_state.set_button('a')
					await controller_state.send()
				elif j.B == 0 and aStatus:
					aStatus=False
					button_state.set_button('a', pushed=False)
					await controller_state.send()

				if j.X == 1:
					yStatus=True
					button_state.set_button('y')
					await controller_state.send()
				elif j.X == 0 and yStatus:
					yStatus=False
					button_state.set_button('y', pushed=False)
					await controller_state.send()

				if j.Y == 1:
					xStatus=True
					button_state.set_button('x')
					await controller_state.send()
				elif j.Y == 0 and xStatus:
					xStatus=False
					button_state.set_button('x', pushed=False)
					await controller_state.send()

				if j.LeftBumper == 1:
					lStatus=True
					button_state.set_button('l')
					await controller_state.send()
				elif j.LeftBumper == 0 and lStatus:
					lStatus=False
					button_state.set_button('l', pushed=False)
					await controller_state.send()

				if j.RightBumper == 1:
					rStatus=True
					button_state.set_button('r')
					await controller_state.send()
				elif j.RightBumper == 0 and rStatus:
					rStatus=False
					button_state.set_button('r', pushed=False)
					await controller_state.send()

				if j.LeftTrigger == 1:
					zlStatus=True
					button_state.set_button('zl')
					await controller_state.send()
				elif j.LeftTrigger == 0 and zlStatus:
					zlStatus=False
					button_state.set_button('zl', pushed=False)
					await controller_state.send()

				if j.RightTrigger == 1:
					zrStatus=True
					button_state.set_button('zr')
					await controller_state.send()
				elif j.RightTrigger == 0 and zrStatus:
					zrStatus=False
					button_state.set_button('zr', pushed=False)
					await controller_state.send()


	finally:
		j.close()
with open("controller.bin", 'rb') as spi_flash_file:
		spi_flash = spi_flash_file.read()

# Check for config file
try:
    configFile = open("config.ini")
    temp=configFile.readline().rstrip()				# First line should always be mac address of a paired console
    if "SwitchBTADDR" in temp:
    	temp = temp.split("=")
    	switchBTADDR = str(temp[1])
    	print(" [+] Paired to Switch with BT address : "+ switchBTADDR)
    configFile.close()
except IOError:
    print(" [+] Initiating pairing with a Switch Console.")
    switchBTADDR = None

    

if switchBTADDR != None:
	print(" [+] Connecting to paired Switch Console.")

loop = asyncio.get_event_loop()
loop.run_until_complete(_main(controller,switchBTADDR,spi_flash))


