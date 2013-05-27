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
    sigma = mat.std()
    return s, sup, sigma


def cv(f):
    cv = f.std()/f.mean()
    return cv

def rmsd(f,n):
    rmsd = np.sqrt(np.sum(np.square(f))/n)
    return rmsd

def rmsd_r(f1,f2,n):
    rmsd_r = np.sqrt(np.sum(np.square(f1/f2))/n)
    return rmsd_r


# Diplay PILATUS images with the selected spot using red circle.
def plotCBF(cbf,x,y):
    disp.disp(cbf)
    for items in position:
        graphics.points(x,y, col='red')

    


    