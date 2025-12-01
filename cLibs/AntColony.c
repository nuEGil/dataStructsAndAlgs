#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<ctype.h>
#include<stdint.h>

typedef struct World{
    int [] positions; // list of positions N
    int [][] DistanceMatrix; // precomputed distance matrix
    int [][] VisitationCounts; // use to compute pheremone updates
} World;

typedef struct Ant{
    bool live; // use as an ant exit condition
    int x;
    int y;
    // you can make this a dynamic length array 
    // and have the ant end if the next posible node is head, or if the array size limit is met
    int sites []; // dynamic array
} Ant;


/*
GenerateSites()
    generate a variable length array called sites [N][2] 
    that is the list of points to be visited. should sort it.
    return sites -- but I can use the index of the sites; 

Construct Graph()
    Pointer Juggle to create a graph.

GenerateAnts()
    return a list of Ant objects

ComputeProbability(GraphNode *graphNode, Ant *ant)
    compute eta --> can be stored
    compute probability of a move

UpdateAntPosition()
    exactly what it sounds like, update x,y, and append to the track node... 

StepAnts()
    itterate through live ants
        ComputeProbability()
        UpdateAntPosition();

FreeGraph()
FreeAnts()
FreeVisitedSites()

*/

int main(){



    return EXIT_SUCCESS;
}