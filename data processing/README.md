# MTB
MTB counting project.

The current detector is implemented in [dlib](https://github.com/davisking/dlib) and is described in this [paper](https://arxiv.org/abs/1502.00046). Because of the special loss function proposed in the paper, the detector can achive great performance using a very limited number training samples. Recently, the same detector has been made available using CNN features instead of HoG. It could be interesting to try the CNN features.

# Instructions

The zipped frames must be extracted :sleepy:

The frames may happen to be oriented wrongly or single frames may be corrupted. Scripts for fixing stuff like this should be available in /data processing/tools/

To run the program:
```bash
main.py -p ../data/testing/2016-08-09-14-58-testing/ -a ../data/annotations/bb/2016-08-09-14-58_bb.csv -f 723
```

Allmost everything is run from main.py, in the bottom of the file you can call different functions that e.g. train a detector, run the detector on a number of frames, preview bounding box annotations.

There is currently a problem with the tracker ...



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
