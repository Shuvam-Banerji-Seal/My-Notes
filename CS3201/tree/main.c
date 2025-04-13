
// The fundamental libs
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// The User created libs

#include "utils.h"
#include "binary_tree.h"
#include "binary_search_tree.h"

//// Function prototypes:
void displayMainMenu();
void displayPracticeSet1Menu();
void displayPracticeSet2Menu();

btNode* createRandomTree(int n);
btNode* createTreeFromUser();
btNode* createHardcodedTree();

///////////////////////////////////////////
int main()
{
  btnode *root = NULL;
}

//////////////////////////////////////
void displayPracticeSet1Menu()
{
  printf("\n--- Practice Set 01: Binary Tree Practice Problems ---\n");
  printf(" 1. Insertion done Manually (Problem 01)\n");
  printf(" 2. Display Tree Properly (Problem 02)\n");
  printf(" 3. InOrder Traversal (Non-Recursive) (Problem 03)\n");
  printf(" 4. PostOrder Traversal (Non-Recursive) (Problem 04)\n");
  printf(" 5. Find the Maximum Value from the Binary Tree\n");
  printf(" 6. Check if the Value Exists\n");
  printf(" 7. Get the Tree Height\n");
  printf(" 8. Get the Given Node's Depth/Level\n");
  printf(" 9. Level Order Traversalsal\n");
  printf(" 10. ZigZag Order Traversal\n");
  printf(" 11. Get the Leaf Node Counts\n");
  printf(" 12. Get the Full Node Counts\n");
  printf(" 13. Get the Half Node Counts\n");
  printf(" 14. Check if the two trees are identical\n");
  printf(" 15. Check if the Trees are Enantiomers\n");
  printf(" 16. Print the ancestors of a node\n");
  printf(" 17. Get the breadth of a tree\n");
  printf(" 18. Build A Complete Binary Tree from User Input\n")
}

///////////////////////////////////////////////
///
void displayMainMenu()
{
  printf("\n====== Main Menu ======\n");
  printf("1. Create Random Tree\n");
  printf("2. Create Tree from User Input (Manual Insertion)\n");
  printf("3. Use the HardCoded Example tree\n");
  printf("4. Display Current Trees\n");
  printf("5. Practice Set 01\n");
  printf("6. Practice Set 02\n");
  printf("0. Exit\n");
}
