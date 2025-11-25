#include<stdlib.h>
#include<stdio.h>
#include<string.h>

typedef struct Node{
	char data;
	struct Node *next;
	struct Node *prev; 
} Node;

typedef struct DoublyLinkedList{
	Node *firstNode;
	Node *lastNode;
} DoublyLinkedList;

void insertAfter(DoublyLinkedList *dll, Node *node, Node *newNode){
	newNode->prev = node;	

	if(!node->next){				// intserting at a tail
		newNode->next = NULL;
		node->next = newNode;
		dll->lastNode = newNode;
	} else{							// inserting in middle
		newNode->next = node->next;
		node->next->prev = newNode;
		node->next = newNode;
	}
}

void removeNode(DoublyLinkedList *dll, Node *node){
    if (!node) return;  // safety napkin

    // unlink from prev
    if (!node->prev) {              // removing the head
        dll->firstNode = node->next;
    } else {
        node->prev->next = node->next;
    }

    // unlink from next
    if (!node->next) {              // removing the tail
        dll->lastNode = node->prev;
    } else {
        node->next->prev = node->prev;
    }

    //cut the node and free it to prevent mem leak
    node->prev = NULL;
    node->next = NULL;
}

void forwardMotion(DoublyLinkedList *dll){
	 for (Node *p = dll->firstNode; p; p = p->next)
        putchar(p->data);
    putchar('\n');
}

void forwardAdder(DoublyLinkedList *dll, char noiseChar){
    for (Node *p = dll->firstNode; p;) {
		Node *next = p->next; // save so we can remove nodes if needed
	
        if (p->data == 'i') {
            Node *noise = malloc(sizeof(Node)); // you have to make a new node on each call. 
            noise->data = noiseChar;
            noise->prev = NULL;
            noise->next = NULL;
            insertAfter(dll, p, noise);

        } else if(p->data =='o' || p->data =='a'){ // rememebr | bitwise or not logical, here we want logical
			removeNode(dll, p);
			free(p); // free p because we no longer need this node
		}
		p = next; // always goto the next node
    }
}

void freeList(DoublyLinkedList *dll) {
    Node *p = dll->firstNode;
    while (p) {
        Node *next = p->next;
        free(p);
        p = next;
    }
    free(dll);
}

int main(){
	char const *text = "there is literal text here. it might not be the best. but it is here";
	size_t len = strlen(text); // get the length of the text. 	
	
	// construct the doubly linked list 
	Node *head = NULL;
	Node *p = NULL;
	for (int i = 0; i < len; i++) {
		Node *newNode = malloc(sizeof(Node));
		newNode->data = text[i];   // single char
		newNode->prev = p;
		newNode->next = NULL;

		if (p) p->next = newNode;
		else head = newNode;

		p = newNode;
	}
	DoublyLinkedList *doubly =malloc(sizeof(DoublyLinkedList));
	doubly->firstNode = head;
	doubly->lastNode = p;

	forwardMotion(doubly);
	forwardAdder(doubly, '*');
	forwardMotion(doubly);

	// free all the allocated memory at the end of this
	freeList(doubly);

	return EXIT_SUCCESS;
}
