#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h> // For boolean types

// --- Basic Binary Tree Node Structure ---
// Defines a node in the binary tree.
// Each node holds an integer data value and pointers to its left and right children.
typedef struct btNode {
    int data;
    struct btNode *left;
    struct btNode *right;
} btNode;

// --- Function Prototypes ---

/**
 * @brief Creates a new binary tree node.
 *
 * Allocates memory for a new node, initializes its data,
 * and sets its left and right children to NULL.
 *
 * @param data The integer value to store in the node.
 * @return A pointer to the newly created node, or NULL if memory allocation fails.
 */
btNode* createNode(int data);

/**
 * @brief Finds a node with the given data value in the tree.
 *
 * Performs a recursive search (pre-order traversal) to find the first node
 * containing the specified data.
 *
 * @param root The root of the tree (or subtree) to search within.
 * @param data The data value to search for.
 * @return A pointer to the found node, or NULL if the data is not found.
 */
btNode* findNode(btNode* root, int data);

/**
 * @brief Frees the memory allocated for the entire tree.
 *
 * Performs a post-order traversal to recursively delete all nodes
 * starting from the root.
 *
 * @param root A pointer to the root of the tree to be deleted.
 */
void freeTree(btNode* root);


// --- Queue Structure (for Level Order Traversal, Breadth, etc.) ---
// Simple queue implementation using an array for storing node pointers.

#define MAX_QUEUE_SIZE 100 // Define a maximum size for the queue

typedef struct Queue {
    btNode* items[MAX_QUEUE_SIZE];
    int front;
    int rear;
    int count; // Number of items currently in the queue
} Queue;

/**
 * @brief Creates and initializes an empty queue.
 * @return A pointer to the newly created queue.
 */
Queue* createQueue();

/**
 * @brief Checks if the queue is empty.
 * @param q Pointer to the queue.
 * @return True if the queue is empty, false otherwise.
 */
bool isQueueEmpty(Queue* q);

/**
 * @brief Checks if the queue is full.
 * @param q Pointer to the queue.
 * @return True if the queue is full, false otherwise.
 */
bool isQueueFull(Queue* q);

/**
 * @brief Adds a node pointer to the rear of the queue.
 * @param q Pointer to the queue.
 * @param node Pointer to the btNode to add.
 * @return True if enqueue was successful, false if the queue was full.
 */
bool enqueue(Queue* q, btNode* node);

/**
 * @brief Removes and returns the node pointer from the front of the queue.
 * @param q Pointer to the queue.
 * @return Pointer to the btNode removed from the front, or NULL if the queue was empty.
 */
btNode* dequeue(Queue* q);

/**
 * @brief Frees the memory allocated for the queue structure.
 * @param q Pointer to the queue to be freed.
 */
void freeQueue(Queue* q);


// --- Stack Structure (for Non-Recursive Traversals) ---
// Simple stack implementation using an array for storing node pointers.

#define MAX_STACK_SIZE 100 // Define a maximum size for the stack

typedef struct Stack {
    btNode* items[MAX_STACK_SIZE];
    int top; // Index of the top element
} Stack;

/**
 * @brief Creates and initializes an empty stack.
 * @return A pointer to the newly created stack.
 */
Stack* createStack();

/**
 * @brief Checks if the stack is empty.
 * @param s Pointer to the stack.
 * @return True if the stack is empty, false otherwise.
 */
bool isStackEmpty(Stack* s);

/**
 * @brief Checks if the stack is full.
 * @param s Pointer to the stack.
 * @return True if the stack is full, false otherwise.
 */
bool isStackFull(Stack* s);

/**
 * @brief Pushes a node pointer onto the top of the stack.
 * @param s Pointer to the stack.
 * @param node Pointer to the btNode to push.
 * @return True if push was successful, false if the stack was full.
 */
bool push(Stack* s, btNode* node);

/**
 * @brief Pops and returns the node pointer from the top of the stack.
 * @param s Pointer to the stack.
 * @return Pointer to the btNode popped from the top, or NULL if the stack was empty.
 */
btNode* pop(Stack* s);

/**
 * @brief Returns the node pointer from the top of the stack without removing it.
 * @param s Pointer to the stack.
 * @return Pointer to the btNode at the top, or NULL if the stack was empty.
 */
btNode* peek(Stack* s);

/**
 * @brief Frees the memory allocated for the stack structure.
 * @param s Pointer to the stack to be freed.
 */
void freeStack(Stack* s);


#endif // UTILS_H
