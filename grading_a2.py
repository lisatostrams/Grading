# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 11:10:46 2019

@author: Lisa
"""   

import os
import random

import numpy as np

graders = {"Stijn":  "A.A.deBoer@student.ru.nl", "Francesca":  "F.Drummer@student.ru.nl","Lizzy":  "l.grootjen@student.ru.nl",
"Ron":  "R.Hommelsheim@student.ru.nl", "Elena":  "E.Kreis@student.ru.nl","David":  "h.leeftink@student.ru.nl",
"Lars":  "L.vanRhijn@student.ru.nl","Steffen":  "S.Ricklin@student.ru.nl","Jessie":  "J.vanSchijndel@student.ru.nl"}



import zipfile
import json

markdown = {'2.1.1.a':0,
            '2.1.1.b':3,
            '2.1.2':5,
            '2.2.1':8,
            '2.3.1.i':11,
            '2.3.1.ii':13,
            '2.3.1.iii':15,
            '2.3.1.iv':17,
            '2.3.1.v':19       
        }

code_answers = {'2.1.1.a':1,
            '2.1.2':6,
            '2.2.1':9,
            '2.3.1.i':12,
            '2.3.1.ii':14,
            '2.3.1.iii':16,
            '2.3.1.v':20       
        }

md_answers = {'2.1.1.a':2,
            '2.1.1.b':4,
            '2.1.2':7,
            '2.2.1':10,
            '2.3.1.iv':18,
            '2.3.1.v':21       
        }

points = {'2.1.1.a':3,
            '2.1.1.b':0.5,
            '2.1.2':1,
            '2.2.1':4,
            '2.3.1.i':0.3,
            '2.3.1.ii':0.15,
            '2.3.1.iii':0.3,
            '2.3.1.iv':0.3,
            '2.3.1.v':0.3       
        }


from itertools import combinations
appendages = np.array([2,3,6,8,11,18])
c2 = combinations(appendages,2)
c2_means=[]
for c in c2:
    c2_means.append(np.mean(c))        
c4 = combinations(appendages,4)    
c4_means=[]
for c in c4:
    c4_means.append(np.mean(c))

means2 = ['{}'.format(m) for m in c2_means]
means4 = ['{}'.format(m) for m in c4_means]
means = means2+means4

def get_notebooks(files):
    files = [file for file in files if 'ipynb' in file and not 'checkpoints' in file]
    return files
    
def check_notebook(dirc,f,files):
    if len(files) > 1:
        print('More than one notebook found, what do')
        return files
    if len(files) == 0:
        try:
            files = os.listdir(dirc+'/'+f)
            files = [file for file in files if 'zip' in file]
            print(dirc + ' has a zip file, subtract a point!')
        except:
            print(dirc+'/'+f+' not found, moving on to next folder')
            return []
        try:
            with zipfile.ZipFile(dirc+'/'+f+'/'+files[0], 'r') as zip_ref:
                zip_ref.extractall(dirc+'/'+f)
            files = os.listdir(dirc+'/'+f)
            files = get_notebooks(files)
        
            if len(files) == 0:
                files = os.listdir(dirc+'/'+f)
                files = [file for file in files if not 'zip' in file]
                folder = files[0]
                files = os.listdir(dirc+'/'+f+'/'+folder)
                files = [folder+'/'+file for file in files if 'ipynb' in file and not 'checkpoints' in file]
        except:
            print('It\'s not a zip, not a notebook, please check {} manually'.format(f))
        return files
    return files

def open_notebook(dirc,f,files):
    try:
        with open(dirc+'/'+f+'/'+files[0], "r") as file:
            file = json.load(file)
        return file, files[0]
    except:
        try:
#            print('Trying different encoding')
            with open(dirc+'/'+f+'/'+files[0], "r",encoding='utf-8') as file:
                file = json.load(file)
            return file, files[0]
        except:
            print('could not open file in {}'.format(f))
            return None, None
    

def count_unexecuted_cells(file):
    c = 0
    cells = {}
    idx=0
    for cell in file['cells']:
        if cell['cell_type'] == 'code' and cell["execution_count"] == None and len(cell['source'])>0:
            c +=1
            cells[idx] = 'unexecuted'
        idx+=1
    return c, cells
            
def count_undocumented_plots(file):
    c = 0
    cells = {}
    idx = 0
    for cell in file['cells']:
    
        if cell['cell_type'] == 'code' and len(cell['source'])>0:
            source = '#'.join(cell['source'])
            plots = source.count('.plot(') + source.count('.imshow(') + source.count('.bar') + source.count('.scatter(')
            titles = source.count('.title(') + source.count('.set_title(')
            labels = source.count('ylabel(') + source.count('xlabel(')
            if plots>titles or plots>labels:
                cells[idx] = 'More plots than titles/labels'
                c += 1
        idx += 1
            
            
    return c, cells
    
def count_empty_cells(file):
    c = 0
    cells = {}
    idx = 0
    for cell in file['cells']:
        if len(cell['source'])==0:
            cells[idx] = 'Empty cell'
            c += 1
        if cell['cell_type'] == 'markdown' and len(cell['source']) < 60:
            source = '#'.join(cell['source'])
            if 'write your answer to' in source:
                cells[idx] = 'Empty markdown answer cell'
                c += 1
            
        idx += 1
            
            
    return c, cells
    

def solution_file(assignment_nr):
    with open('Assignment_{}_solutions.ipynb'.format(assignment_nr), "r") as file:
            file = json.load(file)
    return file

def find_assignment(mdcells,file,solution):

    filea1 = {}

    idx=0
    for cell in file['cells']:
        if cell['cell_type'] == 'markdown':
            sourcefile = ''.join(cell['source'])
            sourcefile = sourcefile[:min(30,len(sourcefile))]
            for sol in mdcells:
                sourcesol = ''.join(solution['cells'][mdcells[sol]]['source'])
                sourcesol = sourcesol[:min(30,len(sourcesol))]

                if sourcesol == sourcefile:
                    
                    filea1[sol] = idx+1
                    break
        idx+=1

    return filea1
    
def check_code_output(mdcells,codecells,file,solution,empty):

    cells = {}

    filea11 = find_assignment(mdcells,file,solution)
    for cell in filea11:
        if filea11[cell] not in empty and file['cells'][filea11[cell]]['cell_type']=='code':
            if  len(file['cells'][filea11[cell]]['outputs']) >0:
                if 'text' in file['cells'][filea11[cell]]['outputs'][0].keys() and 'text' in solution['cells'][codecells[cell]]['outputs'][0].keys():
                    if file['cells'][filea11[cell]]['outputs'][0]['text'] != solution['cells'][codecells[cell]]['outputs'][0]['text']:
                        cells[cell] = 'incorrect'
            else:
                cells[cell] = 'empty'

    return cells


def check_in_code_output(mdcells,file,solution,should_contain):

    cells = {}

    filea11 = find_assignment(mdcells,file,solution)
    for cell in filea11:
        if file['cells'][filea11[cell]]['cell_type']=='code':
            if  len(file['cells'][filea11[cell]]['outputs']) >0:
                if 'text' in file['cells'][filea11[cell]]['outputs'][0].keys():
                    missing = []
                    for term in should_contain[cell]:        
                        if term not in ''.join(file['cells'][filea11[cell]]['outputs'][0]['text']):
                            missing.append(term)
                    if len(missing)>0:
                        cells[cell] = missing
            else:
                cells[cell] = ['empty']

    return cells

def check_markdown_answer(mdcells,file,solution,should_contain):
    cells = {}
    filecells = find_assignment(mdcells,file,solution)
    for cell in filecells:
        if file['cells'][filecells[cell]]['cell_type']=='markdown' and len(file['cells'][filecells[cell]]['source'])>0:
            source = ''.join(file['cells'][filecells[cell]]['source']).lower()
            for word in should_contain[cell]:
                missing = []
                if word not in source:
                    missing.append(word)
                if len(missing)>0:
                    cells[cell] = missing
        else:
            if file['cells'][filecells[cell]+1]['cell_type']=='markdown':
                source = ''.join(file['cells'][filecells[cell]+1]['source']).lower()
                missing = []
                for word in should_contain[cell]:
                    
                    if word not in source:
                        missing.append(word)
                    if len(missing)>0:
                        cells[cell] = missing
    return cells
                

def check_code_answer(mdcells,file,solution,should_contain):
    cells = {}
    filecells = find_assignment(mdcells,file,solution)
    for cell in filecells:
        if file['cells'][filecells[cell]]['cell_type']=='code':
            incr = 0
            source=''
            while file['cells'][filecells[cell]+incr]['cell_type']=='code':
                source += ''.join(file['cells'][filecells[cell]+incr]['source']).lower()
                incr+=1
            missing = []
            for word in should_contain[cell]:
               
                if word not in source:
                    missing.append(word)
                if len(missing)>0:
                    cells[cell] = missing
    return cells

def count_in_code_answer(mdcells,file,solution,should_contain,times):
    cells = {}
    filecells = find_assignment(mdcells,file,solution)
    for cell in filecells:
        if file['cells'][filecells[cell]]['cell_type']=='code':
            count = 0
            incr = 0
            while file['cells'][filecells[cell]+incr]['cell_type']=='code':
                source = ''.join(file['cells'][filecells[cell]+incr]['source']).lower()
                incr+=1
                for word in should_contain:
                    count+= source.count(word)
            if count < times:
                cells[cell] = [count,times]

    return cells
                    
                
    
def write_feedback_assignment(cells,grading,feedbackfile):
    
    for cl in cells:
        feedbackfile.write(cl+') ')
        feedbackfile.write(cells[cl]+'  ')
        feedbackfile.write('-{:.2f}\n'.format(grading[cl]))
        
    
def write_feedback_line(feedback,feedbackfile):
    print(feedback)
    feedbackfile.write(feedback+'\n')
        
    


def unexecuted_cells(file,feedbackfile):
    unexec, unexcells = count_unexecuted_cells(file)
    if unexec > 0:
        print('found {} unexecuted cells in {}'.format(unexec,f))
        feedbackfile.write('There are {} unexecuted codecells with code in the source: -{:.1f} points\n\n'.format(unexec, min(unexec*0.2,1)))
    return  min(unexec*0.2,1), unexcells

def undocumented_plots(file,feedbackfile):
    undoc, undoccells = count_undocumented_plots(file)
    if undoc > 0:
        print('found {} undocumented plots in {}'.format(undoc,f))
        feedbackfile.write('There are {} cells that include more plots than titles/labels: -{:.2f}\n'.format(undoc, min(undoc*0.25,1)))
        feedbackfile.write('Please check the codecells belonging to the following questions:\n')
        for cl in undoccells:
            i=1
            while file['cells'][cl-i]['cell_type'] != 'markdown':
                i += 1
                
            source = ''.join(file['cells'][cl-i]['source'])
            feedbackfile.write('\t cell {} : {} ... \n'.format(cl-1,source[:100]))
    
    return min(undoc*0.25,1)
    
def empty_cells(file,feedbackfile):
    empty, empcells = count_empty_cells(file)
    if empty > 0:
        print('found {} emptys in {}'.format(empty, f))
        feedbackfile.write('\nThere are {} empty cells. \n'.format(empty))
        feedbackfile.write('Please check the cells belonging to the following questions:\n')
        for cl in empcells:
            i=1
            while file['cells'][cl-i]['cell_type'] != 'markdown' or len(file['cells'][cl-i]['source'])==0:
                i += 1
            source = u''.join(file['cells'][cl-i]['source']).encode('utf-8')
            feedbackfile.write('\t cell {} : {} ... \n'.format(cl-1,source[:100]))
  
def sum_deduction_points(assignment):
    deduct=0
    for cell in assignment:
        for deduction in cell:
            deduct += ((cell[deduction][0])/cell[deduction][1])*(points[deduction])
            
    return deduct

def sum_deduction_lists(assignment,should_contain):
    deduct=0
    for cell in assignment:
        for deduction in cell:
            if 'empty' in ''.join(cell[deduction]):
                cell[deduction] = ['Output empty. If code is correct, only deduct points for unexecuted cell']
                deduct += points[deduction]
            else:
                deduct += (len(cell[deduction]))/len(should_contain[deduction])*points[deduction]
    return deduct

def get_sub_dict(keys,dictionary):
    if isinstance(keys, str):
        if keys in dictionary.keys():
            return {keys:dictionary[keys]}
        else:
            return {}
    return {k:dictionary[k] for k in keys}

def write_feedback(file,feedback,f,filename,grader,email):
    feedbackfile= open(feedback+f+'/'+filename[:-5]+'txt',"w")
    info = f.split(' - ')
    identifier = info[0]
    group = info[2]
    time_date = info[4]
    
    feedbackfile.write(identifier+'\n\n')
    feedbackfile.write('Group: {}\n'.format(group))
    feedbackfile.write('Submitted: {}\n\n'.format(time_date))
    feedbackfile.write('Graded by: {}\n'.format(grader))
    feedbackfile.write('For questions or remarks, please email <{}>\n\n\n'.format(email))
    
    feedbackfile.write('Feedback:\n')
    print()

    grade=10
    deduction,unexcells = unexecuted_cells(file,feedbackfile)
    grade -= deduction
    grade -= undocumented_plots(file,feedbackfile)
    empty_cells(file,feedbackfile)
    unex = list(unexcells.keys())
    write_feedback_line('',feedbackfile)
    
    
    plots = ['.plot(','.scatter(']
    q211a = count_in_code_answer(get_sub_dict('2.1.1.a',markdown),file,solution,['hist(','boxplot('],4)
    should_contain = {'2.1.1.b':['mean','']}
    md = {}
    md.update(should_contain)
    q211b = check_markdown_answer(get_sub_dict('2.1.1.b',markdown),file,solution,should_contain)
    q212code = check_code_answer(get_sub_dict('2.1.2',markdown),file,solution,{'2.1.2':['scatter','pearsonr','','']})
    md.update({'2.1.2':['scatter','pearsonr','','','']})
    should_contain = {'2.1.2':['alcohol','acidity','density','','','']}
    md['2.1.2'].append(should_contain['2.1.2'])
    q212md = check_markdown_answer(get_sub_dict('2.1.2',markdown),file,solution,should_contain)
    
    deduct = sum_deduction_points([q211a]) + sum_deduction_lists([q211b,q212code,q212md],md)
    
    write_feedback_line('2.1 Total: {:.2f}/4.5 pts'.format(4.5-deduct),feedbackfile)
    
    write_feedback_line('2.1.1.a {:.2f}/3 pts'.format(3-sum_deduction_points([q211a])),feedbackfile)
    for cell in q211a:
        write_feedback_line('<possibly> Not enough histograms/boxplots -{:.2f}'.format(sum_deduction_points([q211a])),feedbackfile)

    
    write_feedback_line('2.1.1.b {:.2f}/0.5 pts'.format(0.5-sum_deduction_lists([q211b],md)),feedbackfile)
    for cell in q211b:
        write_feedback_line('Missing important/suspicious terms from explanation: [{}]  -{:.2f}'.format(' '.join(q211b[cell]),sum_deduction_lists([q211b],md)),feedbackfile)

    write_feedback_line('2.1.2 {:.2f}/1 pts'.format(1-(sum_deduction_lists([q212code,q212md],md))),feedbackfile)
    for cell in q212code:
        write_feedback_line('Missing suspicious commands from code: [{}] -{:.2f}'.format(' '.join(q212code[cell]),sum_deduction_lists([q212code],md)),feedbackfile)
    for cell in q212md:
        write_feedback_line('Missing important/suspicious terms from explanation: [{}]  -{:.2f}'.format(' '.join(q212md[cell]),sum_deduction_lists([q212md],md)),feedbackfile)

    grade-=deduct
   

    md = {}
    should_contain = {'2.2.1':['np.linalg.svd','np.dot','subplot','imshow','Axes3D','','','','','']}
    q221code = check_code_answer(get_sub_dict('2.2.1',markdown),file,solution,should_contain)
    md.update(should_contain)
    should_contain = {'2.2.1':['noise','separate']}
    q221md = check_markdown_answer(get_sub_dict('2.2.1',markdown),file,solution,should_contain) 
    md['2.2.1'].append(should_contain['2.2.1'])
    deduct = sum_deduction_lists([q221code,q221md],md)
    write_feedback_line('\n2.2 Total: {:.2f}/4 pts'.format(4-deduct),feedbackfile)
    for cell in q221code:
        write_feedback_line('Missing suspicious commands from code: [{}] -{:.2f}'.format(' '.join(q221code[cell]),sum_deduction_lists([q221code],md)),feedbackfile)
    for cell in q221md:
        write_feedback_line('Missing important/suspicious terms from explanation: [{}]  -{:.2f}'.format(' '.join(q221md[cell]),sum_deduction_lists([q221md],md)),feedbackfile)

    grade-=deduct
    
   
    should_contain = {'2.3.1.i':['8','5.3'],'2.3.1.ii':means,'2.3.1.iii':['8','1.7','3.4']}
    q231iii = check_in_code_output(get_sub_dict(list(should_contain.keys()),markdown),file,solution,should_contain)
   
    deduct = sum_deduction_lists([q231iii],should_contain)
    grade-=deduct
    write_feedback_line('\n2.3 Total: {:.2f}/1.5 pts'.format(1.5-deduct),feedbackfile)
    deduct = sum_deduction_lists([get_sub_dict('2.3.1.i',q231iii)],should_contain)
    write_feedback_line('2.3.1.i: {:.2f}/0.3 pts'.format(0.3-deduct),feedbackfile)
    for cell in get_sub_dict('2.3.1.i',q231iii):
        write_feedback_line('Missing from output: [{}]   -{:.2f}'.format(' '.join(q231iii['2.3.1.i']),deduct),feedbackfile)
    deduct = sum_deduction_lists([get_sub_dict('2.3.1.ii',q231iii)],should_contain)
    write_feedback_line('2.3.1.ii: {:.2f}/0.3 pts'.format(0.3-deduct),feedbackfile)
    for cell in get_sub_dict('2.3.1.ii',q231iii):
        write_feedback_line('Did not list (all) means. Missing from output: [{}]   -{:.2f}'.format(' '.join(q231iii['2.3.1.ii']),deduct),feedbackfile)
    deduct = sum_deduction_lists([get_sub_dict('2.3.1.iii',q231iii)],should_contain)
    write_feedback_line('2.3.1.iii: {:.2f}/0.3 pts'.format(0.3-deduct),feedbackfile)
    for cell in get_sub_dict('2.3.1.iii',q231iii):
        write_feedback_line('Missing from output: [{}]   -{:.2f}'.format(' '.join(q231iii['2.3.1.iii']),deduct),feedbackfile)
    print('Grade: {:.2f}'.format(grade))
    feedbackfile.write('\n <predicted> Grade: {:.2f}'.format(max(0,grade)))
     
def partition (list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]


#%%
assignment_nr = 2
dirc = 'Assignment{}'.format(assignment_nr)

solution = solution_file(assignment_nr)


folders = os.listdir(dirc)
folders = [f for f in folders if 'HA{}'.format(assignment_nr) in f]
folders = partition(folders,len(graders))
graders_random = list(graders.keys())
random.shuffle(graders_random)
#%%


for part, grader in enumerate(graders_random):
    
    os.makedirs(dirc+'/'+grader,exist_ok=True)
#    folders = os.listdir(dirc+'/'+grader)
    os.makedirs(dirc+'/'+grader+'/Feedback',exist_ok=True)
    feedback = dirc+'/'+grader+'/Feedback/'
    
    
    for f in folders[part]:
        if not os.path.exists(dirc+'/{}/{}'.format(grader,f)):    
            os.rename(dirc+'/'+f,dirc+'/{}/{}'.format(grader,f))
        files = os.listdir(dirc+'/'+grader+'/'+f)
#        files = os.listdir(dirc+'/'+f)
        files = get_notebooks(files)
        files = check_notebook(dirc+'/'+grader,f,files)
        
        
        file, filename=open_notebook(dirc+'/'+grader,f,files)
        
        if file:
            try:
                os.makedirs(os.path.dirname(feedback+f+'/'+filename[:-5]+'txt')) 
                write_feedback(file,feedback,f,filename,grader,graders[grader])
            except:
                print('Already existed')
            
        
        
#%%
            
            
import os


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
         
            
for grader in graders_random:
    print(grader)
    zipf = zipfile.ZipFile('{}/{}_{}.zip'.format(dirc,grader, dirc), 'w', zipfile.ZIP_DEFLATED)
    zipdir('{}/{}/'.format(dirc,grader), zipf)
    zipf.close()  
    
    
    
    