#!/usr/bin/env python
from random import *
from time import *
from thread import *
from Tkinter import *
import os
from getpass import getpass

autosave = True
quitgame = False
def new():
    global stocklist
    print 'Starting stock creator. Name up to 20 stocks and press enter, then just press enter to exit.'
    name = ' '
    while True:
        if len(stocklist) >= 20:
            print 'Maxinum amount of stocks (20) reached!'
            break
        name = raw_input('Type in the name of the new stock: ')
        if name == '' and len(stocklist) > 0:
            break
        elif name == '' and len(stocklist) == 0:
            print 'Requires at least one stock'
        elif name in stocklist:
            print 'That stock already exists!'
        elif len(name) > 12:
            print 'Stocks have a maxinum length of 12 characters'
        else:
            stocklist[name] = 0
            stocks[name] = 0
            print "Created the stock '%s'" % name
    print 'Exiting stock creator'
    save()
def update():
    global stocklist
    global autosave
    global company
    global money
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
        if company not in [False, True]:
            if company[1] != 0 and company[0] != '':
                if randint(0,100) == 100 and [] in company[2]:
                    print '\nOne of your offers were purchased for %i' % company[1]
                    for offer in range(len(company[2])):
                        if company[2][offer] == []:
                            company[2][offer] = [company[1],randint(20,200)]
                            break
                for offer in range(len(company[2])):
                    if company[2][offer] == []:
                        continue
                    if company[2][offer][0] + company[2][offer][1] <= company[1]:
                        money -= company[1]
                        print '\nOne of your offers were sold for %i' % company[1]
                        continue
                    change = randint(-4,4)
                    if change in range(3, -3):
                        continue
                    change /= 4
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
        file.write('["'+str(password)+'",'+str(money)+','+str(stocklist)+','+str(stocks)+','+str(company)+']')
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
    global company
    stop = False
    while not stop:
        cmd = raw_input('-> ')
        if cmd.lower() == 'help':
            print 'Help: View this list\nBuy: Buy a stock\nSell: Sell a stock\nMoney: View your money'
            print 'Stocks: View all the stocks\nStop: Quit the simulator\nSave: Save the game'
            print 'ToggleSave: Turn autosaving on/off'
            if company == True:
                print 'Start: Start your company for $1000000'
            if company not in [False,True]:
                print 'Name: Set the name of your company and stock\nPrice: Change the price of your stock\nNew offer: Offer another of your stock'
            print '\nAlso note that capital letters do not affect the commands, only names of stocks.'
        elif cmd.lower() == 'money':
            print 'Your money: $%i' % money
        elif cmd[0:3].lower() == 'buy':
            try:
                if cmd[5] != ' ' and cmd[6] == ' ':
                    raise StandardError
            except:
                print 'Requires the name of one of the stocks'
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
            try:
                if cmd[5] != ' ' and cmd[6] == ' ':
                    raise StandardError
            except:
                print 'Requires the name of one of the stocks you own'
                continue
            try:
                stock = cmd[5:]
                if stocks[stock] == 0:
                    print "You don't own this stock"
                else:
                    money += stocklist[stock]
                    print 'Sold stock %s for $%i (Total money is $%i)' % (stock, stocklist[stock], money)
                    stocks[stock] -= 1
                    if company == False and money >= 1000000:
                        print 'You win! You can now create a company and control a stock!'
                        company = True
                        if autosave:
                            save()
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
                elif stocks[stock] == 1:
                    print ': 1 share, price : $%i' % stocklist[stock]
                else:
                    print ': %i shares, price : $%i' % (stocks[stock],stocklist[stock])
            if company not in [False, True]:
                print '%s : %i shares offered, price : $%i' % (company[0],len(company[2]),company[1])
        elif cmd[0:4].lower() == 'name':
            if company in [False, True]:
                print 'You do not have access to that command'
            else:
                try:
                    if cmd[4] != ' ' and cmd[5] == ' ':
                        raise StandardError
                except:
                    print 'Requires the new name for your company after the command'
                else:
                    company[0] = cmd[5:]
        elif cmd[0:5].lower() == 'price':
            if company in [False, True]:
                print 'You do not have access to that command'
                continue
            else:
                try:
                    if cmd[5] != ' ' and cmd[6] == ' ':
                        raise StandardError
                except:
                    print 'Requires the new price for your company after the command'
                else:
                    try:
                        newprice = cmd[6:]
                        company[1] = int(newprice)
                    except:
                        print '\'%s\' is not a number' % cmd[6:]
        elif cmd.lower() == 'new offer':
            if company in [False, True]:
                print 'You do not have access to that command'
                continue
            company[2] += [[]]
            print 'Added a new offer'
        elif cmd[0:5].lower() == 'start':
            if company != True:
                print 'You do not have access to that command'
            else:
                try:
                    if cmd[5] != ' ' and cmd[6] == ' ':
                        raise StandardError
                except:
                    print 'Requires the name for your new company after the command'
                else:
                    if money < 1000000:
                        print 'Not enough money'
                        continue
                    money -= 1000000
                    company = [cmd[6:], 0, []]
        elif cmd == '':
            pass
        else:
            print 'Command was not found. Type \'help\' to get a list of commands'
def start():
    print 'Starting game. Type \'help\' to get a list of commands.'
    start_new_thread(update,())
    start_new_thread(cmd,())
while __name__ == '__main__' and not quitgame:
    if not os.path.exists('stocksgame'):
        os.makedirs('stocksgame')
    slot = ''
    print 'Welcome to the stocks game! (V1.1)'
    while True:
        files = os.listdir('stocksgame/')
        for file in range(len(files)):
            files[file] = files[file][:-4]
        print 'Type in the name of one of the following files and press Enter/Return to select it'
        print 'Type in \'N\' and press Enter/Return to create a new file'
        print 'Type in \'About Stocks sim\' and press Enter/Return to learn how to play'
        print 'Or just press enter to exit'
        if len(files) > 0:
            for file in files:
                print file
        else:
            print '\nNo files exist! Create a file with \'N\''
        while True:
            slot = raw_input('-> ')
            if slot in files or slot.lower() in ['n','about stocks sim']:
                break
            if slot == '':
                print 'Goodbye!'
                sleep(1)
                exit()
            print 'Please select a valid file'
        if slot.lower() == 'n':
            slot = raw_input('Type in the name of the file: ')
            password = ''
            stocklist = {}
            stocks = {}
            money = 1000
            company = False
            new()
        elif slot.lower() == 'about stocks sim':
            raw_input('A stock is just an investment in any company')
            raw_input('Prices for each stock change as time passes, regardless of if you do anything')
            raw_input('Your goal is to become a millionare just off of buying and selling stocks')
            raw_input('Then you can start your own company and control your own stock\'s prices')
            raw_input('But you only start with $1000, so the road to this is very long!')
            raw_input('Good luck!')
            break
        password = ''
        while True:
            with open('stocksgame/' + slot + '.txt', 'r') as file:
                data = file.read()
            exec 'data = ' + data
            if password != data[0]:
                while True:
                    password = getpass('Password: ')
                    if password in [data[0], '']:
                        break
                    print 'Incorrect password'
                if password == '':
                    print 'Canceled!'
                    break
            print 'File: ' + slot + '\n'
            print 'S: Set password\nP: Play\nR: Rename\nM: Make a copy\nD: Delete\nC: Cancel'
            l = raw_input('-> ')
            if l.lower() in ['p','r','m','s']:
                if l.lower() == 'p':
                    money = data[1]
                    stocklist = data[2]
                    stocks = data[3]
                    company = data[4]
                if l.lower() in ['r','m']:
                    name = raw_input('Type in the new name: ')
                    with open('stocksgame/' + name + '.txt', 'w') as file:
                        file.write(str(data))
                    if l.lower() == 'r':
                        os.remove('stocksgame/' + slot + '.txt')
                        slot = name
                if l.lower() == 's':
                    print 'Type in a password and press Enter/Return, or just press Enter to remove it'
                    password = getpass('Password: ')
                    if password == getpass('Reenter your password: '):
                        data[0] = password
                        with open('stocksgame/' + slot + '.txt', 'w') as file:
                            file.write(str(data))
                    else:
                        password = data[0]
                    continue
            if l.lower() == 'd':
                yn = ''
                while yn not in ['y','n','Y','N']:
                    print 'Are you sure you want to delete this file (Y/N)?'
                    yn = raw_input('-> ')
                if yn.lower() == 'y':
                    os.remove('stocksgame/' + slot + '.txt')
                    break
            if l.lower() in ['c','p']:
                break
            print 'That is not one of the options'
        if l.lower() == 'p':
            stop = False
            start()
            while not stop:
                pass
