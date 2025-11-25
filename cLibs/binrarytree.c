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

typedef struct Node {
	char letter;
	unsigned int count;
	struct Node* left;
	struct Node* right;
} Node;

Node* make_node(char letter, int count) {
	Node* n = malloc(sizeof(Node));
	n->letter = letter;
	n->count = count;
	n->left = NULL;
	n->right = NULL;
	return n;
}

void insert(Node** root, char letter, int count) {
	// empty tree case
	if (*root==NULL) {
		*root = make_node(letter, count);
		return;
	}

	Node *curr = *root;

	while (1) {
		if (count < curr->count) {
			if (curr->left == NULL) {
				curr->left = make_node(letter, count);
				return;
			}
			curr = curr->left;
		}
		else {
			if (curr->right == NULL) {
				curr->right = make_node(letter, count);
				return;
			}
			curr = curr->right;
		}
	}
}

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

	// there are like 1000 characters here.... ok if all characters are equal prob- 1/26 * 1000 -> E=38 for each char... 
	// we can get away with unsinged int here, it's a count
	unsigned int countArray[26] = { 0 }; // if no hash map then I can just use the array here. 
	
	for (int i = 0; text[i]; ++i) { // keeps running till you hit \0
		int id = (int)tolower(text[i]) - 97;
		if (id < 26 && id >= 0) { // logical and
			countArray[id] += 1;
			//printf("char: %c id: %d i: %d count: %d\n", tolower(text[i]), id, i, countArray[id]); // printf instead of debugger for now
		}
	}
	
	Node *root = NULL;
	// printing the array and build the tree
	for (int i = 0; i < 26; ++i) {
		printf("%c:[%d]",'a'+i, countArray[i]);
		insert(&root, 'a' + i, countArray[i]);

	}
	printf("\n");

		
	return EXIT_SUCCESS;

}