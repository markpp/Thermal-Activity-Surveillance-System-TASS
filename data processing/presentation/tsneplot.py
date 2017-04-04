#
#  tsne.py
#
# Implementation of t-SNE in Python. The implementation was tested on Python 2.7.10, and it requires a working
# installation of NumPy. The implementation comes with an example on the MNIST dataset. In order to plot the
# results of this example, a working installation of matplotlib is required.
#
# The example can be run by executing: `ipython tsne.py`
#
#
#  Created by Laurens van der Maaten on 20-12-08.
#  Copyright (c) 2008 Tilburg University. All rights reserved.

import numpy as Math
import pylab as Plot
import cPickle as pickle

if __name__ == "__main__":
	
	with open('MTBdata.pickle', 'rb') as f:
		inputData = pickle.load(f)
	
	Y = Math.array(inputData['data'])
	#dictStructure = {'X' : np.array(entrail), 'Y' : np.array(label)}
	#labels = Math.loadtxt("mnist2500_labels.txt");
	Plot.scatter(Y[:,0], Y[:,1], s=40, c=inputData['labels']);
	#print 'her'
	Plot.show();
