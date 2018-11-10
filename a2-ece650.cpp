#include<stdio.h>
#include <stdlib.h>
#include<iostream>

#ifndef INFINITE
#define INFINITE 999999999
#endif

typedef struct _SpNode
{
	int d;
	int predecessor;
} SpNode;

typedef struct _Node
{
	int d;
	struct _Node* next;
} Node;

typedef struct _NodeList
{
	Node* head;
} NodeList;

typedef struct _Graph
{
	int V;
	NodeList* array;
} Graph;

Graph* initGraph(int V)
{
	Graph* graph = (Graph*) malloc(sizeof(Graph));
	graph->V = V;
	if( V == 0)
	{
		graph->array = NULL;
		return graph;
	}
	graph->array = (NodeList*) malloc(V*sizeof(NodeList));
	int i;
	for(i = 0; i < V; i++) {
		graph->array[i].head = NULL;
	}
	return graph;
}

void destroyGraph(Graph** graph)
{
	if (*graph == NULL)
		return;
	int i;
	for(i = 0; i < (*graph)->V; i++)
	{
		Node* head = (*graph)->array[i].head;
		while(head != NULL)
		{
			Node* next = head->next;
			free(head);
			head = next;
		}
	}
	free((*graph)->array);
	free(*graph);
	*graph = NULL;
}

int addEdge(Graph* graph, int src, int dest)
{
	if(src >= graph->V || dest >= graph->V || src<0 || dest<0)
	{
		std::cout<<"Error: Unexisted Vertex in edge<"<<src<<","<<dest<<">\n";
		return 0;
	}
	if (src == dest)
		return 1;

	Node* newNode = (Node*) malloc(sizeof(Node));
	newNode->d = dest;
	newNode->next = graph->array[src].head;
	graph->array[src].head = newNode;


	newNode = (Node*) malloc(sizeof(Node));
	newNode->d = src;
	newNode->next = graph->array[dest].head;
	graph->array[dest].head = newNode;
	return 1;
}

SpNode* initSingleSource(int V, int src)
{
	int v;

	SpNode* spArray = (SpNode*) malloc(V * sizeof(SpNode));
	for (v = 0; v < V; v++) {

		spArray[v].d = INFINITE;
		spArray[v].predecessor = -1;
	}
	spArray[src].d = 0;

	return spArray;
}


void relax(int uIndex, SpNode* u, SpNode* v)
{
	if(v->d > (u->d + 1)){
		v->d = u->d + 1;
		v->predecessor = uIndex;
	}
}

SpNode* bellmanFord(Graph* graph, int src)
{
	SpNode* spArray = initSingleSource(graph->V, src);
	int i;
	int v;

	for(i = 0; i < graph->V; i++) {

		for(v = 0; v < graph->V; v++) {
			Node* pCrawl = graph->array[v].head;
			while(pCrawl) {
				relax(v, &spArray[v], &spArray[pCrawl->d]);
				pCrawl = pCrawl->next;
			}
		}
	}
	return spArray;
}

void printSPath(SpNode* spArray ,int src, int dest)
{
	if(spArray[dest].predecessor == -1)
	{
		std::cout<<src;
		return;
	}
	printSPath(spArray, src, spArray[dest].predecessor);
	std::cout<<"-"<<dest;
}

void printSpathWrapper( Graph* graph, int src, int dest)
{
	if (src >= graph->V || dest >= graph->V || src < 0 || dest < 0)
	{
		std::cout<<"Error: specified not existed Vertex in \'s\' command.\n";
		return;
	}

	if(src == dest)
	{
		std::cout<<src<<"\n";
		return;
	}
	SpNode* spArray = bellmanFord(graph, src);

	if(spArray[dest].d == INFINITE)
		std::cout<<"Error: Path not existed between"<<src<<" and "<<dest<<"\n";
	else
	{
		printSPath(spArray, src, dest);
		std::cout<<"\n";
	}
	free(spArray);
}

int main(int argc, char const *argv[])
{
	Graph *graph = NULL;
	SpNode *spArray = NULL;
	int scanResult;

	while(1)
	{
		char command;
		int V;
		int leftN;
		int rightN;
		scanResult = scanf(" %c", &command);
		if (scanResult == EOF)
			break;
		if (scanResult < 1)
		{
			std::cout<<"Error:Unexpected input while waiting next command.\n";
			continue;
		}
		if (command == 'V' || command == 'v')
		{
			std::cin>>V;
			if( V < 0)
			{
				std::cout<<"Error: invalid number of Vertex.\n";
				continue;
			}
			if(graph != NULL)
				destroyGraph(&graph);
			graph = initGraph(V);


			scanResult = scanf( " E {");
			while(1)
			{
				scanResult = scanf("<%d,%d>,", &leftN, &rightN);
				if (scanResult < 2)
					break;
				if (!addEdge(graph, leftN, rightN))
					break;
			}
			scanResult = scanf("}");
		} else if( command == 's' || command == 'S')
		{
			int src, dest;
			scanResult = scanf(" %d %d", &src, &dest);
			if (graph == NULL) {
				std::cout<<"Error: please input V,E before input s.\n";
				continue;
			}
			if (scanResult == 2)
				printSpathWrapper(graph, src, dest);

		}
	}
	return 0;
}
