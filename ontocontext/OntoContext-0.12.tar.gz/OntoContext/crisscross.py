# Author:      BEDHIAFI walid
#
# Created:     20/08/2016
# Copyright:   (c) BEDHIAFI walid 2016
# Licence:     <MIT>
#-------------------------------------------------------------------------------
#!/usr/bin/python


from Tkinter import *
import sqlite3 as lite
import operator

###############################Graphical interface###############################################

class ListBoxChoice(object):
    def __init__(self, master=None, title=None, message=None, list=[]):
        self.master = master
        self.value = None
        self.list = list[:]
        
        self.modalPane = Toplevel(self.master)

        self.modalPane.transient(self.master)
        self.modalPane.grab_set()

        self.modalPane.bind("<Return>", self._choose)
        self.modalPane.bind("<Escape>", self._cancel)

        if title:
            self.modalPane.title(title)

        if message:
            Label(self.modalPane, text=message).pack(padx=5, pady=5)

        listFrame = Frame(self.modalPane)
        listFrame.pack(side=TOP, padx=5, pady=5)
        
        xscrollbar = Scrollbar(listFrame, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)
        
        scrollBar = Scrollbar(listFrame)
        scrollBar.pack(side=RIGHT, fill=Y)
        self.listBox = Listbox(listFrame, selectmode=SINGLE)
        self.listBox.pack(side=LEFT, fill=Y)
        scrollBar.config(command=self.listBox.yview)
        xscrollbar.config(command=self.listBox.xview)
        self.listBox.config(yscrollcommand=scrollBar.set)
        self.listBox.config(xscrollcommand=xscrollbar.set)
        #self.list.sort()
        for item in self.list:
            self.listBox.insert(END, item)

        buttonFrame = Frame(self.modalPane)
        buttonFrame.pack(side=BOTTOM)

        chooseButton = Button(buttonFrame, text="Choose", command=self._choose)
        chooseButton.pack()

        cancelButton = Button(buttonFrame, text="Cancel", command=self._cancel)
        cancelButton.pack(side=RIGHT)

    def _choose(self, event=None):
        try:
            firstIndex = self.listBox.curselection()[0]
            self.value = self.list[int(firstIndex)]
        except IndexError:
            self.value = None
        self.modalPane.destroy()

    def _cancel(self, event=None):
        self.modalPane.destroy()
        
    def returnValue(self):
        self.master.wait_window(self.modalPane)
        return self.value


class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

###############################Generate Children###############################################
def all_children(concepts, table):
	con = lite.connect('Concepts.sqlite')
	cur = con.cursor()
	cc='/'+concepts+'/'
	req1=('Select Distinct Concept From '+table+' where Anc LIKE ("%'+cc+'%")')
	cur.execute(req1)
	return cur.fetchall()

###############################User parameters from the graphical interface#####################
def param():
	def allstates(): 
		print(list(lng.state()), list(tgl.state()))
		return (list(lng.state()), list(tgl.state()))
	root=Tk()
	lng = Checkbar(root, ['Sort by alphabetic order', 'Sort by frequency'])
	tgl = Checkbar(root, ['Only texts where gene are mentioned'])
	lng.pack(side=TOP,  fill=X)
	tgl.pack(side=LEFT)
	Button(root, text='Validate', command=root.quit).pack(side=RIGHT)
	Button(root, text='My choice', command=allstates).pack(side=RIGHT)
	root.mainloop()
	return allstates()

###############################Select art with mentioned gene#####################
def first_inter(text_table):
	K=param()
	C=K[1]
	if K[1]==[1]:
		text_list=list()
		con = lite.connect('Concepts.sqlite')
		cur = con.cursor()
		req=("Select Distinct Art From " +text_table)
		cur.execute(req)
		sec2=cur.fetchall()
		for i in sec2:
			text_list=text_list+[i[0]]
	else:
		text_list=list()
		con = lite.connect('Concepts.sqlite')
		cur = con.cursor()
		req=("Select Distinct Art From "+text_table+" where Onto LIKE ('%B-%')")
		cur.execute(req)
		sec2=cur.fetchall()
		for i in sec2:
			text_list=text_list+[i[0]]
	return (text_list,K)

###############################The choosing process##################################
def choosing (text_table,ontology, part):
	text_liste=first_inter(text_table)
	text_list=text_liste[0]
	L=text_liste[1]
	print "This step may take few minutes"
	con = lite.connect('Concepts.sqlite')
	cur = con.cursor()
	my_cell_liste=list()
	for i in text_list:
		req=('SELECT DISTINCT Concept FROM '+ text_table+' WHERE Onto="'+ontology+'" and Art="'+i+'"')
		cur.execute(req)
		sec2=cur.fetchall()
		for i in sec2:
			my_cell_liste=my_cell_liste+[i[0]]
	list(set(my_cell_liste))
	my_concept_list=list()
	my_dict_concept=dict()
	for i in list(set(my_cell_liste)):
		C=list(set(all_children(str(i), str(ontology)+'_ALL_PATH')))
		my_concept_list=my_concept_list+[i]
		my_dict_concept[i]=[i]
		for u in C:
			my_concept_list=my_concept_list+[u[0]]
			my_dict_concept[i]=my_dict_concept[i]+[u[0]]
	KK=dict()
	My_dict_art=dict()
	My_dict_art1=dict()
	for i in my_dict_concept:
		My_dict_art1[i]=list()
		for g in list(set(my_dict_concept[i])):
			req=('SELECT DISTINCT Art FROM '+ text_table+' WHERE Onto="'+ontology+'" and Concept="'+g+'"')
			cur.execute(req)
			sec2=cur.fetchall()
			if sec2:
				for j in sec2:
					My_dict_art1[i]=My_dict_art1[i]+[j[0]]
		My_dict_art[i]=list(set(My_dict_art1[i]))
		KK[i]=len(My_dict_art[i])
	if L[0][0]==1:
		GG=sorted(KK.items(), key=lambda x:x[0])
	else:
		GG= sorted(KK.items(), key=lambda x:x[1], reverse=True)
	list_cell=list()
	for o in GG:
		texte=str(o[1])+'\t'+str(o[0])
		list_cell=list_cell+[texte]
	root=Tk()
	returnValue = True
	my_cell_list=list()
	while returnValue:
		returnValue = ListBoxChoice(root, str(part)+" part", "When your choice is done clic choose", list_cell).returnValue()
		my_cell_list=my_cell_list+[returnValue]
	root.mainloop()
	my_choosed_list=list()
	for i in my_cell_list:
		if i:		
			h=i.split('\t')
			my_choosed_list=my_choosed_list+[h[1]]
	terms_dict=dict()
	for i in my_choosed_list:
		terms_list=[i]
		for j in my_dict_concept:
			if i == j:
				print my_dict_concept[j]
				for k in my_dict_concept[j]:
					print str(i)+' has mentioned child: '+str(k)
					terms_list=terms_list+[k]
		terms_dict[i]=list(set(terms_list))
	return (terms_dict,My_dict_art)
###############################The crossover##################################
def crisscross(text_table):
	con = lite.connect('Concepts.sqlite')
	cur = con.cursor()
	CC=choosing (text_table,'CL', 'Cell populations')
	Dis=choosing (text_table,'DOID', 'Diseases')
	Ana=choosing (text_table,'UBERON', 'Anatomy')
	protein_dict=dict()
	DNA_dict=dict()
	RNA_dict=dict()
	print "starting the crisscross process"
	for i in CC[0]:
		for j in Dis[0]:
			for k in Ana[0]:
				dict_name=str(i)+str(j)+str(k)
				protein_dict[dict_name]=list()
				DNA_dict[dict_name]=list()
				RNA_dict[dict_name]=list()
				for l in list(set(CC[1][i])):
					for m in list(set(Dis[1][j])):
						for n in list(set(Ana[1][k])):
							if l==m==n:
								req=('SELECT DISTINCT Concept FROM '+ text_table+' WHERE Onto="B-protein"and Art="'+l+'"')
								cur.execute(req)
								sec2=cur.fetchall()
								if sec2:
										for o in sec2:
											protein_dict[dict_name]=protein_dict[dict_name]+[o[0]]
								req2=('SELECT DISTINCT Concept FROM '+ text_table+' WHERE Onto="B-DNA"and Art="'+l+'"')
								cur.execute(req2)
								sec3=cur.fetchall()
								if sec3:
										for p in sec3:
											DNA_dict[dict_name]=DNA_dict[dict_name]+[p[0]]
								req4=('SELECT DISTINCT Concept FROM '+ text_table+' WHERE Onto="B-RNA"and Art="'+l+'"')
								cur.execute(req4)
								sec4=cur.fetchall()
								if sec3:
										for q in sec3:
											RNA_dict[dict_name]=RNA_dict[dict_name]+[q[0]]
	return (protein_dict,DNA_dict,RNA_dict)
