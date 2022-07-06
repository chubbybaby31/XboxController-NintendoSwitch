# XboxController-NintendoSwitch
Control your Nintendo Switch with an Xbox Controller using a raspberry pi

### Requirements
1 - Raspberry Pi (This projected was only tested with Raspberry pi 4 but any Raspberry Pi with bluetooth capabilities should work)

2 - Micro SD card with 8GB or more of storage

3 - USB-A to Micro-USB cable to connect XBox One controller to Pi

4 - Xbox One controller

### Installation
Install Rasbperry Pi OS onto your Raspberry Pi's Micro SD card: https://www.raspberrypi.com/software/

Clone this repository onto your Pi's home directory
```
git clone https://github.com/chubbybaby31/XboxController-NintendoSwitch.git
```
Install the required dependencies and setup auto-run on boot
(Make sure to run setup.py as root user)
```
cd XboxController-NintendoSwitch
sudo python3 setup.py
```
Install the dbus-python and libhidapi-hidraw0 packages
```
sudo apt install python3-dbus libhidapi-hidraw0
```

The Switch can not connect to the ports of the emulated controller, if the "input" plugin in Bluez is enabled.
To disable it we must edit ```/lib/systemd/system/bluetooth.service```
```
sudo nano /lib/systemd/system/bluetooth.service
```
Then change the line ```ExecStart=/usr/lib/bluetooth/bluetoothd``` to ```ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=input```

Now restart the bluetooth services
```
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
```

### Usage
Once installed, reboot your Raspberry Pi and connect your Controller to the Pi via USB

When the Pi boots back up the Xbox controller should vibrate. (If the controller doesn't automatically turn on after vibration you may have to manually turn it on by pressing the Xbox button)

Turn on your switch and navigate to the Change Grip/Order menu

After a couple minutes you should see a Pro-Controller paired to the switch (If this does not happen, reboot the Raspberry Pi and try again)

Keep pressing B on you controller (pressing B on Xbox Controller will be A on the switch) until you leave the Change Grip/Order Menu.

The Pi may lose connection with the switch after leaving the menu but should recconect after a couple seconds (If it does not recconect, reboot the Pi and try again)

Once recconected you can now use your Xbox Controller as a Nintendo Switch Pro Conotroller

### Credit
This project is a modified verison of https://github.com/Aodrulez/SwitchX and is heavily reliant on https://github.com/mart1nro/joycontrol

