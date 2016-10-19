# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 16:06:39 2016

@author: Suhas Somnath
"""

# TODO: Make SHO guess and fit work on any dataset
# TODO: Modularize to the extent possible

from __future__ import division # int/int = float

from multiprocessing import cpu_count
from time import time as getTicks
from warnings import warn

import numpy as np
from BESHOutils import visualizeSHOResults
from ufitter.SHO_lib import SHO_fast_fit, SHO_func
from ufitter.fitting_model import ufitter_model
from ufitter.universal_fitter import ufitter
from ..io.BEutils import maxReadPixels, reshapeToOneStep, reshapeToNsteps
from ..io.SPMnode import MicroDataset, MicroDataGroup
from ..io.ioHDF5 import ioHDF5
from ..io.ioUtils import checkIfMain, getDataSet, getAuxData, getAvailableMem, getH5DsetRefs, findH5group, \
    getH5RegRefIndices, createRefFromIndices

from pycroscopy.io.be_hdf_utils import isReshapable
from pycroscopy.io.hdf_utils import copyRegionRefs, buildReducedSpec

sho32 = np.dtype([('Amplitude [V]',np.float32),('Frequency [Hz]',np.float32),('Quality Factor',np.float32),('Phase [rad]',np.float32),('R2 Criterion',np.float32)])

class BESHOFitter(object):
    '''
    This class enables calculation of the initial guesses / fits to the Band Excitation (BE)
    data using a Simple Harmonic Oscillator (SHO) model. 
    '''
    
    def __init__(self, h5_path, max_RAM_mb=1024, cores=None, chunksize=None, show_plots=True, save_plots=True):
        '''
        Parameters
        ----------
        h5_path : String / Unicode
            Absolute path of the h5 path with raw data
        max_RAM_mb : (Optional) Unsigned int
            Maximum memory (in megabytes) that the fitter is allowed to use
        cores : (Optional) Unsigned int
            Number of [logical] CPU cores to use.
            By default, the fitter uses two fewer than the number of available 
            logical cores in the computer
        chunksize : (Optional) unsigned int
            Number of jobs per core. Leave this as default
        show_plots : (Optional) Boolean 
            Show loops and other snapshots to validate fitting
        save_plots : (Optional) Boolean
            Save plots to disk
        '''
        self.h5_path = h5_path
        
        hdf = ioHDF5(h5_path)
        expt_type = hdf.file.attrs['data_type']
        hdf.close()
        
        if expt_type not in ['BEPSData','BELineData']:
            warn('Invalid data format')
            return
        
        # Ensuring that at least one core is available for use / 2 cores are available for other use
        max_cores = max(1,cpu_count()-2)
#         print 'max_cores',max_cores         
        if not cores: 
            cores = max_cores
        else:
            cores = min(round(abs(cores)), max_cores)            
        self.cores = int(cores)
#         print 'cores',self.cores
        self.max_memory = min(max_RAM_mb*1024**2, 0.75*getAvailableMem())
        if self.cores != 1:
            self.max_memory = int(self.max_memory/2)
#         print 'max_memory',self.max_memory
        
        self.chunksize = chunksize
        self.__show_plots__ = show_plots
        self.__save_plots__ = save_plots
        
    
    def guessSHOfits(self, fit_points=5):
        '''
        Calcualtes (fairly accurate) initial guesses for fitting the BE data. 
        Reads the raw data from the H5 file and writes the fit guess results to the file
        
        Parameters 
        ------------------
        fit_points : unsigned int (Optional. Default = 5)
            number of two-point pairs to use to guess the SHO parameters
        
        Returns
        ------------------
        None
        '''
        hdf = ioHDF5(self.h5_path)

        dataList = getDataSet(hdf.file,'Raw_Data')

        for h5_main in dataList:
            self._guessSHODataset(h5_main, hdf, fit_points)

        hdf.close()

        if self.__show_plots__ or self.__save_plots__:
            visualizeSHOResults(hdf.path, mode=0, save_plots=self.__save_plots__, show_plots = self.__show_plots__)

    def __isLegalBEDataset(self, h5_main):

        # First check if this dataset is linked to the four ancillary datasets
        if checkIfMain(h5_main):
            # Next check if the spectroscopic indices / values contain a dimension named 'Frequency'
            h5_spec_vals = getAuxData(h5_main, auxDataName=['Spectroscopic_Values'])[0]
            if 'Frequency' in h5_spec_vals.attrs['labels']:
                return True
        return False


    def _guessSHODataset(self, h5_main, hdf=None, fit_points=5):

        self.fit_points = fit_points

        # Create all the ancilliary datasets, allocate space.....

        h5_spec_inds = getAuxData(h5_main, auxDataName=['Spectroscopic_Indices'])[0]
        h5_spec_vals = getAuxData(h5_main, auxDataName=['Spectroscopic_Values'])[0]

        udvs_step_starts = np.where(h5_spec_inds[0] == 0)[0]
        num_udvs_steps = len(udvs_step_starts)

        ds_guess = MicroDataset('Guess', data=[],
                                maxshape=(h5_main.shape[0], num_udvs_steps),
                                chunking=(1, num_udvs_steps), dtype=sho32)

        not_freq = h5_spec_inds.attrs['labels']!='Frequency'
        if h5_spec_inds.shape[0] > 1:
            # More than just the frequency dimension, eg Vdc etc - makes it a BEPS dataset

            ds_sho_inds, ds_sho_vals = buildReducedSpec(h5_spec_inds, h5_spec_vals, not_freq, udvs_step_starts)

        else:
            '''
            Special case for datasets that only vary by frequency. Example - BE-Line
            '''
            ds_sho_inds = MicroDataset('Spectroscopic_Indices', np.array([[0]], dtype=np.uint32))
            ds_sho_vals = MicroDataset('Spectroscopic_Values', np.array([[0]], dtype=np.float32))

            ds_sho_inds.attrs['labels'] = {'Single_Step': (slice(0, None), slice(None))}
            ds_sho_vals.attrs['labels'] = {'Single_Step': (slice(0, None), slice(None))}
            ds_sho_inds.attrs['units'] = ''
            ds_sho_vals.attrs['units'] = ''

        dset_name = h5_main.name.split('/')[-1]
        sho_grp = MicroDataGroup('-'.join([dset_name,
                                           'SHO_Fit_']),
                                 h5_main.parent.name[1:])
        sho_grp.addChildren([ds_guess,
                             ds_sho_inds,
                             ds_sho_vals])
        sho_grp.attrs['SHO_guess_method'] = "PySPM BESHOFitter/guessSHOfits"

        if hdf is None:
            hdf = ioHDF5(h5_main.file)

        h5_sho_grp_refs = hdf.writeData(sho_grp)

        h5_guess = getH5DsetRefs(['Guess'],
                                 h5_sho_grp_refs)[0]
        h5_sho_inds = getH5DsetRefs(['Spectroscopic_Indices'],
                                    h5_sho_grp_refs)[0]
        h5_sho_vals = getH5DsetRefs(['Spectroscopic_Values'],
                                    h5_sho_grp_refs)[0]

        # Reference linking before actual fitting
        hdf.linkRefs(h5_guess, [h5_sho_inds, h5_sho_vals])

        # Linking ancillary position datasets:
        aux_dsets = getAuxData(h5_main, auxDataName=['Position_Indices',
                                                     'Position_Values'])
        hdf.linkRefs(h5_guess, aux_dsets)

        copyRegionRefs(h5_main, h5_guess)

        self.__doSHOonDataset__(h5_main, h5_guess, udvs_step_starts)

    def doSHOfits(self, fit_points=5):
        '''
        Does the actual SHO fitting. Reads the raw data from the H5 file and 
        writes the fit guess results to the file
        
        Parameters
        ------------------
        None
        
        Returns
        ------------------
        None
        '''
        hdf = ioHDF5(self.h5_path)

        dataList = getDataSet(hdf.file,'Raw_Data')

        for h5_main in dataList:
            self._SHOfitDataset(h5_main, hdf, fit_points)
            
        hdf.close()

        if self.__show_plots__ or self.__save_plots__:
            visualizeSHOResults(self.h5_path, mode=1, save_plots=self.__save_plots__, show_plots = self.__show_plots__)


    def _SHOfitDataset(self, h5_main, hdf=None, fit_points=5):
        """
        Always takes the last guess....
        :param h5_main:
        :param hdf:
        :param fit_points:
        :return:
        """
        if not self.__isLegalBEDataset(h5_main):
            print('Provided dataset is not BE compatible')
            return

        self.fit_points = fit_points

        # Check to see if fit guess has been performed:
        try:
            h5_sho_grp = findH5group(h5_main, 'SHO_Fit')[-1]
            h5_guess = h5_sho_grp['Guess']
        except IndexError:
            print('No Fit guess found!  Will generate guess then fit.')
            h5_main.file.close()
            # get the fit guess done instead
            self.guessSHOfits()
            # Then call self to get fitting done
            self.doSHOfits()
            return

        # The folder and fit guesses do indeed exist
        sho_grp = MicroDataGroup(h5_sho_grp.name.split('/')[-1],
                                 h5_sho_grp.parent.name[1:])
        # dataset size is same as guess size
        ds_result = MicroDataset('Fit', data=[], maxshape=(h5_guess.shape[0], h5_guess.shape[1]),
                                 chunking=h5_guess.chunks, dtype=sho32)
        sho_grp.addChildren([ds_result])
        sho_grp.attrs['SHO_fit_method'] = "PySPM BESHOFitter/doSHOfits"

        if hdf is None:
            hdf = ioHDF5(h5_main.file)

        h5_sho_grp_refs = hdf.writeData(sho_grp)

        h5_fit = getH5DsetRefs(['Fit'], h5_sho_grp_refs)[0]

        '''
        Copy attributes of the fit guess
        Check the guess dataset for plot groups, copy them if they exist
        '''
        for attr_name, attr_val in h5_guess.attrs.iteritems():

            if '_Plot_Group' in attr_name:
                ref_inds = getH5RegRefIndices(attr_val, h5_guess, return_method='corners')
                ref_inds = ref_inds.reshape([-1, 2, 2])
                fit_ref = createRefFromIndices(h5_fit, ref_inds)

                h5_fit.attrs[attr_name] = fit_ref
            else:
                h5_fit.attrs[attr_name] = attr_val

        # Reference linking before actual fitting
        hdf.linkRefs(h5_main, [h5_fit])

        h5_spec_inds = getAuxData(h5_main, auxDataName=['Spectroscopic_Indices'])[0]
        udvs_step_starts = np.where(h5_spec_inds[0] == 0)[0]

        self.__doSHOonDataset__(h5_main, h5_guess, udvs_step_starts, h5_fit)

    def __doSHOonDataset__(self, h5_main, h5_guess, step_start_inds, h5_fit=None):
        '''
        Internal function. \n
        Does the SHO operation (guess / fit) on the provided dataset. 
        Fills in the SHO fit results into the provided h5 dataset reference
        
        Parameters
        -------------
        h5_main : HDF5 dataset refernce
            raw BE response data
        h5_guess : HDF5 dataset refernce  
            where the fit guesses are stored
        h5_fit : rHDF5 dataset refernce  
            where the fit results will be stored
        step_start_inds : 1D numpy arary
            unique UDVS steps in the spectroscopic indices
            
        Return
        ----------
        None
        '''


        h5_spec_vals = getAuxData(h5_main, auxDataName=['Spectroscopic_Indices'])[0]

        if isReshapable(h5_main, step_start_inds):
        # if False:
            # vast majority of datasets - Stephen does not like this implementation
            print('Recognized as a simple (reshapable) dataset')
            freq_vec = h5_spec_vals[0,step_start_inds[0]:step_start_inds[1]]

            ''' scale the number of bins with the number of cores because each 
                core will keep a copy of the entire data'''
            max_pix = maxReadPixels(self.max_memory, h5_main.shape[0], h5_main.shape[1]*self.cores, h5_main.dtype.itemsize)
            num_steps = len(step_start_inds)
            st_pix = 0 
            t_start=getTicks()
            while st_pix < h5_main.shape[0]:
                en_pix = int(min(h5_main.shape[0],st_pix + max_pix))
                # Load the specified number of pixels into memory
                print 'Reading pixels:', st_pix, 'to',en_pix, 'of', h5_main.shape[0]
                raw_mat = h5_main[st_pix:en_pix,:]
                # reshape to (bins, step x pix)
                streamlined = reshapeToOneStep(raw_mat, num_steps)
                del raw_mat     
                # Guess / Fit this chunk
                if h5_fit is None:
                    fitted = self.__fitChunk__(streamlined,freq_vec)
                    del streamlined
                    # Now reshape from (5, step * pos) --> (5 * step, pos)            
                    reorganized = reshapeToNsteps(fitted, num_steps)
                    del fitted
                    # Write this chunk to the provided h5 dataset and flush:
                    h5_guess[st_pix:en_pix,:] = reorganized
                else:
                    # We need to read the fit guess accordingly
                    guess_mat = h5_guess['Amplitude [V]','Frequency [Hz]','Quality Factor','Phase [rad]'][st_pix:en_pix,:]
                    # Only keep the desired fields
                    # reshape to (bins, step x pix)
                    guess_mat2 = reshapeToOneStep(guess_mat, num_steps)
                    # do fitting with the streamlined and guess_mat
                    # Make sure that we do NOT send the 5th row.
                    fitted = self.__fitChunk__(streamlined,freq_vec,guess_mat2)
                    # Now reshape from (5, step * pos) --> (5 * step, pos)            
                    reorganized = reshapeToNsteps(fitted, num_steps)
                    # write back to h5
                    h5_fit[st_pix:en_pix,:] = reorganized
                h5_main.file.flush()
                st_pix = en_pix
            print('Took %d seconds to fit all data'%(getTicks() - t_start))
        
        else:
            ''' 
            Very rare conditions but this is how Stephen wants this to be implemented
            Number of bins in each UDVS step can be different. Iterate over (active) UDVS steps
            '''
            print('Recognized as a non-trivial dataset. Iterating through UDVS steps...')

            # create list of slices from the starts of each udvs step
            step_slices = list()
            for step_num in xrange(len(step_start_inds) - 1):
                step_slices.append(slice(step_start_inds[step_num], step_start_inds[step_num + 1]))
            # Add the last one manually
            step_slices.append(slice(step_start_inds[-1], None))

            # Step through each BE spectrum (UDVS step)
            for step_ind, spec_slice in enumerate(step_slices):
                freq_vec = h5_spec_vals[0, spec_slice]

                # Find max number of pixels that can be read in one go
                '''
                scale the number of bins with the number of cores because each 
                core will keep a copy of the entire data
                '''
                max_pix = maxReadPixels(self.max_memory, h5_main.shape[0], (spec_slice.stop - spec_slice.start)*self.cores, 4)
                st_pix = 0
                while st_pix < h5_main.shape[0]:
                    en_pix = min(h5_main.shape[0],st_pix + max_pix)
#                     Load the specified number of pixels into memory
                    print 'Reading pixels:', st_pix, 'to',en_pix,'for step',step_ind
                    raw_mat = h5_main[st_pix:en_pix,spec_slice]
                    if h5_fit is None:
                        fitted = self.__fitChunk__(raw_mat, freq_vec)
                        # Write this chunk to the provided h5 dataset:
                        h5_guess[st_pix:en_pix,step_ind:(step_ind+1)] = fitted
                    else:
                        # We need to read the fit guess accordingly
                        # Make sure that we do NOT read the 5th row.
                        
                        guess_mat =h5_guess['Amplitude [V]','Frequency [Hz]','Quality Factor','Phase [rad]'][st_pix:en_pix,step_ind:(step_ind+1)]
                        fitted = self.__fitChunk__(raw_mat,freq_vec,guess_mat)
                        # write back to h5
                        h5_fit[st_pix:en_pix,step_ind:(step_ind+1)] = fitted
                    # Flush to file!
                    h5_main.file.flush()
                    st_pix = en_pix
                    
                if (100.0*(step_ind+1)/len(step_slices))%10 == 0:
                    print 'completed fitting', int(100 * (step_ind+1) / len(step_slices)), '%'
                    
        

    def __fitChunk__(self, raw_mat,freq_vec,guess_mat=None):
        '''
        Fits the provided raw data on the 0th axis using the provided frequency vector for upper and lower bounds
        
        Parameters
        ----------------
        raw_mat : 2D numpy array
            Raw spectroscopic data arranged as (bins, steps or pixels)
        freq_vec : 1D numpy array
            Frequency
        guess_mat : 2D numpy array (optional)
            SHO guesses arranged as (4 SHO parameters, steps or pixels).
            Used only for SHO fitting
            
        Returns
        ---------
        mode 0 : 2D numpy array
            Containing SHO guesses arranged as (4 + 1 SHO parameters, steps or pixels)
        mode 1 : 2D numpy array
            Containing SHO fits arranged as (4 + 1 SHO parameters, steps or pixels)
        mode 2 : (2D numpy array, 2D numpy array)
            Containing SHO guesses arranged as (4 + 1 SHO parameters, steps or pixels)\n
            Containing SHO fits arranged as (4 + 1 SHO parameters, steps or pixels)
        '''
        # Calculating the appropriate chunksize and cores:
        recom_chunks = self.chunksize
        recom_cores = self.cores
        
        if not recom_chunks:
            recom_chunks = int(raw_mat.shape[0]/self.cores)
        if recom_chunks < 5*recom_cores:
            recom_cores=1
            
        low_bound = [0,np.min(freq_vec),-1e3,-np.pi]
        upp_bound = [1e3,np.max(freq_vec),1e3,np.pi]

        init_cond = guess_mat
        if guess_mat is None:
            # guess instead of fit
            init_cond = SHOfastGuess
            
        # Preparing fitter object
        fit_model = ufitter_model(SHO_func, init_cond, low_bound, upp_bound,4)           
        #print 'sending following sizes to ufitter:', freq_vec.shape,  raw_mat.shape 
        fitter = ufitter(freq_vec, raw_mat, fit_model,self.fit_points, sho32)
                
        # setting appropriate fitting function:
        if guess_mat is None:
            fitting_func = fitter.init_guess_multicore
        else:
            fitting_func = fitter.fit_all_multicore
            
#         max_tasks = int(min(recom_chunks, 1000))
#         chunksize = raw_mat.shape[0]
        max_tasks = None
        chunksize = recom_chunks
#         print 'max_tasks',max_tasks
#         print 'chunksize',chunksize
        # Actual fitting
        fitting_func(cores=recom_cores, chunksize=chunksize, maxtasks=max_tasks)
        # Correspondingly, the fitted data must also be transposed
        fitted = fitter.get_fit_results()
        #print 'got back matrix of size:', fitted.transpose().shape
        fitter.ClearData()
        if guess_mat is None:
            return fitted[:,1:] # Lower half contains the guesses
        else:
            return fitted[:,:1] # Upper half contains the fits


