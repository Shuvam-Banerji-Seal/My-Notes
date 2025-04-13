#ifndef BINARY_TREE_H
#define BINARY_TREE_H

//Problem : 01
//

btNode *insertNodeManual(btNode ** rootRef, int data, int parentData, char direction);
// rootref  pointer to the root of the tree. Passed by ref just to update if the root changes 




//Problem 02: 
void displayTreeHelper(btNode *root, int indent);
void displayTree(btNode *root);




//Problem 03: 
void inorder_nonrecursive(btNode *root);


//Problem 04: 

void postorder_nonrecursive(btNode *root);

//Problem 05: 

int findMax(btNode *root);


//Problem 06: 
int isExists(btNode *root, int d);
//Problem 07:
int getHeight(btNode *root);

//Problem 08: 
int getLevel(btNode *root, int d);//wrapper function for me
int getLevelUtil(btNode *root, int d, int level);
// Might change the logic later

//Problem 09: 
void levelorder(btNode *root);

//Problem 10:

void zigzag(btNode *root);

//Problem 11:
//
int getLeafCount(btNode *root);

//Problem 12:
//
int getFullNodeCount(btNode *root);

//Problem 13:
//
int getHalfNodeCount(btNode *root);

//Problem 14:
//
int isIdentical (btNode *root1, btNode *root2);
//Problem 15: 
int isMirror(btNode *root1, btNode root2);
//Problem 16:
bool printAncestors(btNode *root, int d);
//Problem 17:
int getBreadth(btNode *root);
//Problem 18:
//
btNode *buildCompleteTreeFromInput();
//Problem 09: 



#endif // !BINARY_TREE_H

