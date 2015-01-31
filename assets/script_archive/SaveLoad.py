'''
Source: 
SuperGloop BGE Tutorials
https://www.youtube.com/watch?v=hRnG0P-VgPw
'''

from bge import logic
path = logic.expandPath("//")

def save():
    cont = logic.getCurrentController()
    own = cont.owner 
    # 'info' is what will be saved to the file.
    # Example:
    # info = str(*What you want to save*)
    
    info = str(own['prop'])
        
    file = open(path+str(own)+".txt", 'w')    
    file.write(str(info))
    
    
def load():
    cont = logic.getCurrentController()
    own = cont.owner
    
    file = open(path+str(own)+'.txt','r')
    line = file.readline().replace('\n','').split(',')
    own['prop'] = int(line[0])
    own['prop0'] = float(line[1])
   
    