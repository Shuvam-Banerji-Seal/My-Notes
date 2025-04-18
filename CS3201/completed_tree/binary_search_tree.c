#include "binary_search_tree.h"
#include "utils.h"      // Includes node, queue, stack, stdio, stdlib, stdbool
#include <limits.h>     // For INT_MIN, INT_MAX
#include <string.h>     // For strcmp in Problem 3 comparison, strlen in Problem 12
#include <ctype.h>      // For isspace in Problem 12 file reading

// --- Helper Function ---
// Simple max function (if not already defined or included elsewhere)
#ifndef max
#define max(a, b) ((a) > (b) ? (a) : (b))
#endif
// Simple min function
#ifndef min
#define min(a, b) ((a) < (b) ? (a) : (b))
#endif
// Comparison function for qsort (used in Problem 3 and 7)
int compareInts(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}


// --- Standard BST Insert (Helper) ---
btNode* insertBST(btNode* root, int data) {
    // Base case: If the tree is empty, return a new node
    if (root == NULL) {
        return createNode(data);
    }

    // Otherwise, recur down the tree
    if (data < root->data) {
        root->left = insertBST(root->left, data);
    } else if (data > root->data) {
        root->right = insertBST(root->right, data);
    }
    // Note: If data == root->data, we do nothing (don't insert duplicates)

    // return the (unchanged) node pointer
    return root;
}


// --- Practice Set 2 Function Implementations ---

// Problem 1: Check if Binary Tree is a BST (Utility)
bool isBSTUtil(btNode* node, int min_val, int max_val) {
    // Base case: An empty tree is a BST
    if (node == NULL) {
        return true;
    }

    // Check the current node's value against the allowed range
    if (node->data <= min_val || node->data >= max_val) {
        return false;
    }

    // Recursively check the left and right subtrees
    // Left subtree: max value becomes current node's data
    // Right subtree: min value becomes current node's data
    return isBSTUtil(node->left, min_val, node->data) &&
           isBSTUtil(node->right, node->data, max_val);
}

// Problem 1: Check if Binary Tree is a BST (Wrapper)
int isBST(btNode* root) {
    // Use INT_MIN and INT_MAX as initial bounds
    // Note: If tree nodes can actually hold INT_MIN/INT_MAX, need a different approach
    //       (e.g., passing pointers to previous node in inorder traversal).
    //       Assuming standard integer ranges for typical problems.
    return isBSTUtil(root, INT_MIN, INT_MAX);
}


// Problem 2: Get Elements in Range [k1, k2] (Inorder Traversal)
void printRange(btNode* root, int k1, int k2) {
    if (root == NULL) {
        return;
    }

    // If root's data is greater than k1, recursively call for left subtree
    if (root->data > k1) {
        printRange(root->left, k1, k2);
    }

    // If root's data is within the range [k1, k2], print it
    if (root->data >= k1 && root->data <= k2) {
        printf("%d ", root->data);
    }

    // If root's data is smaller than k2, recursively call for right subtree
    if (root->data < k2) {
        printRange(root->right, k1, k2);
    }
}


// Problem 3: Check if Two BSTs Contain Same Information
// Helper: Store Inorder Traversal
void storeInorder(btNode* root, int arr[], int* index) {
    if (root == NULL) {
        return;
    }
    storeInorder(root->left, arr, index);
    arr[*index] = root->data;
    (*index)++;
    storeInorder(root->right, arr, index);
}

// Helper: Count Nodes
int countNodes(btNode* root) {
    if (root == NULL) {
        return 0;
    }
    return 1 + countNodes(root->left) + countNodes(root->right);
}

// Problem 3: Main function
int haveSameInfo(btNode* root1, btNode* root2) {
    int n1 = countNodes(root1);
    int n2 = countNodes(root2);

    // If node counts are different, they cannot have the same info
    if (n1 != n2) {
        return 0;
    }
    if (n1 == 0) {
        return 1; // Both are empty, same info
    }

    // Allocate arrays to store inorder traversals
    int* arr1 = (int*)malloc(n1 * sizeof(int));
    int* arr2 = (int*)malloc(n2 * sizeof(int));
    if (!arr1 || !arr2) {
        fprintf(stderr, "Memory allocation failed in haveSameInfo.\n");
        if (arr1) free(arr1);
        if (arr2) free(arr2);
        return 0; // Indicate error or difference
    }

    // Store inorder traversals
    int index1 = 0, index2 = 0;
    storeInorder(root1, arr1, &index1);
    storeInorder(root2, arr2, &index2);

    // Inorder traversal of a BST is sorted.
    // If they have the same info, their inorder traversals must be identical.
    int result = 1; // Assume they are the same initially
    for (int i = 0; i < n1; i++) {
        if (arr1[i] != arr2[i]) {
            result = 0; // Found a difference
            break;
        }
    }

    // Free allocated memory
    free(arr1);
    free(arr2);

    return result;
}


// Problem 4: Check if Height Balanced (Utility)
int checkBalanceAndHeight(btNode* root, bool* isBalanced) {
    if (root == NULL) {
        return -1; // Height of empty tree
    }
    if (!(*isBalanced)) {
        return -1; // If already unbalanced somewhere below, stop early
    }

    int leftHeight = checkBalanceAndHeight(root->left, isBalanced);
    // Check if left subtree became unbalanced during the recursive call
    if (!(*isBalanced)) {
        return -1;
    }

    int rightHeight = checkBalanceAndHeight(root->right, isBalanced);
     // Check if right subtree became unbalanced during the recursive call
    if (!(*isBalanced)) {
        return -1;
    }


    // Check balance at the current node
    if (abs(leftHeight - rightHeight) > 1) {
        *isBalanced = false; // Set the flag to unbalanced
        return -1; // Return value doesn't matter now
    }

    // If balanced at this node, return its height
    return max(leftHeight, rightHeight) + 1;
}

// Problem 4: Check if Height Balanced (Wrapper)
int isHeightBalanced(btNode* root) {
    bool isBalanced = true; // Start assuming it's balanced
    checkBalanceAndHeight(root, &isBalanced); // Function modifies isBalanced if needed
    return isBalanced ? 1 : 0;
}


// Problem 5: Remove Elements Outside Range [a, b]
btNode* removeOutsideRange(btNode* root, int a, int b) {
    // Base case
    if (root == NULL) {
        return NULL;
    }

    // Recursively fix the left and right subtrees
    root->left = removeOutsideRange(root->left, a, b);
    root->right = removeOutsideRange(root->right, a, b);

    // Now consider the current node 'root'

    // Case 1: root->data < a (Root value is too small)
    // The entire left subtree must also be too small.
    // The correct tree structure must come from the right subtree.
    if (root->data < a) {
        btNode* rightChild = root->right;
        free(root); // Delete the current node
        return rightChild; // Return the right child as the new root of this subtree
    }

    // Case 2: root->data > b (Root value is too large)
    // The entire right subtree must also be too large.
    // The correct tree structure must come from the left subtree.
    if (root->data > b) {
        btNode* leftChild = root->left;
        free(root); // Delete the current node
        return leftChild; // Return the left child as the new root of this subtree
    }

    // Case 3: root->data is within the range [a, b]
    // Keep the root node and return it.
    return root;
}


// Problem 6: Create Sum Tree (Helper: Sum of values)
int sumTreeValues(btNode* root) {
    if (root == NULL) {
        return 0;
    }
    return root->data + sumTreeValues(root->left) + sumTreeValues(root->right);
}

// Problem 6: Create Sum Tree (Main logic)
btNode* createSumTree(btNode* root) {
    if (root == NULL) {
        return NULL;
    }

    // Create a new node for the sum tree with the calculated sum
    int sum = root->data + sumTreeValues(root->left) + sumTreeValues(root->right);
    btNode* sumNode = createNode(sum);
    if(!sumNode) return NULL; // Allocation failed

    // Recursively create the left and right subtrees for the sum tree
    sumNode->left = createSumTree(root->left);
    sumNode->right = createSumTree(root->right);

    return sumNode;
}


// Problem 7: Convert Binary Tree to BST
// Helper: Build Balanced BST from Sorted Array
btNode* sortedArrayToBST(int arr[], int start, int end) {
    // Base case
    if (start > end) {
        return NULL;
    }

    // Get the middle element and make it root
    int mid = start + (end - start) / 2;
    btNode* root = createNode(arr[mid]);
    if (!root) return NULL; // Allocation failed

    // Recursively construct the left and right subtrees
    root->left = sortedArrayToBST(arr, start, mid - 1);
    root->right = sortedArrayToBST(arr, mid + 1, end);

    return root;
}

// Problem 7: Convert Binary Tree to BST (Main logic)
btNode* convertBTtoBST(btNode* root) {
    if (root == NULL) {
        return NULL;
    }

    // 1. Count nodes
    int n = countNodes(root);
    if (n == 0) return NULL;

    // 2. Store Inorder traversal of the BT in an array
    int* arr = (int*)malloc(n * sizeof(int));
     if (!arr) {
        fprintf(stderr, "Memory allocation failed in convertBTtoBST.\n");
        return NULL;
    }
    int index = 0;
    storeInorder(root, arr, &index); // Note: Inorder of BT is not necessarily sorted

    // 3. Sort the array
    qsort(arr, n, sizeof(int), compareInts);

    // 4. Build a balanced BST from the sorted array
    btNode* bstRoot = sortedArrayToBST(arr, 0, n - 1);

    // 5. Free the temporary array
    free(arr);

    return bstRoot;
}


// Problem 8: Convert BST to Sorted Doubly Linked List (DLL) - Utility
void convertBSTtoDLLUtil(btNode* root, btNode** headRef, btNode** prevRef) {
    if (root == NULL) {
        return;
    }

    // Recursively convert the left subtree
    convertBSTtoDLLUtil(root->left, headRef, prevRef);

    // Process the current node (during inorder traversal)
    if (*prevRef == NULL) {
        // This is the first node visited (leftmost), so it's the head of the DLL
        *headRef = root;
    } else {
        // Link the previous node (in inorder) to the current node
        (*prevRef)->right = root; // right pointer acts as 'next'
        root->left = *prevRef;   // left pointer acts as 'prev'
    }
    // Update the previous node reference to the current node
    *prevRef = root;

    // Recursively convert the right subtree
    convertBSTtoDLLUtil(root->right, headRef, prevRef);
}

// Problem 8: Convert BST to Sorted Doubly Linked List (DLL) - Wrapper
btNode* convertBSTtoDLL(btNode* root) {
    btNode* head = NULL; // Head of the DLL
    btNode* prev = NULL; // Previously visited node
    convertBSTtoDLLUtil(root, &head, &prev);
    return head; // Return the head of the created list
}

// Problem 8: Print DLL (Helper for verification)
void printDLL(btNode* head) {
     if (head == NULL) {
        printf("DLL is empty.\n");
        return;
    }
    printf("DLL (Forward): ");
    btNode* current = head;
    btNode* tail = NULL; // Keep track of the tail for backward printing
    while (current != NULL) {
        printf("%d ", current->data);
        tail = current; // Update tail
        current = current->right; // Move using the 'next' pointer (right)
    }
    printf("\n");

    // Optional: Print backward from tail using 'prev' pointer (left)
    /*
    printf("DLL (Backward): ");
    current = tail;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->left; // Move using the 'prev' pointer (left)
    }
    printf("\n");
    */
}


// Problem 9: Sum of Values in BST
int sumBSTValues(btNode* root) {
    // Can simply reuse the function from Problem 6
    return sumTreeValues(root);
}


// Problem 10: Modify BST based on value m
void modifyBST(btNode* root, int m) {
    if (root == NULL) {
        return;
    }

    // Modify the current node's data based on m
    if (root->data <= m) {
        root->data += 5;
    } else {
        root->data -= 5;
    }

    // Recursively modify left and right subtrees
    modifyBST(root->left, m);
    modifyBST(root->right, m);
}


// Problem 11: Find m-th Largest Element in BST (Utility - Reverse Inorder)
void findMthLargestUtil(btNode* root, int m, int* count, int* result) {
    if (root == NULL || *count >= m) {
        return; // Stop if tree ends or m-th largest is already found
    }

    // 1. Traverse the right subtree first (larger elements)
    findMthLargestUtil(root->right, m, count, result);

    // 2. Process the current node if m-th largest not found yet
    if (*count < m) {
        (*count)++; // Increment count for the current node
        // If this node is the m-th largest, store its value
        if (*count == m) {
            *result = root->data;
            return; // Found it, no need to proceed further
        }
    }

     // 3. Traverse the left subtree if m-th largest not found yet
    if (*count < m) {
        findMthLargestUtil(root->left, m, count, result);
    }
}

// Problem 11: Find m-th Largest Element in BST (Wrapper)
int findMthLargest(btNode* root, int m) {
    if (m <= 0) {
        fprintf(stderr, "Error: m must be positive for m-th largest.\n");
        return INT_MIN; // Indicate error
    }
    int count = 0;      // Counter for nodes visited in reverse inorder
    int result = INT_MIN; // Variable to store the result
    findMthLargestUtil(root, m, &count, &result);

    if (result == INT_MIN && count < m) {
         fprintf(stderr, "Error: Tree has fewer than %d nodes.\n", m);
    }

    return result;
}


// Problem 12: BST based on Word Length and Frequency

// Create a frequency node
freqNode* createFreqNode(int length) {
    freqNode* newNode = (freqNode*)malloc(sizeof(freqNode));
    if (!newNode) {
        perror("Memory allocation failed for freq node");
        return NULL;
    }
    newNode->length = length;
    newNode->freq = 1; // Initialize frequency to 1
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

// Insert into frequency BST
freqNode* insertFreqBST(freqNode* root, int length) {
    if (root == NULL) {
        return createFreqNode(length);
    }

    if (length < root->length) {
        root->left = insertFreqBST(root->left, length);
    } else if (length > root->length) {
        root->right = insertFreqBST(root->right, length);
    } else {
        // Length already exists, increment frequency
        root->freq++;
    }
    return root;
}

// Display frequency BST (Inorder: shows length and frequency sorted by length)
void displayFreqBST(freqNode* root) {
    if (root != NULL) {
        displayFreqBST(root->left);
        printf("Length: %d, Frequency: %d\n", root->length, root->freq);
        displayFreqBST(root->right);
    }
}

// Free frequency BST (Postorder)
void freeFreqTree(freqNode* root) {
     if (root == NULL) {
        return;
    }
    freeFreqTree(root->left);
    freeFreqTree(root->right);
    free(root);
}


// Build frequency BST from file
freqNode* buildFreqBSTFromFile(const char* filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        fprintf(stderr, "Please ensure '%s' exists in the current directory.\n", filename);
        return NULL;
    }

    freqNode* root = NULL;
    char word[100]; // Assume max word length

    // Read words from the file
    while (fscanf(file, "%99s", word) == 1) {
        int len = strlen(word);
        if (len > 0) {
            root = insertFreqBST(root, len);
        }
    }

    fclose(file);
    printf("Frequency BST built from '%s'.\n", filename);
    return root;
}
