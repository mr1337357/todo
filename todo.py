import sys
import ini
import datetime
import tty
import termios

def getch():   # define non-Windows version
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class todoitem():
    def __init__(self,name=''):
        self.name=name
        self.created=''
        self.due=''
        self.status='todo'

    def load(self,data):
        self.status=data['status']
        if not self.status in ['todo','done','working']:
            raise Exception('invalid status')
        self.due=data['due']
        self.created=data['date']
        
    def new(self):
        d = datetime.date.today()
        self.created = d.strftime("%Y.%m.%d")

    def save(self):
        data={}
        data['status']=self.status
        data['due']=self.due
        data['date']=self.created
        return data
    
    def __repr__(self):
        out = '[{}] {} {} {}'
        status=''
        if self.status=='todo':
            status=' '
        if self.status=='working':
            status='-'
        if self.status=='done':
            status='*'
        name = self.name
        if len(name)>20:
            name=name[:20]
        name='"{}"'.format(name)
        name=name.ljust(22,' ')
        return out.format(status,name,self.created,self.due)

def sortlist(todolist,sortedby='status'):
    def keyfunc(item):
        return item.due
    if sortedby == 'status':
        def keyfunc(item):
            if item.status=='todo':
                return 1
            if item.status=='working':
                return 2
            if item.status=='done':
                return 3
            return 4
    return sorted(todolist,key=keyfunc)

def show(todolist,index):
    print('    |name                  |created   |due')
    i=index-10
    if i < 0:
        i = 0
    todolist=todolist[i:i+20]
    for todo in todolist:

        if index==i:
            sys.stdout.write('>')
        else:
            sys.stdout.write(' ')
        print(todo)
        i+=1

def save(todolist,todofile):
    todofile.sections={}
    for entry in todolist:
        name=entry.name
        todofile.sections[name]=entry.save()
    todofile.save()

if __name__ == '__main__':
    try:
        todofile=ini.inifile('to.do')
        todofile.load()
    except:
        open('to.do','w+').close()
        todofile=ini.inifile('to.do')
        todofile.load()
    todolist=[]
    for section in todofile.sections:
        if section == '':
            continue
        item = todoitem(section)
        item.load(todofile.sections[section])
        todolist.append(item)
    index=0
    message=''
    sortedby='status'
    while True:
        sys.stdout.write('\x1bc')
        todolist = sortlist(todolist,sortedby)
        if len(message)>0:
            print(message)
            message=''
        show(todolist,index)
        key = getch()
        if key == 'n':
            n = todoitem()
            n.new()
            n.name=input('name:')
            todolist.append(n)
        elif key == 'w':
           save(todolist,todofile) 
           message = 'saved'
        elif key == 'd':
            due = input('due:')
            todolist[index].due=due
        elif key == ' ':
            st = todolist[index].status
            if st == 'todo':
                st = 'working'
            elif st == 'working':
                st = 'done'
            elif st == 'done':
                st = 'todo'
            todolist[index].status = st
        elif key == 'x':
            sys.exit(0)
        elif key == '\x1b':
            #escape sequence
            key = getch()
            if key == '\x5b':
                key = getch()
                if key == '\x41':
                    if index > 0:
                        index -= 1
                if key == '\x42':
                    if index < len(todolist)-1:
                        index += 1
            else:
                print(hex(ord(key)))
        else:
            print(hex(ord(key)))
