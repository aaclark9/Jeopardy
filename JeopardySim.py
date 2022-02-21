# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:08:39 2022

@author: user190344
"""
import tkinter as tk
import random
import ctypes
import os
#from PIL import Image

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class InvalidGameFile(Exception):
    pass



class IllegalCategoryCount(Exception):
    pass


class IllegalPointsCount(Exception):
    pass

class GameTile:
    def __init__(self, category='', points=0, question='', answer=''):
        self.category = category  # The question category
        self.points = points  # The point value of this question
        self.question = question  # The question
        self.answer = answer  # The answer

    def __str__(self):  # This method creates a string representation of this object
        # Let's store all of our properties in a dict object
        result = {'category': self.category,
                  'points': self.points,
                  'question': self.question,
                  'answer': self.answer}

        # Now we can convert the dict to a string which will give us friendly formatting
        return str(result)

    def __repr__(self):
        # This method also creates a String representation of a Python object
        # The Python debugger calls this method rather than __str__
        # But we can just reuse our code by calling __str__
        return self.__str__()
    
class Teamscore:
    def __init__(self, name='', score=0):
        self.name = name
        self.score = score
        
    def __str__(self):
        result = {'name': self.name,
                  'score': self.score}
        return str(result)
    
    def __repr__(self):
        return self.__str__()
    

    
def readGameBoard(gameFile):
    # Read the entire file into memory
    rawLines = open(gameFile, 'r', encoding='utf-8').readlines()
    
    fileLines = []
    for line in rawLines:
        # remove any '\n' characters and store them in fileLines
        fileLines.append(line.strip())

   
    #split by ::
    #[0] holds topics
    categories = fileLines[0].split('::')
    
    
    
    #[1] holds points
    points = []  
    pointValues = fileLines[1].split('::')
    
    # change str to int
    for pv in pointValues:
       
        points.append(int(pv))
        
    qsttile = {}  # Store all of the questions here
    
    # Read the rest of the file
    for line in fileLines[2:]:  # Ignore categories and points in file
        #split
        parts = line.split('::')
        #Check categories and points against cat/pt list
        if parts[0] in categories and int(parts[1]) in points:
            # Make Gametiles
            gameTile = GameTile(category=parts[0],
                                points=int(parts[1]),
                                question=parts[2],
                                answer=parts[3])
            # Make a new list for a new category in nested list
            if parts[0] not in qsttile:
                qsttile[parts[0]] = {}
                if int(parts[1]) not in qsttile[parts[0]]:
                    qsttile[parts[0]][int(parts[1])] = []
                    qsttile[parts[0]][int(parts[1])].append(gameTile)
            else:
                if int(parts[1]) not in qsttile[parts[0]]:
                    qsttile[parts[0]][int(parts[1])] = []
                    qsttile[parts[0]][int(parts[1])].append(gameTile)
                else:
                    qsttile[parts[0]][int(parts[1])].append(gameTile)
                
    return qsttile, categories, points # Return dictionary and category list

def Startmenu():
        
        
    def Gamescreen(c,teamlst):
        
        
        
        Gs = tk.Toplevel()
        Gs.state('zoomed') #Windows
        #root.attributes('-zoomed', True) #Linux
        Gs.configure(bg='dodgerblue')
        Gs.title('English Jeopardy')
        tmlbls = []
        lblclmn=0
        for i in teamlst:
            i.score = 0
            if c >= 1:
               tmlbls.append(tk.Label(Gs, text=i.name + ': ' + str(i.score) ,font=("Helvetica",30),wraplength= root.winfo_screenwidth()/5))
               tmlbls[lblclmn].grid(row=0, column=lblclmn)
               lblclmn = lblclmn + 1
               c = c - 1
            
                
        #split root into different sections rows and columns
        Gs.rowconfigure([0,1,2,3,4,5,6], weight=1,pad=2)
        Gs.columnconfigure([0,1,2,3,4], weight=1, pad=2)
        #Category frame for holding section titles
        catfrm = tk.Frame(Gs, bg='dodgerblue') 
        catfrm.grid(row=1, column=0, columnspan=5, sticky='news',pady=0, padx=0 )
        catfrm.columnconfigure([0,1,2,3,4], weight=1)
        catx=0
        
        #initialize lists to hold buttons and qsttile
        qbtns= []
        qsttilelist=[]
        qbtncnt=0
        
        
            
        #Read file with questions
        qsttile, categories, points = readGameBoard('some_ideas.txt')
        
        for k in categories:
            
            catlbl = tk.Label(catfrm, text=k, font=("Helvetica",30),wraplength= catfrm.winfo_screenwidth()/5)
            catlbl.grid(row=1, column=catx, sticky='nsew',pady=0, padx=0)
            btnrow=2
            for p in points:
                #make a list for each point category
                tempqsttilelist = []
                for j in qsttile[k][p]:
                    #hold quesions for each point value in each category
                    tempqsttilelist.append(j)
                    
                #choose a random question for each button
                rndqst = random.randint(0,len(tempqsttilelist)-1)
                qsttilelist.append(tempqsttilelist[rndqst])
                #create button that calls btnclick when pressed
                qbtns.append(tk.Button(Gs, text=qsttilelist[qbtncnt].points, font= ("Helvetica",20),wraplength= root.winfo_screenwidth()/5,
                        command=lambda c=qbtncnt: btnclick(qsttilelist[c],tmlbls,teamlst,qbtns[c])))
                qbtns[qbtncnt].grid(row=btnrow, column=catx, sticky='news',
                                    pady=0, padx=0)
                btnrow=btnrow+1
                qbtncnt=qbtncnt+1
            catx+=1
        
       
       
    def btnclick(btncall,tmlbls,teamlst,qbtns):
        #print(btncall.question)
        qbtns.destroy()
        qstmenu=tk.Toplevel()
        qstmenu.configure(bg='dodgerblue')
        qstmenu.title(btncall.category)
        qstmenu.state('zoomed') #windows
        #qstmenu.attributes('-zoomed', True) #linux
        qstmenu.rowconfigure([0,1,2,3], weight=1)
        qstmenu.columnconfigure([0,1,2,3,4], weight=1)
        
        if btncall.category == 'Music':
            mscpath = []
            mscpath = btncall.question.split(":")
            mscbtn = tk.Button(qstmenu, text='play', command= lambda: os.system(mscpath[0]))
            mscbtn.grid(row=3, column=4, sticky='news')
            qstbtn = tk.Button(qstmenu, text=mscpath[1] , font=("Helvetica",50), 
                          wraplength= qstmenu.winfo_screenwidth(), bg='dodgerblue',
                          command=lambda :QuestionClick(btncall, qstmenu) )
            qstbtn.grid(row=0, column=0, columnspan=5)
            
# =============================================================================
#         elif btncall.category == 'Picture':
#             imgpath = Image.open(btncall.question)
#             #picim = tk.PhotoImage(imgpath)
#             picbtn = tk.Button(qstmenu, image=imgpath)
#             picbtn.grid(row=0, column=0, columnspan=3)
#             qstbtn = tk.Button(qstmenu, text='Question: Who is this?', font=("Helvetica",50), 
#                           wraplength= qstmenu.winfo_screenwidth(), bg='dodgerblue',
#                           command=lambda :QuestionClick(btncall, qstmenu) )
#             qstbtn.grid(row=0, column=1, columnspan=2)
# =============================================================================
        else:
            qstbtn = tk.Button(qstmenu, text='Question: ' + btncall.question, font=("Helvetica",50), 
                          wraplength= qstmenu.winfo_screenwidth(), bg='dodgerblue',
                          command=lambda :QuestionClick(btncall, qstmenu) )
            qstbtn.grid(row=0, column=0, columnspan=5)
            
        tmindex=0
        while tmindex < len(tmlbls):
            btn= tk.Button(qstmenu, text=teamlst[tmindex].name, bg='white', 
                           command= lambda tm=tmindex:calcscore(tmlbls[tm], teamlst[tm], btncall, 
                                                      qstmenu))
            btn.grid(row=2, column=tmindex, sticky='news')
            tmindex=tmindex + 1
        extbtn = tk.Button(qstmenu, text='No-body', bg='white', 
                           command= qstmenu.destroy) #windows, test on linux
        extbtn.grid(row=3, sticky='news')
    def calcscore(tmlbls, teamlst, btncall, qstmenu):
        
        teamlst.score = teamlst.score + btncall.points
        
        tmlbls.configure(text = teamlst.name + ': ' + str(teamlst.score))
        qstmenu.destroy()
    def QuestionClick(btncall, qstmenu):
        anslbl= tk.Label(qstmenu, text='Answer: ' + btncall.answer, 
                         font=("Helvetica",50), bg='dodgerblue',
                         wraplength= qstmenu.winfo_screenwidth())
        anslbl.grid(row=1, column=0, columnspan = 5)
        
        #qstmenu.attributes('-zoomed', True) #linux
        
# =============================================================================
#    start startmenu()    
# =============================================================================
    
    #creating tinker instance
    root=tk.Tk()
    #setting window size
    root.state('zoomed') #Windows
    #root.attributes('-zoomed', True) #Linux
    root.configure(bg='dodgerblue')
    root.title('English Jeopardy')
    root.rowconfigure([0,1,2,3], weight=1)
    root.columnconfigure([0,1,2,3,4], weight=1)
    
    #Title label
    Jeopardyttl_lbl = tk.Label(root, text='Jeopardy',font=("Helvetica",50), bg='dodgerblue')
    Jeopardyttl_lbl.grid(row=0, column=0, columnspan=5, sticky='nsew')
    
    
    
    teambtn=[]
    teamlst=[]
    
    
    
    for i in range(1,6):
        team=Teamscore(name='team ' + str(i), score=0)
        teamlst.append(team)
        
        teambtn.append(tk.Button(root, text=str(i) + ' team(s)',
                                 command=lambda c=i: Gamescreen(c, teamlst)))
        teambtn[i-1].grid(row=1, column=i-1,sticky='news', pady=50)
    
    #strtbtn = tk.Button(root, text='start', command=lambda: Gamescreen())
    #strtbtn.grid(row=3, column=1, sticky='news', pady=50)
    extbtn= tk.Button(root, text='exit', command= root.destroy)
    extbtn.grid(row=3, column=2, sticky='news', pady=50)
    return root
        
# =============================================================================
# end def
# =============================================================================

root = Startmenu()

root.mainloop()
