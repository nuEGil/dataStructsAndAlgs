#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<ctype.h>
#include<stdint.h>
#define MAX_TRACK 512

typedef struct {
    bool live;
    int x;
    int y;
    int* track;        // dynamic array of visited nodes
    int trackSize;     // how many entries currently used
    int trackCapacity; // allocated length
} Ant;

typedef struct {
    // Immutable list of points (store as array of coordinates)
    // Example: x and y as separate arrays or a Point struct
    int pointCount;
    int* pointX;
    int* pointY;

    // Pheromone matrix Tau[i][j]
    double** Tau;

    // Desirability matrix Eta[i][j]
    double** Eta;

    // Scalar parameters
    double Rho;    // evaporation
    double Alpha;  // pheromone weight
    double Beta;   // desirability weight
    double Q;      // pheromone deposit amount

} World;

Ant* createAnt(int capacity) {
    Ant* a = malloc(sizeof(Ant));
    a->live = false;
    a->x = 0;
    a->y = 0;

    a->track = malloc(sizeof(int) * capacity);
    a->trackSize = 0;
    a->trackCapacity = capacity;

    return a;
}

void destroyAnt(Ant* a) {
    free(a->track);
    free(a);
}

World* createWorld(int n, double rho, double alpha, double beta, double q) {
    World* w = malloc(sizeof(World));
    w->pointCount = n;
    w->points = malloc(sizeof(Point) * n);

    w->Tau = malloc(n * sizeof(double*));
    w->Eta = malloc(n * sizeof(double*));
    for (int i = 0; i < n; i++) {
        w->Tau[i] = calloc(n, sizeof(double));
        w->Eta[i] = calloc(n, sizeof(double));
    }

    w->Rho = rho;
    w->Alpha = alpha;
    w->Beta = beta;
    w->Q = q;
    return w;
}

void destroyWorld(World* w) {
    if (!w) return;

    // Free Tau and Eta matrices row-by-row
    for (int i = 0; i < w->pointCount; i++) {
        free(w->Tau[i]);
        free(w->Eta[i]);
    }

    // Free the arrays of row pointers
    free(w->Tau);
    free(w->Eta);

    // Free the points array
    free(w->points);

    // Finally free the struct itself
    free(w);
}

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