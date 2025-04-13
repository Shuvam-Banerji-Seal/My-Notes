#include "utils.h"


#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/*
 * This is for creating a node
 */
btNode * createNode(int data){
    btNode *newNode = (btNode *)malloc(sizeof(btNode));
    if (newNode == NULL) {
        perror("Failed to allocate memory for new node");
        return NULL;
    }
    newNode->data = data;
    newNode->left = newNode->right = NULL;
    return newNode;
}


btNode *findNode(btNode *root, int data)
{
  if (root==NULL)
  {
    return  NULL; //Base case: empty tree or node is not found inside the tree
  }
  if (root->data== data)
  {
    return root;
  }

  btNode *foundNode = findNode(root->left, data);
  if (foundNode!=NULL)
  {
    return foundNode; // Node is found in the left subtree
  }


  return findNode(btNode->right, data);
}


void freeTree(btNode *root)
{
  if (root==NULL)
  {
    return; 
  }
  freeTree(root->left);
  freeTree(root->right);
  free(root);

}

Queue *createQueue() {
    Queue *q = (Queue *)malloc(sizeof(Queue));
    if (q == NULL) {
        perror("Failed to allocate memory for queue");
        return NULL;
    }
    q->front = 0;
    q->rear = -1;
    q->count = 0;
    return q;
}
bool isQueueEmpty(Queue *q) {
    return (q->count == 0);
}
bool isQueueFull(Queue *q) {
    return (q->count == MAX_QUEUE_SIZE);
}
btNode *enqueue(Queue *q, btNode *node) {
    if (isQueueFull(q)) {
        fprintf(stderr, "Queue is full. Cannot enqueue.\n");
        return NULL;
    }
    q->rear = (q->rear + 1) % MAX_QUEUE_SIZE;
    q->items[q->rear] = node;
    q->count++;
    return node;
}


btNode *dequeue(Queue *q) {
    if (isQueueEmpty(q)) {
        fprintf(stderr, "Queue is empty. Cannot dequeue.\n");
        return NULL;
    }
    btNode *node = q->items[q->front];
    q->front = (q->front + 1) % MAX_QUEUE_SIZE;
    q->count--;
    return node;
}
void freeQueue(Queue *q) {
    if (q != NULL) {
        free(q);
    }
}


Stack *createStack()
{
  Stack *s = (Stack *)malloc(sizeof(Stack));
  if (!s)
  {
    perror("Failed to allocate memory to the Stack \n");
    return  NULL;
  }

  s->top=-1;
  return s;
}



bool isStackEmpty(Stack *s) {
    return (s->top == -1);
}
bool isStackFull(Stack *s) {
    return (q->top == MAX_STACK_SIZE-1);
}


bool push(Stack *s, btNode* node)
{
  if(isStackFull(s))
  {
    fprintf(stderr, "Error!!! StackOverflow\n");
    return false;

  }
  s->top++;
  s->items[s->top] = node;
  return true;

}

btNode *pop(Stack *s)
{
  if (isStackEmpty(s))
  {
    perror("\n Error!!! Stack Underflow\n");
    return  NULL;
  }
  btNode *item = s->items[s->top];
  s->top--;
  return item;
}


btNode *peek(Stack *s)
{
  if (isStackEmpty(s))
  {
    printf("\n What the heck is there to peek?\n")
    return NULL;
  }
  return s->items[s->top];
}

void freeStack(Stack *s)
{
  if (s!=NULL)
  {
    free (s);
  }
}
