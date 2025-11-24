#include<stdlib.h>
#include<stdio.h>
#include<string.h>

typedef struct Node{
	char data; // could be a pointer to data by the way
	struct Node *next;
	struct Node *prev; 
} Node;

int main(){
	char const *text = "there is literal text here. it might not be the best. but it is here";
	size_t len = strlen(text); // get the length of the text. 	
	
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
	
	return EXIT_SUCCESS;
}
