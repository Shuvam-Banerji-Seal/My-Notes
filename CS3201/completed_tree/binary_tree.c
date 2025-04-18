#include "binary_tree.h"
#include "utils.h" // Includes stdio, stdlib, stdbool, node, queue, stack defs
#include <limits.h> // For INT_MIN in findMax
#include <math.h>   // For max function

// --- Helper Function ---
// Simple max function for integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

// --- Practice Set 1 Function Implementations ---

// Problem 1: Manual Insertion
btNode* insertNodeManual(btNode** rootRef, int data, int parentData, char direction) {
    btNode* newNode = createNode(data);
    if (!newNode) {
        fprintf(stderr, "Failed to create new node.\n");
        return *rootRef; // Return original root on failure
    }

    // Case 1: Inserting the root node
    if (parentData == -1) { // Using -1 to signify root insertion
        if (*rootRef != NULL) {
            fprintf(stderr, "Error: Root already exists. Cannot insert %d as root.\n", data);
            free(newNode); // Free the allocated node
            return *rootRef; // Return existing root
        }
        *rootRef = newNode; // Update the root pointer
        printf("Node %d inserted as root.\n", data);
        return *rootRef;
    }

    // Case 2: Inserting a non-root node
    if (*rootRef == NULL) {
         fprintf(stderr, "Error: Tree is empty. Cannot insert %d with parent %d.\n", data, parentData);
         free(newNode);
         return NULL;
    }

    btNode* parentNode = findNode(*rootRef, parentData);
    if (parentNode == NULL) {
        fprintf(stderr, "Error: Parent node %d not found.\n", parentData);
        free(newNode); // Free the allocated node
        return *rootRef; // Return original root
    }

    // Check direction and if the position is free
    if ((direction == 'L' || direction == 'l')) {
        if (parentNode->left == NULL) {
            parentNode->left = newNode;
            printf("Node %d inserted as left child of %d.\n", data, parentData);
        } else {
            fprintf(stderr, "Error: Left child of %d already exists (contains %d).\n", parentData, parentNode->left->data);
            free(newNode); // Free the allocated node
        }
    } else if ((direction == 'R' || direction == 'r')) {
        if (parentNode->right == NULL) {
            parentNode->right = newNode;
             printf("Node %d inserted as right child of %d.\n", data, parentData);
        } else {
            fprintf(stderr, "Error: Right child of %d already exists (contains %d).\n", parentData, parentNode->right->data);
            free(newNode); // Free the allocated node
        }
    } else {
        fprintf(stderr, "Error: Invalid direction '%c'. Use 'L' or 'R'.\n", direction);
        free(newNode); // Free the allocated node
    }

    return *rootRef; // Return the root (might be unchanged)
}


// Problem 2: Display Tree (Helper for indentation)
void displayTreeHelper(btNode *root, int indent) {
    if (root == NULL) {
        return;
    }
    // Print right subtree first for a more intuitive visual layout
    displayTreeHelper(root->right, indent + 4);

    // Print current node with indentation
    for (int i = 0; i < indent; i++) {
        printf(" ");
    }
    printf("%d\n", root->data);

    // Print left subtree
    displayTreeHelper(root->left, indent + 4);
}

// Problem 2: Display Tree (Wrapper)
void displayTree(btNode *root) {
    printf("--- Tree Display ---\n");
    if (root == NULL) {
        printf("(Empty Tree)\n");
        return;
    }
    displayTreeHelper(root, 0);
    printf("--------------------\n");
}


// Problem 3: Non-recursive Inorder Traversal
void inorder_nonrecursive(btNode *root) {
    if (root == NULL) {
        printf("Tree is empty.\n");
        return;
    }

    Stack* s = createStack();
    if (!s) return; // Failed to create stack

    btNode *current = root;

    printf("Inorder (Non-Recursive): ");
    while (current != NULL || !isStackEmpty(s)) {
        // Reach the leftmost node of the current node
        while (current != NULL) {
            push(s, current); // Place pointer to node on stack before traversing left subtree
            current = current->left;
        }

        // Current must be NULL at this point
        current = pop(s); // Pop the top item from stack
        if (current) {
             printf("%d ", current->data); // Print popped item

            // We have visited the node and its left subtree. Now, it's right subtree's turn
            current = current->right;
        }
    }
    printf("\n");
    freeStack(s); // Clean up the stack
}


// Problem 4: Non-recursive Postorder Traversal (Using two stacks)
void postorder_nonrecursive(btNode *root) {
     if (root == NULL) {
        printf("Tree is empty.\n");
        return;
    }

    Stack* s1 = createStack();
    Stack* s2 = createStack(); // Second stack to store the postorder sequence
    if (!s1 || !s2) {
        if(s1) freeStack(s1);
        if(s2) freeStack(s2);
        return;
    }

    // Push root to first stack
    push(s1, root);
    btNode* node;

    // Run while first stack is not empty
    while (!isStackEmpty(s1)) {
        // Pop an item from s1 and push it to s2
        node = pop(s1);
        if (node) {
            push(s2, node);

            // Push left and right children of removed item to s1
            if (node->left)
                push(s1, node->left);
            if (node->right)
                push(s1, node->right);
        }
    }

    // Print all elements of second stack
    printf("Postorder (Non-Recursive): ");
    while (!isStackEmpty(s2)) {
        node = pop(s2);
        if (node) {
            printf("%d ", node->data);
        }
    }
    printf("\n");

    freeStack(s1);
    freeStack(s2);
}


// Problem 5: Find Maximum Value (Recursive)
int findMax(btNode *root) {
    if (root == NULL) {
        return INT_MIN; // Return minimum possible integer if tree is empty
    }

    int res = root->data; // Initialize result with root's data
    int lres = findMax(root->left); // Find max in left subtree
    int rres = findMax(root->right); // Find max in right subtree

    // Compare root's data with max of left and right subtrees
    if (lres > res)
        res = lres;
    if (rres > res)
        res = rres;

    return res;
}


// Problem 6: Check Existence (Recursive)
int isExists(btNode *root, int d) {
    if (root == NULL) {
        return 0; // Data not found in this path
    }
    if (root->data == d) {
        return 1; // Data found
    }
    // Check left subtree OR right subtree
    return isExists(root->left, d) || isExists(root->right, d);
}


// Problem 7: Get Height (Recursive)
int getHeight(btNode *root) {
    if (root == NULL) {
        return -1; // Height of an empty tree is -1
    } else {
        // Compute the height of left and right subtrees
        int lheight = getHeight(root->left);
        int rheight = getHeight(root->right);

        // Use the larger one and add 1 for the current node
        return max(lheight, rheight) + 1;
    }
}


// Problem 8: Get Level of a Node (Util function)
int getLevelUtil(btNode *root, int d, int level) {
    if (root == NULL) {
        return -1; // Node not found in this path
    }
    if (root->data == d) {
        return level; // Node found at the current level
    }

    // Check left subtree
    int downlevel = getLevelUtil(root->left, d, level + 1);
    if (downlevel != -1) {
        return downlevel; // Return level if found in left subtree
    }

    // Check right subtree
    return getLevelUtil(root->right, d, level + 1);
}

// Problem 8: Get Level of a Node (Wrapper)
int getLevel(btNode *root, int d) {
    return getLevelUtil(root, d, 0); // Start search from level 0
}


// Problem 9: Level Order Traversal
void levelorder(btNode *root) {
    if (root == NULL) {
        printf("Tree is empty.\n");
        return;
    }

    Queue* q = createQueue();
    if (!q) return; // Failed to create queue

    enqueue(q, root); // Enqueue root node

    printf("Level Order: ");
    while (!isQueueEmpty(q)) {
        btNode* current = dequeue(q); // Dequeue a node
        if (current) {
            printf("%d ", current->data); // Print its data

            // Enqueue left child if it exists
            if (current->left != NULL) {
                enqueue(q, current->left);
            }
            // Enqueue right child if it exists
            if (current->right != NULL) {
                enqueue(q, current->right);
            }
        }
    }
    printf("\n");
    freeQueue(q); // Clean up the queue
}


// Problem 10: Zigzag Level Order Traversal
void zigzag(btNode *root) {
     if (root == NULL) {
        printf("Tree is empty.\n");
        return;
    }

    // Declare two stacks
    Stack* currentLevel = createStack();
    Stack* nextLevel = createStack();
     if (!currentLevel || !nextLevel) {
        if(currentLevel) freeStack(currentLevel);
        if(nextLevel) freeStack(nextLevel);
        return;
    }


    // Push the root
    push(currentLevel, root);
    bool leftToRight = true; // Flag to indicate traversal direction

    printf("Zigzag Order: ");
    while (!isStackEmpty(currentLevel)) {
        btNode* temp = pop(currentLevel); // Pop node from current level stack

        if (temp) {
            // Print node's data
            printf("%d ", temp->data);

            // Store data according to current order.
            if (leftToRight) {
                // If moving left to right, push left child then right child to next level stack
                if (temp->left)
                    push(nextLevel, temp->left);
                if (temp->right)
                    push(nextLevel, temp->right);
            } else {
                // If moving right to left, push right child then left child to next level stack
                if (temp->right)
                    push(nextLevel, temp->right);
                if (temp->left)
                    push(nextLevel, temp->left);
            }
        }

        // If current level stack is empty, swap stacks and change direction
        if (isStackEmpty(currentLevel)) {
            leftToRight = !leftToRight; // Flip the direction
            Stack* tempStack = currentLevel; // Swap stacks
            currentLevel = nextLevel;
            nextLevel = tempStack;
        }
    }
    printf("\n");
    freeStack(currentLevel);
    freeStack(nextLevel);
}


// Problem 11: Count Leaf Nodes (Recursive)
int getLeafCount(btNode *root) {
    if (root == NULL) {
        return 0; // No leaves in an empty tree
    }
    if (root->left == NULL && root->right == NULL) {
        return 1; // This node is a leaf
    } else {
        // Sum of leaves in left and right subtrees
        return getLeafCount(root->left) + getLeafCount(root->right);
    }
}


// Problem 12: Count Full Nodes (Recursive)
int getFullNodeCount(btNode *root) {
    if (root == NULL) {
        return 0;
    }
    int count = 0;
    // Check if the current node is a full node
    if (root->left != NULL && root->right != NULL) {
        count = 1;
    }
    // Add counts from left and right subtrees
    return count + getFullNodeCount(root->left) + getFullNodeCount(root->right);
}


// Problem 13: Count Half Nodes (Recursive)
int getHalfNodeCount(btNode *root) {
     if (root == NULL) {
        return 0;
    }
    int count = 0;
    // Check if the current node is a half node (exactly one child is NULL)
    if ((root->left != NULL && root->right == NULL) || (root->left == NULL && root->right != NULL)) {
        count = 1;
    }
     // Add counts from left and right subtrees
    return count + getHalfNodeCount(root->left) + getHalfNodeCount(root->right);
}


// Problem 14: Check if Identical (Recursive)
int isIdentical(btNode *root1, btNode *root2) {
    // If both trees are empty, they are identical
    if (root1 == NULL && root2 == NULL) {
        return 1;
    }
    // If one tree is empty and the other is not, they are not identical
    if (root1 == NULL || root2 == NULL) {
        return 0;
    }
    // Check if data matches and recursively check left and right subtrees
    return (root1->data == root2->data) &&
           isIdentical(root1->left, root2->left) &&
           isIdentical(root1->right, root2->right);
}


// Problem 15: Check if Mirror Images (Recursive)
int isMirror(btNode *root1, btNode *root2) {
    // If both trees are empty, they are mirrors
    if (root1 == NULL && root2 == NULL) {
        return 1;
    }
    // If one tree is empty and the other is not, they cannot be mirrors
    if (root1 == NULL || root2 == NULL) {
        return 0;
    }
    // Check if data matches and recursively check mirrored subtrees
    // (left of root1 with right of root2, and right of root1 with left of root2)
    return (root1->data == root2->data) &&
           isMirror(root1->left, root2->right) &&
           isMirror(root1->right, root2->left);
}


// Problem 16: Print Ancestors (Recursive)
/**
 * @brief Recursive helper to find and print ancestors.
 * If target is present in tree rooted with root, then prints the ancestors
 * and returns true, otherwise returns false.
 */
bool printAncestors(btNode *root, int targetData) {
    if (root == NULL) {
        return false; // Base case: target not found here
    }

    // If target is found at the root, we don't print the root itself as an ancestor
    if (root->data == targetData) {
        return true;
    }

    // Check if target is in the left or right subtree
    if (printAncestors(root->left, targetData) || printAncestors(root->right, targetData)) {
        // If target was found in either subtree, the current node is an ancestor
        printf("%d ", root->data);
        return true; // Indicate that an ancestor was printed (or target found downstream)
    }

    // If target was not found in either subtree
    return false;
}


// Problem 17: Get Breadth (Maximum Width) - Using Level Order
int getBreadth(btNode *root) {
    if (root == NULL) {
        return 0; // Width of an empty tree is 0
    }

    Queue* q = createQueue();
    if (!q) return 0; // Error creating queue

    enqueue(q, root);
    int maxWidth = 0;

    while (!isQueueEmpty(q)) {
        // Get the number of nodes at the current level
        int levelWidth = q->count;

        // Update the maximum width found so far
        if (levelWidth > maxWidth) {
            maxWidth = levelWidth;
        }

        // Process (dequeue) all nodes at the current level and enqueue nodes of the next level
        for (int i = 0; i < levelWidth; i++) {
            btNode* current = dequeue(q);
            if (current) { // Should always be true here unless queue logic is flawed
                 if (current->left != NULL) {
                    enqueue(q, current->left);
                }
                if (current->right != NULL) {
                    enqueue(q, current->right);
                }
            }
        }
    }

    freeQueue(q);
    return maxWidth;
}


// Problem 18: Build Complete Binary Tree from Input (Level Order Insertion)
btNode* buildCompleteTreeFromInput() {
    int data;
    btNode *root = NULL;
    Queue* q = createQueue();
     if (!q) return NULL; // Error creating queue

    printf("Enter positive integers to build the tree (0 or negative to stop):\n");

    // Read the root node first
    printf("Enter root value: ");
    scanf("%d", &data);
    if (data <= 0) {
        printf("No nodes entered. Tree is empty.\n");
        freeQueue(q);
        return NULL;
    }

    root = createNode(data);
    if (!root) {
        freeQueue(q);
        return NULL; // Error creating node
    }
    enqueue(q, root);

    // Continue reading values and inserting them level by level
    while (true) {
        btNode* currentParent = dequeue(q);
        if (!currentParent) break; // Should not happen if logic is correct and queue not empty initially

        // Get data for the left child
        printf("Enter left child for %d (<=0 to skip/stop): ", currentParent->data);
        scanf("%d", &data);
        if (data <= 0) {
             enqueue(q, currentParent); // Put parent back if we stop early, might mess up queue order? No, just stop.
             break; // Stop building
        }
        currentParent->left = createNode(data);
        if (currentParent->left) {
            enqueue(q, currentParent->left); // Enqueue the new left child
        } else {
            break; // Stop if node creation fails
        }


        // Get data for the right child
        printf("Enter right child for %d (<=0 to skip/stop): ", currentParent->data);
        scanf("%d", &data);
         if (data <= 0) {
            break; // Stop building
        }
        currentParent->right = createNode(data);
         if (currentParent->right) {
            enqueue(q, currentParent->right); // Enqueue the new right child
         } else {
             break; // Stop if node creation fails
         }
    }

    // Clear remaining items potentially in the queue if stopped early
    // while(!isQueueEmpty(q)) { dequeue(q); } // Not strictly necessary as we just free it

    freeQueue(q);
    printf("Tree building complete.\n");
    return root;
}
