#!/usr/bin/env python

__author__ = "Rita Giordano"
__copyright__ = "Copyright 2013, PSI "
__credits__ = ["Rita Giordano", "Ezequiel Panepucci", "Meitian Wang"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Rita Giordano"
__email__ = "rita.giordano@psi.ch"
__status__ = "Beta"


"""
    This code will read the spot position and the coordinates of the measurement box previously calculated with FindingSpot.py.
    The csv-input will be the csv-output form FindingSpot.py.
    ReadSpot.py will read all the still images and will found the same spit as in the first still images.
    The output will be in the form:
    Xp Yp Intensity_i cv
    Where (Xp,Yp) are the coordinated of the peak. Intensity_i with i=1...n is the images index and cv in the coefficent of variation.
    
"""

### Import all packages necessary for the code

import rpy2
import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import sys
from rpy2.robjects.numpy2ri import numpy2ri
rpy2.robjects.numpy2ri.activate()
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects import IntVector, Formula
from rpy2.robjects import Environment
import rpy2.rinterface
import time
import csv
from Function import *

from optparse import OptionParser


parser = OptionParser()

parser.add_option("-i", "--images", dest="images",
                  help="All CBF images from a still measurement; replace image index number with the quotation character '?' for example: liso_1_?.cbf")

parser.add_option("--csv-input", dest="csv_input",
                  help="The filename for the input in CSV coming from FindingSpots.py")

parser.add_option("--csv-output", dest="csv_output",
                  help="The filename for the output CSV .....")

parser.add_option("--num-frames", dest="num_frames", type="int",
                  help="The number of frames to analyze.")

parser.add_option("-q", "--quiet",
                  action="store_true", dest="verbose", default=False,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

print options

print 'The input CBF file name is %s' % (options.images,)
print 'The output CSV file name is %s' % (options.csv_output,)

if options.verbose:
    print "I should be more talktative."

#sys.exit()



r=robjects.r

# Import R package (DISP) to read the cbf images and the other R packages that will be used in the code.
disp = importr('DISP')
grdevices = importr('grDevices')
reshape = importr('reshape2')    ### for the function melt
#stats = importr('stats')
#base = importr('base')
utilis = importr('utils')

## Read the spot position and the coordinates of the measurement box for each spot previously founded
## using only the first images.

data=utilis.read_csv(options.csv_input)#data1=data.replace('dataSpot.csv',sys.argv[1])
Xp = data.rx2(2)
Yp = data.rx2(3)
Peak = data.rx2(4)
Yi = data.rx2(5)
Xi = data.rx2(6)
Yf = data.rx2(7)
Xf = data.rx2(8)

Xbox = zip(Xi,Xf)
Ybox = zip(Yi,Yf)
## Create a tuple with coordinates of the measurement box.
Measbox = zip(Yi, Yf, Xi, Xf)

## Define the path where are the files.
## Open the images.

I = []
sigma = []
Isigma = []
PeakI = []
t=time.time()
for i in range(1,options.num_frames):
    filename=options.images.replace('?','%05d' % i)
    dty = robjects.r('readCBF("'+filename+'")').transpose()
    a = np.array(dty)
    NewboxI = []
    NewboxS = []
    NewboxIS = []
    NewboxIpeak = []
    for item in Measbox:
        box = a[item[0]:item[1],item[2]:item[3]]
        m=matCal(box)
        NewboxI.append(m[0])
        NewboxS.append(m[1])
        NewboxIS.append(m[2])
        NewboxIpeak.append(m[3])
    I.append(NewboxI)
    sigma.append(NewboxS)
    Isigma.append(NewboxIS)
    PeakI.append(NewboxIpeak)
print "run time: %.3f s" % (time.time()-t)
Iarray = np.array(I)

### Create a data frame with 

#ofile = open(options.csv_output, 'wb')
ofile = open('temp.csv','wb')
writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
header = ['XP', 'YP']

for i in range(1,options.num_frames+1):
    header.append('Int_im_' + str(i))

writer.writerow(header)

for idx,j in enumerate(Iarray[0]):
    row = []
    row.append(Xp[idx])
    row.append(Yp[idx])
    row.extend(Iarray[:,idx])
    writer.writerow(row)
ofile.close()

# Read the intensity file and calculated the cv for each spot in the file.
#dataf = robjects.DataFrame.from_csvfile(options.csv_output)
dataf = robjects.DataFrame.from_csvfile('temp.csv')
number_of_peaks = len(dataf[0])
cvI = []
newRow = []
for i in range(1,number_of_peaks+1):
    row = dataf.rx(i,True)
    rowA = np.array(row)
    newRow.append(rowA[2:])
    cvI.append(cv(rowA[2:]))
cv_r=robjects.conversion.py2ri(cvI)
df_cv = {'CV' : cv_r}
dataf_cv = robjects.DataFrame(df_cv)
dtf_cv = robjects.r.melt(dataf_cv)
d=dataf.cbind(dtf_cv.rx(2))
d.names[tuple(d.colnames).index('value')] = 'CV'
utilis.write_csv(d, options.csv_output)

# Plot the cv of reflection for all images using ggplot2: http://had.co.nz/ggplot2/

dc = dtf_cv.cbind(n_peak = robjects.IntVector(range(1,number_of_peaks)))
gp = ggplot2.ggplot(db)
pp=gp+ggplot2.aes_string(x='n_peak',y='value') + ggplot2.geom_point()+ggplot2.theme_bw()+ ggplot2.ggtitle('Coefficient of Variation')+ \
ggplot2.scale_x_continuous("Number of Peaks")+ ggplot2.scale_y_continuous("CV")

r.X11()

pp.plot()




