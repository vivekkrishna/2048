# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:34:45 2017

@author: vc185059
"""

from random import randint
from BaseAI import BaseAI
 
gridvaluedict={}
class PlayerAI(BaseAI):
    def getMove(self, grid):
        #moves = grid.getAvailableMoves()
        #return moves[randint(0, len(moves) - 1)] if moves else None
        height=0        
        #print(gridvaluedict)
        (move, utility)=self.Maximize(grid, float('-inf'), float('inf'), height)
        return move
        
    def Maximize(self, grid, alpha, beta, height):
        global gridvaluedict
        if height>3 or len(grid.getAvailableMoves())==0:  #This can change the depth
            l=''          
            for i in range(grid.size):
                for j in range(grid.size):
                    l+=str(grid.map[i][j])  
            try:
                return (None,gridvaluedict[l])  
            except KeyError:
                gridvaluedict[l]=self.eval(grid)
                return (None,gridvaluedict[l])
        
        (maxmov,maxutility)=(None,float('-inf'))        
        
        moves = grid.getAvailableMoves()
        
        for move in moves:
            # Validate Move
            if move != None and move >= 0 and move < 4:
                if grid.canMove([move]):
                    gridCopy = grid.clone()
                    gridCopy.move(move)
                    (_,utility)=self.Minimize(gridCopy, alpha, beta, height+1)
                    
                    if utility>maxutility:
                        (maxmov,maxutility)=(move,utility)
                        
                    if maxutility>=beta:
                        break
                        
                    if maxutility>alpha:
                        alpha=maxutility
                    
        return (maxmov,maxutility)
        
        
    def Minimize(self, grid, alpha, beta, height):
        global gridvaluedict
        if height>2 or len(grid.getAvailableCells())==0:
            l=''          
            for i in range(grid.size):
                for j in range(grid.size):
                    l+=str(grid.map[i][j])   
            try:
                return (None,gridvaluedict[l])  
            except KeyError:
                gridvaluedict[l]=self.eval(grid)
                return (None,gridvaluedict[l])
        
        (move,minutility)=(None,float('inf'))  
        
        gridCopy = grid.clone()
        cells = gridCopy.getAvailableCells()
        
        for move in cells:
            if move and gridCopy.canInsert(move):
                for j in [2]:
                    gridCopy = grid.clone()
                    gridCopy.setCellValue(move, j)
                    (_,utility)=self.Maximize(gridCopy, alpha, beta, height+1)
                    
                    if utility<minutility:
                        (mingrid,minutility)=(gridCopy,utility)
                        
                    if minutility<=alpha:
                        break
        
                    if minutility<beta:
                        beta=minutility
                        
                    
        return (mingrid,minutility)         
        
    def eval(self,grid):
        
        h1=grid.getMaxTile()
        
        freetiles=len(grid.getAvailableCells())
#        if freetiles<7:
#            lowfreetilepenalty=(16-freetiles)*10
#        else:
#            lowfreetilepenalty=0
        h3=freetiles
        count=0
        sumdiffadj=0
        lrmonotonicity=0
        totlrmonotonicity=0
        tdmonotonicity=0
        tottdmonotonicity=0
        smoothness=0
        bell=0
#        for i in range(4):
#            for j in range(4):
#                pos=(i,j)
#                posit=(i,j+1)
#                if (i==1 or j==1) and (i==2 or j==2):
#                    bell+=grid.getCellValue(pos)
#                else:
#                    bell-=grid.getCellValue(pos)
#                if grid.getCellValue(pos)==grid.getCellValue(posit):
#                        smoothness+=1  
                
        gradheuristic=0
        gradarray=[]
        gradarray.append([1,1,2,3])
        gradarray.append([1,2,3,4])
        gradarray.append([2,3,4,5])
        gradarray.append([3,4,5,6])
        for i in range(4):
            for j in range(4):
                pos=(i,j)
                gradheuristic+=grid.getCellValue(pos)*gradarray[i][j]
                count+=grid.getCellValue(pos)
                posit=(i,j+1)
                if j<3:
                    if grid.getCellValue(pos)<grid.getCellValue(posit):
                        lrmonotonicity+=1
                    elif grid.getCellValue(pos)>grid.getCellValue(posit) :
                        lrmonotonicity-=1
                
                    if grid.getCellValue(pos)==grid.getCellValue(posit):
                        smoothness+=1                        
                    #sumdiffadj+=grid.getCellValue(posit)-grid.getCellValue(pos)
                pos=(j,i)
                posit=(j+1,i)
                if j<3:
                    if grid.getCellValue(pos)<grid.getCellValue(posit):
                        tdmonotonicity+=1
                    elif grid.getCellValue(pos)>grid.getCellValue(posit):
                        tdmonotonicity-=1
#                        
                    if grid.getCellValue(pos)==grid.getCellValue(posit):
                        smoothness+=1   
#                    sumdiffadj+=grid.getCellValue(posit)-grid.getCellValue(pos)
#                       
                
#            lrmonotonicity=abs(lrmonotonicity)
#            tdmonotonicity=abs(tdmonotonicity)
#            totlrmonotonicity+=lrmonotonicity
#            tottdmonotonicity+=tdmonotonicity
#                if j<3:
#                    posit=(i,j+1)
#                    sumdiffadj+=grid.getCellValue(posit)-grid.getCellValue(pos)
#                if i<3:
#                    posit=(i+1,j)
#                    sumdiffadj+=grid.getCellValue(posit)-grid.getCellValue(pos)
#                if h3<6:
#                    for adj1 in range(i-1,i+2):
#                        for adj2 in range(j-1,j+2):
#                            if adj1 in range(4) and adj2 in range(4):
#                                adjpos=(adj1,adj2)
#                                sumdiffadj+=abs(grid.getCellValue(pos)-grid.getCellValue(adjpos))
#                        
        
#        h2=count     
###        
        h5=lrmonotonicity+tdmonotonicity
#        h6=smoothness
##        #h4=sumdiffadj
#        density=h2/(16-h3)
#        h7=density
        
#        if h3<3:
#            penalty=2000
#        else:
#            penalty=0
        #return h1+h2+((h1+h2)//2)*h3-h4
        #return h2+(h2//2)*h3-h4
        #return (2*h5+2*h6)+h7
        #return 100*h7+100*h6-penalty
        #(h5+2*h6)+h7 - 1024
        #return (h5+16*h6)+3*h7+h1 min is 1024
        #return (h5+16*h6)+3*h7+h1#-sumdiffadj
        #return gradheuristic+10*((h5+16*h6)+10*h7)+h1#+100*density
        return gradheuristic+100*smoothness
        #return -sumdiffadj
        #return bell+100*smoothness