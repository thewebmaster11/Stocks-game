#!/usr/bin/env python
from random import *
from time import *
from thread import *
from Tkinter import *
from os import *

autosave = True
quitgame = False
def new():
    global stocklist
    else:
        print 'Starting stock creator. Name as many stocks as you want and press enter to exit.'
        name = ' '
        while True:
            name = raw_input('Type in the name of the new stock: ')
            if name == '':
                break
            else:
                stocklist[name] = 0
                stocks[name] = 0
                print "Created the stock '%s'" % name
        print 'Exiting stock creator'
        save()
def update():
    global stocklist
    global autosave
    wait = 0
    while not stop:
        for item in stocklist:
            change = randint(-10,10)
            if change in range(-5,5):
                continue
            if change < 0:
                change += 5
            if change > 0:
                change -= 5
            stocklist[item] += change
            if stocklist[item] < 0:
                stocklist[item] = 0
        sleep(0.1)
        wait += 1
        if not autosave:
            wait = 0
        if wait == 600:
            save(True)
            wait = 0
def save(cmd=False):
    if cmd:
        print ''
    print 'Saving...',
    with open('stocksgame\%s.txt' % slot,'w') as file:
        file.write('['+str(money)+','+str(stocklist)+','+str(stocks)+']')
    print 'Saved!'
    if cmd:
        print '-> ',
    sleep(1)
def cmd():
    global stop
    global money
    global stocks
    global stocklist
    global slot
    global autosave
    stop = False
    while not stop:
        cmd = raw_input('-> ')
        if cmd.lower() == 'help':
            print 'Help: View this list\nBuy: Buy a stock\nSell: Sell a stock\nMoney: View your money'
            print 'Stocks: View all the stocks\nStop: Quit the simulator\nSave: Save the game\nToggleSave: Turn autosaving on/off'
            print '\nAlso note that capital letters do not affect the commands, only names of stocks.'
        elif cmd.lower() == 'money':
            print 'Your money: $%i' % money
        elif cmd[0:3].lower() == 'buy':
            if cmd[4] != ' ':
                print 'Requires the name of a stock after the command'
                continue
            try:
                stock = (cmd[4:])
                if money > stocklist[stock]:
                    if stocklist[stock] != 0:
                        money -= stocklist[stock]
                        stocks[stock] += 1
                        print 'Bought stock %s for $%i ($%i remaining)' % (stock,stocklist[stock],money)
                    else:
                        print 'Cannot pay stock currently'
                else:
                    print 'Not enough money'
            except:
                print 'Requires an existing stock after the command'
        elif cmd[0:4].lower() == 'sell':
            if cmd[4] != ' ':
                print 'Requires the name of a stock'
                continue
            try:
                stock = cmd[5:]
                if stocks[stock] == 0:
                    print "You don't own this stock"
                else:
                    money += stocklist[stock]
                    newstocks = []
                    print 'Sold stock %s for $%i (Total money is $%i)' % (stock, stocklist[stock], money)
                    stocks[stock] -= 1
            except:
                print 'Requires an existing stock after the command'
        elif cmd.lower() == 'stop':
            if autosave:
                save()
            stop = True
        elif cmd.lower() == 'save':
            save()
        elif cmd.lower() == 'togglesave':
            autosave = not autosave
            if autosave:
                print 'Autosave ON'
            else:
                print 'Autosave OFF'
        elif cmd.lower() == 'stocks':
            for stock in stocklist:
                print stock,
                if stocks[stock] == 0:
                    print ': no shares, price : $%i' % stocklist[stock]
                else:
                    print ': %i share(s), price : $%i' % (stocks[stock],stocklist[stock])
        elif cmd == '':
            pass
        else:
            print 'Command was not found. Type \'help\' to get a list of commands'
def start():
    print 'Starting game. Type \'help\' to get a list of commands.'
    start_new_thread(update,())
    start_new_thread(cmd,())
while __name__ == '__main__' and not quitgame:
    if not path.exists('stocksgame'):
        makedirs('stocksgame')
    slot = ''
    while True:
        files = listdir('stocksgame/')
        if len(files) != 0:
            for file in range(len(files)):
                files[file] = files[file][:-4]
            print 'Select one of the following, or type \'N\' to create a new file, or press Enter to exit.'
            for file in files:
                print file
            while True:
                slot = raw_input('-> ')
                if slot in files + ['n','N']:
                    break
                print 'Please select a valid file'
        else:
            print 'Welcome to the stocks game!'
            slot = 'N'
        if slot.lower() == 'n':
            slot = raw_input('Type in the name of the file: ')
            stocklist = {}
            stocks = {}
            money = 1000
            new()
            break
        while True:
            print 'P: Play\nR: Rename\nM: Make a copy\nD: Delete\nC: Cancel'
            l = raw_input('-> ')
            if l.lower() in ['p','r','m']:
                with open('stocksgame/%s.txt' % slot) as file:
                    data = file.read()
                if l.lower() == 'p':
                    exec 'data = ' + data
                    money = data[0]
                    stocklist = data[1]
                    stocks = data[2]
                if l.lower() in ['r','m']:
                    name = raw_input('Type in the new name: ')
                    with open('stocksgame/' + name + '.txt', 'w') as file:
                        file.write(data)
                    if l.lower() == 'r':
                        remove('stocksgame/' + slot + '.txt')
            if l.lower() == 'd':
                remove('stocksgame/' + slot + '.txt')
            if l.lower() in ['c','d','r','p','m']:
                break
            print 'That is not one of the options'
        if not l.lower() in ['c','d','r','m']:
            break
    stop = False
    start()
    while not stop:
        pass
