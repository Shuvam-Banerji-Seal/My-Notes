#ifndef BINARY_TREE_H
#define BINARY_TREE_H

#include "utils.h" // Include the basic node definition and utilities

// --- Function Prototypes for Practice Set 1 ---

// Problem 1: Manual Insertion
/**
 * @brief Inserts a new node as a child of a specified parent node.
 *
 * Finds the parent node with `parentData`. If found, creates a new node
 * with `data` and attaches it as the left or right child based on `direction`.
 * Handles the case where the tree is initially empty (if parentData is -1 or similar).
 *
 * @param root Pointer to the root of the tree. Passed by reference to update if root changes.
 * @param data The data for the new node.
 * @param parentData The data of the parent node. Use a special value (e.g., -1) if inserting the root.
 * @param direction 'L' or 'l' for left child, 'R' or 'r' for right child.
 * @return Pointer to the (potentially new) root of the tree. Returns NULL on failure (e.g., parent not found, child position occupied).
 */
btNode* insertNodeManual(btNode** rootRef, int data, int parentData, char direction);

// Problem 2: Display Tree
/**
 * @brief Displays the binary tree structure in a readable format (e.g., indented pre-order).
 * @param root The root of the tree to display.
 * @param indent Indentation level (used internally for recursion).
 */
void displayTreeHelper(btNode *root, int indent);
void displayTree(btNode *root); // Wrapper function

// Problem 3: Non-recursive Inorder Traversal
/**
 * @brief Performs and prints the inorder traversal of the tree non-recursively using a stack.
 * @param root The root of the tree.
 */
void inorder_nonrecursive(btNode *root);

// Problem 4: Non-recursive Postorder Traversal
/**
 * @brief Performs and prints the postorder traversal of the tree non-recursively using two stacks or one stack with flags.
 * @param root The root of the tree.
 */
void postorder_nonrecursive(btNode *root);

// Problem 5: Find Maximum Value
/**
 * @brief Finds the maximum integer value stored in the binary tree.
 * @param root The root of the tree.
 * @return The maximum value found, or INT_MIN (defined in limits.h) if the tree is empty.
 */
int findMax(btNode *root);

// Problem 6: Check Existence
/**
 * @brief Checks if a given data value exists in the tree.
 * @param root The root of the tree.
 * @param d The data value to search for.
 * @return 1 if the value exists, 0 otherwise.
 */
int isExists(btNode *root, int d);

// Problem 7: Get Height
/**
 * @brief Calculates the height of the binary tree.
 * Height of an empty tree is -1, height of a tree with one node is 0.
 * @param root The root of the tree.
 * @return The height of the tree.
 */
int getHeight(btNode *root);

// Problem 8: Get Level of a Node
/**
 * @brief Finds the level of a node containing the given data.
 * Level of the root is 0.
 * @param root The root of the tree.
 * @param d The data value of the node whose level is to be found.
 * @param level The current level (used internally for recursion, start with 0).
 * @return The level of the node if found, -1 otherwise.
 */
int getLevelUtil(btNode *root, int d, int level);
int getLevel(btNode *root, int d); // Wrapper function

// Problem 9: Level Order Traversal
/**
 * @brief Performs and prints the level order (breadth-first) traversal of the tree using a queue.
 * @param root The root of the tree.
 */
void levelorder(btNode *root);

// Problem 10: Zigzag Level Order Traversal
/**
 * @brief Performs and prints the level order traversal in a zigzag pattern (left-to-right, then right-to-left, etc.).
 * @param root The root of the tree.
 */
void zigzag(btNode *root);

// Problem 11: Count Leaf Nodes
/**
 * @brief Counts the number of leaf nodes (nodes with no children) in the tree.
 * @param root The root of the tree.
 * @return The total count of leaf nodes.
 */
int getLeafCount(btNode *root);

// Problem 12: Count Full Nodes
/**
 * @brief Counts the number of full nodes (nodes with both left and right children) in the tree.
 * @param root The root of the tree.
 * @return The total count of full nodes.
 */
int getFullNodeCount(btNode *root);

// Problem 13: Count Half Nodes
/**
 * @brief Counts the number of half nodes (nodes with exactly one child) in the tree.
 * @param root The root of the tree.
 * @return The total count of half nodes.
 */
int getHalfNodeCount(btNode *root);

// Problem 14: Check if Identical
/**
 * @brief Checks if two binary trees are structurally identical and have the same node values.
 * @param root1 The root of the first tree.
 * @param root2 The root of the second tree.
 * @return 1 if the trees are identical, 0 otherwise.
 */
int isIdentical(btNode *root1, btNode *root2);

// Problem 15: Check if Mirror Images
/**
 * @brief Checks if two binary trees are mirror images of each other.
 * @param root1 The root of the first tree.
 * @param root2 The root of the second tree.
 * @return 1 if the trees are mirror images, 0 otherwise.
 */
int isMirror(btNode *root1, btNode *root2);

// Problem 16: Print Ancestors
/**
 * @brief Prints all ancestors of a node with the given data value.
 * @param root The root of the tree.
 * @param targetData The data value of the node whose ancestors are to be printed.
 * @return True if the target node was found (and ancestors printed), false otherwise.
 */
bool printAncestors(btNode *root, int targetData);

// Problem 17: Get Breadth (Maximum Width)
/**
 * @brief Calculates the maximum width (maximum number of nodes at any level) of the tree.
 * @param root The root of the tree.
 * @return The maximum width of the tree.
 */
int getBreadth(btNode *root);

// Problem 18: Build Complete Binary Tree from Input (Simplified: using level order insertion)
/**
 * @brief Builds a complete binary tree by inserting nodes level by level.
 * This is a simplified interpretation for creating a tree structure from sequential input.
 * Stops when 0 or negative input is given.
 * @return Pointer to the root of the constructed complete binary tree.
 */
btNode* buildCompleteTreeFromInput();


#endif // BINARY_TREE_H
