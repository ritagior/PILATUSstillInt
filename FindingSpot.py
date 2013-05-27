#!/usr/bin/env python
## Python code to select and read the spot from cbf images for PILATUS detector.


__author__ = "Rita Giordano"
__copyright__ = "Copyright 2013, PSI "
__credits__ = ["Rita Giordano", "Ezequiel Panepucci", "Meitian Wang"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Rita Giordano"
__email__ = "rita.giordano@psi.ch"
__status__ = "Beta"


"""
    This code read the first still image collect using the R package DISP.
    This image is used to find the spot position, which will be used for the others images.
    The output of this code will produce a csv file containing:

"""


from optparse import OptionParser

# Options to run the code from command line.

parser = OptionParser()

parser.add_option("-i", "--image", dest="image",
                  help="A CBF image from a still measurement.")

parser.add_option("-p", "--peak", dest="peak",type="int", default=500,
                  help="Minimum integrated peak height for the selection of the spot; default = 500.")

parser.add_option("--min-pixel-count", dest="min_pixel_count", type="int", default=500,
                  help="Minimum pixel count of strongest pixel in peak box; default = 500.")

parser.add_option("--csv-output", dest="csv_output",
                  help="The filename for the output in CSV format.")

parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

if options.image is None or options.csv_output is None:
    parser.print_help()
    parser.error('All options are mandatory.')

print options

print 'The input CBF file name is %s' % (options.image,)
print 'The output CSV file name is %s' % (options.csv_output,)

if options.verbose:
    print "I should be more talktative."


import rpy2
import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import sys
from rpy2.robjects.numpy2ri import numpy2ri
rpy2.robjects.numpy2ri.activate()
#import rpy2.robjects.numpy2ri
#import rpy2.robjects.lib.ggplot2 as ggplot2
#import math, datetime
#from rpy2.robjects import IntVector, Formula
#from rpy2.robjects import Environment
#import rpy2.rinterface
import time
#import csv
from Function import *



r=robjects.r

# Import DISP package to read the cbf images and the other R packages.
disp = importr('DISP')
#grdevices = importr('grDevices')
#reshape = importr('reshape2')    ### for the function melt
#stats = importr('stats')
base = importr('base')
utilis = importr('utils')
graphics = importr('graphics')
grDev = importr('grDevices')


# Read a CBF images using DISP function readCBF, transpose the matrix and transform to a NUMPY array.
dty = robjects.r('readCBF("'+options.image+'")')
dty_t=dty.transpose()
a = np.array(dty_t)

# Calculate the dimension of the matrix, in this case the code will
dimCBF = base.dim(dty)
x = dimCBF[0]
y = dimCBF[1]

# Define the initial coordinate of the measurement box, starting for the top left corner of the image.
X0i=0
X0f=15
Y0i=0
Y0f=15
centerPosition = X0f * Y0f / 2 # means highest pixel count is in center of measurement box

### Definition of empty array to be fill in the next for loop
measurement_box = []
position_measurement_box = []
position_peak = []
append = measurement_box.append
append1 = position_peak.append
coorappend = position_measurement_box.append
t=time.time()

## Select the measurement box. This loop will start for the measurement box with coordinates[Y0i:Y0f,X0i:X0f], it will read each pixel of the detector imahes and will find the good measurement box containing the spot. The criterias for the spot selection are: 1) the sum of the pixels in measurement box, definded as 'stat[0]', > 5000 counts; 2) The maximum value on the matrix mb > 500 and 3) the peak should lie in the center of the measurement box.

print " This calculation will takes about 5 minutes, you have the time for a coffee :) "

for i in xrange(0,x):
    for j in xrange(0,y):
        m=a[Y0i+j:Y0f+j,X0i+i:X0f+i]
        stat = matCal(m)
        Yc=((Y0i+j)+(Y0f+j))/2
        Xc=((X0i+i)+(X0f+i))/2
        Y=[Y0i+j,Y0f+j]
        X=[X0i+i,X0f+i]
        if (stat[0]>options.peak and stat[1]> options.min_pixel_count and
            m.argmax()== centerPosition):
            append(m)
            append1((Xc,Yc))
            coorappend((Y,X))
        del m
print "run time: %.3f s" % (time.time()-t)


## Calculate the maximum peak for each spot
max_peak = []
for h in measurement_box:
    max_peak.append(h.max())

# Define the parameter to be write in the output file.
max_peak_Array = np.array(max_peak)
pos_peak_Array = np.array(position_peak)
pos_measurement_box_Array = np.array(position_measurement_box)

# Convert the numpy array to rpy objects.

max_peak_R = robjects.conversion.py2ri(max_peak_Array)
pos_peak_R = robjects.conversion.py2ri(pos_peak_Array)
pos_measurement_box_R = robjects.conversion.py2ri(pos_measurement_box_Array)

### Create a data frame with the maximum peak, the position of the peak and the measurement box of the spot.
dataf = {'Peak': max_peak_R, 'Coor': pos_peak_R, 'MeasB': pos_measurement_box_R}
dataframe = robjects.DataFrame(dataf)

utilis.write_csv(dataframe, options.csv_output)

# Using DISP package display the post found previously

f=file("/Users/giordano_r/Desktop/Rscript/zoomDisp.R")
code=''.join(f.readlines())
result = robjects.r(code)
zoom = rpy2.robjects.globalenv['zoom']
ident = rpy2.robjects.globalenv['ident']

grDev.X11()
graphics.par(mfrow=[2,2])
disp.disp(dty)
x = []
y = []
for item in position_peak:
    graphics.points(item[0],item[1],col='red', cex=0.5)
    x.append(item[0])
    y.append(item[1])

x = np.array(x)
y = np.array(y)
ident(dty,x,y)

raw_input()

