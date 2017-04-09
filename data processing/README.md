# MTB
MTB counting project.

The current detector is implemented in [dlib](https://github.com/davisking/dlib) and is described in this [paper](https://arxiv.org/abs/1502.00046). Because of the special loss function proposed in the paper, the detector can achive great performance using a very limited number training samples. Recently, the same detector has been made available using CNN features instead of HoG. It could be interesting to try the CNN features.

# Instructions
The program was created by Mark Philip Philipsen. 

The file and dir structure of the project is as list here:
. 
├── README.md


To run the program:
python main.py -p ...

To execute experimental code(e.g. unfinished or extra visualization):
python experiment.py -p ...
