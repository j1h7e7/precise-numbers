

class AccurateNumber:
    def __init__(self, units, decimals = [], error = 0, positive=True):

        for x in units:
            if x>9 or x<0:
                print(units)
                raise ValueError
        for x in decimals:
            if x>9 or x<0:
                print(decimals)
                raise ValueError

        self.units = units
        self.decimals = decimals
        self.error = error
        self.positive = positive

    @classmethod
    def from_int(cls, value):
        p = value>=0
        u = []
        v = abs(value)
        for i in range(20):
            u.append(v%10)
            v = int(v/10)
            if v==0: break

        return cls(u[::-1],[],0,p)

    @classmethod
    def from_float(cls, value):
        p = value>=0
        u = []
        v = int(abs(value))
        for i in range(20):
            u.append(v%10)
            v = int(v/10)
            if v==0: break
        
        d = []
        v = abs(value)-int(abs(value))
        while abs(v)>=0.000001:
            v*=10
            d.append(int(v))
            v-=int(v)

        return cls(u[::-1],d,0,p)
    
    def __str__(self):
        u = [str(x) for x in self.units]
        d = [str(x) for x in self.decimals]

        e = ""
        if self.error>0: e = " ±"+str(self.error)
        sign = "" if self.positive else "-"
        if len(u)==0: u=["0"]

        return sign+"".join(u)+("." if len(d) else "")+"".join(d)+e

    def get_numerical_value(self):
        value = 0

        for i in range(len(self.units)):
            value += self.units[-1-i]*10**i

        for i in range(len(self.decimals)):
            value += self.decimals[i]*10**-(i+1)

        return value

    def truncated(self, places, witherror = False):
        if places>=len(self.decimals): return self

        d = self.decimals[:places]
        e = self.error
        if witherror: e = max(self.error,0.5*(10**-places))

        return AccurateNumber(self.units,d,e,self.positive)

    def __neg__(self):
        return AccurateNumber(self.units,self.decimals,self.error,not self.positive)

    def __add__(self, other):
        num2 = to_accurate_number(other)

        u = max(len(self.units), len(num2.units))+1
        d = max(len(self.decimals), len(num2.decimals))

        u = [0]*u
        d = [0]*d

        # add
        for i in range(len(u)):
            if i<len(self.units): u[i] += (1 if self.positive else -1)*self.units[-1-i]
            if i<len(num2.units): u[i] += (1 if num2.positive else -1)*num2.units[-1-i]
        for i in range(len(d)):
            if i<len(self.decimals): d[i] += (1 if self.positive else -1)*self.decimals[i]
            if i<len(num2.decimals): d[i] += (1 if num2.positive else -1)*num2.decimals[i]

        u = u[::-1]

        #carry
        def docarries():
            for i in range(len(d)):
                if d[-1-i]>=10:
                    d[-1-i]-=10
                    if i+1<len(d): d[-2-i]+=1
                    else: u[-1]+=1
                elif d[-1-i]<-10:
                    d[-1-i]+=20
                    if i+1<len(d): d[-2-i]-=2
                    else: u[-1]-=2
                elif d[-1-i]<0:
                    d[-1-i]+=10
                    if i+1<len(d): d[-2-i]-=1
                    else: u[-1]-=1
            for i in range(len(u)-1):
                if u[-1-i]>=10:
                    u[-1-i]-=10
                    u[-2-i]+=1
                elif u[-1-i]<-10:
                    u[-1-i]+=20
                    u[-2-i]-=2
                elif u[-1-i]<0:
                    u[-1-i]+=10
                    u[-2-i]-=1

        docarries()

        negative = u[0]<0
        if negative:
            for i in range(1,len(u)): u[i] = 10-u[i]
            for i in range(len(d)):   d[i] = 10-d[i]
            u[0]=-u[0]-1
        
        docarries()

        #remove zeros:
        while len(u)>0 and u[0]==0: u=u[1:]
        while len(d)>0 and d[-1]==0: d=d[:-1]

        return AccurateNumber(u,d,self.error+num2.error,not negative)

        print(u,d)

    def __sub__(self,num2):
        return self+(-num2)

    def __mul__(self, other):
        num2 = to_accurate_number(other)

        u1 = [0]*max(0,len(num2.units)-len(self.units))+self.units
        u2 = [0]*max(0,len(self.units)-len(num2.units))+num2.units

        d1 = self.decimals+[0]*max(0,len(num2.decimals)-len(self.decimals))
        d2 = num2.decimals+[0]*max(0,len(self.decimals)-len(num2.decimals))

        n1 = (u1+d1)[::-1]
        n2 = (u2+d2)[::-1]

        nfinal = []

        for i in range(len(n1)):
            term = 0
            for j in range(i+1):
                term += n1[j]*n2[i-j]
            nfinal.append(term)
        for i in range(len(n1)-1):
            term = 0
            for j in range(len(n1)-i-1):
                term += n1[len(n1)-1-j]*n2[i+j+1]
            nfinal.append(term)
        
        nfinal += [0,0,0]

        for i in range(len(nfinal)-1):
            carry = int(nfinal[i]/10)
            nfinal[i+1]+=carry
            nfinal[i] = nfinal[i]%10

        dfinal = nfinal[:2*len(d1)]
        ufinal = nfinal[2*len(d1):]

        while len(dfinal)>0 and dfinal[0]==0:  dfinal=dfinal[1:]
        while len(ufinal)>0 and ufinal[-1]==0: ufinal=ufinal[:-1]
            
        return AccurateNumber(ufinal[::-1],dfinal[::-1],self.error*num2.error,self.positive==num2.positive)

    def squared(self):
        return self*self

    def __lt__(self, other):
        num2 = to_accurate_number(other)
        return not (self-num2).positive
    
    def __gt__(self, other):
        num2 = to_accurate_number(other)
        return (self-num2).positive

    def abs(self):
        return AccurateNumber(self.units,self.decimals,self.error,True)


def to_accurate_number(number):
    if type(number)==int:     return AccurateNumber.from_int(number)
    elif type(number)==float: return AccurateNumber.from_float(number)
    else:                     return number
