# Data structures and algorithms
Implmentations of some data structures and algorithms to get better at each language. 
first thing. lots of pointers. lots and lots of pointers. 

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

