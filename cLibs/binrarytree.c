#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<ctype.h>
/* Following: https://en.wikipedia.org/wiki/Binary_tree

I want to do a succinct encoding verion of this. information theoretical lower bounds 
number of different binary trees on n nodes is C_n -- nth Catalan number (trees w identical 
structure are identical) for large n, this is 4^n -- need at least about log2 4^n = 2n bits to 
encode it. A succinct binary tree occupies 2n+o(n) bits ......

you ouput a 1 for an internal node, and a 0 for a leaf. 

hmm. long long is 64 bits.... so I can use 1 long long to represent a tree of depth 64... 
8 bytes... vs if I did an array of ints for this I'd have 64*4 = 256 bytes.  

C doesnt have a hash table.... betrayed

*/




int main() {
	char text[] = "In computer science, a binary tree is a tree data structure in which each node has at most two children, \
referred to as the left child and the right child. That is, it is a k-ary tree where k = 2. A recursive definition using set \
theory is that a binary tree is a triple (L, S, R), where L and R are binary trees or the empty set and S is a singleton \
(a single–element set) containing the root.[1][2] From a graph theory perspective, binary trees as defined here are arborescences.\
[3] A binary tree may thus be also called a bifurcating arborescence, [3] a term which appears in some early programming books[4] \
before the modern computer science terminology prevailed.It is also possible to interpret a binary tree as an undirected, \
rather than directed graph, in which case a binary tree is an ordered, rooted tree.[5] \
Some authors use rooted binary tree instead of binary tree to emphasize the fact that the tree is rooted, but as defined above, \
a binary tree is always rooted.[6]\0";

	// there are like 1000 characters here.... wrong type on character array
	long long int countArray[26] = { 0 }; // if no hash map then I can just use the array here. 
	
	for (int i = 0; text[i]; ++i) { // keeps running till you hit \0
		int id = (int)tolower(text[i]) - 97; // use 'a' as 0
		//printf("char: %c id: %d i: %d\n", tolower(text[i]), id, i); // printf instead of debugger for now
		if (id < 26) { // int has wrap around of negative numbers  -- so you just have to check if it's less than 26 to work 
			countArray[id] += 1;
		}
	}
	 	
	for (int i = 0; i < 26; ++i) {
		printf("%c:[%lld]",'a'+i, countArray[i]);
	}
	printf("\n");
	
	return EXIT_SUCCESS;

}