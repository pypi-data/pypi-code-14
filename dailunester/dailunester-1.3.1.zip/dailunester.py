##def selectsort(alist):          #选择排序
##    for j in range(0,len(alist)):
##        index=j
##        num=alist[j]
##        for i in range(j+1,len(alist)):
##            if num>alist[i]:
##                num=alist[i]
##                index=i
##        temp=alist[j]
##        alist[j]=alist[index]
##        alist[index]=temp
##    print(alist)
##def bubble(alist):               #冒泡排序
##    for j in range(0,len(alist)):
##        for i in range(0,len(alist)-1):
##            if alist[i]>alist[i+1]:
##                temp=alist[i]
##                alist[i]=alist[i+1]
##                alist[i+1]=temp
##    print(alist)
##def mergesort(alist):           #归并排序
##    middle=int(len(alist)/2)
##    while len(alist)==1:
##        return alist
##    result=merge(mergesort(alist[:middle]),mergesort(alist[middle:]))
##    return result
##def merge(left,right):          #mergesort的help函数
##    result=[]
##    i,j=0,0
##    while i<len(left) and j<len(right):
##        if   left[i]<=right[j]:
##                result.append(left[i])
##                i+=1
##        else:
##                result.append(right[j])
##                j+=1
##    while i<len(left):
##            result.append(left[i])
##            i+=1
##    while j<len(right):
##            result.append(right[j])
##            j+=1        
##    return result
##def readfloat(requestMsg,errorMsg):    #异常 
##    while True:
##        val = input(requestMsg)
##        try:
##            val = float (val)
##            return val
##        except:
##            print (errorMsg)
##def getGrade(fname):                #异常
##    try:
##        gradesFile=open(fname,'r')
##    except IOError:
##        print ('Could not open' , fname)
##        raise ('GetGradeError1')
##    grades =[]
##    for line in gradesFile:
##        grades.append(float(line))
##    return grades
##def fastfib(n,memo):              #fib1的辅助函数
##    if not n in memo:
##        memo[n] = fastfib(n-1,memo)+fastfib(n-2,memo)
##    return memo[n]
##def fib1(n):                    #overlapped sub-problem高效解决递归
##    memo = {0:1,1:1}
##    return fastfib(n,memo)
##def fib(n):                    #递归方法解决斐波那契
##    if n<=1:
##        return 1
##    else:
##        return fib(n-1)+fib(n-2)
##numCalls=0
##w=[1,1,5,5,3,3,23,23,12,12,6,6]
##v=[15,15,10,10,9,9,11,11,5,5,2,2]
##def maxVal(w,v,i,aW):        #决策树  最优子结构
##    global numCalls
##    numCalls+=1
##    if i ==0:
##        if w[i]<=aW:return v[i]
##        else:return 0
##    without_i=maxVal(w,v,i-1,aW)
##    if w[i] >aW:
##        return without_i
##    else:
##        with_i = v[i] + maxVal(w,v,i-1,aW - w[i])
##    return max(with_i,without_i)
##def fastmaxVal(x,v,i,aW,m):    #maxVal1的辅助函数
##    global numCalls
##    numCalls +=1
##    try: return m[(i,aW)]
##    except KeyError:
##        if i == 0:
##            if w[i]<=aW:
##                m[(i,aW)] = v[i]
##                return v[i]
##            else:
##                m[(i,aW)] = 0
##                return 0
##        without_i = fastmaxVal(w,v,i-1,aW,m)
##        if w[i] > aW:
##            m[(i,aW)] = without_i
##            return without_i
##        else:
##            with_i = v[i] + fastmaxVal(w,v,i-1,aW- w[i],m)
##        res= max(with_i,without_i)
##        m[(i,aW)] = res
##        return res
##def maxVal1(w,v,i,aW):  #overlapped 解决决策树问题  背包问题
##    m={}
##    return fastmaxVal(w,v,i,aW,m)
##        
##class cartesianPoint:
##    pass
##cp1 = cartesianPoint()
##cp2 = cartesianPoint()
##cp1.x = 1.0
##cp1.y = 2.0
##cp2.x = 1.0
##cp2.y = 3.0
##class cPoint:                   #结构
##    def __init__(self,x,y):
##            self.x = x
##            self.y = y
##            self.radius = math.sqrt(self.x*self.x +self.y*self.y)
##            self.angle = math.atan2(self.y,self.x)
##            def cartesian(self):
##                    return (self.x,self.y)
##            def polar(self):
##                    return (self.radius,self.angle)
##            def __str__(self):
##                    return '(' +str(self.x) + ', ' +str(self.y)+')'
##            def __cmp__(self,other):
##                    return (self.x > other.x) and (self.y >other.y)
##    
##class pPoint:                           #结构
##    def __init__(self,r,a):
##        self.radius = r
##        self.angle = a
##        self.x = r * math.cos(a)
##        self.y = r * math.sin(a)
##    def cartesian(self):
##        return (self.x,self.y)
##    def polar(self):
##        return (self.radius,self.angle)
##    def __str__(self):
##        return '(' + str(self.x) +  ',' + str(self.y) + ')'
##    def __cmp__(self, s):
##        if self.x < s.x and self.y < s.y:
##            return -1
##        elif self.x > s.x and self.y > s.y:
##            return 1
##        else:
##            return 0
##class Person(object):
##    def __init__(self,family_name,first_name):
##        self.family_name = family_name
##        self.first_name = first_name
##    def familyName(self):
##        return self.family_name
##    def firstName(self):
##        return self.first_name
##    def __cmp__(self,other):
##        return operator.le((self.family_name,self.first_name),
##                           (other.family_name,other.first_name))
##    def __str__(self):
##        return 'Person is the ' + self.first_name + self.family_name
##    def say(self,toWhom,something):
##        return self.first_name + self.family_name
##    def sing(self,toWhom,something):
##        return 1
##class MITPerson(Person):
##    nextIDNum=0
##    def __init__(self,familyname,firstname):
##        Person.__init__(self,familyname,firstname)
##        self.idNum = MITPerson.nextIDNum
##        MITPerson.nextIDNum += 1
##    def getIdNum(self):
##        return self.idNum
##    def __str__(self):
##        return 'MIT Person %s %s' %(self.first_name,self.family_name)
##    def __cmp__(self):
##        return cmp(self.idNUm,other.idNum)
##class DG(MITPerson):
##    def __init__(self,familyName,firstName):
##        MITPerson.__init__(self,familyName,firstName)
##        self.year = None
##    def setYear (self,year):
##        if year>5: raise OverflowError('DG error')
##        self.year = year
##    def getYear (self):
##        return self.year
##    def say (self ,toWhom,something):
##        return MITPerson.say(self,toWhom,something)
##class Faculty(object):
##    def __init__(self):
##        self.name = []
##        self.IDs=[]
##        self.members = []
##        self.place = None
##    def add(self,who):
##        if type(who)!=prof :raise TypeError ('not a professor')
##        if who.getIdNum() is self.IDs : raise ValueError('duplicate Id')
##        self.names.append(who,getIdNum())
##        self.IDs.append(who.getIdNum())
##        self.members.append(who)
##    def __iter__(self):
##        self.place = 0
##        return self
##    def next(self):
##        if self.place>=len(self.names):
##            return StopIteration
##        self.place +=1
##        return self.members[self.place-1]
##    
##import math,random,pylab
##class Location(object):                #位置
##    def __init__(self,x,y):
##        self.x=float(x)
##        self.y=float(y)
##    def move(self,xc,yc):
##        return Location(self.x+float(xc),self.y+float(yc))
##    def getCoords(self):
##        return self.x,self.y
##    def getDist(self,other):
##        ox,oy=other.getCoords()
##        xDist = self.x - ox
##        yDist = self.y - oy
##        return math.sqrt(xDist**2 + yDist**2)
##class CompassPt(object):            #方向
##    possibles = ('N','S','E','W')
##    def __init__(self,pt):
##        if pt in self.possibles:self.pt = pt
##        else: raise ValueError('in Compasspt._init ')
##    def move(self,dist):
##        if self.pt == 'N' :return (0,dist)
##        elif self.pt == 'S' :return (0,-dist)
##        elif self.pt == 'E' :return (dist,0)
##        elif self.pt == 'W' :return (-dist,0)
##        else: raise ValueError('in CompassPt.move')
##    
##class Field(object):
##    def __init__(self,drunk,loc):
##        self.drunk = drunk
##        self.loc = loc
##    def move(self,cp,dist):
##        oldLoc = self.loc
##        xc,yc = cp.move(dist)
##        self.loc = oldLoc.move(xc,yc)
##    def getLoc(self):
##        return self.loc
##    def getDrunk(self):
##        return self.drunk
##class Drunk(object):
##    def __init__(self,name):
##        self.name = name
##    def move(self,field,cp,dist=1):
##        if field.getDrunk().name !=self.name:
##            raise ValueError('Drunk.move called with drunk not in field')
##        for i  in range(dist):
##            field.move(cp,1)
##def performTrial(time,f):
##    start = f.getLoc()
##    distances = [0.0]
##    for t in range(1,time + 1):
##        f.getDrunk().move(f,)
##        newLoc = f.getLoc()
##        distance = newLoc.getDist(start)
##        distances.append(distance)
##    return distances
####def firsttest():
####    drunk = Drunk('Homer Simpson')
####    for i in range(3):
####        f = Field(drunk,Location(0,0))
####        distances=performTrial(500,f)
####        pylab.plot(distances)
####    pylab.title('Homer\'s Random Walk')
####    pylab.xlabel('Time')
####    pylab.ylabel('Distance from Origin')
##
###firsttest()
##class oddField(Field):
##    def isChute(self):
##        x,y=self.loc.getCoords()
##        return abs(x) - abs(y) ==0
##    def move(self,cp,dist):
##        Field.move(self,cp,dist)
##        if self.isChute():
##            self.loc = Location(0,0)
##class UsualDrunk(Drunk):
##    def move(self,field,dist=1):
##        cp=random.choice(CompassPt.possibles)
##        Drunk.move(self,field,CompassPt(cp),dist) #Note notation of call
##class ColdDrunk(Drunk):
##    def move(self,field,dist=1):
##        cp = random.choice(CompassPt.possibles)
##        if cp=='S':
##            Drunk.move(self,field,CompassPt(cp),2*dist)
##        else:
##            Drunk.move(self,field,CompassPt(cp),dist)
##class EWDrunk(Drunk):
##    def move(self,field,time=1):
##        cp=random.choice(CompassPt.possibles)
##        while cp!='E' and cp!='W':
##            cp = random.choice(CompassPt.possibles)
##        Drunk.move(self,field,CompassPt(cp),time)    
##def performSim(time,numTrials,drunkType):
##    distLists = []
##    for trial in range(numTrials):
##        d = drunkType('Drunk' + str(trial))
##        f = oddField(d,Location(0,0))
##        distances = performTrial(time,f)
##        distLists.append(distances)
##    return distLists
##def ansQuest(maxTime,numTrials,drunkType,title):
##    means=[]
##    distLists = performSim(maxTime,numTrials,drunkType)
##    for t in range(maxTime + 1):
##        tot = 0.0
##        for distL in distLists:
##            tot+=distL[t]
##        means.append(tot/len(distLists))
##    pylab.figure()
##    pylab.plot(means)
##    pylab.ylabel('distance')
##    pylab.xlabel('time')
##    pylab.title('Average Distance vs. Time (' + str(len (distLists)) + ' trials)')
##
####ansQuest(500,100,UsualDrunk,'UsualDrunk')
####pylab.show()
##
##from pylab import *
##import random, math
##def flipTrial(numFlips):
##    heads,tails = 0, 0
##    for i in xrange(0,numFlips):
##        coin = random.randint(0,1)
##        if coin == 0:heads +=1
##        else:tails +=1
##    return heads,tails
##def simFlips(numFlips,numTrials):
##    diffs=[]
##    for i in xrange(0,numTrials):
##        heads,tails=flipTrial(numFlips)
##        diffs.append(abs(heads - tails))
##    diffs = array(diffs)
##    print diffs
##    diffMean =sum(diffs)/len(diffs)
##    diffPercent = (diffs/float(numFlips))*100
##    percentMean = sum(diffPercent)/len(diffPercent)
##    hist(diffs)
##    axvline(diffMean,color='r',label = 'Mean')
##    legend()
##    titleString = str(numFlips) + ' Flips, ' + str(numTrials) + ' Trials'
##    title(titleString)
##    xlabel('Difference between heads and tails')
##    ylabel('number of Trials')
##    figure()
##    plot(diffPercent)
##    axhline(percentMean,label = 'Mean')
##    legend()
##    title(titleString)
##    xlabel('Trial number')
##    ylabel('Percent Difference between heads and tails')
####simFlips(1000,100)           
####show()                                    
###Tell Python which local standard to use
##import locale
###locale.setlocale(locale.LC_ALL,'en_US.UTF-8')  #不允许该 在cmd中set更改
###Format ints according to local standard
##def formatInt(i):
##    return locale.format('%d',i,grouping = True)
##from pylab import *
##import random,math
##def throwDarts(numDarts,shouldPlot):
##    inCircle = 0
##    estimates = []
##    for darts in xrange(1,numDarts + 1 ,1):
##        x = random.random()
##        y = random.random()
##        if math.sqrt(x*x + y*y)<=1.0:
##            inCircle += 1
##        if shouldPlot:
##            piGuess = 4*(inCircle/float(darts))
##            estimates.append(piGuess)
##        if darts%1000000 == 0: #so I know it's making progress
##            piGuess = 4*(inCircle/float(darts))
##            dartsStr=locale.format('%d',darts,True)
##            print 'Estimate with',formatInt(darts),'darts:',piGuess
##    if shouldPlot:
##        xAxis = arange(1,len(estimates)+1)
##        semilogx(xAxis,estimates)
##        titleString = 'Estimations of pi , final estimate: ' + str(piGuess)
##        title(titleString)
##        xlabel('Number of Darts Thrown')
##        ylabel('Estimate of pi')
##        axhline(3.14159)
##    return 4*(inCircle/float(numDarts))
##def findPi(numDarts,shouldPlot=False):
##        piGuess = throwDarts(numDarts,shouldPlot)
##        print 'Estimated value of pi with',formatInt(numDarts),'darts:',piGuess
##findPi(100,True)
##findPi(1000)
##show()
movies=["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
	["Graham Chapman" ,["Michael Palin","John Cleese","Terry Gilliam",
			   "Eric Idle","Terry Jones"]]]
def print_lol(the_list,indent=false,num=0,to=sys.stdout):                  #print列表（包括内嵌的列表）
    for each_item in the_list:
        if isinstance(each_item,list):
                print_lol(each_item,indent,num+1,to)
        else:
            if indent:
              for i in range(num):
                  print('\t',end='',file=to)
            print(each_item,file=to)