"""
GNU GENERAL PUBLIC LICENSE Version 2

Created on Thu Oct 16 17:33:47 2014

@author: Wasit
"""

import numpy as np


try:
    __import__('imp').find_module('pforest')
    print "Found pforest"
    from pforest.master import mnode
except ImportError:
    print "Not found pforest. Importing local modules"        
    from master import mnode

class tree(mnode):    
    def settree(self,root=mnode(0,0,0)):
        self.theta=root.theta  #vector array
        self.tau=root.tau  #scalar
        self.H=root.H  #scalar
        self.P=root.P  #vector array
        self.parent=root.parent  #mnode
        self.depth=root.depth  #int
        self.char=root.char
        self.Q=root.Q
        if root.L is not None:
            self.L=tree()  #mnode
            self.L.settree(root.L)
            self.R=tree()  #mnode
            self.R.settree(root.R)
    def classify(self,Ix):
        if self.tau is None:#reaching terminal node
            return self.P
        else:
            if(Ix[ int(self.theta) ]<self.tau):
                return self.L.classify(Ix)
            else:
                return self.R.classify(Ix)
    def getP(self,x,dset):
        '''
        input:
            x sample index [int]
            dset the dataset object
        output:
            P [1d ndarray] probability P(L|Ix)
        '''
        #print("test>>mnode:{}".format(self))
        if self.tau is None:#reaching terminal node
            return self.P
        else:
            #if (self.L is not None and goLeft) :
            if (dset.getI(self.theta,x)<self.tau) :
                return self.L.getP(x,dset)
            else:
                return self.R.getP(x,dset)
   
    def getL(self,x,dset):
        '''
        input:
            x sample index [int]
            dset the dataset object
        output:
            L [integer] label
        '''
        return np.argmax(self.getP(x,dset))
    def show(self):
        print self.table()

if __name__ == '__main__':
    import pickle
    from matplotlib import pyplot as plt      
    try:
        __import__('imp').find_module('pforest')
        print "Found pforest"
        from pforest.dataset import dataset
    except ImportError:
        print "Not found pforest. Importing local modules"        
        from dataset import dataset
    #from scmaster import master
#    #training
#    m=master()
#    m.reset()
#    m.train()    
#    print m.root.table()
#    #recording the tree pickle file
#    pickleFile = open('out/root.pic', 'wb')
#    pickle.dump(m.root, pickleFile, pickle.HIGHEST_PROTOCOL)
#    pickleFile.close()
    
    #reading the tree pickle file    
    pickleFile = open('out_tree.pic', 'rb')
    root = pickle.load(pickleFile)
    pickleFile.close()
    
    #init the test tree
    t=tree()
    t.settree(root)
    t.show()
    #compute recall rate
    dset=dataset()
    correct=0;
    for x in xrange(dset.size):
        L=t.getL(np.array([x]),dset)
        if dset.getL(x) == L:
            correct=correct+1
        dset.setL(x,L)
    print("recall rate: {}%".format(correct/float(dset.size)*100))


        
    #setup the new test-set
    d=0.01
    y, x = np.mgrid[slice(-1, 1+d, d), slice(-1, 1+d, d)]
    #create dataset       
    dset2=dataset()
    
    #start labeling   
    
    L=np.zeros(x.shape,dtype=int)
    for r in xrange(x.shape[0]):
        for c in xrange(x.shape[1]):
            Prob=t.classify(( x[r,c],y[r,c] ))
            L[r,c]=np.argmax(Prob)
    
    #plot the lalbel out put
    plt.close('all')
    plt.axis([-1,1,-1,1])
    plt.pcolor(x,y,L)
    plt.show()
    
    #overlaying new input data
    plt.hold(True)
    plt.set_cmap('jet')
    marker=['bo','co','go','ro','mo','yo','ko',
            'bs','cs','gs','rs','ms','ys','ks']
    z=np.random.randint(0,dset.size,1000)
    for i in z:
        plt.plot(dset2.I[i,0],dset2.I[i,1],marker[dset2.samples[i]])
    
    
    
    
    