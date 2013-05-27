#!/usr/bin/env python

__author__ = "Rita Giordano"
__copyright__ = "Copyright 2013, PSI "
__credits__ = ["Rita Giordano", "Ezequiele Panepucci", "Meitian Wang"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Rita Giordano"
__email__ = "rita.giordano@psi.ch"
__status__ = "Beta"


"""
    This code, plot the cbf images and show where the selected spot are located. By clickling on the spot is possible to show a zoom of the spot and the spot profile in X and Y. The coordinates of the highest peak and the integrated intensity of the spot will be also show in the frame.
"""

from optparse import OptionParser

# Options to run the code from command line.

parser = OptionParser()

parser.add_option("-i", "--image", dest="image",
                  help="A CBF image from a still measurement.")

parser.add_option("--csv-input", dest="csv_input",
                  help="The filename for the output in CSV format.")

parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

if options.image is None or options.csv_input is None:
    parser.print_help()
    parser.error('All options are mandatory.')

print 'The input CBF file name is %s' % (options.image,)
print 'The input CSV file name is %s' % (options.csv_input,)

if options.verbose:
    print "I should be more talktative."

print options

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr


r=robjects.r

# Import DISP package to read the cbf images and the other R packages.
disp = importr('DISP')
utilis = importr('utils')
graphics = importr('graphics')
grDev = importr('grDevices')

# Read R script to zoom on the spot. This function will also show the spot profile. 
f=file("/Users/giordano_r/Desktop/Rscript/zoomDisp.R")
code=''.join(f.readlines())
result = robjects.r(code)
zoom = rpy2.robjects.globalenv['zoom']
ident = rpy2.robjects.globalenv['ident']

# Display the cbf images with ths spot 
dty = robjects.r('readCBF("'+options.image+'")')
data=utilis.read_csv(options.csv_input)
x = data.rx2(2)
y = data.rx2(3)
grDev.X11()
graphics.par(mfrow=[2,2])
disp.disp(dty)
graphics.points(x,y,col='red', cex=0.5)
ident(dty,x,y)
raw_input()