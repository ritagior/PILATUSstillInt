### R package necessary to run the code:
rpy2
R:
    1.  DISP from me not the version from David Watermann 
    2.  grDevices from CRAN
    3.  reshape2  from CRAN
    4.  stats included in R 
    5.  base  included in R
    6.  utils included in R
    7.  graphics included in R
    9.  ggplot2

From me:
zoomDisp.R    

USAGE:

./FindingSpot.py -i 'image path' --csv-output 'filename: file contatining the peak position and the position of the measurement box.'

./ReadSpot.py -i 'images path' --csv-input 'filename: This sould be the output from FindingSpot.py' --csv-output 'filename: this is the output with the intesntity for each images with the cv value'

This code will plot only on still images with the spot, including spot zoom and spot profile.

./DispCBF.py -i 'image path' --csv-input 'csv file containing the spot positions.This is the file in putput from FindingSpot.py'
