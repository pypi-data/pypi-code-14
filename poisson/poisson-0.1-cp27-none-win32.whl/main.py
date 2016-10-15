# -*- coding: utf-8 -*-
import poisson.pypoissonMG as pypoissonMG
import numpy
import time
import math
import matplotlib.tri as tri
import matplotlib.pyplot as plt


TYPE_CARTESIAN = 10
TYPE_AXIAL = 11
TYPE_AXIAL_VECT = 12
TYPE_POLAR = 13

RESTRICTION_INJECTION = 20
RESTRICTION_HALFWEIGHTING = 21
RESTRICTION_FULLWEIGHTING = 22


            
class Poisson:
    def __init__(self,pw_min,ph_min,levels,w,h,x0=0.0,y0=0.0,restriction=RESTRICTION_INJECTION):
        self.px = pw_min+levels-1
        self.py = ph_min+levels-1
        self.finegrid = 2**(levels-1)
        self.width = 2**self.px+1
        self.height = 2**self.py+1
        self.dx = w*1.0/(2**self.px)
        self.dy = h*1.0/(2**self.py)
        self.w = w*1.0
        self.h = h*1.0
        self.coord = "cartesian"
        self.x0 = x0
        self.y0 = y0
        self.extent = (x0,x0+w,y0,y0+h)
        pypoissonMG.open(TYPE_CARTESIAN,pw_min,ph_min,levels,w,h,restriction)
  
    def close(self):
        pypoissonMG.close()
    def laplacien(self):
        pypoissonMG.laplacien()
    def get_optimal_omega(self):
        r = (self.dx/self.dy)**2
        rho = (math.cos(math.pi/self.width)+r*math.cos(math.pi/self.height))/(1.0+r)
        return 2.0/(1.0+math.sqrt(1-rho*rho))    
    def dirichlet_borders(self,value):
        pypoissonMG.dirichlet_borders(value)
    def dirichlet_polygon(self,istart,jstart,lilist,ljlist,value):
        pypoissonMG.dirichlet_polygon(int(istart),int(jstart),lilist,ljlist,value)
    def source(self,i,j,s):
        pypoissonMG.source(int(i),int(j),s)        
    def source_polygon(self,istart,jstart,lilist,ljlist,source):
        pypoissonMG.source_polygon(int(istart),int(jstart),lilist,ljlist,source)       
    def source_rect(self,ci,cj,width,height,s):
        pypoissonMG.source_rect(int(ci),int(cj),int(width),int(height),s)
    def neumann_borders(self,source,derivX1,derivX2,derivY1,derivY2):
        pypoissonMG.neumann_borders(source,derivX1,derivX2,derivY1,derivY2)
    def neumann_polygon(self,istart,jstart,lilist,ljlist,derivXlist,derivYlist,source):
        pypoissonMG.neumann_polygon(int(istart),int(jstart),lilist,ljlist,derivXlist,derivYlist,source)
    def interface_polygon(self,istart,jstart,lilist,ljlist,source,a1,a2):
        pypoissonMG.interface_polygon(int(istart),int(jstart),lilist,ljlist,source,a1,a2)
    def sinus_mode(self,mx,my):
        pypoissonMG.sinus_mode(mx,my)
    def step_mode(self):
        pypoissonMG.step_mode()        
    def init_array(self):
        pypoissonMG.init_array()      
    def iterations(self,niter,threads=1,omega=1.0):
        if threads==1:
            pypoissonMG.finegrid_iterations(niter,omega)
        elif threads==2:
            pypoissonMG.finegrid_iterations_2threads(niter,omega)
        elif threads==4:
            pypoissonMG.finegrid_iterations_4threads(niter,omega)
        else:
            pypoissonMG.finegrid_iterations(niter,omega)
    def get_residu_norm(self):
        return pypoissonMG.get_finegrid_residu_norm()
    def iterations_norm(self,niter,nblocks,threads=1,omega=1.0):
        i = 0
        ni = [i]
        norm = [pypoissonMG.get_finegrid_array_norm()]
        if threads==1:
            iterations = pypoissonMG.finegrid_iterations
        elif threads==2:
            iterations = pypoissonMG.finegrid_iterations_2threads
        elif threads==4:
            iterations = pypoissonMG.finegrid_iterations_4threads
        else:
            iterations = pypoissonMG.finegrid_iterations
        for b in range(nblocks):
            iterations(niter,omega)
            i += niter
            ni.append(i)
            n = pypoissonMG.get_finegrid_array_norm()
            norm.append(n)
            #print("norm = %f"%n)
        return [ni,norm]
    def opencl_platforms(self):
        pypoissonMG.opencl_platforms()
    def set_opencl_platform_device(self,platform,device):
        pypoissonMG.set_opencl_platform_device(platform,device)        
    def opencl_iterations(self,niter,omega=1.0):
        pypoissonMG.opencl_init()
        pypoissonMG.opencl_create_memory_finegrid()
        pypoissonMG.opencl_iterations_finegrid(niter,omega)
        pypoissonMG.opencl_release_memory_finegrid()
        pypoissonMG.opencl_release()
    def opencl_iterations_norm(self,niter,nblock,omega=1.0):
        pypoissonMG.opencl_init()
        pypoissonMG.opencl_create_memory_finegrid()
        i = 0
        ni = [i]
        norm = [pypoissonMG.get_finegrid_array_norm()]
        for b in range(nblock):
            pypoissonMG.opencl_iterations_finegrid(niter,omega)
            i += niter
            ni.append(i)
            norm.append(pypoissonMG.get_finegrid_array_norm())
        pypoissonMG.opencl_release_memory_finegrid()
        pypoissonMG.opencl_release()
        return [ni,norm]
    def multigrid_iterations_norm(self,nsteps,nlevels,niter_list,nblocks,omega=1.0,tolerance=1.0e-6):
        if nlevels*2-1 != len(niter_list):
            raise RuntimeError("Erreur de définition du multigrille")
        n = nlevels*2-1
        wu = 0
        r = 1.0
        l = 0
        for l in range(nlevels-1):
            wu += 1.0/r*(niter_list[l]+niter_list[n-1-l])
            r *= 4
        if l!=0:
            l += 1
        wu += 1.0/r*niter_list[l]
        wu *= nsteps
        i = 0
        ni = [i]
        norm = [pypoissonMG.get_finegrid_array_norm()]
        b = 0
        residu = 1.0
        while b<nblocks and residu>tolerance:
            pypoissonMG.multigrid_iterations(nsteps,nlevels,niter_list,omega)
            residu = pypoissonMG.get_finegrid_residu_norm()
            print("Résidu : %g"%residu)
            i += wu
            ni.append(i)
            norm.append(pypoissonMG.get_finegrid_array_norm())
            b += 1
        return [ni,norm]
    def multigrid_Vcycles_norm(self,nsteps,nlevels,niter,nu1,nu2,nblocks,tolerance=1.0e-8):
        n = nlevels*2-1
        wu = 0
        r = 1.0
        for l in range(nlevels-1):
            wu += 1.0/r*(nu1+nu2)
            r *= 4
        wu += 1.0/r*niter
        wu *= nsteps
        i = 0
        ni = [i]
        norm = [pypoissonMG.get_finegrid_array_norm()]
        b = 0
        residu = 1.0
        while b<nblocks and residu>tolerance:
            pypoissonMG.multigrid_Vcycles(nsteps,nlevels,niter,nu1,nu2)
            residu = pypoissonMG.get_finegrid_residu_norm()
            print("Résidu : %g"%residu)
            i += wu
            ni.append(i)
            norm.append(pypoissonMG.get_finegrid_array_norm())
            b += 1
        return [ni,norm]

    def multigrid_full_norm(self,mcycle,nlevels,niter,nu1,nu2):
        norm = [pypoissonMG.get_finegrid_array_norm()]
        wu = pypoissonMG.multigrid_full(mcycle,nlevels,niter,nu1,nu2)
        residu = pypoissonMG.get_finegrid_residu_norm()
        print("Résidu : %g"%residu)
        norm.append(pypoissonMG.get_finegrid_array_norm())
        print("WU : %g"%wu)
        return [[0,wu],norm]
       
    def get_array(self,symetry=0):
        return pypoissonMG.get_array(symetry)
    def get_extent(self,symetry=0):
        if symetry!=0:
            return (self.x0,self.x0+self.w,self.y0-self.h,self.y0+self.h)
        else:
            return (self.x0,self.x0+self.w,self.y0,self.y0+self.h)
    def get_mask(self,symetry=0):
        return pypoissonMG.get_mask(symetry)    
    def get_derivX(self,symetry=False):
        return pypoissonMG.get_derivX(symetry)  
    def get_derivY(self,symetry=False):
        return pypoissonMG.get_derivY(symetry)
    def get_x(self):
        return numpy.arange(self.x0,self.x0+self.w,self.w/(self.width))
    def get_y(self):
        return numpy.arange(self.y0,self.y0+self.h,self.h/(self.height))
    def get_z(self):
        return self.get_x()
    def get_r(self,symetry=0):
        if symetry:
            n = 2**(self.py+1)+1
            dr = 2*self.h/(n-1)
            r = numpy.zeros(n)
            for k in range(n):
                r[k] = -self.h+k*dr
            return r
        else:    
            return self.get_y()
        
class PoissonAxial(Poisson):
    def __init__(self,pw_min,ph_min,levels,w,h,x0=0.0,y0=0.0,restriction=RESTRICTION_INJECTION):
        self.px = pw_min+levels-1
        self.py = ph_min+levels-1
        self.finegrid = 2**(levels-1)
        self.width = 2**self.px+1
        self.height = 2**self.py+1
        self.dx = w*1.0/(2**self.px)
        self.dy = h*1.0/(2**self.py)
        self.w = w*1.0
        self.h = h*1.0
        self.coord = "axial"
        self.x0 = x0
        self.y0 = y0
        self.extent = (x0,x0+w,y0,y0+h)
        pypoissonMG.open(TYPE_AXIAL,pw_min,ph_min,levels,w,h,restriction)
    def get_derivZ(self,symetry=False):
        return pypoissonMG.get_derivX(symetry)  
    def get_derivR(self,symetry=False):
        return pypoissonMG.get_derivY(symetry)
    def get_derivRUR(self,symetry=False):
        return pypoissonMG.get_derivRUR_axial(symetry)
        
class PoissonAxialVect(Poisson):
    def __init__(self,pw_min,ph_min,levels,w,h,x0=0.0,y0=0.0,restriction=RESTRICTION_INJECTION):
        self.px = pw_min+levels-1
        self.py = ph_min+levels-1
        self.finegrid = 2**(levels-1)
        self.width = 2**self.px+1
        self.height = 2**self.py+1
        self.dx = w*1.0/(2**self.px)
        self.dy = h*1.0/(2**self.py)
        self.w = w*1.0
        self.h = h*1.0
        self.coord = "axialvect"
        self.x0 = x0
        self.y0 = y0
        self.extent = (x0,x0+w,y0,y0+h)
        pypoissonMG.open(TYPE_AXIAL_VECT,pw_min,ph_min,levels,w,h,restriction)
    def get_derivZ(self,symetry=False):
        return pypoissonMG.get_derivX(symetry)  
    def get_derivR(self,symetry=False):
        return pypoissonMG.get_derivX(symetry)
    def get_derivRUR(self,symetry=False):
        return pypoissonMG.get_derivRUR_axial(symetry)
    def get_z(self):
        return self.get_x()
    def get_r(self,symetry=0):
        if symetry:
            n = 2**(self.py+1)+1
            dr = 2*self.h/(n-1)
            r = numpy.zeros(n)
            for k in range(n):
                r[k] = -self.h+k*dr
            return r
        else:    
            return self.get_y()

class PoissonPolar(Poisson):
    def __init__(self,pw_min,ph_min,levels,w,h,x0=0.0,y0=0.0,restriction=RESTRICTION_INJECTION):
        self.px = pw_min+levels-1
        self.py = ph_min+levels-1
        self.finegrid = 2**(levels-1)
        self.width = 2**self.px
        self.height = 2**self.py+1
        self.dx = w*1.0/(2**self.px)
        self.dy = h*1.0/(2**self.py)
        self.w = w*1.0
        self.h = h*1.0
        self.coord = "polar"
        self.x0 = x0
        self.y0 = y0
        self.extent = (x0,x0+w,y0,y0+h)
        pypoissonMG.open(TYPE_POLAR,pw_min,ph_min,levels,w,h,restriction)
    def neumann_border_ext(self,source,value):
        pypoissonMG.neumann_border_ext_polar(source,value)
    def neumann_border_int(self,j,source,value):
        pypoissonMG.neumann_border_int_polar(int(j),source,value)
    def get_theta(self):
        return numpy.arange(0,self.width)*2*math.pi/self.width
    def get_r(self):
        return self.get_y()        
    def get_derivTheta(self):
        return pypoissonMG.get_derivTheta_polar()
    def opencl_platforms(self):
        raise RuntimeError("OpenCL non disponible en coordonnées polaires")
    def set_opencl_platform_device(self,platform,device):
        raise RuntimeError("OpenCL non disponible en coordonnées polaires")        
    def opencl_iterations(self,niter,omega=1.0):
        raise RuntimeError("OpenCL non disponible en coordonnées polaires")
    def opencl_iterations_norm(self,niter,nblock,omega=1.0):
        raise RuntimeError("OpenCL non disponible en coordonnées polaires")
    def get_xyu(self):
        U = self.get_array().flatten()
        U = numpy.delete(U,range(1,self.width))
        x = numpy.zeros(self.width*(self.height-1)+1)
        y = numpy.zeros(self.width*(self.height-1)+1)
        dtheta = 2*math.pi/self.width
        dr = self.dy
        x[0] = 0.0
        y[0] = 0.0
        k = 1
        for j in range(1,self.height):
            r = dr*j
            for i in range(self.width):
                theta = dtheta*i
                x[k] = r*math.cos(theta)
                y[k] = r*math.sin(theta)
                k += 1
        return (x,y,U)
    def contourplot(self,n):
        (x,y,U) = self.get_xyu()
        plt.tricontour(x,y,U,n)
    def colorplot(self,shading,cmap=plt.cm.jet):
        (x,y,U) = self.get_xyu()
        plt.tripcolor(x,y,U,shading=shading,cmap=cmap)        
    
