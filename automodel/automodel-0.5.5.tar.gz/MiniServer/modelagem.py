#!/usr/bin/python
#imports = ["os","sys"]
#for eachimport in imports:
#    import eachimport
import os
import sys
import subprocess
#import Pyro4
import pdb
import sequence

from modeller import *
from modeller.automodel import *    # Load the automodel class

class mold:
    def __init__(self,file_format_pir):
        self.file_format_pir = file_format_pir

    def make_build_profilepy(self):
        script = """\
from modeller import *

log.verbose()
env = environ()

#-- Prepare the input files

#-- Read in the sequence database
sdb = sequence_db(env)
sdb.read(seq_database_file='""" + self.__installfolder__() + """/pdb/pdb_95.pir', seq_database_format='PIR', chains_list='ALL', minmax_db_seq_len=(30, 4000), clean_sequences=True)

#-- Write the sequence database in binary form
sdb.write(seq_database_file='""" + self.__installfolder__() + """/pdb/pdb_95.bin', seq_database_format='BINARY', chains_list='ALL')

#-- Now, read in the binary database
sdb.read(seq_database_file='""" + self.__installfolder__() + """/pdb/pdb_95.bin', seq_database_format='BINARY', chains_list='ALL')

#-- Read in the target sequence/alignment
aln = alignment(env)
aln.append(file='""" + self.file_format_pir + """', alignment_format='PIR', align_codes='ALL')

#-- Convert the input sequence/alignment into
#   profile format
prf = aln.to_profile()

#-- Scan sequence database to pick up homologous sequences
prf.build(sdb, matrix_offset=-450, rr_file='${LIB}/blosum62.sim.mat', gap_penalties_1d=(-500, -50), n_prof_iterations=1, check_profile=False, max_aln_evalue=0.01)

#-- Write out the profile in text format
prf.write(file='""" + os.path.dirname(self.file_format_pir) + '/build_profile.prf'"""', profile_format='TEXT')

#-- Convert the profile back to alignment format
aln = prf.to_alignment()

#-- Write out the alignment fileo
aln.write(file='""" + os.path.dirname(self.file_format_pir) + '/build_profilePIR.ali' + """', alignment_format='PIR')
aln.write(file='""" + os.path.dirname(self.file_format_pir) + '/build_profilePAP.ali' + """', alignment_format='PAP')
"""
        arq = file(os.path.dirname(self.file_format_pir) + '/build_profile.py', 'w')
        arq.write(script)
        arq.close()

    def __installfolder__(self):
        '''Returns where the AutoModel was instaled'''
        return os.path.dirname(os.path.realpath(sys.argv[0]))
#        return "/home/joaoluiz/IC/AutoModelIIH"

    def __folder_of_model__(self):
        return(os.path.dirname(self.file_format_pir))

    def find_templates(self):
        processo = modeller_caller()
        processo.run(self.__folder_of_model__() + '/build_profile.py')

class Align:
    def __init__(self,pdb_folder,modeldir,pdb_file,seq_ali):
        self.seq_ali = modeldir + seq_ali
        self.pdb_folder = pdb_folder
        self.modeldir = modeldir
        self.pdb_file = pdb.pdb(modeldir + pdb_file)
        self.strname = self.pdb_file.NomedaEstrutura()
    def make_readseq_py(self):
        script = """\
    # Step 1: Readin the structure file
    #
    # Reading the structure and passing the sequence to a seg
    # file.
from modeller import *
env = environ()
env.io.hetatm = env.io.water = True
env.io.atom_files_directory = ['"""+ self.pdb_folder + """']
code = '""" + self.strname + """'   #   estrutura a ser lida#
mdl = model(env, file=code)
aln = alignment(env)
aln.append_model(mdl, align_codes=code)
aln.write(file='""" + self.modeldir + """/str.seq')
    """
        arq = file(self.modeldir + '/readseq.py', 'w')
        arq.write(script)
        arq.close()

    def make_readseq_py2(self):
      script = """\
    # Step 1: Readin the structure file
    #
    # Reading the structure and passing the sequence to a seg
    # file.

env = environ()
env.io.hetatm = env.io.water = True
env.io.atom_files_directory = ['"""+ self.pdb_folder + """']
code = '""" + self.strname + """'   #   estrutura a ser lida#
mdl = model(env, file=code)
aln = alignment(env)
aln.append_model(mdl, align_codes=code)
aln.write(file='""" + self.modeldir + """str.seq')
aln.write(file='""" + self.modeldir + """str.str')
    """
      arq = file(self.modeldir + 'readseq.py', 'w')
      arq.write(script)
      arq.close()

    def make_align2d_py(self):
          script = """\
from modeller import *

env = environ()
env.io.hetatm = env.io.water = True
env.io.atom_files_directory = ['""" + self.modeldir + """']
aln = alignment(env)
mdl = model(env, file='""" + self.strname + """', model_segment=('FIRST:""" + self.pdb_file.chains()[0]+ """','LAST:""" + self.pdb_file.chains()[-1] + """'))
aln.append_model(mdl, align_codes='""" + self.strname + """', atom_files='""" + self.strname  + """.pdb')
aln.append(file='""" + self.seq_ali + """', align_codes='seq.ali')
aln.align2d()
aln.write(file='""" + self.modeldir + """ali.ali', alignment_format='PIR')
aln.write(file='""" + self.modeldir + """ali.pap', alignment_format='PAP')
        """
          arq = file(self.modeldir + 'align2d.py', 'w')
          arq.write(script)
          arq.close()
    def __folder_of_model__(self):
        return self.modeldir

    def read_sequence(self):
        processo = modeller_caller()
        processo.run(self.__folder_of_model__() + '/readseq.py')

    def align_sequence(self):
        processo = modeller_caller()
        processo.run(self.__folder_of_model__() + '/align2d.py')

class Modeler:
    def __init__(self,pdb_folder,modeldir,pdb_file,ali_ali):
        self.ali_ali = modeldir + ali_ali
        self.pdb_folder = pdb_folder
        self.modeldir = modeldir
        self.seq = sequence.Sequence(self.ali_ali)
        print self.seq.structures_names()
        self.structures = str(self.seq.structures_names()[0:-1])[1:-1]

    def make_get_model_py(self):
        script = """\
from modeller import *
from modeller.automodel import *    # Load the automodel class
import os
os.chdir('""" + self.__folder_of_model__() + """')

log.verbose()

env = environ(rand_seed=-12312)  # To get different models from another script
# directories for input atom files
env.io.hetatm = env.io.water = True


env.io.atom_files_directory = ['""" + self.modeldir + """']
a = automodel(env,
              alnfile='""" + self.ali_ali + """',      # alignment filename (ali.ali)
              knowns=(""" + self.structures + """),             # codes of the templates (variavel da est)
              sequence='seq.ali',           # code of the target (seq.ali)
              assess_methods=assess.GA341)  # request GA341 assessment
a.starting_model= 1                 # index of the first model
a.ending_model  = 5                 # index of the last model
                                    # (determines how many models to calculate)
a.deviation = 4.0                   # has to >0 if more than 1 model

a.make()                            # do homology modelling"""
        arq = file(self.modeldir + 'get_model.py', 'w')
        arq.write(script)
        arq.close()

    def __folder_of_model__(self):
        return self.modeldir

    def model_sequence(self):
        processo = modeller_caller()
        processo.run(self.__folder_of_model__() + 'get_model.py')

    def get_results(self):
        folder = self.modeldir
        mof = 0
        filemof = ""
        for files in os.listdir(folder):
            if (files.startswith('seq.ali.B')):
                    arqr = file(folder + '/' + files, 'r')
                    arqr.readline()
                    linha = arqr.readline()
                    if (mof == 0) or (linha.partition(':      ')[2] < mof):
                            mof = linha.partition(':      ')[2]
                            filemof = folder + '/' + files
                            arqr.close()
        # if not (os.path.exists(folder + '/../results')):
        #         os.mkdir(folder + '/../results')
        # os.popen('cp '+ filemof +  ' ' + folder + '/../results/')
        return filemof

# class Evaluate:
#     def __init__(self,pdb_file,model_file,ali_ali_file,workdir):
#         self.pdb_file = workdir + os.path.basename(pdb_file)
#         self.model_file = workdir + os.path.basename(model_file)
#         self.ali_ali_file = workdir + os.path.basename(ali_ali_file)
#         self.workdir = workdir
#         self.evaluatedir = self.workdir
#         self.path = self.evaluatedir
#         self.dope_profile = None

#     def prepare_evaluate(self):
#         pastaevaluate = self.workdir + 'evaluate/'
#         if(os.path.exists(pastaevaluate) == False):
#             os.mkdir(pastaevaluate)
#         os.popen("cp "+ self.pdb_file + " " + pastaevaluate)
#         os.popen("cp "+ self.model_file + " " + pastaevaluate)
#         os.popen("cp "+ self.ali_ali_file + " " + pastaevaluate)
#         return(pastaevaluate)

#     def make_evaluate_model(self,arquivopdb):
#             script = """\
# from modeller import *
# from modeller.scripts import complete_pdb

# log.verbose()    # request verbose output
# env = environ()
# env.libs.topology.read(file='$(LIB)/top_heav.lib') # read topology
# env.libs.parameters.read(file='$(LIB)/par.lib') # read parameters

# # read model file
# mdl = complete_pdb(env, '"""+ self.evaluatedir + os.path.basename(arquivopdb) + """')

# # Assess with DOPE:
# s = selection(mdl)   # all atom selection
# s.assess_dope(output='ENERGY_PROFILE NO_REPORT', file='"""+ self.evaluatedir  + os.path.basename(arquivopdb.split(".")[0]) + """.profile',
#               normalize_profile=True, smoothing_window=15)"""
#             arq = file(self.evaluatedir + 'evaluate_model.py', 'w')
#             arq.write(script)
#             arq.close()


#     def get_dope_profile(self):
#         return self.dope_profile

#     def __folder_of_evaluate__(self):
#         return self.evaluatedir

#     def get_evaluate(self):
#         processo = modeller_caller()
#         processo.run(self.__folder_of_evaluate__() + 'evaluate_model.py')

#     def plot_profiles(self):
#       self.create_script_in_folder(self.pdb_file, self.model_file)
#       processo = modeller_caller()
#       processo.run(self.__folder_of_evaluate__() + 'plot_profile.py')

#     def create_script_in_folder(self, template,model):
#         template = os.path.basename(template)[0:-4]
#         model = os.path.basename(model)[0:-4]
#         # myloop = os.path.basename(myloop)[0:-4]
#         # self.path = os.path.dirname(model)
#         pdbtemplate = pdb.pdb(self.pdb_file)
#         script = """import pylab
# import modeller
# import os

# os.chdir('""" + self.path + """')
# def get_profile(profile_file, seq):
#     '''Read `profile_file` into a Python array, and add gaps corresponding to
#        the alignment sequence `seq`.'''
#     # Read all non-comment and non-blank lines from the file:
#     f = file(profile_file)
#     vals = []
#     for line in f:
#         if not line.startswith('#') and len(line) > 10:
#             spl = line.split()
#             vals.append(float(spl[-1]))
#     # Insert gaps into the profile corresponding to those in seq:
#     for n, res in enumerate(seq.residues):
#         for gap in range(res.get_leading_gaps()):
#             vals.insert(n, None)
#     # Add a gap at position '0', so that we effectively count from 1:
#     vals.insert(0, None)
#     return vals

# e = modeller.environ()
# a = modeller.alignment(e, file='ali.ali')

# template = get_profile('""" + self.evaluatedir + os.path.basename(self.pdb_file).split(".")[0] + '.profile'"""', a['""" + str(pdbtemplate.NomedaEstrutura()) + """'])
# model = get_profile('""" + self.evaluatedir + os.path.basename(self.pdb_file).split(".")[0] + '.profile'"""', a['seq.ali'])
# # Plot the template and model profiles in the same plot for comparison:
# pylab.figure(1, figsize=(10,6))
# pylab.xlabel('Alignment position')
# pylab.ylabel('DOPE per-residue score')
# pylab.plot(model, color='red', linewidth=2, label='Model')
# pylab.plot(template, color='green', linewidth=2, label='Template')
# pylab.legend()
# pylab.savefig('dope_profile.png', dpi=65)
# """
#         script_path = self.path + os.sep + "plot_profile.py"
#         loop_script = file(script_path, "w")        
#         loop_script.write(script)
#         loop_script.close()
#         self.myscript = script_path
#         self.dope_profile = self.evaluatedir  + 'dope_profile.png'



    # def plot_profiles(self):
    #     import pylab
    #     import modeller
    #     pdbtemplate = pdb.pdb(self.pdb_file)
    #     def get_profile(profile_file, seq):
    #         # Read all non-comment and non-blank lines from the file:
    #         f = file(profile_file)
    #         vals = []

    #         for line in f:
    #             if not line.startswith('#') and len(line) > 10:
    #                 spl = line.split()
    #                 vals.append(float(spl[-1]))
    #         # Insert gaps into the profile corresponding to those in seq:
    #         for n, res in enumerate(seq.residues):
    #             for gap in range(res.get_leading_gaps()):
    #                 vals.insert(n, None)
    #         # Add a gap at position '0', so that we effectively count from 1:
    #         vals.insert(0, None)
    #         return vals
    #     e = modeller.environ()
    #     a = modeller.alignment(e, file=self.evaluatedir + 'ali.ali')
    #     print pdbtemplate.NomedaEstrutura()
    #     print self.evaluatedir + os.path.basename(self.pdb_file).split(".")[0] + '.profile'
    #     template = get_profile(self.evaluatedir + os.path.basename(self.pdb_file).split(".")[0] + '.profile', a[str(pdbtemplate.NomedaEstrutura())])
    #     model = get_profile(self.evaluatedir + os.path.basename(self.pdb_file).split(".")[0] + '.profile', a['seq.ali'])
    #     # Plot the template and model profiles in the same plot for comparison:
    #     pylab.figure(1, figsize=(10,6))
    #     pylab.xlabel('Alignment position')
    #     pylab.ylabel('DOPE per-residue score')
    #     pylab.plot(model, color='red', linewidth=2, label='Model')
    #     pylab.plot(template, color='green', linewidth=2, label='Template')
    #     pylab.legend()
    #     pylab.savefig(self.evaluatedir  + 'dope_profile.png', dpi=65)


    #     self.dope_profile = self.evaluatedir  + 'dope_profile.png'

class modeller_caller:
    def __init__(self):
        self.modeller_executable = "python"
        self.process = None
    def run(self,script):
        try:
            process = subprocess.Popen([self.modeller_executable,script])
        except:
            print "Modeller or Script not found!"
        return process.wait()

class Procheck_Evaluate:
    def __init__(self,workdir,template):
        self.workdir = workdir
        self.procheck_workdir = self.prepare_folder()
        self.template = self.workdir + os.path.basename(template)
        self.template_on_procheck_folder = None
    def prepare_folder(self):
        pastadeavaliacao = self.workdir + 'avaliacao_procheck/'
        if os.path.exists(pastadeavaliacao):
	        os.popen('rm -fr '+ pastadeavaliacao)
        os.mkdir(pastadeavaliacao)
        return pastadeavaliacao

    def copy_templates_for_procheck_evaluate(self):
        os.popen('cp '+ self.template +  ' ' + self.procheck_workdir)
        self.template_on_procheck_folder = self.procheck_workdir + os.path.basename(self.template)

    def run_prochek(self):
      script = """\
import os
#path = os.getcwd()
os.chdir('""" + self.procheck_workdir + """')
os.popen('procheck '+ '""" + self.template_on_procheck_folder + """' +  ' ' + str(2.0))
#os.chdir(path)
      """
      script_path = self.procheck_workdir + "procheck.py"
      procheck_script = file(script_path, "w")        
      procheck_script.write(script)
      procheck_script.close()
      os.popen("python " + script_path)
      return self.procheck_workdir[0:-1]       

class Loop_Refinement(object):
    """docstring for Loop_Refinement"""
    def __init__(self, initial_model, start_residue, end_residue):
            self.initial_model = initial_model
            self.start_residue = start_residue
            self.end_residue = end_residue
            self.myscript = ""
    
    def create_script_in_folder(self,path):
        script = """\
# Loop refinement of an existing model
from modeller import *
from modeller.automodel import *
import os

log.verbose()
env = environ()
os.chdir('""" + path + """')

# directories for input atom files
env.io.atom_files_directory = './:../atom_files'

# Create a new class based on 'loopmodel' so that we can redefine
# select_loop_atoms (necessary)
class MyLoop(loopmodel):
    # This routine picks the residues to be refined by loop modeling
    def select_loop_atoms(self):
        # 10 residue insertion 
        return selection(self.residue_range('""" + self.start_residue + """', ' """ + self.end_residue + """'))

m = MyLoop(env,
           inimodel='""" + self.initial_model + """', # initial model of the target
           sequence='seq.ali')          # code of the target

m.loop.starting_model= 1           # index of the first loop model 
m.loop.ending_model  = 5          # index of the last loop model
m.loop.md_level = refine.very_fast # loop refinement method; this yields
                                   # models quickly but of low quality;
                                   # use refine.slow for better models

m.make()
""" 
        script_path = path + os.sep + "loop.py"
        loop_script = file(script_path, "w")        
        loop_script.write(script)
        loop_script.close()
        self.myscript = script_path

    def __folder_of_evaluate__(self):
        pass

    def get_model(self):
        processo = modeller_caller()
        processo.run(self.myscript)
        
    def get_results(self):
        folder = os.path.dirname(self.myscript)
        mof = 0
        filemof = ""
        for files in os.listdir(folder):
            if (files.startswith('seq.ali.BL')):
                    arqr = file(folder + '/' + files, 'r')
                    arqr.readline()
                    linha = arqr.readline()
                    if (mof == 0) or (linha.partition(':      ')[2] < mof):
                            mof = linha.partition(':      ')[2]
                            filemof = folder + '/' + files
                            arqr.close()
        # if not (os.path.exists(folder + '/../loop')):
        #         os.mkdir(folder + '/../loop')
        # os.popen('cp '+ filemof +  ' ' + folder + '/../loop/')
        return filemof

class Malign(object):
    """docstring for Malign"""
    def __init__(self, path):
        self.path = path
        self.myscript = ""

    def create_script_in_folder(self, template, best_sequence, loop_sequence):
        script = """from modeller import *
import os

os.chdir('""" + self.path + """')
log.verbose()
env = environ()

env.io.atom_files_directory = './:../atom_files/'

aln = alignment(env)
for (code, chain) in (('""" + template + """', 'A'), ('""" + best_sequence + """', ''), ('""" + loop_sequence + """', '')):
    mdl = model(env, file=code, model_segment=('FIRST:'+chain, 'LAST:'+chain))
    aln.append_model(mdl, atom_files=code, align_codes=code+chain)

for (weights, write_fit, whole) in (((1., 0., 0., 0., 1., 0.), False, True),
                                    ((1., 0.5, 1., 1., 1., 0.), False, True),
                                    ((1., 1., 1., 1., 1., 0.), True, False)):
    aln.salign(rms_cutoff=3.5, normalize_pp_scores=False,
               rr_file='$(LIB)/as1.sim.mat', overhang=30,
               gap_penalties_1d=(-450, -50),
               gap_penalties_3d=(0, 3), gap_gap_score=0, gap_residue_score=0,
               dendrogram_file='ali.tree',
               alignment_type='tree', # If 'progresive', the tree is not
                                      # computed and all structues will be
                                      # aligned sequentially to the first
               feature_weights=weights, # For a multiple sequence alignment only
                                        # the first feature needs to be non-zero
               improve_alignment=True, fit=True, write_fit=write_fit,
               write_whole_pdb=whole, output='ALIGNMENT QUALITY')

#aln.write(file='ali.pap', alignment_format='PAP')
aln.write(file='ali.ali', alignment_format='PIR')

aln.salign(rms_cutoff=1.0, normalize_pp_scores=False,
           rr_file='$(LIB)/as1.sim.mat', overhang=30,
           gap_penalties_1d=(-450, -50), gap_penalties_3d=(0, 3),
           gap_gap_score=0, gap_residue_score=0, dendrogram_file='1is3A.tree',
           alignment_type='progressive', feature_weights=[0]*6,
           improve_alignment=False, fit=False, write_fit=True,
           write_whole_pdb=False, output='QUALITY')
"""
        script_path = self.path + os.sep + "salign.py"
        loop_script = file(script_path, "w")        
        loop_script.write(script)
        loop_script.close()
        self.myscript = script_path

    def get_model(self):
        processo = modeller_caller()
        processo.run(self.myscript)

class Malign2(object):
    """docstring for Malign"""
    def __init__(self, path):
        self.path = path
        self.myscript = ""

    def create_script_in_folder(self, template, best_sequence):
        script = """from modeller import *
import os

os.chdir('""" + self.path + """')
log.verbose()
env = environ()

env.io.atom_files_directory = './:../atom_files/'

aln = alignment(env)
for (code, chain) in (('""" + template + """', 'A'), ('""" + best_sequence + """', '')):
    mdl = model(env, file=code, model_segment=('FIRST:'+chain, 'LAST:'+chain))
    aln.append_model(mdl, atom_files=code, align_codes=code+chain)

for (weights, write_fit, whole) in (((1., 0., 0., 0., 1., 0.), False, True),
                                    ((1., 0.5, 1., 1., 1., 0.), False, True),
                                    ((1., 1., 1., 1., 1., 0.), True, False)):
    aln.salign(rms_cutoff=3.5, normalize_pp_scores=False,
               rr_file='$(LIB)/as1.sim.mat', overhang=30,
               gap_penalties_1d=(-450, -50),
               gap_penalties_3d=(0, 3), gap_gap_score=0, gap_residue_score=0,
               dendrogram_file='ali.tree',
               alignment_type='tree', # If 'progresive', the tree is not
                                      # computed and all structues will be
                                      # aligned sequentially to the first
               feature_weights=weights, # For a multiple sequence alignment only
                                        # the first feature needs to be non-zero
               improve_alignment=True, fit=True, write_fit=write_fit,
               write_whole_pdb=whole, output='ALIGNMENT QUALITY')

#aln.write(file='ali.pap', alignment_format='PAP')
aln.write(file='ali.ali', alignment_format='PIR')

aln.salign(rms_cutoff=1.0, normalize_pp_scores=False,
           rr_file='$(LIB)/as1.sim.mat', overhang=30,
           gap_penalties_1d=(-450, -50), gap_penalties_3d=(0, 3),
           gap_gap_score=0, gap_residue_score=0, dendrogram_file='1is3A.tree',
           alignment_type='progressive', feature_weights=[0]*6,
           improve_alignment=False, fit=False, write_fit=True,
           write_whole_pdb=False, output='QUALITY')
"""
        script_path = self.path + os.sep + "salign.py"
        loop_script = file(script_path, "w")        
        loop_script.write(script)
        loop_script.close()
        self.myscript = script_path

    def get_model(self):
        processo = modeller_caller()
        processo.run(self.myscript)

class GetProt(object):
    """docstring for GetProt"""
    def __init__(self, loop_folder):
        self.myscript = ""
        self.path = loop_folder

    def create_script_in_folder(self, template,model,myloop):
        template = os.path.basename(template)[0:-4]
        model = os.path.basename(model)[0:-4]
        myloop = os.path.basename(myloop)[0:-4]
        # self.path = os.path.dirname(model)
        script = """import pylab
import modeller
import os

os.chdir('""" + self.path + """')
def get_profile(profile_file, seq):
    '''Read `profile_file` into a Python array, and add gaps corresponding to
       the alignment sequence `seq`.'''
    # Read all non-comment and non-blank lines from the file:
    f = file(profile_file)
    vals = []
    for line in f:
        if not line.startswith('#') and len(line) > 10:
            spl = line.split()
            vals.append(float(spl[-1]))
    # Insert gaps into the profile corresponding to those in seq:
    for n, res in enumerate(seq.residues):
        for gap in range(res.get_leading_gaps()):
            vals.insert(n, None)
    # Add a gap at position '0', so that we effectively count from 1:
    vals.insert(0, None)
    return vals

e = modeller.environ()
a = modeller.alignment(e, file='ali.ali')

template = get_profile('""" + template + """.profile', a['""" + template + """A'])
model = get_profile('""" + model + """.profile', a['""" + model + """'])
myloop  = get_profile('""" + myloop + """.profile', a['""" + myloop + """'])
# Plot the template and model profiles in the same plot for comparison:
pylab.figure(1, figsize=(10,6))
pylab.xlabel('Alignment position')
pylab.ylabel('DOPE per-residue score')
pylab.plot(model, color='red', linewidth=2, label='Model')
pylab.plot(template, color='green', linewidth=2, label='Template')
pylab.plot(myloop, color='blue', linewidth=2, label='Loop refinement')
pylab.legend()
pylab.savefig('dope_profile_loop.png', dpi=65)
"""
        script_path = self.path + os.sep + "plot_profile.py"
        loop_script = file(script_path, "w")        
        loop_script.write(script)
        loop_script.close()
        self.myscript = script_path

    def get_model(self):
        processo = modeller_caller()
        processo.run(self.myscript)

class GetProt2(object):
    """docstring for GetProt"""
    def __init__(self, loop_folder):
        self.myscript = ""
        self.path = loop_folder

    def create_script_in_folder(self, template,model):
        template = os.path.basename(template)[0:-4]
        model = os.path.basename(model)[0:-4]
        # myloop = os.path.basename(myloop)[0:-4]
        # self.path = os.path.dirname(model)
        script = """import pylab
import modeller
import os

os.chdir('""" + self.path + """')
def get_profile(profile_file, seq):
    '''Read `profile_file` into a Python array, and add gaps corresponding to
       the alignment sequence `seq`.'''
    # Read all non-comment and non-blank lines from the file:
    f = file(profile_file)
    vals = []
    for line in f:
        if not line.startswith('#') and len(line) > 10:
            spl = line.split()
            vals.append(float(spl[-1]))
    # Insert gaps into the profile corresponding to those in seq:
    for n, res in enumerate(seq.residues):
        for gap in range(res.get_leading_gaps()):
            vals.insert(n, None)
    # Add a gap at position '0', so that we effectively count from 1:
    vals.insert(0, None)
    return vals

e = modeller.environ()
a = modeller.alignment(e, file='ali.ali')

template = get_profile('""" + template + """.profile', a['""" + template + """A'])
model = get_profile('""" + model + """.profile', a['""" + model + """'])
# Plot the template and model profiles in the same plot for comparison:
pylab.figure(1, figsize=(10,6))
pylab.xlabel('Alignment position')
pylab.ylabel('DOPE per-residue score')
pylab.plot(model, color='red', linewidth=2, label='Model')
pylab.plot(template, color='green', linewidth=2, label='Template')
#pylab.plot(myloop, color='blue', linewidth=2, label='Loop refinement')
pylab.legend()
pylab.savefig('dope_profile_loop.png', dpi=65)
"""
        script_path = self.path + os.sep + "plot_profile.py"
        loop_script = file(script_path, "w")        
        loop_script.write(script)
        loop_script.close()
        self.myscript = script_path

    def get_model(self):
        processo = modeller_caller()
        processo.run(self.myscript)

class MakeProfile(object):
    """docstring for MakeProfiles"""
    def __init__(self):
        pass
    
    def create_script_in_folder(self,pdb_file):
        self.path = os.path.dirname(pdb_file)
        script = """from modeller import *
from modeller.scripts import complete_pdb
import os

os.chdir('""" + self.path + """')
log.verbose()    # request verbose output
env = environ()
env.libs.topology.read(file='$(LIB)/top_heav.lib') # read topology
env.libs.parameters.read(file='$(LIB)/par.lib') # read parameters

# directories for input atom files
env.io.atom_files_directory = './:../atom_files'

# read model file
mdl = complete_pdb(env, '""" + pdb_file + """')

s = selection(mdl)
s.assess_dope(output='ENERGY_PROFILE NO_REPORT', file='""" + os.path.basename(pdb_file)[0:-4] + """.profile',
              normalize_profile=True, smoothing_window=15)
"""
        script_path = self.path + os.sep + "get_profile.py"
        loop_script = file(script_path, "w")        
        loop_script.write(script)
        loop_script.close()
        self.myscript = script_path

    def get_model(self):
        processo = modeller_caller()
        processo.run(self.myscript)

class MakeProfile2(object):
    """docstring for MakeProfiles"""
    def __init__(self):
        pass
    
    def create_script_in_folder(self,pdb_file):
        self.path = os.path.dirname(pdb_file)
        script = """from modeller import *
from modeller.scripts import complete_pdb
import os

os.chdir('""" + self.path + """')
log.verbose()    # request verbose output
env = environ()
env.libs.topology.read(file='$(LIB)/top_heav.lib') # read topology
env.libs.parameters.read(file='$(LIB)/par.lib') # read parameters

# directories for input atom files
env.io.atom_files_directory = './:../atom_files'

# read model file
mdl = complete_pdb(env, '""" + pdb_file + """')

s = selection(mdl)
s.assess_dope(output='ENERGY_PROFILE NO_REPORT', file='""" + os.path.basename(pdb_file)[0:-4] + """.profile',
              normalize_profile=True, smoothing_window=15)
"""
        script_path = self.path + os.sep + "get_profile.py"
        loop_script = file(script_path, "w")        
        loop_script.write(script)
        loop_script.close()
        self.myscript = script_path

    def get_model(self):
        processo = modeller_caller()
        processo.run(self.myscript)