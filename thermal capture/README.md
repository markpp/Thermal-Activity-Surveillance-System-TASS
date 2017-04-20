
NB: A few things are out of date and needs to be updated

To start user interface, type:
```bash
startx
```

The capture program is executed from a script that runs when booting up. To enable/disable automatic capture on boot up:

- $ `sudo nano /etc/profile`

comment/uncomment last line “sudo python /home/pi/startupCapture/capture.py

When transferring files, use filezilla. The large number of files cannot be transferred to usb stick or compressed to e.g. .zip
