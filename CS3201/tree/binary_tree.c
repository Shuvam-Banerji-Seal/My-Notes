#include "binary_tree.h"
#include "utils.h"
#include <math.h>
#include <limits.h>

int max(int a, int b)
{
  return (a>b)? a:b;
}


// Problem 01
btNode *insertNodeManual(btNode ** rootRef, int data, int parentData, char direction)
{
  btNode *newNode = createNode(data);
  if (!newNode)
  {
    fprintf(stderr, "\n Failed to create a new node\n");
    return *rootRef; //returning the root itself
  }
  //Case 01: When it is the beginning of the universe
  if (parentData == -1)
  {
    if (*rootRef != NULL)
    {
      fprintf(stderr, "\n Root Already exists\n");
      free(newNode);
      return  *rootRef;
    }
    *rootRef=newNode;
    printf("\n Node %d is inserted as ROOT\n", data);
  }

  //Case 02: Inserting as NON-ROOT
  if (*rootRef == NULL)
  {
    fprintf(stderr, "\n Tree is empty\n");
    free(newNode);
    return  NULL;
  }
  
  btNode *parentNode = findNode(*rootRef, parentData);

  if (parentNode == NULL)
  {
    fprintf(stderr, "\n Parent doesn't exist or NOT FOund\n");
    free(newNode);

    /////////////////////////////////////////
    ///Remember this place might give that possibly reachable memory blocks and I want to test it if the following line makes any difference
    // free(parentNode);

    retrun NULL;
  }

  if ((direction=='L'||direction=='l'))
  {
    if (parentNode->left == NULL)
    {
      parentNode-> newNode;
      printf("\n Node %d is inserted successfully as the left child of %d\n", data, parentData);
    }
    else 
  {
      fprintf(stderr, "\n Left Child already exits\n");
      free(newNode);
    }

  }

  else if((direction=='R'||direction=='r')){
      if (parentNode->right == NULL)
      {
        parentNode->right = newNode;
        printf("\n Node %d is inserted successfully as the right child of %d\n", data, parentNode);
      }
    else {
      fprintf(stderr, "\n Right child already exists\n");
      free(newNode);
    }
    }
    else{
      fprintf(stderr, "\n Are you stupid??? Use 'L' or 'R' for left and right\n");
      free(newNode);
    }

  return *rootRef;
  // free(parentNode); // This is not needed as the parentNode is not dynamically allocated

}


//Problem 02
void displayTree(btNode *root)
{
  printf("\n ----- TREE DISPLAY -----\n");
  if (root==NULL)
  {
    printf("\n Empty TRee\n");
    return ;
  }
  displayTreeHelper(root, 0);
  printf("\n -------------------------------------\n");
}


void displayTreeHelper(btNode *root, int indent)
{
  if (root==NULL)
  {
    return;
  }
  displayTreeHelper(root->right, indent + 4);

  for (int i =0; i <indent; i++)
  {
    printf(" ");
  }
  printf("%d\n", root->data);

  displayTreeHelper(root->left, indent + 4);
}

//Problem 03
void inorder_nonrecursive(btNode *root)
{
  if (root==NULL)
  {
    printf("\n Tree is Empty\n");
    return;
  }

  Stack *s = createStack();
  if (!s) return;

  // LDR
  //
  btNode *current = root;
  printf("\n inorder_nonrecursive\n");
  while (current!= NULL || !isStackEmpty(s))
  { 
    while (current!=NULL)
    {
      push(s, current);
      current= current->left;
    }
  
  // Current must be at the NULL of the left most leaf
  current = pop (s);
  if (current)
  {
    printf("%d\t", current->dat);
    current = current->right;
  }
  }

  printf("\n");

  freeStack(s);
}



// Problem: 04
void postorder_nonrecursive(btNode *root)
{
  if (root==NULL)
  {
    printf("\n Tree is Empty\n");
    return;
  }
  //LRD
  Stack *s1 = createStack();
  Stack *s2 = createStack();

  if (!s1 || !s2)
  {
    if (s1) freeStack(s1);
    if (s2) freeStack (s2);
    return  ;
  }

  push(s1, root);
  btNode *current;
  //
  printf("\n POST order_nonrecursive\n");
  while (!isStackEmpty(s1))
  {
    current = pop(s1);
    if (current)
    {
      push(s2, current);
      if (current->left)
        push(s1, current->left);
      if (current->right)
        push(s1, current->right);
    }
  }

  while (!isStackEmpty(s2)) {
    current = pop (s2);
    if (current)
    {
      printf("%d\t", current->data);
    }
  }

  printf("\n");

  freeStack(s1);
  freeStack(s2);

}



//Problem : 05

int findMax(btNode *root)
{
  if (root == NULL)
  {
    return INT_MIN; 
  }

  int res = root->data;
  int left_res = findMax(root->left);
  int right_res = findMax(root->right);


  if (left_res >res)
    res = left_res;
  if (right_res > res)
    res = right_res;

  return res;
}



// Problem: 06
//
int isExists(btNode *root, int d)
{
  if (root==NULL)
  {
    return 0;
  }
  if (root->data== d)
  {
    return 1;
  }
  return isExists(root->left,d ) || isExists(root->right, d);
}

//Problem: 07
 
int getHeight(btNode *root)
{
  if (root == NULL)
    return -1;
  else {
    int left_height = getHeight(root->left);
    int right_height = getHeight(root->right);
    return max(left_height, right_height) + 1;
  }
}
