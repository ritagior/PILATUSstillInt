#!/usr/bin/env python

import rpy2
import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import sys
from rpy2.robjects.numpy2ri import numpy2ri
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects import FloatVector
import math, datetime
import array
from rpy2.robjects import IntVector, Formula
from rpy2.robjects import Environment
from Function import *

from optparse import OptionParser

__author__ = "Rita Giordano"
__copyright__ = "Copyright 2013, PSI "
__credits__ = ["Rita Giordano", "Ezequiel Panepucci", "Meitian Wang"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Rita Giordano"
__email__ = "rita.giordano@psi.ch"
__status__ = "Beta"

parser = OptionParser()

parser.add_option("--csv-input", dest="csv_input",
                  help="The filename for the input in CSV coming from FindingSpots.py")

parser.add_option("--csv-output", dest="csv_output",
                  help="The filename for the output CSV .....")

parser.add_option("-q", "--quiet",
                  action="store_true", dest="verbose", default=False,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

print options



r=robjects.r

# Import DISP package
disp = importr('DISP')
grdevices = importr('grDevices')
reshape = importr('reshape2')    ### for the function melt
stats = importr('stats')
base = importr('base')
utilis = importr('utils')
graphics = importr('graphics')

# Read the intensity value
dataf = robjects.DataFrame.from_csvfile(options.csv_input)

number_of_peaks = len(dataf[0])


cvI = []
newRow = []
for i in range(1,number_of_peaks+1):
    row = dataf.rx(i,True)
    rowA = np.array(row)
    newRow.append(rowA[2:])
    cvI.append(cv(rowA[2:]))
#cv.append(rowA[2:].std()/rowA[2:].mean())
cv_r=robjects.conversion.py2ri(cvI)
df_cv = {'CV' : cv_r}
dataf_cv = robjects.DataFrame(df_cv)
dtf_cv = robjects.r.melt(dataf_cv)
d=dataf.cbind(dtf_cv.rx(2))
d.names[tuple(d.colnames).index('value')] = 'CV'
#d = base.merge_data_frame(dataf,dtf_cv.rx(2))
utilis.write_csv(d, options.csv_output)


dc = dtf_cv.cbind(n_peak = robjects.IntVector(range(1,number_of_peaks+1)))
#n_peak = robjects.IntVector(1,number_of_peaks)
gp = ggplot2.ggplot(dc)
pp=gp+ggplot2.aes_string(x='n_peak',y='value') + ggplot2.geom_point()+ggplot2.theme_bw()+ ggplot2.ggtitle('Coefficient of Variation')+ \
ggplot2.scale_x_continuous("Number of Peaks")+ ggplot2.scale_y_continuous("CV")

r.X11()
pp.plot()

