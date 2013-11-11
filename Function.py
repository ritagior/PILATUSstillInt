# Definition of the function used in the code:

__author__ = "Rita Giordano"
__copyright__ = "Copyright 2013, PSI "
__credits__ = ["Rita Giordano", "Ezequiel Panepucci", "Meitian Wang"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Rita Giordano"
__email__ = "rita.giordano@psi.ch"
__status__ = "Beta"


def matCal(mat):
    s = mat.sum()
    sup = mat.max()
    return s, sup

# Coefficient of Variation
def cv(f):
    #cv = np.std(f)/np.mean(f)
    cv = f.std()/f.mean()
    return cv

#Calculation of rms:
def rmsd(f,n):
    rmsd = np.sqrt(np.sum(np.square(f))/n)
    return rmsd

def rmsd_r(f1,f2,n):
    rmsd_r = np.sqrt(np.sum(np.square(f1/f2))/n)
    return rmsd_r


# Function to calculate the distance in pixel of the spot from the beam center.
def distPx(Xspot,beamX,Yspot,beamY):
    distPx = np.sqrt(np.square(Xspot-Xbeam)+np.square(Yspot-Ybeam))

# Distance on the detector from the direct beam.
def distM(distPx):
    distM = 0.172 * distPx

#Function defining the resolution of each spot
# w= wavelength
def res(w,distM,detectorDistance):
    res = w/(2*sin(0.5*atan(distM/detectorDistance)))



# Diplay PILATUS images with the selected spot using red circle.
def plotCBF(cbf,x,y):
    disp.disp(cbf)
    for items in position:
        graphics.points(x,y, col='red')

    


    
