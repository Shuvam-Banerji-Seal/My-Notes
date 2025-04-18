#include "utils.h"
#include <stdio.h>
#include <stdlib.h>

// --- Node Utility Implementation ---

/**
 * @brief Creates a new binary tree node.
 */
btNode* createNode(int data) {
    // Allocate memory for the new node
    btNode* newNode = (btNode*)malloc(sizeof(btNode));
    if (newNode == NULL) {
        perror("Memory allocation failed for new node");
        return NULL; // Return NULL if allocation fails
    }
    // Initialize the node's data and children pointers
    newNode->data = data;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode; // Return the pointer to the new node
}

/**
 * @brief Finds a node with the given data value in the tree (recursive pre-order search).
 */
btNode* findNode(btNode* root, int data) {
    if (root == NULL) {
        return NULL; // Base case: empty tree or node not found in this path
    }
    if (root->data == data) {
        return root; // Node found
    }
    // Recursively search in the left subtree
    btNode* foundNode = findNode(root->left, data);
    if (foundNode != NULL) {
        return foundNode; // Node found in the left subtree
    }
    // If not found in left, search in the right subtree
    return findNode(root->right, data);
}

/**
 * @brief Frees the memory allocated for the entire tree (post-order traversal).
 */
void freeTree(btNode* root) {
    if (root == NULL) {
        return; // Base case: empty tree
    }
    // Recursively free left and right subtrees
    freeTree(root->left);
    freeTree(root->right);
    // Free the current node
    // printf("Freeing node: %d\n", root->data); // Optional: for debugging
    free(root);
}


// --- Queue Implementation ---

/**
 * @brief Creates and initializes an empty queue.
 */
Queue* createQueue() {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    if (!q) {
        perror("Failed to allocate memory for queue");
        return NULL;
    }
    q->front = 0;
    q->rear = -1; // Initialize rear to -1
    q->count = 0;
    return q;
}

/**
 * @brief Checks if the queue is empty.
 */
bool isQueueEmpty(Queue* q) {
    return q->count == 0;
}

/**
 * @brief Checks if the queue is full.
 */
bool isQueueFull(Queue* q) {
    return q->count == MAX_QUEUE_SIZE;
}

/**
 * @brief Adds a node pointer to the rear of the queue.
 */
bool enqueue(Queue* q, btNode* node) {
    if (isQueueFull(q)) {
        fprintf(stderr, "Error: Queue is full.\n");
        return false; // Cannot enqueue if full
    }
    // Calculate the next rear position with wrap-around
    q->rear = (q->rear + 1) % MAX_QUEUE_SIZE;
    q->items[q->rear] = node;
    q->count++;
    return true;
}

/**
 * @brief Removes and returns the node pointer from the front of the queue.
 */
btNode* dequeue(Queue* q) {
    if (isQueueEmpty(q)) {
        // fprintf(stderr, "Warning: Queue is empty.\n"); // Can be noisy
        return NULL; // Cannot dequeue if empty
    }
    // Get the item from the front
    btNode* item = q->items[q->front];
    // Move front forward with wrap-around
    q->front = (q->front + 1) % MAX_QUEUE_SIZE;
    q->count--;
    return item;
}

/**
 * @brief Frees the memory allocated for the queue structure.
 */
void freeQueue(Queue* q) {
    if (q != NULL) {
        free(q);
    }
}


// --- Stack Implementation ---

/**
 * @brief Creates and initializes an empty stack.
 */
Stack* createStack() {
    Stack* s = (Stack*)malloc(sizeof(Stack));
     if (!s) {
        perror("Failed to allocate memory for stack");
        return NULL;
    }
    s->top = -1; // Initialize top to -1 (empty stack)
    return s;
}

/**
 * @brief Checks if the stack is empty.
 */
bool isStackEmpty(Stack* s) {
    return s->top == -1;
}

/**
 * @brief Checks if the stack is full.
 */
bool isStackFull(Stack* s) {
    return s->top == MAX_STACK_SIZE - 1;
}

/**
 * @brief Pushes a node pointer onto the top of the stack.
 */
bool push(Stack* s, btNode* node) {
    if (isStackFull(s)) {
        fprintf(stderr, "Error: Stack overflow.\n");
        return false; // Cannot push if full
    }
    s->top++; // Increment top
    s->items[s->top] = node; // Add the item
    return true;
}

/**
 * @brief Pops and returns the node pointer from the top of the stack.
 */
btNode* pop(Stack* s) {
    if (isStackEmpty(s)) {
        // fprintf(stderr, "Warning: Stack underflow.\n"); // Can be noisy
        return NULL; // Cannot pop if empty
    }
    // Get the item from the top and decrement top
    btNode* item = s->items[s->top];
    s->top--;
    return item;
}

/**
 * @brief Returns the node pointer from the top of the stack without removing it.
 */
btNode* peek(Stack* s) {
     if (isStackEmpty(s)) {
        return NULL; // Return NULL if empty
    }
    return s->items[s->top]; // Return the top item
}


/**
 * @brief Frees the memory allocated for the stack structure.
 */
void freeStack(Stack* s) {
    if (s != NULL) {
        free(s);
    }
}
