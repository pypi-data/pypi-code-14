# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

from .class_algebra import ClassAlgebra
from . import geometry
import matplotlib.pyplot as plt

class WrongNumLayers(Exception):
    pass

class IterableLaminate(object):

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.list[index]

        elif isinstance(index, slice):
            return type(self)(*self.list[index])

    def __setitem__(self, index, v):
        if isinstance(index, int):
            self.list[index] = v
            
        elif isinstance(index, slice):
            if isinstance(v,IterableLaminate):
                self.list[index] = v.list
            elif isinstance(v,list):
                self.list[index] = v
            else:
                raise(Exception())

    def __iter__(self):
        for item in self.list:
            yield item

    def __len__(self):
        return len(self.list)

class Laminate(IterableLaminate,ClassAlgebra):
    def __init__(self, *layers):
        self.layers = list(layers)
        self.id = id(self)

    def copy(self,identical = True):
        new = type(self)(*[layer.copy(identical) for layer in self.layers])
        if identical:        
            new.id = self.id
        return new

    def plot(self,new=False):
        import matplotlib.cm
        cm = matplotlib.cm.plasma
        l = len(self.layers)        
        if new:
            plt.figure()
        for ii,geom in enumerate(self.layers):
            geom.plot(color = cm((ii)/(l)))

    def plot_layers(self):
        import matplotlib.cm
        cm = matplotlib.cm.plasma
        l = len(self.layers)        
        for ii,geom in enumerate(self.layers):
            plt.figure()
            geom.plot(color = cm((ii)/(l)))
    
    @property
    def list(self):
        return self.layers

    def binary_operation(self,function_name,other,*args,**kwargs):
        if len(self.layers)!=len(other.layers):
            raise(WrongNumLayers())
        else:
            layers = []
            for layer1,layer2 in zip(self.layers,other.layers):
                function = getattr(layer1,function_name)
                layers.append(function(layer2))
            return type(self)(*layers)

    def unary_operation(self,function_name,*args,**kwargs):
            layers = []
            for layer1 in self.layers:
                function = getattr(layer1,function_name)
                layers.append(function(*args,**kwargs))
            return type(self)(*layers)
            
    def union(self,other):
        return self.binary_operation('union',other)

    def difference(self,other):
        return self.binary_operation('difference',other)

    def symmetric_difference(self,other):
        return self.binary_operation('symmetric_difference',other)

    def intersection(self,other):
        return self.binary_operation('intersection',other)
    
    def buffer(self,*args,**kwargs):
        return self.unary_operation('buffer',*args,**kwargs)

    def dilate(self,*args,**kwargs):
        return self.unary_operation('dilate',*args,**kwargs)

    def erode(self,*args,**kwargs):
        return self.unary_operation('erode',*args,**kwargs)

    def translate(self,*args,**kwargs):
        return self.unary_operation('translate',*args,**kwargs)
        
    def rotate(self,*args,**kwargs):
        return self.unary_operation('rotate',*args,**kwargs)

    def scale(self,*args,**kwargs):
        return self.unary_operation('scale',*args,**kwargs)

    def affine_transform(self,*args,**kwargs):
        return self.unary_operation('affine_transform',*args,**kwargs)

    def map_line_stretch(self,*args,**kwargs):
        import math
        import numpy

        p1 = numpy.array(args[0])
        p2 = numpy.array(args[1])
        p3 = numpy.array(args[2])
        p4 = numpy.array(args[3])

        x_axis = numpy.array([1,0])

        pre_rotate = geometry.planar_angle(x_axis,p2-p1)
        post_rotate = geometry.planar_angle(x_axis,p4-p3)
        scale = geometry.length(p4-p3)/geometry.length(p2-p1)

        laminate = self.translate(*(-p1))
        laminate = laminate.rotate(-pre_rotate*180/math.pi,origin=(0,0))
        laminate = laminate.affine_transform([scale,0,0,1,0,0])
        laminate = laminate.rotate((post_rotate)*180/math.pi,origin=(0,0))
        laminate = laminate.translate(*p3)
        return laminate
        
    def export_dxf(self,name):
        for ii,layer in enumerate(self.layers):
            layername = name+str(ii)
            layer.export_dxf(layername)
    def mesh_items(self,thickness = None):
        if thickness is None:
            thickness = [1]*len(self)
        import matplotlib.cm as cm
        mi = []
#        lines = []
        z = 0
        for ii,(layer,t) in enumerate(zip(self,thickness)):
            color1 = list(cm.plasma(ii/(len(self))))
            mi.extend(layer.mesh_items(z,color1))
        #    color1[3] = .1
            z+=t
        return mi
        