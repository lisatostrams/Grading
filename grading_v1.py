# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 11:10:46 2019

@author: Lisa
"""   

import os
dirc = 'Assignment1'
graders = {"Stijn":  "A.A.deBoer@student.ru.nl", "Francesca":  "F.Drummer@student.ru.nl","Lizzy":  "l.grootjen@student.ru.nl",
"Ron":  "R.Hommelsheim@student.ru.nl", "Elena":  "E.Kreis@student.ru.nl","David":  "h.leeftink@student.ru.nl",
"Lars":  "L.vanRhijn@student.ru.nl","Steffen":  "S.Ricklin@student.ru.nl","Jessie":  "J.vanSchijndel@student.ru.nl"}



import zipfile
import json

m11 = {'a':0,'b':3,'c':5,'d':7,'e':9,'f':11,'g':13}
m12 = {'a':17,'b':19,'c':21}
m21 = {'b':31}
m22 = {'a':33,'b':35,'d':39}
m31 = {'a':48}

c11 = {'a':2,'b':4,'c':6,'d':8,'e':10,'f':12,'g':14}
c12 = {'a':18,'b':20,'c':22}
c21 = {'b':32}
c22 = {'a':34,'b':36,'c':38,'d':40}
c31 = {'a':49}

g11 = {'a':0.3, 'b':0.2, 'c':0.2, 'd':0.2, 'e':0.2, 'f':0.2, 'g':0.2}
g12 = {'a':0.2, 'b':0.2, 'c':0.2}
g21 = {'b':0.3}
g22 = {'a':0.5,'b':0.25,'c':1,'d':0.5}
g31 = {'a':0.5}

def get_notebooks(files):
    files = [file for file in files if 'ipynb' in file and not 'checkpoints' in file]
    return files
    
def check_notebook(dirc,f,files):
    if len(files) > 1:
        print('More than one notebook found, what do')
        return files
    if len(files) == 0:
        files = os.listdir(dirc+'/'+f)
        files = [file for file in files if 'zip' in file]
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
    

def solution_file():
    with open('Assignment_1_solutions.ipynb', "r") as file:
            file = json.load(file)
    return file

def find_assignment(mdcells,file,solution):

    filea1 = {}

    idx=0
    for cell in file['cells']:
        if cell['cell_type'] == 'markdown':
            sourcefile = ''.join(cell['source'])[:30]
            for sol in mdcells:
                sourcesol = ''.join(solution['cells'][mdcells[sol]]['source'])[:30]
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

def check_markdown_answer(mdcells,file,solution,should_contain):
    cells = {}
    filecells = find_assignment(mdcells,file,solution)
    for cell in filecells:
        if file['cells'][filecells[cell]]['cell_type']=='markdown':
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
                for word in should_contain[cell]:
                    missing = []
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
            source = ''.join(file['cells'][filecells[cell]]['source']).lower()
            for word in should_contain[cell]:
                missing = []
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
            source = ''.join(file['cells'][filecells[cell]]['source']).lower()
            count = 0
            for word in should_contain:
                count+= source.count(word)
            if count < times:
                cells[cell] = times-count
            else:
                cells[cell] = 0
    return cells
                    
                
    
def write_feedback_assignment(cells,grading,feedbackfile):
    
    for cl in cells:
        feedbackfile.write(cl+') ')
        feedbackfile.write(cells[cl]+'  ')
        feedbackfile.write('-{:.2f}\n'.format(grading[cl]))
        
    
def write_feedback_line(feedback,feedbackfile):
    feedbackfile.write(feedback+'\n')
        
    


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

    grade=10
    unexec, unexcells = count_unexecuted_cells(file)
    if unexec > 0:
        print('found {} unexecuted cells in {}'.format(unexec,f))
        feedbackfile.write('There are {} unexecuted codecells with code in the source: -{:.1f} points\n\n'.format(unexec, min(unexec*0.2,1)))
    grade -=  min(unexec*0.2,1)
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
    empty, empcells = count_empty_cells(file)
    grade -= min(undoc*0.25,1)
    
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
  
    
    unex = list(unexcells.keys())
    
    a11cells = check_code_output(m11,c11,file,solution,unex)
    deduct1 = sum([g11[cell] for cell in a11cells])
    a12cells = check_code_output(m12,c12,file,solution,unex)
    deduct2 = sum([g12[cell] for cell in a12cells])
    feedbackfile.write('\nAssignment 1.1 ({:.2f})/2.75pts \n'.format(2.75-(deduct1+deduct2)))
    feedbackfile.write('Assignment 1.1.1 ({:.2f})/1.5pts \n'.format(1.5-deduct1))
    write_feedback_assignment(a11cells,g11,feedbackfile)
    feedbackfile.write('Assignment 1.1.2 ({:.2f})/1.25pts \n'.format(1.25-deduct2))
    write_feedback_assignment(a12cells,g12,feedbackfile)
    grade -= (deduct1+deduct2)
    a21cells = count_in_code_answer(m21,file,solution,['scatter','plot'],4)
    if 'b' in a21cells.keys():
        deduct1 = min(g21['b'],(g21['b']/4) * a21cells['b'])
#        print('deduct {:.2f}'.format(deduct1))
    else:
        deduct1 = 0
    
    a22should_contain = {'a':['dimension','reduc','variance','linear'], 'b':['explain'],'d':['eigenvector','square']}
    
    a22cells = check_markdown_answer(m22,file,solution,a22should_contain)
    for cell in a22cells:
        deduct2 += len(a22cells[cell])*(g22[cell]/len(a22should_contain[cell]))
    
    should_contain = {'c':['np.linalg.svd','np.dot']}
    a22ccells = check_code_answer({'c':37},file,solution,should_contain)
    if 'c' in a22ccells.keys():
        deduct3= len(a22ccells['c'])*0.5
    else:
        deduct3=0
    feedbackfile.write('\nAssignment 1.2 ({:.2f})/6pts \n'.format(6-(deduct1+deduct2+deduct3)))
    grade -= (deduct1+deduct2+deduct3)
    feedbackfile.write('Assignment 1.2.1 ({:.2f})/0.5pts \n'.format(0.5-deduct1))
    if deduct1>0:
        write_feedback_line('b) missing {} plots  -{:.2f}'.format(a21cells['b'],deduct1),feedbackfile)
    feedbackfile.write('Assignment 1.2.2 ({:.2f})/5.5pts \n'.format(5.5-(deduct2+deduct3)))
    for cell in a22cells:
        write_feedback_line('{}) missing important terms from explanation: {}  -{:.2f}'.format(cell,''.join(a22cells[cell]),len(a22cells[cell])*(g22[cell]/len(a22should_contain[cell]))),feedbackfile)
    

    for cell in a22ccells:
        write_feedback_line('c) didn\'t use the following commands (which is very suspicious): {}   -{:.2f}'.format(''.join(a22ccells[cell]),len(a22ccells)*0.5),feedbackfile)
    
    feedbackfile.write('\nAssignment 1.3 (1.25)/1.25pts \n')
    
    feedbackfile.write('Assignment 1.3.1 (1.25)/1.25pts \n')
    
    print('Predicted grade: {:.2f}'.format(grade))
    feedbackfile.write('\nPredicted Grade: {:.2f}'.format(max(0,grade)))
     




solution = solution_file()


for grader in graders:
    
    folders = os.listdir(dirc+'/'+grader)
    os.makedirs(dirc+'/'+grader+'/Feedback',exist_ok=True)
    feedback = dirc+'/'+grader+'/Feedback/'
    
    
    for f in folders:
        files = os.listdir(dirc+'/'+grader+'/'+f)
        files = get_notebooks(files)
        files = check_notebook(dirc+'/'+grader,f,files)
        
        
        file, filename=open_notebook(dirc+'/'+grader,f,files)
        
        if file:
            try:
                os.makedirs(os.path.dirname(feedback+f+'/'+filename[:-5]+'txt'),exist_ok=True)   
            except:
                print('Already existed')
            write_feedback(file,feedback,f,filename,grader,graders[grader])
        
    
    
    
    