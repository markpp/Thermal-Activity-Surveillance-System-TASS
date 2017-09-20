# MTB
MTB counting project.

# TODO
1. Try to get an overview of what each program/script does(especially those located under tools). Write it down in short in this README file and in the file it self.
    * see `/data processing/tools/copyActivityFrames.py` for an example of what the comment in if `__name__ == "__main__":` could look like.
2. Use my findFramesOfInterrest cpp program to create list of interesting areas(frame numbers) in the clips
    * Better idea: implement the same functionality but using python
3. Convert the found frame numbers into hours, min and sec after 11.00 using `frame_number2time_stamp.py`
4. Combine the frames into video clips because that is what RUBA takes
    * Possibly resize to higher resolution
5. Use RUBA to annotate events in the remaining clips using the frame numbers you found in (2.)
6. Use `data processing/main.py` to preview my bounding box annotations on each of the clips
7. Create a program to preview event annotations, e.g. show frames that are in an interval around events

present results:
- Confusion matrix
- Cumulative graph - count vs. frame_nr
- Prgram timing

On the raspberry pi, install dlib using this - sudo python setup.py install --yes USE_AVXINSTRUCTIONS --compiler-flags "-O3 -mfpu=neon" to fully utilize the arm in the pi
# Method

# Detector
The current detector is implemented in [dlib](https://github.com/davisking/dlib) and is described in this [paper](https://arxiv.org/abs/1502.00046). Because of the special loss function proposed in the paper, the detector can achieve great performance using a very limited number training samples. Recently, the same detector has been made available using CNN features instead of HoG. It could be interesting to try the CNN features.

Current performance 

c 9

MTB detector evaluation:
- Training accuracy: precision: 0.94032, recall: 0.941005, average precision: 0.931985
- Testing accuracy: precision: 0.939781, recall: 0.770189, average precision: 0.746143
PED detector evaluation:
- Training accuracy: precision: 0.898455, recall: 0.962175, average precision: 0.94484
- Testing accuracy: precision: 0.879433, recall: 0.709924, average precision: 0.682731

0.82s no optimization, 1 upsampling
0.44s with optimization, 1 upsampling

# Tracking


# Instructions

The zipped frames must be extracted :sleepy:

The frames may happen to be oriented wrongly or single frames may be corrupted. Scripts for fixing stuff like this should be available in /data processing/tools/

The first and last part of each clip should be discarded because it contains the person that put up and take down the camera. These parts of the clips can usually be found using the find activity script.

To run the program:
```bash
main.py -p ../data/testing/2016-08-09-14-58-testing/ -a ../data/annotations/bb/2016-08-09-14-58_bb.csv -f 723
```

Allmost everything is run from main.py, in the bottom of the file you can call different functions that e.g. train a detector, run the detector on a number of frames, preview bounding box annotations.

There is currently a problem with the tracker, when you have finished the current TODO list we will look at that.

## Install

### MacOS

Since the detector is from dlib it must be installed along with dependencies:
```bash
brew install boost --with-python
```

```bash
brew install boost-python
```

clone https://github.com/davisking/dlib

```bash
python setup.py install --yes USE_AVX_INSTRUCTIONS
```

Kalman filter:
- $ `pip install filterpy`


tracker:
- $ `pip install munkres`

### Linux

use `apt-get install` to install boost, boost-python and possibly pip

use pip to install python dependencies them same way as on MacOS
