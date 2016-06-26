from Tkinter import *
from socket import *

def download():
    loader = socket(AF_INET,SOCK_STREAM)
    loader.connect(('raw.githubusercontent.com',80))
    loader.sendall('GET /thewebmaster11/Stocks-game/master/Stock%20simulator.py HTTP/1.1')
    file = loader.recv(8000)
    loader.close()
    file = file[85:-20]
    global file
def downloadwin()
    download()
    with open('C:\Python27\Stock simulator.py') as trg:
        trg.write(file)
    exit()
view = Tk(screenName='Install Socket Game for Python 2.7')
downloadw = Button(view)
downloadw['text'] = 'Download for Windows'
downloadw['command'] = downloadwin
downloadw.pack()
mainloop()
