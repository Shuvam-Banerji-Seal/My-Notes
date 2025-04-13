#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


typedef struct btNode{
  int data;
  struct btNode *left;
  struct btNode *right;

} btNode;


btNode * createNode(int data); //done
btNode *findNode(btNode *root, int data);

void freeTree(btNode *root);


///Queue Structure
///
#define MAX_QUEUE_SIZE 100

typedef struct Queue {
  btNode *items[MAX_QUEUE_SIZE];
  int front;
  int rear;
  int count;
  int count; //Number of item currently in the Queue
}Queue;

Queue *createQueue();
bool isQueueEmpty(Queue *q);
bool isQueueFull(Queue *q);
btNode *enqueue(Queue *q, btNode * node);
btNode *dequeue(Queue *q);
void freeQueue(Queue *q);

#define MAX_STACK_SIZE 100

typedef struct Stack {
  btNode *items[MAX_STACK_SIZE];
  int top;
  // int count;
}Stack;

Stack *createStack();
bool isStackEmpty(Stack *s);
bool isStackFull(Stack *s);
bool push(Stack *s, btNode * node);
btNode *pop(Stack *s);
btNode *peek(Stack *s);
void freeStack(Stack *s);


#endif // !UTILS_H
