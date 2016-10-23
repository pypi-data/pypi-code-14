def KelvinToCelsius(x):
    assert (x >= 0),"Mas frio que el cero absoluto"
    return x-273

kelvin = -1
print(str(kelvin)+"K = "+str(KelvinToCelsius(kelvin))+"ºC")
