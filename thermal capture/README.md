# Boot mode

The raspberry pi will boot up in one of two ways, immediately recording or to commandline where the user interface can be started. Which one, depends on whether the following line is commended out in

- $ `sudo nano /etc/profile`

comment/uncomment last line `# sudo python /home/pi/startupCapture/capture.py`

The capture program is executed from a script that runs when booting up. If you want to stop the automatic capturing, simply interrupt using ctrl + c

To start user interface from commandline, type:
```bash
startx
```

# Data transfer

When transferring files, use filezilla. The large number of files cannot be transferred to usb stick or compressed to e.g. .zip
