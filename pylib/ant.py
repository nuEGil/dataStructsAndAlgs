'''
challenge to not use numpy and treat it like C... 
Note - the code is not going to be one to one, theres language quirks 

python speed things 
fastest to slowest
1. Built-in function, len(), sum(), abs(), any() -- implemented in C
2. Free python function --> name look up + python call stack
3. bound method obj.method() --> attribute lookup + descriptor binding + python call
4. dunder method obj.__len__() -- same overhead as method -- manual special lookup
5. callable object -- attribute lookup, python call, custom_call...

probability distribution should be restricted to allowed moves not all moves. 
if you do this though, the tau and eta matrices might change size.... think some more



messed up. attrativeness is the distance matrix dude. tau is the pheremone part. 
should be easy to update. but I need some lunch. 

need to mask the proability of any point visited.... because if not the ant would just stay 
put. distance is 0 so it would stay. 

current version prioritizes long distance travel.... this is good for goggins, but bad
becuase every step they try to jump to the opposite end of the map. 
'''
import math
import random

# define structures first
class world():
    def __init__(self, PointList, DistanceMat, AttractivenessMat):
        self.PointList = PointList 
        self.Distances = DistanceMat
        self.AttractivenessMatrix = AttractivenessMat

class ant():
    # all ants have the same max track
    MAX_TRACK = 100 # if you do ant.MaxTrack =101 -it changes for all ant object
                   # if you do ant().MaxTrack = 101 you do an instance level override... 
    def __init__(self):
        self.live = False
        self.xy = None 
        self.track = None
        
# define functions 
def SpawnAnts(PointList, nAnts):
    # python way to do this would be to have it as a method... 
    AntList = []
    for i in range(nAnts):
        a = ant()
        a.live = True 
        a.xy = PointList[random.randrange(len(PointList))]
        a.track = [a.xy] # pointlist is a list of tuples so this is now safe
        AntList.append(a)
    return AntList   

def LiveDeadAssay(AntList):
    return sum([a.live for a in AntList])

def GenerateZeroMat(N):
    # returns list of list of floats of 0.0s
    return [[0.0 for i in range(N)] for j in range(N)]

def GenerateOneMat(N):
    # returns list of list of floats of 0.0s
    return [[1.0 for i in range(N)] for j in range(N)]

def GeneratePoints(N=20, max_x=100, max_y=100):
    # Returns unique points so you dont get 0 distance 
    assert N < max_x*max_y, "N must be < max_x * max_y"
    
    full_axis = [c for c in range(max_x * max_y)]
    choice_ids = random.sample(full_axis, N)
    #print('choice ids ',choice_ids)
    point_list = [(i % max_x, i // max_x) for i in choice_ids]   
    point_list = sorted(point_list, key = lambda x: (x[0], x[1]))
    #print('point list ', point_list)
    return point_list

def generate_sample(distribution):
    # Inverse transform sampling 
    # https://en.wikipedia.org/wiki/Inverse_transform_sampling
    # so  generate a random number from uniform dist -- plug it into inverse of 
    # cumulative dist function (CDF). we dont have that for a user defined dist 
    # but we can set a numerical approximation - by generating the number
    # so r is uniformly distributed -- so it has a p[i] probability of 
    # being less than or equal to p[i], then it has p[i]+p[i+1] prob of 
    # being lower than p[i+1]  and so on thats what a CDF is 
    # probability sums  so we just take advantage of that. 
    # normally, we use numpy to do this part because it's implemented in C
    # and because this thing has O(N) scaling where N is the size of the 
    # distribution. 
    # if you actually have the mathematical inverse of the cdf - then you 
    # can implement that equation and get O(N) scaling with the number of samples. 
    # O(1) with the distribution.... 
    r = random.random() # uniformly distributed random number [0,1]
    cumulative = 0.0 # cumulative sum

    for i, prob in enumerate(distribution):
        cumulative += prob
        if r<=cumulative:
            return i

def ComputeDistances(points):
    # returns list of lists of floats -- NxN where N is point list length 
    # float array - when optmizing, only compute triangle matrix
    distance_mat = GenerateZeroMat(len(points))
    # print('output ', len(distance_mat), len(distance_mat[0]))    
    for i in range(len(points)):
        for j in range(len(points)):
            xdiff = (points[i][0] - points[j][0])**2
            #print('xdiff', xdiff)
            ydiff = (points[i][1] - points[j][1])**2
            distance_mat[i][j] = (math.sqrt(xdiff + ydiff))  
    #print(distance_mat)
    return distance_mat

def ComputDenom(DistanceMat, AttractivenessMat):
    # DistanceMat -> atractiveness eta
    # AttractivenessMat -> pheremone tau    
    # should only need to compute this once at each epoch
    # store the value then just point to it for every pk_xy
    # distance and attractiveness are the same size 
    # include size as args in C
    DenomSums = [0.0 for i in range(len(DistanceMat))]
    for i in range(len(DistanceMat)):
        for j in range(len(DistanceMat[0])):
            DenomSums[i] += DistanceMat[i][j] * AttractivenessMat[i][j]
    
    return DenomSums

# implement choice masking -- mask DistanceMat later.

def sumAttractMat(AttractivenessMat):
    cummulative = 0
    for a in AttractivenessMat:
        cummulative+=sum(a)
    return cummulative

def ComputeMoveChoice(AntList, PointList, DistanceMat, AttractivenessMat, pDenomSums):
    print('attractiveness mat sum ',sumAttractMat(AttractivenessMat))
    
    move_set = [[0,0] for a in AntList] # list to hold each ant's move
    
    for ia, ant in enumerate(AntList):
        if ant.live:
            pt_id = PointList.index(ant.xy)
            d = DistanceMat[pt_id]
            a = AttractivenessMat[pt_id]
            p_xy= [0.0 for j in range(len(DistanceMat))] 
        
            # get the denominator - no zero check, should have unique points
            inv_sum = 1.0 / pDenomSums[pt_id]  
            # compute probabilites
            for i in range(len(DistanceMat)): 
                p_xy[i] += d[i]*a[i]
        
            for i in range(len(DistanceMat)):
                p_xy[i] *= inv_sum

            # once you have probability, sample it. 
            new_pt_id = generate_sample(p_xy)
            ant.xy = PointList[new_pt_id]
            ant.track.append(PointList[new_pt_id])
           
            #print('pt_id', pt_id, new_pt_id)
        
            # implment check for ant live dead
            if len(ant.track) >= ant.MAX_TRACK:
                ant.live = False

            if ant.xy == ant.track[0]:
                ant.live = False

            # need to do this here otherwise attractiveness changes 
            # before all ants march. 
            move_set[ia][0] += pt_id
            move_set[ia][1] += new_pt_id
    
    # update attractiveness matrix following march
    for m in move_set:
        #print(m)
        AttractivenessMat[m[0]][m[1]] += 1
    print('new attractiveness mat sum ',sumAttractMat(AttractivenessMat))
        
if __name__ =='__main__':
    # powers of 2
    nPoints = 128
    nAnts = 64
    nLiveAnts = 0+nAnts
    # point to these
    PointList = GeneratePoints(N = nPoints) 
    print('should be equal', len(set(PointList)), len(PointList))

    DistanceMat = ComputeDistances(PointList)
    AttractivenessMat = GenerateOneMat(len(PointList)) # because gen 0 would make a 0 denom
    w = world(PointList, DistanceMat, AttractivenessMat)
    
    # python thinks of these things like pointers - you have to use deep copy to make 
    print('object id for a test \nPointList@:{} \nw.PointList@:{} \nSame?:{}'\
          .format(id(PointList), id(w.PointList), id(PointList)==id(w.PointList)))
    
    AntList = SpawnAnts(PointList, nAnts)      
    print('number of live ants ', LiveDeadAssay(AntList))
    print('point list index ',PointList.index(AntList[0].xy))
    
    # begin main actions. 
    
    #for j in range (10):
    while (nLiveAnts > nAnts//2):
        pDenomSums = ComputDenom(DistanceMat, AttractivenessMat)
        ComputeMoveChoice(AntList, PointList, DistanceMat, AttractivenessMat, pDenomSums)
        print('outside scope',sumAttractMat(AttractivenessMat))

        nLiveAnts = LiveDeadAssay(AntList)
        print('number of living ants ', nLiveAnts)
    
   


    '''
    Next step you need a while loop that says -- even this, you would need to do a live / dead check function.
    actually do that lol because you can do a live dead assay here, and measure graph complexity.    
    
    memorize the shortest track
    For Epochs
        while LiveDeadAssay(AntList) > nAnts//4 :
            compute ant move based on the probability function
            move ant
            increment visiation matrix 
            if ant reaches it's start point or if max track reached 
            check to see if any of the ants got a shorter track than the prev shortest
        now update the pheremone matrix
        
    once you finish the epochs, return the shortest track the ants have on file. 
    '''