# Boot mode

The raspberry pi will boot up in one of two ways, immediately recording or to commandline where the user interface can be started. Which one, depends on whether the following line is commended out in

- $ `sudo nano /etc/profile`

comment/uncomment last line `# sudo python /home/pi/startupCapture/capture.py`

The capture program is executed from a script that runs when booting up. If you want to stop the automatic capturing, simply interrupt using ctrl + c

To start user interface from commandline, type:
```bash
startx
```

# Data storage

The captured frames are stored in folders on the desktop. Since the clock is only set when connected to the internet and stops when the power is disconnected it is never correct when recording in the wild, the time stamps mostly used to create folders that are unique.

You might need to delete the captured data using the commandline when cleaning up:

- $ `cd /home/pi/Desktop/output/`
- $ `rm -rf 2017-xx-xx-xx-xx`

# Data transfer

When transferring files, use filezilla. The large number of files cannot be transferred to usb stick or compressed to e.g. .zip

# TODO

The camera can be unstable and unreachable. Reasons might be a loose connection or unstable voltage resulting in bad initialization. Current solution reboot or unplug camera and keep trying. If capturing, a green LED will blick with a spacing of a few seconds because of disk activity. This should be improved so the system is more robust and it should be easier to see if things are working.

Currently I'm unable to get in contract with the camera. 

The code is based on this example: https://github.com/groupgets/pylepton try getting that to work. 

