import unittest
import random
class mySet(object):
    def __init__ (self, *args):
        self.length = 8
        self.min_length = 8
        self.used = 0
        self.list = [None]*self.length
        self.reindex_flag = False
        self.p_function = False
        if len(args) != 0:
            for value in args:
                if hasattr(value, '__iter__'):
                    for v in value:
                        self.add(v)
                else:
                    self.add(value)

    def setCollisions(self,flag):
        self.p_function = flag
    
    def p(self,value):
        if self.p_function is False:
            return hash(value)%self.length 
        else:
            #for the sake of collisions!
            return random.randint(0,50)%self.length

    def housekeeping(self):
        if self.used > (self.length//3*2): 
            self.reindex_flag = True
            self.length = self.length * 2
            self.buf_list = list(self.list)
            self.list  = [None]*self.length
            self.used = 0
            for value in self.buf_list:
                self.add(value)
            del self.buf_list
            self.reindex_flag = False
        
        elif self.used < self.length//4 and self.length//2 > self.min_length: 
            self.reindex_flag = True
            self.length = self.length // 2
            self.buf_list = list(self.list)
            self.list = [None]*self.length
            self.used = 0
            for value in self.buf_list:
                self.add(value)
            del self.buf_list
            self.reindex_flag = False
        
    def add(self,value):        
        if not self.reindex_flag:
            self.housekeeping()
        if value is not None:
            if value == (None,'theFlag'):
                return
            if self.has(value)[0]:
                return
            else:
                index = self.p(value)
                step = 0
                while True:
                    if self.list[index] is None or self.list[index] == (None,'theFlag'):
                        self.list[index] = value
                        self.used += 1
                        break
                    else:
                        index = (index + 1)%self.length
            

    def has(self,value):
        index = self.p(value)
        step = 0
        if self.list[index] == None:
            return (False,step)
        elif self.list[index] == value:
            return(True,step)
        else:
            while self.list[index] is not None:
                step +=1 
                if self.list[index] == value:
                    return (True,step)
                index = (index+1)%self.length
        return (False,step)
            
        
    
    def delete(self,value):
        if not self.reindex_flag:
            self.housekeeping()

        if value is not None:
            step = 0
            if not self.has(value)[0]:
                return step
            else:
                index = self.p(value)
                while self.list[index] is not None:
                    step += 1
                    if self.list[index] == value:
                        self.list[index] = (None, 'theFlag')
                        self.used = self.used -1
                        return (step)
                        
                    else:
                        index = (index+1)%self.length

    
    def values(self):
        res = []
        for value in self.list:
            if value is not None:
                if value != (None, 'theFlag'):
                    res.append(value)
        if res == []:
            return None
        return res

    def getStats(self):
        return (self.used,self.length) 




#####some test cases:
class TestMySet(unittest.TestCase):
    
    def test_None(self):
        testSet = mySet()
        self.assertEqual(testSet.values(),None)
        
    
    def test_Settiness(self):
        testSet = mySet()
        testSet.add(1)
        testSet.add(1)
        testSet.add(2)
        self.assertEqual([1,2],testSet.values())
        testSet.delete(1)
        self.assertEqual([2],testSet.values())
    
    
    def test_Has(self):
        testSet = mySet()
    
        #random fill it with 1500 random ints
        for i in range(1500):
            testSet.add(random.randint(-2000000,2000000))

        #insert some strings
        testSet.add('foo')
        testSet.add('bar')
        self.assertFalse(testSet.has('ololo')[0])
        self.assertTrue(testSet.has('foo')[0])
        self.assertTrue(testSet.has('bar')[0])       
        testSet.delete('bar')
        self.assertFalse(testSet.has('bar')[0])
        

    def test_LowCollisions(self):
        testSet = mySet()
        def collTest(mode):
            if mode == 'Low':
                pass
            else:
                testSet.setCollisions(True)
            
            for k in range(10):
                for i in range(1000):
                    testSet.add(random.randint(-10000,10000))
                res = []
                for i in range(1000):
                    res.append(testSet.has(random.randint(-20000,20000))[1])
                print ("%s collisions random elem .has() avg steps: %s"%(mode,sum(res)/len(res)))


        collTest('Low')
        collTest('High')


    def test_Housekeeping(self):
        testSet = mySet()
        for i in range(20):
            testSet.add(i)
        self.assertEqual((20,32),testSet.getStats())
        for i in range(18):
            testSet.delete(i)
        
        self.assertEqual((2,16),testSet.getStats())

if __name__ == '__main__':
    unittest.main()
