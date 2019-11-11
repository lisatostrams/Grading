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

markdown = {'3.1.1': 1,
            '3.1.2':3,
            '3.1.3':6,
            '3.1.4':9,
            '3.2.1':12,
            '3.2.2':15,
            '3.3.1':18,
            '3.3.2':20,
            '3.3.3':22,
            '3.3.4':25,
            '3.3.5':28,
            '3.3.6':30,
        }

points   = {'3.1.1':0.5,
            '3.1.2':1.5,
            '3.1.3':0.5,
            '3.1.4':1,
            '3.2.1':2,
            '3.2.2':1.5,
            '3.3.1':0.25,
            '3.3.2':0,
            '3.3.3':1,
            '3.3.4':0.5,
            '3.3.5':0.25,
            '3.3.6':1,
        }




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
            labels = source.count('label') + source.count('legend')
            if plots>titles and plots>labels:
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
                cells[cell] = should_contain[cell]
    
    if len(cells)==1:
        
        if len(cells[list(cells.keys())[0]]) == len(should_contain[list(should_contain.keys())[0]]):
  
            for cell in filea11:
                if file['cells'][filea11[cell]+1]['cell_type']=='code':
                    if  len(file['cells'][filea11[cell]+1]['outputs']) >0:
                        if 'text' in file['cells'][filea11[cell]+1]['outputs'][0].keys():
                            missing = []
                            cells = {} 
                            for term in should_contain[cell]: 
                                if term not in ''.join(file['cells'][filea11[cell]+1]['outputs'][0]['text']):
                                    missing.append(term)
                            if len(missing)>0:
                                cells[cell] = missing
                    else:
                        cells[cell] = should_contain[cell]
    
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
    
    sol = solution['cells'][2]['outputs'][0]['text']
    out = []
    for s in sol:
        out+= ''.join(x for x in s if x.isalpha() or x is ' ' or x is ',').split(', ')
    out11 = {'3.1.1':out+13*['']}
    notout11 = {'3.1.1':['array','dtype','<U']}
    notq = check_in_code_output(get_sub_dict('3.1.1',markdown),file,solution,notout11)
    q11 = check_in_code_output(get_sub_dict('3.1.1',markdown),file,solution,out11)
    
    deduct11 = sum_deduction_lists([q11],out11)
    
    if len(notq)==0:
        deduct11 = max(0.25,deduct11)

    
    
    out12 = {'3.1.2':['Residual','Red','White','Density','','','','','','','','']}
    q12 = check_in_code_output(get_sub_dict('3.1.2',markdown),file,solution,out12)
    deduct12 = sum_deduction_lists([q12],out12)  
    
    code13 = {'3.1.3':['predict','']}
    md13 = {'3.1.3':['total sulfur dioxide','chlorides','sulphates','','','']}
    q13c = check_code_answer(get_sub_dict('3.1.3',markdown),file,solution,code13)
    q13m = check_markdown_answer(get_sub_dict('3.1.3',markdown),file,solution,md13)
    deduct13 = sum_deduction_lists([q13c],code13)+sum_deduction_lists([q13m],md13)
    
    code14 = {'3.1.4':['predict','']}
    md14 = {'3.1.4':['98','']}
    q14c = check_code_answer(get_sub_dict('3.1.4',markdown),file,solution,code14)
    q14m = check_markdown_answer(get_sub_dict('3.1.4',markdown),file,solution,md14)
    deduct14 = sum_deduction_lists([q14c],code13)+sum_deduction_lists([q14m],md14)
    
    q31 = [key for key in points.keys() if '3.1.' in key]
    total = sum([points[q] for q in q31])
    grade -= (deduct11+deduct12+deduct13+deduct14)
    
    write_feedback_line('3.1 Total: {:.2f}/{:.2f} pts'.format(total-(deduct11+deduct12+deduct13+deduct14),total),feedbackfile)
    
    write_feedback_line('3.1.1 {:.2f}/{:.2f} pts'.format(points['3.1.1']-deduct11,points['3.1.1']),feedbackfile)

    if len(notq)==0 and len(q11)==0:
        write_feedback_line('Didn\'t clean class names/attribute names -{:.2f}'.format(deduct11),feedbackfile)

    for cell in q11:
        if len(notq)==0:
            write_feedback_line('Didn\'t clean class names/attribute names',feedbackfile)
        write_feedback_line('Missing class names/attribute names -{:.2f}'.format(deduct11),feedbackfile)


    write_feedback_line('3.1.2 {:.2f}/{:.2f} pts'.format(points['3.1.2']-deduct12,points['3.1.2']),feedbackfile)
    for cell in q12:
        write_feedback_line('Missing class names/attribute names from tree -{:.2f}'.format(deduct12),feedbackfile)
    
    write_feedback_line('3.1.3 {:.2f}/{:.2f} pts'.format(points['3.1.3']-deduct13,points['3.1.3']),feedbackfile)
    for cell in q13c:
        write_feedback_line('Missing term from code <{}> -{:.2f}'.format(' '.join(q13c[cell]),sum_deduction_lists([q13c],code13)),feedbackfile)
    
    for cell in q13m:
        write_feedback_line('Missing term from explanation <{}> -{:.2f}'.format(' '.join(q13m[cell]),sum_deduction_lists([q13m],md13)),feedbackfile)
    
    write_feedback_line('3.1.4 {:.2f}/{:.2f} pts'.format(points['3.1.4']-deduct14,points['3.1.4']),feedbackfile)
    for cell in q14c:
        write_feedback_line('Missing term from code <{}> -{:.2f}'.format(' '.join(q14c[cell]),sum_deduction_lists([q14c],code14)),feedbackfile)
    
    for cell in q14m:
        write_feedback_line('Missing term from explanation <{}> -{:.2f}'.format(' '.join(q14m[cell]),sum_deduction_lists([q14m],md14)),feedbackfile)
    

    code21 = {'3.2.1':['train_test_split','','','']}
    q21c = check_code_answer(get_sub_dict('3.2.1',markdown),file,solution,code21)
    deduct21 = sum_deduction_lists([q21c],code21)
    
    code22 = {'3.2.2':['kfold','','','','','']}
    q22c = check_code_answer(get_sub_dict('3.2.2',markdown),file,solution,code22)
    deduct22 = sum_deduction_lists([q22c],code22)
    
        
    q32 = [key for key in points.keys() if '3.2.' in key]
    total = sum([points[q] for q in q32])
    grade -= (deduct21+deduct22)
    
    
    write_feedback_line('3.2 Total: {:.2f}/{:.2f} pts'.format(total-(deduct21+deduct22),total),feedbackfile)
    
    write_feedback_line('3.2.1 {:.2f}/{:.2f} pts'.format(points['3.2.1']-deduct21,points['3.2.1']),feedbackfile)

    for cell in q21c:
        write_feedback_line('Missing command from code <{}> -{:.2f}'.format(' '.join(q21c[cell]),deduct21),feedbackfile)
   
    write_feedback_line('3.2.2 {:.2f}/{:.2f} pts'.format(points['3.2.2']-deduct22,points['3.2.2']),feedbackfile)

    for cell in q22c:
        write_feedback_line('Missing command from code <{}> -{:.2f}'.format(' '.join(q22c[cell]),deduct22),feedbackfile)


    md31 = {'3.3.1':['84','21/25']}
    q31m = check_markdown_answer(get_sub_dict('3.3.1',markdown),file,solution,md31)
    if len(q31m) == 1:
        if len(q31m['3.3.1']) == 1:
            q31m = {}
    deduct31 = sum_deduction_lists([q31m],md31)
    
    code33 = {'3.3.3':['roc_curve','plot','','']}
    q33c = check_code_answer(get_sub_dict('3.3.3',markdown),file,solution,code33)
    deduct33 = sum_deduction_lists([q33c],code33)
    
    out34 = {'3.3.4':['.95','.96','.76']}
    q34o = check_in_code_output(get_sub_dict('3.3.4',markdown),file,solution,out34)
    if len(q34o) == 1:
        if len(q34o['3.3.4']) == 1:
            q34o = {}
    deduct34 = sum_deduction_lists([q34o],out34)
    
    out35 = {'3.3.5':['.85','.86','.69']}
    q35o = check_in_code_output(get_sub_dict('3.3.5',markdown),file,solution,out35)
    if len(q35o) == 1:
        if len(q35o['3.3.5']) == 1:
            q35o = {}
    deduct35 = sum_deduction_lists([q35o],out35)
          
    out36 = {'3.3.6':['66','26','8','7','','','','']}
    q36o = check_in_code_output(get_sub_dict('3.3.6',markdown),file,solution,out36)
    out36_2 = {'3.3.6':['.003','.002']}
    q36o_2 = check_in_code_output(get_sub_dict('3.3.6',markdown),file,solution,out36_2)
    if len(q36o_2) == 1:
        if len(q36o_2['3.3.6']) == 1:
            q36o_2 = {}
    deduct36 = min(1,sum_deduction_lists([q36o],out36) + 0.5*sum_deduction_lists([q36o_2],out36_2))
    
           
    q33 = [key for key in points.keys() if '3.3.' in key]
    total = sum([points[q] for q in q33])
    grade -= (deduct31+deduct33+deduct34+deduct35+deduct36)
    
    write_feedback_line('3.3 Total: {:.2f}/{:.2f} pts'.format(total-(deduct31+deduct33+deduct34+deduct35+deduct36),total),feedbackfile)
    
    write_feedback_line('3.3.1 {:.2f}/{:.2f} pts'.format(points['3.3.1']-deduct31,points['3.3.1']),feedbackfile)

    for cell in q31m:
        write_feedback_line('Incorrect value in answer -{:.2f}'.format(deduct31),feedbackfile)
   
    write_feedback_line('3.3.3 {:.2f}/{:.2f} pts'.format(points['3.3.3']-deduct33,points['3.3.3']),feedbackfile)

    for cell in q33c:
        write_feedback_line('Missing command from code <{}> -{:.2f}'.format(' '.join(q33c[cell]),deduct33),feedbackfile)
 
    write_feedback_line('3.3.4 {:.2f}/{:.2f} pts'.format(points['3.3.4']-deduct34,points['3.3.4']),feedbackfile)

    for cell in q34o:
        write_feedback_line('Missing/incorrect value in answer -{:.2f}'.format(deduct34),feedbackfile)

    write_feedback_line('3.3.5 {:.2f}/{:.2f} pts'.format(points['3.3.5']-deduct35,points['3.3.5']),feedbackfile)

    for cell in q35o:
        write_feedback_line('Missing/incorrect value in answer -{:.2f}'.format(deduct35),feedbackfile)
 
    write_feedback_line('3.3.6 {:.2f}/{:.2f} pts'.format(points['3.3.6']-deduct36,points['3.3.6']),feedbackfile)

    for cell in q36o:
        write_feedback_line('Missing table/incorrect value in table -{:.2f}'.format(0.5),feedbackfile)
    for cell in q36o_2:
        write_feedback_line('Missing pvalue/incorrect pvalue -{:.2f}'.format(0.5),feedbackfile)
   
     
   
    print('Grade: {:.2f}'.format(grade))
    feedbackfile.write('\n <predicted> Grade: {:.2f}'.format(max(0,grade)))
     
def partition (list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]


#%%
assignment_nr = 3
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
    
    
    
    