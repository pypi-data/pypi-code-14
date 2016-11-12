"""First API, local access only"""
import hug
import logging
from pprint import pprint
import json
import os
from mykatlas.utils import check_args
from mykatlas.analysis import AnalysisResult
from mykatlas.typing import CoverageParser
from mykatlas.typing import Genotyper
from mykrobe.predict import TBPredictor
from mykrobe.predict import StaphPredictor
from mykrobe.predict import GramNegPredictor
from mykrobe.predict import MykrobePredictorSusceptibilityResult
from mykrobe.metagenomics import AMRSpeciesPredictor
from mykrobe.metagenomics import MykrobePredictorPhylogeneticsResult
from mykrobe.version import __version__ as predictor_version
from mykatlas.version import __version__ as atlas_version

from mongoengine import EmbeddedDocumentField
from mongoengine import IntField
from mongoengine import DictField
from mongoengine import StringField

STAPH_PANELS = ["data/panels/staph-species-160227.fasta.gz",
                "data/panels/staph-amr-probe_set_v0_3_13-160715.fasta.gz"]

GN_PANELS = [
    "data/panels/gn-amr-genes",
    "data/panels/Escherichia_coli",
    "data/panels/Klebsiella_pneumoniae",
    "data/panels/gn-amr-genes-extended"]


class MykrobePredictorResult(object):

    def __init__(self, susceptibility, phylogenetics,
                 variant_calls, sequence_calls,
                 kmer, probe_sets, files, version):
        self.susceptibility = susceptibility
        self.phylogenetics = phylogenetics
        self.variant_calls = variant_calls
        self.sequence_calls = sequence_calls
        self.kmer = kmer
        self.probe_sets = probe_sets
        self.files = files
        self.version = version

    def to_dict(self):
        return {"susceptibility": self.susceptibility.to_dict().values()[0],
                "phylogenetics": self.phylogenetics.to_dict().values()[0],
                "variant_calls": self.variant_calls,
                "sequence_calls": self.sequence_calls,
                "kmer": self.kmer,
                "probe_sets": self.probe_sets,
                "files": self.files,
                "version": self.version
                }


@hug.get()
def predict(file: hug.types.text):
    sample = file.split(".")[0]

    base_json = {sample: {}}
    hierarchy_json_file = None
    TB_PANELS = [
        "data/panels/tb-species-160330.fasta.gz",
        "data/panels/tb-amr-walker_2015.fasta.gz"]

    panels = TB_PANELS
    panel_name = "tb-amr"
    hierarchy_json_file = "data/phylo/mtbc_hierarchy.json"
    # Predictor = GramNegPredictor
    logging.info("Running AMR prediction with panels %s" % ", ".join(panels))
    version = {}
    version["mykrobe-predictor"] = predictor_version
    version["mykrobe-atlas"] = atlas_version
    # Get real paths for panels
    panels = [
        os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                f)) for f in panels]
    if hierarchy_json_file is not None:
        hierarchy_json_file = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                hierarchy_json_file))
    # Run Cortex
    cp = CoverageParser(
        sample=sample,
        panel_file_paths=panels,
        seq=[file],
        kmer=21,
        force=False,
        threads=1,
        verbose=False,
        tmp_dir="/tmp",
        skeleton_dir="atlas/data/skeletons/",
        mccortex31_path="mccortex31")
    cp.run()
    # Detect species
    species_predictor = AMRSpeciesPredictor(
        phylo_group_covgs=cp.covgs.get(
            "complex",
            cp.covgs.get(
                "phylo_group",
                {})),
        sub_complex_covgs=cp.covgs.get(
            "sub-complex",
            {}),
        species_covgs=cp.covgs["species"],
        lineage_covgs=cp.covgs.get(
            "sub-species",
            {}),
        hierarchy_json_file=hierarchy_json_file)
    phylogenetics = species_predictor.run()

    # ## AMR prediction

    depths = []
    Predictor = None
    if species_predictor.is_saureus_present():
        depths = [species_predictor.out_json["phylogenetics"]
                  ["phylo_group"]["Staphaureus"]["median_depth"]]
        Predictor = StaphPredictor
    elif species_predictor.is_mtbc_present():
        depths = [species_predictor.out_json["phylogenetics"]["phylo_group"][
            "Mycobacterium_tuberculosis_complex"]["median_depth"]]
        Predictor = TBPredictor
    elif species_predictor.is_gram_neg_present():
        Predictor = GramNegPredictor
        try:
            depths = [species_predictor.out_json["phylogenetics"][
                "species"]["Klebsiella_pneumoniae"]["median_depth"]]
        except KeyError:
            depths = [species_predictor.out_json["phylogenetics"]
                      ["species"]["Escherichia_coli"]["median_depth"]]
    # pprint (species_predictor.out_json["phylogenetics"]["species"])
    # Genotype
    variant_calls_dict = {}
    sequence_calls_dict = {}
    if depths:
        gt = Genotyper(sample=sample, expected_depths=depths,
                       variant_covgs=cp.variant_covgs,
                       gene_presence_covgs=cp.covgs["presence"],
                       base_json=base_json,
                       contamination_depths=[],
                       report_all_calls=True,
                       ignore_filtered=True,
                       variant_confidence_threshold=0,
                       sequence_confidence_threshold=1
                       )
        gt.run()
        variant_calls_dict = gt.variant_calls_dict
        sequence_calls_dict = gt.sequence_calls_dict
    else:
        depths = cp.estimate_depth()
    mykrobe_predictor_susceptibility_result = MykrobePredictorSusceptibilityResult()
    predictor = Predictor(variant_calls=gt.variant_calls,
                          called_genes=gt.gene_presence_covgs,
                          base_json=base_json[sample],
                          depth_threshold=1,
                          ignore_filtered=True)
    mykrobe_predictor_susceptibility_result = predictor.run()
    base_json[
        sample] = MykrobePredictorResult(
        susceptibility=mykrobe_predictor_susceptibility_result,
        phylogenetics=phylogenetics,
        variant_calls=variant_calls_dict,
        sequence_calls=sequence_calls_dict,
        probe_sets=panels,
        files=[file],
        kmer=21,
        version=version).to_dict()
    cp.remove_temporary_files()
    return base_json
