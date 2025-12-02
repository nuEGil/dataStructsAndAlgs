# challenge to not use numpy and treat it like C... 
import math
import random
import time 

random.seed(42)
# define structures 
# defining ant first gives you the option to make an antlist in the world struct

class ant():
    # all ants have the same max track
    MAX_TRACK = 512 # if you do ant.MaxTrack =101 -it changes for all ant object
                   # if you do ant().MaxTrack = 101 you do an instance level override... 
    def __init__(self):
        self.live = False
        self.xy = None 
        self.track = None
 
class world():
    def __init__(self, PointList, tau, eta, rho, alpha, beta, Q):
        self.PointList = PointList # immutable point list
        self.Tau = tau # pheremone - mutable 
        self.Eta = eta # desireability - mutable
        self.Rho = rho # evaporation parameter
        self.Alpha = alpha # tuning on tau
        self.Beta = beta # tuning on eta
        self.Q = Q # pheremone update param 
        
# define functions 
def SpawnAnts(world, nAnts):
    # python way to do this would be to have it as a method... 
    AntList = []
    for i in range(nAnts):
        a = ant()
        a.live = True 
        a.xy = world.PointList[random.randrange(len(world.PointList))]
        a.track = [a.xy] # pointlist is a list of tuples so this is now safe
        AntList.append(a)
    return AntList   

def GetTrackLength(ant):
    dist = 0.0
    for i in range(len(ant.track)-1):
        x_diff = (ant.track[i+1][0] - ant.track[i][0])**2
        y_diff = (ant.track[i+1][1] - ant.track[i][1])**2
        dist += math.sqrt(x_diff + y_diff)
    return dist

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
    point_list = [(i % max_x, i // max_x) for i in choice_ids]   
    point_list = sorted(point_list, key = lambda x: (x[0], x[1]))
    return point_list

def GenerateSample(distribution):
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
        if r<cumulative:
            return i

def SetEta(points):
    eta = GenerateZeroMat(len(points))
    # update eta (desireability) based on point distance    
    for i in range(len(points)):
        for j in range(len(points)):
            xdiff = (points[i][0] - points[j][0])**2
            ydiff = (points[i][1] - points[j][1])**2
            distance = math.sqrt(xdiff + ydiff) 
            if distance > 0.0:
                eta[i][j] = 1.0 / distance
    return eta

def vecMultiply(A, B):
    # A is a list of lists - and is the same size as B 
    assert (len(A) == len(B) and len(A[0]) == len(B[0])), "Matrices A and B have different sizes"    
    output = [0.0 for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            output[i] += A[i][j] * B[i][j]
    return output

# implement choice masking -- mask DistanceMat later.

def sumMatrix(matrix):
    cummulative = 0
    for a in matrix:
        cummulative+=sum(a)
    return cummulative

def PrintAntTracks(AntList, nPoints):

    for ia, ant in enumerate(AntList):
        dist = GetTrackLength(ant)
        #print(f'ant {ia} len {len(ant.track)} dist {dist}\n', ant.track)
    
        if ia == 0:
            shortest_track = ant.track
            shortest_length = len(ant.track)
            shortest_dist = dist

        else:
            cond0 = len(ant.track)>= nPoints 
            cond1 = dist < shortest_dist
            if cond0 and cond1:
                shortest_track = ant.track
                shortest_length = len(ant.track)
                shortest_dist = dist
    if len(shortest_track)>=nPoints:
        print(f'shortest ant len {len(shortest_track)} dist {shortest_dist}\n', shortest_track)
    else:
        print('shortest path invalid')
    print('--------')
def NormalizeTau(Tau):
    cummulative = 0.0
    new_Tau = Tau.copy()
    for i in range(len(Tau)):
        for j in range(len(Tau[0])):
            cummulative += Tau[i][j]

    for i in range(len(Tau)):
        for j in range(len(Tau[0])):
            new_Tau[i][j]/=cummulative
    return new_Tau

def ComputeMoveChoice(world, AntList):
    #world.Tau = NormalizeTau(world.Tau)
    copy_tau = world.Tau.copy() # copy of tau values
    moves = [[0,0] for a in AntList] # indices in copy_tau to update
    for ia, ant in enumerate(AntList):
        if ant.live:
            pt_id = world.PointList.index(ant.xy)
            eta_ = world.Eta[pt_id]
            tau_ = world.Tau[pt_id]

            # compute initial probabilities
            p_xy = [0.0 for j in range(len(world.Eta))] # square matrix, but should use inner dim. 
            denom = [(e ** world.Alpha) * (a ** world.Beta) for (e, a) in zip(eta_, tau_)]
            inv_sum = 1/sum(denom)

            # compute probabilites
            for i in range(len(world.Eta)): 
                p_xy[i] += (((eta_[i]**world.Alpha)*(tau_[i]**world.Beta)) * inv_sum)
            
            # do a visitation check 
            for t in ant.track:
                pt_id = world.PointList.index(t)
                p_xy[pt_id] = 0.0
            
            # if the probability of all nodes is still 0, flip ant.live
            # ie no valid moves were found
            spxy = sum(p_xy)
            if spxy > 0.0:
                p_xy = [p_ / spxy for p_ in p_xy]
  
                # once you have probability, sample it. 
                new_pt_id = GenerateSample(p_xy)
                ant.xy = world.PointList[new_pt_id]
                ant.track.append(world.PointList[new_pt_id])
           
                # implment check for ant live dead
                if len(ant.track) >= ant.MAX_TRACK:
                    ant.live = False

                if ant.xy == ant.track[0]:
                    ant.live = False

                # Store only changes in copy tau so we have less to itterate over on tau update
                # formula calls for a sum of tau increments.. this will do it. 
                copy_tau[pt_id][new_pt_id] += (world.Q / world.Eta[pt_id][new_pt_id]) 
                moves[ia] = [0+pt_id, 0+new_pt_id]

            else: 
                ant.live = False
     
    # update tau 
    for m in moves:
        world.Tau[m[0]][m[1]] = (1-world.Rho) * world.Tau[m[0]][m[1]] + copy_tau[m[0]][m[1]]
     
    world.Tau = NormalizeTau(world.Tau)
    
def RunBatches(w, nAnts, nPoints, n_iterations = 5):
    # loop this so that you keep updating the world state
    
    for j in range(n_iterations):
        nLiveAnts = 0+nAnts

        AntList = SpawnAnts(w, nAnts)      
        # print('number of live ants ', LiveDeadAssay(AntList))
        # print('point list index ', PointList.index(AntList[0].xy))

        # begin main actions. 
        while (nLiveAnts > nAnts//4):
        
            ComputeMoveChoice(w, AntList)
            nLiveAnts = LiveDeadAssay(AntList)
        
        print(f'--- batch {j} ---')
        PrintAntTracks(AntList, nPoints)
        
if __name__ =='__main__':
    start_time = time.time()
    # powers of 2
    nPoints = 64
    nAnts = 128
    
    rho = 0.9 # evaportation coeff
    alpha = 0.01 # tuning param on tau (pheremone)
    beta  = 0.01 # tuning param on eta (attractiveness)
    Q = 1/nAnts # pheremone update param

    # point to these
    PointList = GeneratePoints(N = nPoints) 
    
    print('should be equal', len(set(PointList)), len(PointList))

    # define initial tau (pheremone deposited), eta (desireability) 
    eta = SetEta(PointList) # 1 / distance.
    tau = GenerateOneMat(len(PointList)) # pheremone.
    
    # create world structure
    w = world(PointList, tau, eta, rho, alpha, beta, Q) 
   
    # python thinks of these things like pointers - you have to use deep copy to make 
    print('object id for a test \nPointList@:{} \nw.PointList@:{} \nSame?:{}'\
          .format(id(PointList), id(w.PointList), id(PointList)==id(w.PointList)))
    
    RunBatches(w, nAnts, nPoints, n_iterations = 10)
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print(f"The code took {elapsed_time:.4f} seconds to run.")
 