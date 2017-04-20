# MTB
A project for recognizing and counting mountain bikers and people walking in the forrest using a small thermal camera.

![box_content](data/examples/box.png "Content of bird box") ![setup_example](data/examples/marked_box.png "Bird box placed in tree with view of path") ![output_example](data/examples/Intensity2.png "Example of a captured thermal image(mapped to fit 8bit)")  

## TODO
This overall todo list is prioritized accoring to what needs to be done first.
1) Contributing to scientific paper writing(deadline 12/5 2017)[AVSS](http://mivia.unisa.it/sav/)
2) Capturing and annotating data
3) Bringing the HW and SW of the prototype to a stage where the system can easily be used by non-technical persons
4) Implement improvements to e.g. the detection and tracking
5) Automated data collection by use of e.g. data connection + presentation of data


# Software
The project is primarily written in python, originally some parts were written in c++ but later every component should now be available in python.

## Getting up and running
More details on using either of the two primary groups of code is described in detail in their respective readmes.

### Data capture
"thermal capture" contains the program and scripts that runs on the raspberry pi for capturing and storing 16 bit 80x60 images at 7 fps to sd card.

### Data processing
"data processing" contains code for preparing and processing the frames after they have been captured on the raspberry pi.

detection

evaluation

#### Annotations
The annotations are located under /data/annotations/ in this repository. 
TODO: annotate events in remaining clips(4)

Event annotation using [RUBA](https://bitbucket.org/aauvap/ruba/downloads/)

BB annotation using [BBA](https://bitbucket.org/aauvap/bounding-box-annotator/downloads/)

# Hardware
Computer: Raspberry Pi 2

Thermal camera: Lepton LWIR 80 × 60

Power: 10.400mAh
