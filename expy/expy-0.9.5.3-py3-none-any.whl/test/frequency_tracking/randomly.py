import pandas as pd
import numpy as np

path = ''

# read list with fixed nonword
stim_py_nonword = pd.read_excel(path+'stimuli_pinyin_with_nonword.xlsx')
stim_py_nonword['Pinyin'] = stim_py_nonword['Pinyin'].apply(lambda x:x.split(' '))

svo = list(stim_py_nonword[(stim_py_nonword.Type=='SVO') & stim_py_nonword.Real==1].Sent)
sv = list(stim_py_nonword[(stim_py_nonword.Type=='SV') & stim_py_nonword.Real==1].Sent)

from collections import Counter

def make_trials(structure,tag,blockID): 
    sentence_list = []
    if structure=='SVO':
        sentence_list = svo
    elif structure=='SV':
        sentence_list = sv

    if tag == 0: structure += '_RND'

    while 1:
        trial_list = [set([s+str(tag) for s in np.random.permutation(np.random.choice(sentence_list,10,replace=False))])]
        for i in range(1,30):
            while 1:
                trial = set([s+str(tag) for s in np.random.permutation(np.random.choice(sentence_list,10,replace=False))])
                if trial&trial_list[i-1]==set():
                    trial_list.append(trial)
                    break

        if Counter([s for i in trial_list for s in list(i)]).most_common(1)[0][1]<8:
            break

    trial_list = [[list(i),structure,True,blockID] for i in trial_list]
    
    for i in np.random.choice(range(30),10,replace=False):
        for j in np.random.choice(range(10),2,replace=False):
            trial_list[i][0][j] = trial_list[i][0][j][:-1]+str(1-tag)
            trial_list[i][2] = False
    
    trial_list = [(' '.join(i[0]),i[1],i[2],i[3]) for i in trial_list]
            
    return trial_list


trials = np.concatenate([make_trials('SVO',1,1),
                         make_trials('SV',1,2),
                         make_trials('SV',0,3),
                         make_trials('SV',1,5),
                         make_trials('SVO',0,6),
                         make_trials('SVO',1,4),])
                         

pd.DataFrame(trials,columns=['content','type','pure','block']).to_csv(path+'trial_list.csv',index=None)