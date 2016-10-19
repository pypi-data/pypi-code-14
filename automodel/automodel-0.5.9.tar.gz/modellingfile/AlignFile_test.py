import unittest
import os
import shutil
from should_dsl import *
from AlignFile import *


class AlignFileTest(unittest.TestCase):
	def setUp(self):
		self.ali_file_name = "tests/models/ali.ali"
		os.remove(self.ali_file_name)
		shutil.copyfile("tests/models/ali2.ali", self.ali_file_name)
		self.aliali = AlignFile(self.ali_file_name)

	def test_if_select_a_sequence(self):
		self.aliali.select_sequence(1)
		self.aliali.selected_sequence |should| equal_to(0)

	def test_if_fix_sequence_internaly(self):
		broken_sequence = [">P1;7mdh\nstructureX:7mdh.pdb:  23 :A:+858 :B:MOL_ID  1; MOLECULE  PROTEIN (MALATE DEHYDROGENASE); CHAIN  A,B; EC  1.1.1.82; ENGINEERED  YES; MUTATION  YES:MOL_ID  1; ORGANISM_SCIENTIFIC  SORGHUM BICOLOR; ORGANISM_COMMON  SORGHUM; ORGANISM_TAXID  4558; TISSUE  LEAF; ORGANELLE  CHLOROPLAST; EXPRESSION_SYSTEM  ESCHERICHIA COLI BL21(DE3); EXPRESSION_SYSTEM_TAXID  469008; EXPRESSION_SYSTEM_STRAIN  BL21(DE3); EXPRESSION_SYSTEM_PLASMID  PET: 2.40: 0.22\nDCFGVFCTWKKLVNIAVSGAAGMISNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLRE\nVSIGIDPYEVFEDVDWALLIGAKPRGPGMERAALLDINGQIFADQGKALNAVASKNVKVLVVGNPCNTNALICLK\nNAPDIPAKNFHALTRLDENRAKCQLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKIDGRPVKEVIKRTKWLEE\nEFTITVQKRGGALIQKWGRSSAASTAVSIADAIKSLVTPTPEGDWFSTGVYTTGNPYGIAEDIVFSMPCRSKGDG\nDYELATDVSNDDFLWERIKKSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLzzzzwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww/RKDCFGVFCTTYDLKSWKKLVNIAVSGAAGMIS\nNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLREVSIGIDPYEVFEDVDWALLIGAKPR\nGPGMERAALLDINGQIFADQGKALNAVASK-NVKVLVVGNPCNTNALICLKNAPDIPAKNFHALTRLDENRAKCQ\nLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKI--DGRPVKEV-IKRTKWLEEEFTITVQKRGGALIQKWGRSS\nAASTAVSIADAIKSLVTPTPEGDWFSTGVYTT-GNPYGIAEDIVFSMPCRSKGDGDYELATDVSNDDFLWERIKK\nSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLPzzzzzwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww*",
		"P1;seq.ali\nsequence:seq.ali:     : :     : :::-1.00:-1.00\n--------MSEAAHVLITGAAGQIGYILSHWIASGELYG-DRQVYLHLLDIPPAMNRLTALTMELEDCAFPHLAG\nFVATTDPKAAFKDIDCAFLVASMPLKPGQVRADLISSNSVIFKNTGEYLSKWAKPSVKVLV--------------\n------------IGNPDN--TNCEIAM---L--------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------HAKNLKP-ENFS------------\n-------------------SLSML--------------------------------D------------------\n-------------------QNRAYYEVASKL-----------------------GVDVKDVHDII----------\n----------------VWGNHGESMVADLTQATFTKEGKTQKVVDVLDHDYVFDTFFKKIGHRAWDILEHRGFTS\nAASPTKAAIQHMKAWLFGTAPGEVLSMGIPVPEGNPYGIKPGVVFSFPCNVDKEGKIHVVEGFKVNDWLREKLDF\nTEKDLFHEKEIALNHLAQGG-------------------------------------------------------\n---------------------------------------*\n"]
		fixed_sequence = [">P1;7mdh\nstructureX:7mdh.pdb:  23 :A:+858 :B:MOL_ID  1; MOLECULE  PROTEIN (MALATE DEHYDROGENASE); CHAIN  A,B; EC  1.1.1.82; ENGINEERED  YES; MUTATION  YES:MOL_ID  1; ORGANISM_SCIENTIFIC  SORGHUM BICOLOR; ORGANISM_COMMON  SORGHUM; ORGANISM_TAXID  4558; TISSUE  LEAF; ORGANELLE  CHLOROPLAST; EXPRESSION_SYSTEM  ESCHERICHIA COLI BL21(DE3); EXPRESSION_SYSTEM_TAXID  469008; EXPRESSION_SYSTEM_STRAIN  BL21(DE3); EXPRESSION_SYSTEM_PLASMID  PET: 2.40: 0.22\nDCFGVFCTWKKLVNIAVSGAAGMISNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLRE\nVSIGIDPYEVFEDVDWALLIGAKPRGPGMERAALLDINGQIFADQGKALNAVASKNVKVLVVGNPCNTNALICLK\nNAPDIPAKNFHALTRLDENRAKCQLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKIDGRPVKEVIKRTKWLEE\nEFTITVQKRGGALIQKWGRSSAASTAVSIADAIKSLVTPTPEGDWFSTGVYTTGNPYGIAEDIVFSMPCRSKGDG\nDYELATDVSNDDFLWERIKKSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLzzzzwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww/RKDCFGVFCTTYDLKSWKKLVNIAVSGAAGMIS\nNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLREVSIGIDPYEVFEDVDWALLIGAKPR\nGPGMERAALLDINGQIFADQGKALNAVASK-NVKVLVVGNPCNTNALICLKNAPDIPAKNFHALTRLDENRAKCQ\nLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKI--DGRPVKEV-IKRTKWLEEEFTITVQKRGGALIQKWGRSS\nAASTAVSIADAIKSLVTPTPEGDWFSTGVYTT-GNPYGIAEDIVFSMPCRSKGDGDYELATDVSNDDFLWERIKK\nSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLPzzzzzwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww*",
		">P1;seq.ali\nsequence:seq.ali:     : :     : :::-1.00:-1.00\n--------MSEAAHVLITGAAGQIGYILSHWIASGELYG-DRQVYLHLLDIPPAMNRLTALTMELEDCAFPHLAG\nFVATTDPKAAFKDIDCAFLVASMPLKPGQVRADLISSNSVIFKNTGEYLSKWAKPSVKVLV--------------\n------------IGNPDN--TNCEIAM---L--------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------HAKNLKP-ENFS------------\n-------------------SLSML--------------------------------D------------------\n-------------------QNRAYYEVASKL-----------------------GVDVKDVHDII----------\n----------------VWGNHGESMVADLTQATFTKEGKTQKVVDVLDHDYVFDTFFKKIGHRAWDILEHRGFTS\nAASPTKAAIQHMKAWLFGTAPGEVLSMGIPVPEGNPYGIKPGVVFSFPCNVDKEGKIHVVEGFKVNDWLREKLDF\nTEKDLFHEKEIALNHLAQGG-------------------------------------------------------\n---------------------------------------*"]
		self.aliali.__fix_sequence__(broken_sequence) |should| equal_to(fixed_sequence)

	def test_if_fix_the_first_sequence_internaly(self):
		broken_sequence = ["P1;7mdh\nstructureX:7mdh.pdb:  23 :A:+858 :B:MOL_ID  1; MOLECULE  PROTEIN (MALATE DEHYDROGENASE); CHAIN  A,B; EC  1.1.1.82; ENGINEERED  YES; MUTATION  YES:MOL_ID  1; ORGANISM_SCIENTIFIC  SORGHUM BICOLOR; ORGANISM_COMMON  SORGHUM; ORGANISM_TAXID  4558; TISSUE  LEAF; ORGANELLE  CHLOROPLAST; EXPRESSION_SYSTEM  ESCHERICHIA COLI BL21(DE3); EXPRESSION_SYSTEM_TAXID  469008; EXPRESSION_SYSTEM_STRAIN  BL21(DE3); EXPRESSION_SYSTEM_PLASMID  PET: 2.40: 0.22\nDCFGVFCTWKKLVNIAVSGAAGMISNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLRE\nVSIGIDPYEVFEDVDWALLIGAKPRGPGMERAALLDINGQIFADQGKALNAVASKNVKVLVVGNPCNTNALICLK\nNAPDIPAKNFHALTRLDENRAKCQLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKIDGRPVKEVIKRTKWLEE\nEFTITVQKRGGALIQKWGRSSAASTAVSIADAIKSLVTPTPEGDWFSTGVYTTGNPYGIAEDIVFSMPCRSKGDG\nDYELATDVSNDDFLWERIKKSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLzzzzwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww/RKDCFGVFCTTYDLKSWKKLVNIAVSGAAGMIS\nNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLREVSIGIDPYEVFEDVDWALLIGAKPR\nGPGMERAALLDINGQIFADQGKALNAVASK-NVKVLVVGNPCNTNALICLKNAPDIPAKNFHALTRLDENRAKCQ\nLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKI--DGRPVKEV-IKRTKWLEEEFTITVQKRGGALIQKWGRSS\nAASTAVSIADAIKSLVTPTPEGDWFSTGVYTT-GNPYGIAEDIVFSMPCRSKGDGDYELATDVSNDDFLWERIKK\nSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLPzzzzzwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww*",
		">P1;seq.ali\nsequence:seq.ali:     : :     : :::-1.00:-1.00\n--------MSEAAHVLITGAAGQIGYILSHWIASGELYG-DRQVYLHLLDIPPAMNRLTALTMELEDCAFPHLAG\nFVATTDPKAAFKDIDCAFLVASMPLKPGQVRADLISSNSVIFKNTGEYLSKWAKPSVKVLV--------------\n------------IGNPDN--TNCEIAM---L--------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------HAKNLKP-ENFS------------\n-------------------SLSML--------------------------------D------------------\n-------------------QNRAYYEVASKL-----------------------GVDVKDVHDII----------\n----------------VWGNHGESMVADLTQATFTKEGKTQKVVDVLDHDYVFDTFFKKIGHRAWDILEHRGFTS\nAASPTKAAIQHMKAWLFGTAPGEVLSMGIPVPEGNPYGIKPGVVFSFPCNVDKEGKIHVVEGFKVNDWLREKLDF\nTEKDLFHEKEIALNHLAQGG-------------------------------------------------------\n---------------------------------------*\n"]
		fixed_sequence = [">P1;7mdh\nstructureX:7mdh.pdb:  23 :A:+858 :B:MOL_ID  1; MOLECULE  PROTEIN (MALATE DEHYDROGENASE); CHAIN  A,B; EC  1.1.1.82; ENGINEERED  YES; MUTATION  YES:MOL_ID  1; ORGANISM_SCIENTIFIC  SORGHUM BICOLOR; ORGANISM_COMMON  SORGHUM; ORGANISM_TAXID  4558; TISSUE  LEAF; ORGANELLE  CHLOROPLAST; EXPRESSION_SYSTEM  ESCHERICHIA COLI BL21(DE3); EXPRESSION_SYSTEM_TAXID  469008; EXPRESSION_SYSTEM_STRAIN  BL21(DE3); EXPRESSION_SYSTEM_PLASMID  PET: 2.40: 0.22\nDCFGVFCTWKKLVNIAVSGAAGMISNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLRE\nVSIGIDPYEVFEDVDWALLIGAKPRGPGMERAALLDINGQIFADQGKALNAVASKNVKVLVVGNPCNTNALICLK\nNAPDIPAKNFHALTRLDENRAKCQLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKIDGRPVKEVIKRTKWLEE\nEFTITVQKRGGALIQKWGRSSAASTAVSIADAIKSLVTPTPEGDWFSTGVYTTGNPYGIAEDIVFSMPCRSKGDG\nDYELATDVSNDDFLWERIKKSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLzzzzwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww/RKDCFGVFCTTYDLKSWKKLVNIAVSGAAGMIS\nNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLREVSIGIDPYEVFEDVDWALLIGAKPR\nGPGMERAALLDINGQIFADQGKALNAVASK-NVKVLVVGNPCNTNALICLKNAPDIPAKNFHALTRLDENRAKCQ\nLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKI--DGRPVKEV-IKRTKWLEEEFTITVQKRGGALIQKWGRSS\nAASTAVSIADAIKSLVTPTPEGDWFSTGVYTT-GNPYGIAEDIVFSMPCRSKGDGDYELATDVSNDDFLWERIKK\nSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLPzzzzzwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww*",
		">P1;seq.ali\nsequence:seq.ali:     : :     : :::-1.00:-1.00\n--------MSEAAHVLITGAAGQIGYILSHWIASGELYG-DRQVYLHLLDIPPAMNRLTALTMELEDCAFPHLAG\nFVATTDPKAAFKDIDCAFLVASMPLKPGQVRADLISSNSVIFKNTGEYLSKWAKPSVKVLV--------------\n------------IGNPDN--TNCEIAM---L--------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------HAKNLKP-ENFS------------\n-------------------SLSML--------------------------------D------------------\n-------------------QNRAYYEVASKL-----------------------GVDVKDVHDII----------\n----------------VWGNHGESMVADLTQATFTKEGKTQKVVDVLDHDYVFDTFFKKIGHRAWDILEHRGFTS\nAASPTKAAIQHMKAWLFGTAPGEVLSMGIPVPEGNPYGIKPGVVFSFPCNVDKEGKIHVVEGFKVNDWLREKLDF\nTEKDLFHEKEIALNHLAQGG-------------------------------------------------------\n---------------------------------------*"]
		self.aliali.__fix_sequence__(broken_sequence) |should| equal_to(fixed_sequence)

	def test_if_create_an_temporary_file(self):
		os.path.exists(self.ali_file_name + ".tmp") |should| equal_to(True)

	def test_if_create_list_of_sequences(self):
		align_content = [">P1;7mdh\nstructureX:7mdh.pdb:  23 :A:+858 :B:MOL_ID  1; MOLECULE  PROTEIN (MALATE DEHYDROGENASE); CHAIN  A,B; EC  1.1.1.82; ENGINEERED  YES; MUTATION  YES:MOL_ID  1; ORGANISM_SCIENTIFIC  SORGHUM BICOLOR; ORGANISM_COMMON  SORGHUM; ORGANISM_TAXID  4558; TISSUE  LEAF; ORGANELLE  CHLOROPLAST; EXPRESSION_SYSTEM  ESCHERICHIA COLI BL21(DE3); EXPRESSION_SYSTEM_TAXID  469008; EXPRESSION_SYSTEM_STRAIN  BL21(DE3); EXPRESSION_SYSTEM_PLASMID  PET: 2.40: 0.22\nDCFGVFCTWKKLVNIAVSGAAGMISNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLRE\nVSIGIDPYEVFEDVDWALLIGAKPRGPGMERAALLDINGQIFADQGKALNAVASKNVKVLVVGNPCNTNALICLK\nNAPDIPAKNFHALTRLDENRAKCQLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKIDGRPVKEVIKRTKWLEE\nEFTITVQKRGGALIQKWGRSSAASTAVSIADAIKSLVTPTPEGDWFSTGVYTTGNPYGIAEDIVFSMPCRSKGDG\nDYELATDVSNDDFLWERIKKSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLzzzzwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww/RKDCFGVFCTTYDLKSWKKLVNIAVSGAAGMIS\nNHLLFKLASGEVFGQDQPIALKLLGSERSFQALEGVAMELEDSLYPLLREVSIGIDPYEVFEDVDWALLIGAKPR\nGPGMERAALLDINGQIFADQGKALNAVASK-NVKVLVVGNPCNTNALICLKNAPDIPAKNFHALTRLDENRAKCQ\nLALKAGVFYDKVSNVTIWGNHSTTQVPDFLNAKI--DGRPVKEV-IKRTKWLEEEFTITVQKRGGALIQKWGRSS\nAASTAVSIADAIKSLVTPTPEGDWFSTGVYTT-GNPYGIAEDIVFSMPCRSKGDGDYELATDVSNDDFLWERIKK\nSEAELLAEKKCVAHLTGEGNAYCDVPEDTMLPzzzzzwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww*",
		">P1;seq.ali\nsequence:seq.ali:     : :     : :::-1.00:-1.00\n--------MSEAAHVLITGAAGQIGYILSHWIASGELYG-DRQVYLHLLDIPPAMNRLTALTMELEDCAFPHLAG\nFVATTDPKAAFKDIDCAFLVASMPLKPGQVRADLISSNSVIFKNTGEYLSKWAKPSVKVLV--------------\n------------IGNPDN--TNCEIAM---L--------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------------------------------\n---------------------------------------------------HAKNLKP-ENFS------------\n-------------------SLSML--------------------------------D------------------\n-------------------QNRAYYEVASKL-----------------------GVDVKDVHDII----------\n----------------VWGNHGESMVADLTQATFTKEGKTQKVVDVLDHDYVFDTFFKKIGHRAWDILEHRGFTS\nAASPTKAAIQHMKAWLFGTAPGEVLSMGIPVPEGNPYGIKPGVVFSFPCNVDKEGKIHVVEGFKVNDWLREKLDF\nTEKDLFHEKEIALNHLAQGG-------------------------------------------------------\n---------------------------------------*"]
		self.aliali.__create_sequence_list__(align_content) 
		flag = True
		for eachObjetct in self.aliali.my_ali_file:
			if flag == True and type(eachObjetct) != PirSequence:
				flag = False
		flag |should| equal_to(True)		

	def test_if_show_exact_number_of_sequences(self):
		self.aliali.number_of_sequences() |should| equal_to(2)

	def  test_if_show_heteroatoms_of_an_selected_sequence(self):
		list_of_heteroatoms = ['z', 'w']
		self.aliali.select_sequence(1)
		self.aliali.show_heteroatoms_of_chain(1) |should| equal_to(list_of_heteroatoms)

	def teste_if_change_heteroatom_of_an_sequence(self):
		heteroatoms = ["z", "i"]
		self.aliali.select_sequence(1)
		self.aliali.change_heteroatom_of_chain(1,'w','i')
		self.aliali.show_heteroatoms_of_chain(1) |should| equal_to(heteroatoms)
	
	def test_if_write_changes_in_ali_file(self):
		#writing align file
		self.aliali.select_sequence(1)
		self.aliali.change_heteroatom_of_chain(1,'w','i')
		self.aliali.write_changes()
		self.aliali.close()
		#reopening and verifying content of align file
		heteroatoms = ["z", "i"]
		new_alifile = AlignFile(self.ali_file_name)
		new_alifile.select_sequence(1)
		new_alifile.show_heteroatoms_of_chain(1) |should| equal_to(heteroatoms)

	def test_if_dont_write_changes_in_wrong_location(self):
		#writing align file
		self.aliali.select_sequence(1)
		self.aliali.change_heteroatom_of_chain(1,'w','i')
		self.aliali.write_changes()
		self.aliali.close()
		#reopening and verifying content of align file
		heteroatoms = ["z", "i"]
		new_alifile = AlignFile(self.ali_file_name)
		new_alifile.select_sequence(1)
		new_alifile.show_heteroatoms_of_chain(1) |should| equal_to(heteroatoms)

	def test_if_copy_the_heteroatoms_from_template_for_sequence(self):
		aliali2 = AlignFile("tests/models/ali4.ali")
		aliali2.copy_heteroatoms(0,1)
		heteroatoms = ['$', '2', 'z', 'w']
		aliali2.show_heteroatoms_of_chain(1) |should| equal_to(heteroatoms)

	def  test_if_copy_heteroatom_in_correct_place(self):
		aliali2 = AlignFile("tests/models/ali4.ali")
		aliali2.copy_heteroatoms(0,1)
		correct_sequence = """--------MSEAAHVLITGAAGQIGYILSHWIASGELYG-DRQVYLHLLDIPPAMNRLTALTMELEDCAFPHLAG
FVATTDPKAAFKDIDCAFLVASMPLKPGQVRADLISSNSVIFKNTGEYLSKWAKPSVKVLVIGNPDNTNCEIAML
HAKNLKPENFSSLSMLDQNRAYYEVASKLGVDVKDVHDIIVWGNHGESMVADLTQATFTKEGKTQKVVDVLD-HD
YVFDTFFKKIGHRAWDILEHRGFTSAASPTKAAIQHMKAWLFGTAPGEVLSMGIPVPEGNPYGIKPGVVFSFPCN
VDKEGKIHVVEGFKVNDWLREKLDFTEKDLFHEKEIALNHLAQGG-----------$2zzwwwwwwwwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww*"""
		aliali2.my_ali_file[1].sequence() |should| equal_to(correct_sequence)

	def test_if_replace_temporary_file_with_align_file(self):
		self.aliali.__replace_files__()
		os.path.exists(self.aliali.aliali_file.name) |should| equal_to(True)

	def test_if_close_align_file(self):
		self.aliali.close()
		self.aliali.aliali_file.closed |should| equal_to(True)

	def test_if_closes_temporary_file(self):
		self.aliali.close()
		self.aliali.tmp_align_file.closed |should| equal_to(True)
########################


if __name__ == '__main__':
	unittest.main()