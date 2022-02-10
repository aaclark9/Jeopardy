# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:08:39 2022

@author: user190344
"""
import tkinter as tk
import random
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class InvalidGameFile(Exception):
    pass



class IllegalCategoryCount(Exception):
    pass


class IllegalPointsCount(Exception):
    pass


temp = 0

def Startmenu():
    
    
    #creating tinker instance
    root=tk.Tk()
    #setting window size
    root.state('zoomed') #Windows
    #root.attributes('-zoomed', True) #Linux
    root.configure(bg='dodgerblue')
    root.title('English Jeopardy')
    
   
    
    #Title label
    Jeopardyttl_lbl = tk.Label(root, text='Jeopardy',font=("Helvetica",50), bg='dodgerblue')
    Jeopardyttl_lbl.grid(row=0, column=0, columnspan=5, sticky='nsew')
    strtbtn= tk.Button(root, text='start', command= lambda: Teamselectscreen(root))
    strtbtn.grid(row=1, column=0,)
    extbtn= tk.Button(root, text='exit', command= root.destroy)
    extbtn.grid(row=1, column=1)
    return root

def Teamselectscreen(root):
    
    teambtn=[]
    numteams=0
    
    #root.rowconfigure([0,1,2] )
    #root.columnconfigure([0,1,2,3,4])
    for i in range(1,5):
        teambtn.append(tk.Button(root, text=str(i) + ' team(s)', 
                                 command=lambda c=i: numteams == c))
        teambtn[i-1].grid(row=0, column=i)
    teamlbl = tk.Label(root, text=numteams)
    teamlbl.grid(row=1,column=0)
    strtbtn = tk.Button(root, text='start', command=lambda: Gamescreen(root))
    strtbtn.grid(row=2, column=0,)
    
def Gamescreen(root):
    
    root.destroy("all")
    #split root into different sections rows and columns
    root.rowconfigure([0,1,2,3,4,5,6], weight=1,pad=2)
    root.columnconfigure([0,1,2,3,4], weight=1, pad=2)
    #Category frame for holding section titles
    catfrm = tk.Frame(root, bg='dodgerblue') 
    catfrm.grid(row=1, column=0, columnspan=5, sticky='news' )
    catfrm.columnconfigure([0,1,2,3,4], weight=1)
    catx=0
    caty=1
    #initialize lists to hold buttons and qsttile
    qbtns= []
    qsttiletlist = []
    qbtncnt=0
    qbuttons= {}


    #Read file with questions
    qsttile, categories = readGameBoard('questionsactive.txt')
    for k in categories:
        catlbl = tk.Label(catfrm, text=k)
        catlbl.grid(row=1, column=catx, sticky='nsew')
        btnrow=2
        for j in qsttile[k]:
            qsttiletlist.append(j)
            #create button that calls btnclick when pressed
            qbtns.append(tk.Button(root, text=j.points, 
                        command=lambda c=qbtncnt: btnclick(qsttiletlist[c])))
            qbtns[qbtncnt].grid(row=btnrow, column=catx, sticky='news')
            btnrow=btnrow+1
            qbtncnt=qbtncnt+1
        catx+=1
    #print(qbtns)
   
    return root
    
def btnclick(btncall):
    #print(btncall.question)
    qstmenu=tk.Tk()
    qstmenu.configure(bg='dodgerblue')
    qstmenu.title(btncall.category)
    qstmenu.state('zoomed') #windows
    qstbtn = tk.Button(qstmenu, text='Question:' + btncall.question, font=("Helvetica",50), 
                      wraplength= qstmenu.winfo_screenwidth(), bg='dodgerblue',
                      command=lambda :QuestionClick(btncall, qstmenu) )
    qstbtn.grid(row=0, column=0)
    extbtn = tk.Button(qstmenu, text='exit', bg='white', 
                       command= qstmenu.destroy) #windows, test on linux
    extbtn.grid(row=2)
    
def QuestionClick(btncall, qstmenu):
    anslbl= tk.Label(qstmenu, text='Answer:' + btncall.answer, 
                     font=("Helvetica",50), bg='dodgerblue',
                     wraplength= qstmenu.winfo_screenwidth())
    anslbl.grid(row=1)
    
    #qstmenu.attributes('-zoomed', True) #linux
    
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
    

        
# =============================================================================
# class GameBoard:
#     def __init__(self, qsttile):
#         self.qsttile = qsttile
# =============================================================================
        
def readGameBoard(gameFile):
    # Read the entire file into memory
    rawLines = open(gameFile, 'r', encoding='utf-8').readlines()
    
    # Now this is going to store our files
    fileLines = []
    for line in rawLines:  # Iterate through rawLines one item at a time
        # Now we need to remove any '\n' characters and store them in fileLines
        fileLines.append(line.strip())

   
    # We are going to split the first line apart by the :: character
    #Len of [0] is number of Topic categories
    categories = fileLines[0].split('::')
    #print(categories)
    
    # So now we read the second line and split it one our :: character
    #Len of [1] number of point categories
    points = []  # Store the points to validate the file later
    pointValues = fileLines[1].split('::')
    #print(pointValues)
    # Now, we have Strings in pointValues, but we need them to be integers
    # So we iterate through pointValues and convert each item to an int
    # before storing it in points. We use the int() function to do the conversion
    for pv in pointValues:
        #print(pv)
        points.append(int(pv))
    #print(points)    
    qsttile = {}  # Store all of the questions here
    
    # Now read everything else
    for line in fileLines[2:]:  # Slice off the first two lines
        #  Get a line and split it into its parts
        parts = line.split('::')
        #print(parts)
        #  Now we check that the category and points are valid
        if parts[0] in categories and int(parts[1]) in points:
            # We can create a GameTile object at this point
            gameTile = GameTile(category=parts[0],
                                points=int(parts[1]),
                                question=parts[2],
                                answer=parts[3])
            # If this our first insertion, we need to create a new list object to store our
            # qsttile in our dictionary
            if parts[0] not in qsttile:
                qsttile[parts[0]] = []
                qsttile[parts[0]].append(gameTile)
            else:
                # Otherwise we can add our gameTile to qsttile. Notice that the category is the key
                qsttile[parts[0]].append(gameTile)
    #print(qsttile)            
    return qsttile, categories # Return our dictionary that contains our question and final Jeopardy








root = Startmenu()

root.mainloop()
