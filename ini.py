class inifile():
    def __init__(self,filename):
        self.filename=filename
        self.sections={}

    def parseSection(self,line):
        start = line.find('[')
        end = line.find(']')
        return line[start+1:end]

    def parseKv(self,line):
        s = line.split('=')
        if len(s)!=2:
            print('invalid line: {}'.format(line))
            raise Exception('bad line')
        k = s[0].strip()
        v = s[1].strip()
        return k,v


    def load(self):
        with open(self.filename,'r') as fd:
            section=''
            self.sections[section]={}
            for line in fd.readlines():
                line=line[:-1]
                offs=line.find('#')
                if offs>-1:
                    line=line[:offs]
                if line.find('[')>-1:
                    section = self.parseSection(line)
                    self.sections[section]={}
                elif line.find('=')>-1:
                    k,v = self.parseKv(line)
                    self.sections[section][k]=v

    def __repr__(self):
        out = ''
        for section in self.sections:
            out+='['+section+']\n'
            for k in self.sections[section]:
                out+=k+'='+self.sections[section][k]+'\n'
        return out

    def save(self):
        with open(self.filename,'w') as fd:
            if '' in self.sections:
                for k,v in self.sections[''].items():
                    fd.write('{}={}\n'.format(k,v))
            for section in self.sections:
                if section == '':
                    continue
                fd.write('[{}]\n'.format(section))
                for k,v in self.sections[section].items():
                    fd.write('{}={}\n'.format(k,v))


if __name__ == '__main__':
    ini = inifile('to.do')
    ini.load()
    print(ini)
    ini.filename='to.done'
    ini.save()
