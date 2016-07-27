#! /usr/local/bin python
import time, socket

class Weather:
    def __init__(self):
        None

    def getValues(self):
        data=[]
        column=[]
        temp=None
        wind=None
        windgusts=None
        humidity=None
        dewpt=None
        sigma=None
        encl=None
        encl35m=None

        """ Send cmd to UDP(host, port). Wait for and print the result. """
        host='wxhost.apo.nmsu.edu'
        port=6251
        cmd='all\n'
        #try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect((host, port))
        s.send(cmd)
        reply = s.recv(1024)
        s.close()
        print reply
        r=reply.split(' ')
        #print r
        for item in r:
            if '=' in item:
                i=item.split('=')
                #print i
                column.append(i[0])
                data.append(i[1])
        #except:
        #    print 'socket failed'
        #    return
        try:
            pos= column.index('airTemp')
            temp=data[pos]
        except:
            temp = -100
        
        try:
            pos=column.index('winds')
            wind=data[pos]
        except:
            wind=-1

        try:
            pos=column.index('gusts')
            windgusts=data[pos]
        except:
            windgusts=-1

        try:
            pos=column.index('humidity')
            humidity=data[pos]
        except:
            humidity=-100

        try:
            pos=column.index('encl35m')
            encl=data[pos]
        except:
            encl=-1
        try:
            pos=column.index('encl25m')
            encl25m=data[pos]
        except:
            encl25m=-1

        try:
            pos=column.index('irscsd')
            sigma=data[pos]
        except:
            sigma=-1
        
        print [temp, sigma,wind,windgusts,humidity, encl,encl25m]
        return [temp, sigma,wind,windgusts,humidity, encl,encl25m]

    def cloudCondition(self, c):
        c=float(c)
        if c==-1:
            return 0
        if c <15:
            return 1
        if c>=15 and c<30:
            return 2
        if c>=30:
            return 3

    def windCondition(self, w,g):
        if w<10 and g<10:
            return 1
        if w>=10 and w<35 and g<35 or g>=10:
            return 2
        if w>=35 or g>=35:
            return 3
        if w==-1:
            return 0
        else: 
            return 0

    def enclosure(self,e):
        if e=='open':
            return 1
        if e=='close':
            return 0
        if e==-1:
            return -1

    def bypass(self):
        arrCat=[]
        arr=[]
        f_in=open('config.dat','r')
        for line in f_in:
            if ';' in line:
                None
            else:
                l=line.rstrip('\n').split('\t')
                arr.append(l)
        f_in.close()
        return arr[0][1],arr[1][1]
        
    def writeFile(self):
        try:
            val=self.getValues()
        #print val
            cloud=self.cloudCondition(val[1])
            wind=self.windCondition(float(val[2]), float(val[3]))
        
            byp = self.bypass()
            if byp[0] == 'no':
                if byp[1] == '35m':
                    enc=self.enclosure(val[5])
                else: 
                    enc=val[6]
            else:
                enc=1
        #print cloud, wind, enc
            
            out = time.strftime("%Y-%m-%d %H:%M:%S ") + 'F M 0 %s 0 %s %s 0 0 0 0 01 0.001 %s %s 1 %s' % (val[0],val[2],val[4], cloud, wind, enc)
        except:
            out = time.strftime("%Y-%m-%d %H:%M:%S ") + 'F M 0 0 0 0 0 0 0 0 0 01 0.001 0 0 0 0'
        print out
        f_out=open('weather.log','w')
        f_out.write(out)
        f_out.close()
    
            

a=ARCSATWeather()
while True:
    try:
        a.writeFile()
        time.sleep(30)
    except:
        print time.strftime("%Y-%m-%d %H:%M:%S failed")
