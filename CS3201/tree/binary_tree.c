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

    return NULL;
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



//Problem: 08
int getLevelUtil(btNode *, int d, int level)
{
  if (root==NULL)
  {
    return -1;
  }
  if (root->data == d)
  {
    return level;
  }

  //check the left subtree 
  int downlevel = getLevelUtil(root->left, d, level + 1);
  if (downlevel != -1)
  {
    return downlevel;
  }
  return getLevelUtil(root->right, d, level + 1);

}

// A wrapper because of the question needs
int getLevel(btNode * root, int d)
{
  return getLevelUtil(root, d, 0);
}

// Probelem: 09
// This is the left biased level ordering
void levelorder (btNode *root)
{
  if (root == NULL)
  {
    printf("\n The Tree is empty\n");
    return  ;
  }

  Queue *q = createQueue();
  if (!q) return  ;

  enqueue (q,root);
  printf("\n Level Order:\n");

  while (!isQueueEmpty(q))
  {
    btNode * current = dequeue(q);
    if (current)
    {
      printf("%d\t", current->data);

      if (current->left != NULL)
      {
        enqueue(q, current->left);
      }

      if (current->right != NULL)
      {
        enqueue(q, current->right);
      }
    }
  }

  printf(" \n");
  freeQueue(q);


}




// Problem 10
//

void zigzag(btNode *root)
{
  if (root == NULL)
  {
    printf("\n Tree is empty\n")
      return  ;
  }

  Stack *currentLevel = createStack();
  Stack *nextLevel = createStack();

  if (!currentLevel !! !nextLevel)
  {
    if (currentLevel) freeStack(currentLevel);
    if (nextLevel) freeStack(nextLevel);
    return  ;

  }

  push(currentLevel, root);
  bool left_to_right = true;
  printf("\n zigzag order: \n");
  while (!isStackEmpty(currentLevel))
  {
    btNode *temp = pop(currentLevel);
    
    if (temp)
    {
      printf("%d\t", temp->data);

      // Suppose we are now moving from left to right
      if (left_to_right)
      {
        if (temp->left)
          push(nextLevel, temp->left);
            // printf("%s\n")
          
        if (temp->right)
          push(nextLevel, temp->right);
      } else {
        if (temp->right)
          push(nextLevel, temp->right);
        if (temp->left)
          push(nextLevel, temp->left);
      }
    }
    // if teh current level stack is empty, I need to change the direction and what if I just swap the stacks
    if (isStackEmpty(currentLevel))
    {
      left_to_right = !left_to_right;
      Stack *tempStack = currentLevel;
      currentLevel = nextLevel;
      nextLevel = tempStack;
    }
  }
  printf("\n");
  freeStack(currentLevel);
  freeStack(nextLevel);

}

// problem: 11
//
int getLeafCount(btNode *root)
{
  if (root == NULL)
  {
    return 0;
  }
  if (root->left == NULL && root->right == NULL)
  {
    return 1;
  }else {
    return getLeafCount(root->left) + getLeafCount(root->right);
  }
}

//problem : 12

int getFullNodeCount(btNode *root)
{
  if (root == NULL)
  {
    return 0;
  }
  int count = 0;
  if (root->left != NULL && root->right != NULL)
  {
    count = 1;
  }else {
    return count + getFullNodeCount(root->left) + getFullNodeCount(root->right);
  }
}




// problem 13
int getHalfNodeCount(btNode *root)
{
  if (root == NULL)
  {
    return 0;
  }
  int count = 0;
  if ((root->left != NULL && root->right == NULL) || (root->left == NULL && root->right != NULL))
  {
    count = 1;
  }else {
    return count + getHalfNodeCount(root->left) + getHalfNodeCount(root->right);
  }
}

// probelem : 14
int isIdentical(btNode *root1, btNode *root2)
{
  if (root1==NULL && root2 == NULL)
    return 1;

  if (root2 == NULL || root1 == NULL)
    return 0;

  return (root1->data == root2->data) && isIdentical(root1->left, root2->left) && isIdentical(root1->right, root2->right);
}



// probelem : 15
int isMirror(btNode *root1, btNode *root2)
{
  if (root1==NULL && root2 == NULL)
    return 1;

  if (root2 == NULL || root1 == NULL)
    return 0;

  return (root1->data == root2->data) && isMirror(root1->left, root2->right) && isIdentical(root1->right, root2->left);
}



//Problem : 16

bool printAncestors(btNode *root, int targetData)
{
  if (root == NULL)
  {
    return false;
  }
  if (root->data == targetData)
    return true;

  if (printAncestors(root->left, targetData) || printAncestors(root->right, targetData))
  {
    printf("%d\t", root->data);
    return true;
  }

  return false;
}

// Problem : 17
//
int getBreadth (btNode *root)
{
  if (root == NULL)
  {
    return 0;
  }

  Queue *q = createQueue();
  if (!q) return 0;

  enqueue(q, root);
  int max_width = 0;

  while (!isQueueEmpty(q))
  {
    int levelWidth = q->count;
    if (levelWidth > max_width)
    {
      max_width = levelWidth;
    }
    // deq all the nodes at the current level and enq nodes of the next level
    for (int i = 0; i< levelWidth; i++)
    {
      btNode *current = dequeue(q);
      if (current)
      {
        if (current->left != NULL)
          enqueue(q, current->left);
        
        if (current->right!=NULL)
            enqueue (q, current->right);
      }
    }
  
  }

  freeQueue(q);
  return max_width;
}


// Problem : 18
// Level Ordering INput``

btNode *buildCompleteTreeFromInput()
{
  int data, r;
  btNode *root = NULL;
  Queue *q = createQueue();
    if (!q) return NULL;
  printf("\n Enter the data as positive integers to build the binary tree (if you enter 0 or negative numbers then the building process will stop):\n");
  printf("\n Enter the Root: \n");
  // r = scanf("%d", &data);
  // if (r!= 1)
    // return NULL;
  scanf("%d", &data);
  if (data<=0)
  {
    printf("\n No Nodes were entered. Tree is Empty\n");
    freeQueue (q);
    return NULL;
  }
  root = createNode(data);
  if (!root)
  {
    freeQueue(q);
    return NULL;
  }
  enqueue(q, root);
  while(true)
  {
    btNode *currentParent = dequeue(q);
    if (!currentParent) break;

    printf("\n Enter the left Child for the Node (%d) (NOTE: <=0 skip this node)\n", currentParent->data);
    scanf("%d", &data);
    if (data<=0)
    {
      enqueue(q, currentParent);
      break;
    }
    currentParent->left = createNode(data);
    if (currentParent->left)
    {
      enqueue(q, currentParent->left);
    }else {
      break;
    }
    printf("\n Enter the right child for the Node (%d) (NOTE: <= 0 skips this node)\n");
    scanf("%d", &data);
    if (data<=0)
    {
      break;
    }
    currentParent->right = createNode(data);
    if (currentParent->right)
    {
      enqueue(q, currentParent->right);

    }else {
      break;
    }
  }
  freeQueue(q);
  printf("\n The Tree Building is Complete\n");
  retturn root;
}
