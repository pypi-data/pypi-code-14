from __future__ import print_function

import csv
from glob import glob

import numpy as np
import os.path
import xml.etree.ElementTree as ET

#=================================================================================================#
class mods_outputs:
    def __init__(self,root_dir):
        self.root_dir = root_dir
        self.data = {}
        
    def _get_ncases(self,algorithm):
        algorithm_dir = "%s/%s" % (self.root_dir,algorithm)
        dir_contents  = glob("%s/*" % algorithm_dir)
        
        for path in dir_contents:
            if os.path.isdir(path):
                subdir_contents = glob("%s/*" % path)
                Ncases = 0
                for subdir_path in subdir_contents:
                    if 'case_' in subdir_path:
                        Ncases += 1
                if Ncases > 0: return Ncases
        print('Failed to detect Ncases')
        return -1
        
    def _get_nruns(self,algorithm):
        of_data_key = self._get_data_key(algorithm,'OF')
        if of_data_key not in self.data:
            self._read_objective_function(algorithm)
        return (self.data[of_data_key])['nrun'].size
        
    def _get_data_key(self,algorithm,subtype):
        return "%s_%s" % (algorithm,subtype)
        
    def _read_objective_function(self,algorithm):
        fname = "%s/%s/%s_OF.csv" % (self.root_dir,algorithm,algorithm)
        dtypes = {'names': ('nrun','lsq_sum'), 'formats': ('i4','f8') }
        nrun,lsq_sum = np.loadtxt(fname,skiprows=1,delimiter=',',usecols=(0,1),dtype=dtypes,unpack=True)
        data     = {'nrun':nrun, 'lsq_sum':lsq_sum}
        data_key = self._get_data_key(algorithm,'OF')
        self.data[data_key] = data
        
    def _read_subtype(self,algorithm,subtype):
        fname = "%s/%s/%s_subtype_%s.csv" % (self.root_dir,algorithm,algorithm,subtype)
        data = np.loadtxt(fname,skiprows=1,delimiter=',')
        data_key = self._get_data_key(algorithm,subtype)
        self.data[data_key] = data
        
    def get_subtype_data(self,algorithm,subtype,cases=None,nbest=None,nlast=None):
        subtype_data_key = self._get_data_key(algorithm,subtype)
        if subtype_data_key not in self.data:
            self._read_subtype(algorithm,subtype)
        all_data = self.data[subtype_data_key]
        if all_data.ndim != 2: pdb.set_trace() # Not setup to handle data of this size
        Nruns  = self._get_nruns(algorithm)
        if all_data.shape[0] != Nruns: pdb.set_trace() # Not setup to handle data of this size
        # Choose one or more runs
        if nbest:
            of_data_key = self._get_data_key(algorithm,'OF')
            if of_data_key not in self.data:
                self._read_objective_function(algorithm)
            
            best_idx = (self.data[of_data_key])['lsq_sum'].argsort()[:nbest]
            data_all_cases = all_data[best_idx,:]
        elif nlast:
            data_all_cases = all_data[-nlast:,:]
        else:
            data_all_cases = all_data
        # Choose one or more cases
        if cases is not None:
            if isinstance(cases, list) or isinstance(cases, tuple):
                case_indices = [c - 1 for c in list(cases)]
            else:
                case_indices = [cases - 1]
                
            Ncases = self._get_ncases(algorithm)
            if data_all_cases.ndim == 1:
                if data_all_cases.size != Ncases:
                    data = data_all_cases[:,case_indices]
            elif data_all_cases.ndim == 2:
                
                Ntot = data_all_cases.shape[1]
                if Ntot % Ncases: pdb.set_trace() 
                Nprof = Ntot/Ncases
                for ii,icase in enumerate(case_indices):
                    case_prof = np.squeeze(data_all_cases[:,icase*Nprof:(icase+1)*Nprof])
                    if (ii==0):
                        data = case_prof
                    elif (ii==1):
                        data = np.append([data],[case_prof],0)
                    else:
                        data = np.append(data,[case_prof],0)
        else:
            data = data_all_cases
            pdb.set_trace()####
        return np.squeeze(data)
#=================================================================================================#           

#=================================================================================================#
class mods_input:
    default_namespace_dict = {'default': 'http://como.cheng.cam.ac.uk/MoDS'}

    def __init__(self,root_dir,namespace_dict=default_namespace_dict):
        self.root_dir = root_dir
        self.ns = namespace_dict
        self.algorithms        = []
        self.Nalgorithms       = 0
        self.algorithm_details = {}

        self.cases        = []
        self.Ncases       = 0
        self.case_details = {}

        self.files        = []
        self.Nfiles       = 0
        self.file_details = {}

        self.functions        = []
        self.Nfunctions       = 0
        self.function_details = {}

        self.parameters        = []
        self.Nparameters       = 0
        self.parameter_details = {}

        self.fname    = root_dir + "/Working_dir/MoDS_inputs.xml"
        self._read_()

    def _read_(self):
        self.tree = ET.parse(self.fname)
        root = self.tree.getroot()
        self._parse_algorithms_(root.find('default:algorithms', self.ns))
        self._parse_cases_(root.find('default:cases', self.ns))
        self._parse_files_(root.find('default:files', self.ns))
        self._parse_functions_(root.find('default:functions', self.ns))
        self._parse_parameters_(root.find('default:parameters', self.ns))

    def _parse_algorithms_(self,node):
        self.Nalgorithms = len(node)
        for algorithm in node:
            name = algorithm.attrib['name']
            self.algorithms.append(name)
            self.algorithm_details[name] = self._parse_details_(name,algorithm.find('default:details', self.ns))

    def _parse_cases_(self,node):
        self.Ncases = len(node)
        for case in node:
            name = case.attrib['name']
            self.cases.append(name)
            self.case_details[name] = self._parse_details_(name,case.find('default:details', self.ns))

    def _parse_files_(self,node):
        self.Nfiles = len(node)
        for file_ in node:
            name = file_.attrib['file_name']
            self.files.append(name)
            self.file_details[name] = self._parse_details_(name,file_.find('default:details', self.ns))

    def _parse_functions_(self,node):
        self.Nfunctions = len(node)
        for function in node:
            name = function.attrib['name']
            self.functions.append(name)
            self.function_details[name] = self._parse_details_(name,function.find('default:details', self.ns))

    def _parse_parameter_file_details_(self,node):
        details = {}
        if node is None: return None
        attribs = node.attrib
        if 'file_name' in attribs:
            fname = attribs['file_name']
        else:
            fname = 'Unknown'
        details['name'] = fname
        details_node = node.find('default:details', self.ns)
        for detail in details_node:
            dname  = detail.attrib['name']
            dvalue = detail.text
            details[dname] = dvalue
        return details

    def _parse_parameters_(self,node):
        self.Nparameters = len(node)
        for parameter in node:
            name = parameter.attrib['name']
            self.parameters.append(name)

            cases_node = parameter.find('default:cases', self.ns)
            cases = []
            for case_node in cases_node:
                cases.append(case_node.text)

            files_node = parameter.find('default:files', self.ns)
            files = {}
            for file_type in ['initial_read','working_read','working_write']:
                files[file_type] = self._parse_parameter_file_details_(files_node.find('default:'+file_type, self.ns))
            self.parameter_details[name] = {'cases': cases, 'files':files}

    def _parse_details_(self,name,node,name_tag='name'):
        details = {}
        for detail in node:
            name  = detail.attrib[name_tag]
            value = detail.text
            details[name] = value
        return details

    def __group_str__(self,group,details):
        s = ""
        for entry in group:
            s += "    %s\n" % entry
            for detail,value in details[entry].items():
                s += "      %s : %s\n" % (detail,value)
        return s

    def __str__(self):
        s = "[MoDS inputs (root_dir=%s)]\n" % self.root_dir
        if self.Nalgorithms > 0:
            s += '  Algorithms:\n'
            s += self.__group_str__(self.algorithms,self.algorithm_details)
        if self.Ncases > 0:
            s += '  Cases:\n'
            s += self.__group_str__(self.cases,self.case_details)
        if self.Nfiles > 0:
            s += '  Files:\n'
            s += self.__group_str__(self.files,self.file_details)
        if self.Nfunctions > 0:
            s += '  Functions:\n'
            s += self.__group_str__(self.functions,self.function_details)
        if self.Nparameters > 0:
            s += '  Parameters:\n'
            for parameter in self.parameters:
                s += '    %s:\n' % parameter
                details = self.parameter_details[parameter]
                if len(details['cases']) > 0:
                    s += '      Cases:\n'
                    for case in details['cases']:
                        s += '        %s\n' % case
                if len(details['files']) > 0:
                    s += '      Files:\n'
                    files = details['files']
                    for file_type in ['initial_read','working_read','working_write']:
                        file_details = files[file_type]
                        if file_details is not None:
                            s += '        %s (%s):\n' % (file_type,file_details['name'])
                            for key,val in file_details.items():
                                if key != 'name':
                                    s += '          %s: %s\n' % (key,val)

        return s
#=================================================================================================#

if __name__=='__main__':
    print('Testing mods_input()')
    f = '/Users/owen/work/MoDS/example_project_dir'
    inp = mods_input(f)
    print(inp)
