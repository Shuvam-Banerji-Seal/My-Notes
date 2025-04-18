#ifndef BINARY_SEARCH_TREE_H
#define BINARY_SEARCH_TREE_H

#include "utils.h" // Includes node definition, utilities
#include <limits.h> // For INT_MIN, INT_MAX

// --- Function Prototypes for Practice Set 2 ---

// Standard BST Insert (Helper function, not explicitly asked but useful for testing)
/**
 * @brief Inserts a value into a Binary Search Tree.
 * Maintains the BST property. Does not insert duplicates.
 * @param root The root of the BST.
 * @param data The value to insert.
 * @return The root of the modified BST.
 */
btNode* insertBST(btNode* root, int data);

// Problem 1: Check if Binary Tree is a BST
/**
 * @brief Utility function to check if a tree is a BST.
 * @param node Current node being checked.
 * @param min Lower bound for the node's data.
 * @param max Upper bound for the node's data.
 * @return True if the subtree rooted at 'node' is a BST within the given bounds, false otherwise.
 */
bool isBSTUtil(btNode* node, int min, int max);
/**
 * @brief Checks if a given binary tree is a Binary Search Tree (BST).
 * @param root The root of the binary tree.
 * @return 1 if the tree is a BST, 0 otherwise.
 */
int isBST(btNode* root);

// Problem 2: Get Elements in Range [k1, k2]
/**
 * @brief Prints all elements in the BST T that fall within the range [k1, k2].
 * @param root The root of the BST.
 * @param k1 The lower bound of the range (inclusive).
 * @param k2 The upper bound of the range (inclusive).
 */
void printRange(btNode* root, int k1, int k2);

// Problem 3: Check if Two BSTs Contain Same Information
/**
 * @brief Stores the inorder traversal of a BST into an array.
 * @param root The root of the BST.
 * @param arr The array to store the traversal.
 * @param index Pointer to the current index in the array.
 */
void storeInorder(btNode* root, int arr[], int* index);
/**
 * @brief Counts the number of nodes in a tree.
 * @param root The root of the tree.
 * @return The number of nodes.
 */
int countNodes(btNode* root);
/**
 * @brief Checks if two BSTs contain the same set of values (structure can differ).
 * @param root1 The root of the first BST.
 * @param root2 The root of the second BST.
 * @return 1 if they contain the same information, 0 otherwise.
 */
int haveSameInfo(btNode* root1, btNode* root2);

// Problem 4: Check if Height Balanced
/**
 * @brief Utility function to check balance and calculate height simultaneously.
 * @param root The root of the tree/subtree.
 * @param isBalanced Pointer to a boolean flag, set to false if unbalance is detected.
 * @return The height of the subtree rooted at 'root'.
 */
int checkBalanceAndHeight(btNode* root, bool* isBalanced);
/**
 * @brief Checks if a binary tree is height-balanced.
 * (Difference between heights of left and right subtrees <= 1 for all nodes).
 * @param root The root of the binary tree.
 * @return 1 if the tree is height-balanced, 0 otherwise.
 */
int isHeightBalanced(btNode* root);

// Problem 5: Remove Elements Outside Range [a, b]
/**
 * @brief Removes nodes from a BST whose values are outside the range [a, b].
 * Modifies the existing tree.
 * @param root The root of the BST. Passed by reference if root might change.
 * @param a The lower bound of the valid range (inclusive).
 * @param b The upper bound of the valid range (inclusive).
 * @return The root of the modified BST.
 */
btNode* removeOutsideRange(btNode* root, int a, int b);

// Problem 6: Create Sum Tree
/**
 * @brief Calculates the sum of all node values in a tree.
 * @param root The root of the tree.
 * @return The sum of all values.
 */
int sumTreeValues(btNode* root);
/**
 * @brief Creates a new tree where each node's value is the sum of the original node's value
 * and the values in its original left and right subtrees.
 * @param root The root of the original binary tree.
 * @return The root of the new "sum tree".
 */
btNode* createSumTree(btNode* root);

// Problem 7: Convert Binary Tree to BST
/**
 * @brief Helper function to build a balanced BST from a sorted array.
 * @param arr The sorted array of values.
 * @param start The starting index in the array.
 * @param end The ending index in the array.
 * @return The root of the constructed balanced BST.
 */
btNode* sortedArrayToBST(int arr[], int start, int end);
/**
 * @brief Converts a given Binary Tree into a Binary Search Tree.
 * Preserves the original set of values.
 * @param root The root of the original Binary Tree.
 * @return The root of the new Binary Search Tree.
 */
btNode* convertBTtoBST(btNode* root);

// Problem 8: Convert BST to Sorted Doubly Linked List (DLL)
/**
 * @brief Converts a BST into a sorted Doubly Linked List in-place.
 * Uses the left pointer as 'prev' and right pointer as 'next'.
 * @param root The root of the BST.
 * @param headRef Pointer to the head of the DLL (used for recursion).
 * @param prevRef Pointer to the previously visited node in inorder traversal (used for linking).
 */
void convertBSTtoDLLUtil(btNode* root, btNode** headRef, btNode** prevRef);
/**
 * @brief Wrapper function to convert BST to sorted DLL.
 * @param root The root of the BST.
 * @return Pointer to the head of the created Doubly Linked List.
 */
btNode* convertBSTtoDLL(btNode* root);
/**
 * @brief Prints the data in a Doubly Linked List created from a BST.
 * @param head The head of the DLL.
 */
void printDLL(btNode* head);


// Problem 9: Sum of Values in BST
/**
 * @brief Calculates the sum of all values in a BST (same as sumTreeValues, but specific context).
 * @param root The root of the BST.
 * @return The sum of all node values.
 */
int sumBSTValues(btNode* root); // Can reuse sumTreeValues

// Problem 10: Modify BST based on value m
/**
 * @brief Modifies the BST: increments values <= m by 5, decrements values > m by 5.
 * @param root The root of the BST.
 * @param m The threshold value.
 */
void modifyBST(btNode* root, int m);

// Problem 11: Find m-th Largest Element in BST
/**
 * @brief Finds the m-th largest element in a BST using reverse inorder traversal.
 * @param root The root of the BST.
 * @param m The rank (e.g., 1 for largest, 2 for second largest).
 * @param count Pointer to a counter tracking visited nodes in reverse inorder.
 * @param result Pointer to store the m-th largest value.
 */
void findMthLargestUtil(btNode* root, int m, int* count, int* result);
/**
 * @brief Wrapper function to find the m-th largest element.
 * @param root The root of the BST.
 * @param m The rank (m >= 1).
 * @return The value of the m-th largest element, or INT_MIN if not found or m is invalid.
 */
int findMthLargest(btNode* root, int m);


// Problem 12: BST based on Word Length and Frequency (Requires different node structure)
// Define a structure specific to this problem
typedef struct freqNode {
    int length;
    int freq;
    struct freqNode *left;
    struct freqNode *right;
} freqNode;

/**
 * @brief Creates a new frequency node.
 * @param length Word length.
 * @return Pointer to the new node.
 */
freqNode* createFreqNode(int length);

/**
 * @brief Inserts a word length into the frequency BST.
 * If length exists, increments frequency; otherwise, adds a new node.
 * @param root The root of the frequency BST.
 * @param length The length of the word to insert/count.
 * @return The root of the modified frequency BST.
 */
freqNode* insertFreqBST(freqNode* root, int length);

/**
 * @brief Displays the frequency BST (inorder).
 * @param root The root of the frequency BST.
 */
void displayFreqBST(freqNode* root);

/**
 * @brief Frees the memory allocated for the frequency BST.
 * @param root The root of the frequency BST.
 */
void freeFreqTree(freqNode* root);

/**
 * @brief Builds a frequency BST from word lengths read from a file.
 * NOTE: This requires a file named "input_words.txt" in the same directory,
 * containing words separated by whitespace.
 * @return The root of the constructed frequency BST.
 */
freqNode* buildFreqBSTFromFile(const char* filename);


#endif // BINARY_SEARCH_TREE_H
