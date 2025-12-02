# Data structures and algorithms
Implmentations of some data structures and algorithms to get better at each language. 
first thing. lots of pointers. lots and lots of pointers. 

## Traveling salesman problem with ant optimization
Ant colony optimization
https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms

procedure ACO_MetaHeuristic is
    while true
        generateSolutions()
        daemonActions()
        pheremoneUpdate() 
end procedure

applied to travelling salesman problem. 
https://en.wikipedia.org/wiki/Travelling_salesman_problem
kth ant moves from state x to state y with probability 
p^k_xy = (tau^alpha_xy)(eta^beta) / sum_zallowed((tau^alpha_xz)(eta^beta_xz))
tau = pheremones
eta = desireability
tau_xy update = (1-rho)tau_xy + sum(change in tau^k_xy)
Q/L_k  if the any uses curve xy in its tour, 0 othterwise... 

Goal: learn a good probability distribution on making moves
other notes:
0. Traveling salesman is an NP hard problem -- there is no guarantee we can find a polynomial time solution, and
the ants colony algorithm does not guarantee we can find a global min short path. 

1. 1. p^k_xy is probability of a move conditioned on desireability = 1/distance, and on 
the number of times a move has been made by the other ants. 

2. This implementation normalizes tau after all ants have made a step; this is to prevent large tau.

3. There is some room to add a track pruning /merging stage to this. Would need to enable backtracking - so dont 0 visited paths
	You can do depth first search with pruning and merging in this case as well.

4. as the number of uniformly distributed random points increases the less structure you have. In this case the Snake video game would be 
	a better solution. 

5. As the number of ants increases the number of points with pheremone starts to saturate. right so its like
	all the ants start to call on eachother. nAnts < nPoints you have unexplored paths...

Things to log to experiment with 
1. shotest track and total distance  vs 
	number of points
	number of ants ( < or > or = nPoints) likely to be inflection points but would need to experiment. 
2. longest number of batches before you get invalid short paths.

This parameter set seems to work well. got about 6 batches out of it. 
	nPoints = 64
    nAnts = 128
    rho = 0.9     evaportation coeff
    alpha = 0.01  tuning param on tau (pheremone)
    beta  = 0.01  tuning param on eta (attractiveness)
    Q = 1/nAnts   pheremone update param


## douby linked list 
https://en.wikipedia.org/wiki/Doubly_linked_list

Memory: malloc Node, which comes with a char and 2 pointers. on 64 bit os thats 
17 bytes total per node (16 b pointers  + 1b char) This implementation then scales
O(2M) --> O(M)  where M is the number of nodes. 

Time: Doubly linked list object has pointer to the first and last nodes, so O(1) 
when opperating on the first and last node. if you need to get any point in the 
middle of the doubly then you take O(N) moves to get to that point in the list 
and operate on it -- the double linkage just allows you to move backwards

Also, here I implemented it so that each character is a node. I could have added 
a step to do n-grams so get n consecutive characters.


## binary tree 
https://en.wikipedia.org/wiki/Binary_tree

Following: https://en.wikipedia.org/wiki/Binary_tree
I want to do a succinct encoding verion of this. information theoretical lower bounds 
number of different binary trees on n nodes is C_n -- nth Catalan number (trees w identical 
structure are identical) for large n, this is 4^n -- need at least about log2 4^n = 2n bits to 
encode it. A succinct binary tree occupies 2n+o(n) bits ......

In this case Im only using the 26 lower case english alphabet to count. so the degenerate tree 
is 26 characters deep. At max i only need a 26 bit string here.... each char if uniform dist 
has 1/26 chance in appearing, and the text i used is about 1000 chars so 1/26*1000 is about 38. 
Expected rate of occurence of each char is 38 ... ill use uint 32 though for the counts gives 2^32 max number. 

ok so the implementation is  abit memory intensive because Im using this struct to cary around every thing

typedef struct Node {
	char letter;
	uint32_t count;
	uint32_t code;
	uint8_t depth;
	struct Node* left;
	struct Node* right;

} Node;

ok but the end encoding, you can loop through and get binary strings for every character... 
the least frequent character has the longest string, and the most frequent character has the shortes.
so now when you write to disk it's a compact encoding... 

## other 
look into  dynamic arrays --
https://en.wikipedia.org/wiki/Dynamic_array
