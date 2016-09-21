# Author:      BEDHIAFI walid
#
# Created:     20/08/2016
# Copyright:   (c) BEDHIAFI walid 2016
# Licence:     <MIT>
#-------------------------------------------------------------------------------
#!/usr/bin/python
import nltk
import re
import os.path
import glob
import sqlite3 as lite
import sys
import time
import geniatagger
#nltk.download()
reload(sys)
sys.setdefaultencoding("utf-8")


#########################################Searching for Ontological concepts############################################ 
#Searching One_word concepts 
def one_Concept(sentence,onto):
	jupper=sentence.upper()
	tokens = nltk.word_tokenize(jupper)
	oneconcept=list()
	for o in tokens:
			con = lite.connect('Concepts.sqlite')
			cur = con.cursor()
			req2=('SELECT Concept from '+onto+'_concepts_tag_up WHERE Reg_exp=="one" and Concept=="%s"'%o)
			cur.execute(req2)
			sec2=cur.fetchall()
			if len(sec2)>0:
				if len(sec2[0][0])>2:
					oneconcept=oneconcept+[sec2[0][0]]
	return oneconcept
#Searching Multi_word concepts
def comp_concept(sentence,onto):
	jupper=sentence.upper()
	tokens = nltk.word_tokenize(jupper)
	pos_tag = nltk.pos_tag(tokens)
	CC=list()
	for i in pos_tag:
		C=list(i)
		if C[1]=='NNP':
			CC=CC+[[C[0],'NN']]
		else:
			CC=CC+[C]
	tt=''
	for i in CC:
		tt=tt+i[1]+' '
	con = lite.connect('Concepts.sqlite')
	cur = con.cursor()
	req2="SELECT Tag from "+onto+"_concepts_tag_up WHERE Reg_exp!='one'"
	cur.execute(req2)
	sec=cur.fetchall()
	C=(set(sec))
	list_reg=list()
	for reg in C:
		if reg[0] in tt or reg[0]==tt:
			list_reg=list_reg+[reg[0]]
	list_term=list()
	for i in list_reg:
		re_i=i.split()
		for j in CC:
			if re_i[0]==j[1]:
				v=CC.index(j)
				l=0
				term=''
				while CC[v][1]==re_i[l] and v<len(CC)-1 and l<len(re_i)-1:
						term=term+CC[v][0]+' '
						v=v+1
						l=l+1
				list_term=list_term+[term+CC[v][0]]
	req_list=list()
	for i in set(list_term):
		X=i.replace('( ','(')
		CV=X.replace(' )',')')
		CV1=CV.replace(' ,',',')
		req_list=req_list+[CV1]
	up_res=list()
	for i in req_list:
		t=i
		cur.execute('SELECT Concept from '+onto+'_concepts_tag_up WHERE Concept =="%s"' %t)
		sec=cur.fetchall()
		if sec:
			up_res=up_res+[sec[0][0]]
	jupper=sentence.lower()
	tokens = nltk.word_tokenize(jupper)
	pos_tag = nltk.pos_tag(tokens)
	CC=list()
	for i in pos_tag:
		C=list(i)
		if C[1]=='NNP':
			CC=CC+[[C[0],'NN']]
		else:
			CC=CC+[C]
	tt=''
	for i in CC:
		tt=tt+i[1]+' '
	con = lite.connect('Concepts.sqlite')
	cur = con.cursor()
	req2="SELECT Tag from "+onto+"_concepts_tag_min WHERE Reg_exp!='one'"
	cur.execute(req2)
	sec=cur.fetchall()
	C=(set(sec))
	list_reg=list()
	for reg in C:
		if reg[0] in tt or reg[0]==tt:
			list_reg=list_reg+[reg[0]]
	list_term=list()
	for i in list_reg:
		re_i=i.split()
		for j in CC:
			if re_i[0]==j[1]:
				v=CC.index(j)
				l=0
				term=''
				while CC[v][1]==re_i[l] and v<len(CC)-1 and l<len(re_i)-1:
						term=term+CC[v][0]+' '
						v=v+1
						l=l+1
				list_term=list_term+[term+CC[v][0]]
	req_list=list()
	for i in set(list_term):
		X=i.replace('( ','(')
		CV=X.replace(' )',')')
		CV1=CV.replace(' ,',',')
		req_list=req_list+[CV1]
	up_res=list()
	for i in req_list:
		t=i
		cur.execute('SELECT Concept from '+onto+'_concepts_tag_min WHERE Concept =="%s"' %t)
		sec=cur.fetchall()
		if sec:
			up_res=up_res+sec
	return up_res
#########################################Searching for gene names############################################ 
def gene (sent,tagger):
	c=tagger.parse(sent)
	tup_gene=list()
	name_list=list()
	for i in c:
		if len(i[4])>1:
			if 'cell' in i[4]:
				print 'in progress'
			else:
				tup_gene=tup_gene+[(i[1],i[4])]
	if len(tup_gene)>0:
		big_list=list()
		for i in range (0,len(tup_gene)):
			if 'B-' in tup_gene[i][1]:
				big_list=big_list+[i]
				genre=tup_gene[i][1]
		big_list=big_list+[len(tup_gene)+1]
		for j in range (0,len(big_list)-1):
			name=''
			c=(big_list[j+1])
			t=big_list[j]
			my_name=''
			t=tup_gene[big_list[j]:c]
			for i in t:
				name=name+' '+i[0]
			name_list=name_list+[(name,genre)]
	return name_list
#########################################Searching synonimes#########################################
def syno (Ontology, liste):
	con = lite.connect('Concepts.sqlite')
	cur = con.cursor()
	listy=list()
	for i in  set(liste):
		try:
			req='SELECT Concept from '+Ontology+'_Synonym WHERE Syno=="%s"'%i.upper()
			cur.execute(req)
			sec=cur.fetchall()
			if sec:
				for j in sec:
					listy=listy+[j[0]]
		except AttributeError:
			req='SELECT Concept from '+Ontology+'_Synonym WHERE Syno=="%s"'%i[0].upper()
			cur.execute(req)
			sec=cur.fetchall()
			if sec:
				for j in sec:
					listy=listy+[j[0]]
	return list(set(listy))
#########################################Annotation concepts############################################ 
def annotation(directory, table_name, GeniaPath):
	tagger = geniatagger.GeniaTagger(GeniaPath)
	con = lite.connect('Concepts.sqlite')
	cur = con.cursor()
	rzq='DROP TABLE IF EXISTS '+table_name
	print rzq
	cur.execute(rzq)
	raq='CREATE TABLE '+table_name+' (Art , Concept , Onto)'
	cur.execute(raq)
	texte=''	
	for filename in glob.glob(os.path.join(directory, '*.txt')):
		tt=time.time()
		print '--------------<'+str(filename)+'>--------------'
		texte=texte+'--------------<'+str(filename)+'>--------------'+'\n'
		fil1=open(filename,'r')
		liste=fil1.read()
		liste2=liste.replace('\n',' ')
		liste1=liste2.split('. ')
		if '' in liste1:
			liste1.remove('')
		list_one_cl=list()
		list_comp_cl=list()
		list_one_doid=list()
		list_comp_doid=list()
		list_one_uberon=list()
		list_comp_uberon=list()
		list_gene=list()
		for sent in liste1:
			list_one_cl=list_one_cl+one_Concept(sent,'CL')
			list_comp_cl=list_comp_cl+comp_concept(sent,'CL')
			list_one_doid=list_one_doid+one_Concept(sent,'DOID')
			list_comp_doid=list_comp_doid+comp_concept(sent,'DOID')
			list_one_uberon=list_one_uberon+one_Concept(sent,'UBERON')
			list_comp_uberon=list_comp_uberon+comp_concept(sent,'UBERON')
			list_gene=gene(sent,tagger)
			liste=['+','-']
			newsent=sent.translate(None, ''.join(liste))
			list_N_gene=gene(newsent,tagger)
		N_list_gene=list_gene+list_N_gene
		all_cell=list_one_cl+list_comp_cl
		#print all_cell
		syno_cell=syno ('CL', all_cell)
		art1=str(filename)
		art2=art1.split('/')
		art3=art2[1].split('.txt')
		art4=art3[0]
		for C in syno_cell:
				with con:
					cur.execute('INSERT INTO '+table_name+' (Art , Concept , Onto) VALUES (?,?,?)',(art4,str(C),'CL'))
		texte=texte+'\n'+'Cell Pop:'
		for k in list(set(list_one_cl)):
			texte=texte+'\t'+str(k)
		for k in list(set(list_comp_cl)):
			texte=texte+'\t'+k[0]
		all_dis=list_one_doid+list_comp_doid
		syno_dis=syno ('DOID', all_dis)
		for C in syno_dis:
			with con:
				cur.execute('INSERT INTO '+table_name+' (Art , Concept , Onto) VALUES (?,?,?)',(art4,str(C),'DOID'))
		texte=texte+'\n'+'Disease:'
		for k in list(set(list_one_doid)):
			texte=texte+'\t'+str(k)
		for k in list(set(list_comp_doid)):
			texte=texte+'\t'+k[0]
		all_ana=list_one_uberon+list_comp_uberon
		syno_ana=syno ('UBERON', all_ana)
		for C in syno_ana:
			with con:
				cur.execute('INSERT INTO '+table_name+' (Art , Concept , Onto) VALUES (?,?,?)',(art4,str(C),'UBERON'))
		texte=texte+'\n'+'Anatomy:'
		for k in list(set(list_one_uberon)):
			texte=texte+'\t'+str(k)
		for k in list(set(list_comp_uberon)):
			texte=texte+'\t'+k[0]
		texte=texte+'\n'+'Gene:'
		for k in list(set(N_list_gene)):
			try: 
				with con:
					cur.execute('INSERT INTO '+table_name+' (Art , Concept , Onto) VALUES (?,?,?)',(art4,str(k[0]),str(k[1])))
				texte=texte+'\t'+k[0]+'||'+k[1]
			except lite.ProgrammingError:
				con = lite.connect('Concepts.sqlite')
				con.text_factory = str
				cur = con.cursor()
				with con:
					cur.execute('INSERT INTO '+table_name+' (Art , Concept , Onto) VALUES (?,?,?)',(art4,str(k[0]),str(k[1])))
		ttt=time.time()		
		texte=texte+'\n'+str(ttt-tt)
		print (ttt-tt)
	lif=directory+'res.txt'
	fil=open(str(lif),'w')
	fil.write(texte)
	fil.close()
	print 'The annotation process is done'

