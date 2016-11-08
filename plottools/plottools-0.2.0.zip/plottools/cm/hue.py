
import numpy as np
from matplotlib.colors import ListedColormap
from colorspacious import cspace_converter 


_JCh_to_sRGB1 = cspace_converter('JCh', 'sRGB1')
  
cm_data = []
for i in range(256):
    RGBi = np.clip(_JCh_to_sRGB1( (50,100,360.*i/255) ),0,1)
    cm_data.append( list(RGBi) )

test_cm = ListedColormap(cm_data, name=__file__)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    try:
        from viscm import viscm
        viscm(test_cm)
    except ImportError:
        print("viscm not found, falling back on simple display")
        plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto',
                   cmap=test_cm)
    plt.show()
