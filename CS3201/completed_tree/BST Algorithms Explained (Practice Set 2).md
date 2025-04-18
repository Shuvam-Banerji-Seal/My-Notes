  
0\. Standard BST Insert (insertBST)

* Problem: (Helper function) Insert a value into a BST while maintaining the BST property (left child \< parent \< right child) and avoiding duplicates.  
* Function: btNode\* insertBST(btNode\* root, int data)  
* Logic:  
  1. Base Case: If the current root is NULL, it means we've found the correct position to insert. Create a new node with the data and return it.  
  2. Recursive Step:  
     * If data is less than root-\>data, the new node belongs in the left subtree. Recursively call insertBST on the left child (root-\>left \= insertBST(root-\>left, data)). The assignment updates the left child pointer in case the left subtree was initially NULL.  
     * If data is greater than root-\>data, it belongs in the right subtree. Recursively call insertBST on the right child (root-\>right \= insertBST(root-\>right, data)).  
     * If data is equal to root-\>data, do nothing (duplicates are not inserted).  
  3. Return: Return the original root pointer (it might have been modified if a child was added).  
* Example: Insert 15 into BST {20, 10, 30}.  
  * insertBST(root=20, data=15): 15 \< 20, call insertBST(root=10, data=15).  
  * insertBST(root=10, data=15): 15 \> 10, call insertBST(root=NULL, data=15).  
  * insertBST(root=NULL, data=15): Base case, create node 15, return it.  
  * Node 10's right child becomes the new node 15\. Return node 10\.  
  * Node 20's left child remains node 10\. Return node 20\. Final tree: {20, {10, NULL, 15}, 30}.

1\. Check if Binary Tree is a BST (isBST)

* Problem: Given a *binary tree*, determine if it satisfies the properties of a BST.  
* Functions: int isBST(btNode\* root), bool isBSTUtil(btNode\* node, int min\_val, int max\_val)  
* Logic: The core idea is that for any node in a BST, all nodes in its left subtree must be *less than* the node's value, and all nodes in its right subtree must be *greater than* the node's value. This property must hold recursively for all nodes.  
  1. isBSTUtil (Recursive Helper): This function checks if the subtree rooted at node is a valid BST *within a given range* (min\_val, max\_val).  
     * Base Case: An empty tree (node \== NULL) is a valid BST. Return true.  
     * Check Current Node: If node-\>data is NOT strictly greater than min\_val OR NOT strictly less than max\_val, it violates the BST property within the allowed range. Return false.  
     * Recursive Check:  
       * Recursively check the left subtree. The left child's maximum allowed value becomes the current node-\>data. The minimum remains min\_val. (isBSTUtil(node-\>left, min\_val, node-\>data))  
       * Recursively check the right subtree. The right child's minimum allowed value becomes the current node-\>data. The maximum remains max\_val. (isBSTUtil(node-\>right, node-\>data, max\_val))  
       * Return true only if *both* recursive calls return true.  
  2. isBST (Wrapper): Calls isBSTUtil starting at the root, with the initial range set to the minimum and maximum possible integer values (INT\_MIN, INT\_MAX) to allow any valid integer at the root.  
* Example: Tree {10, 5, 20, \#, \#, 15, \#} (where \# is NULL)  
  * isBST(root=10) calls isBSTUtil(10, INT\_MIN, INT\_MAX).  
  * isBSTUtil(10, INT\_MIN, INT\_MAX): 10 is in range. Check left: isBSTUtil(5, INT\_MIN, 10). Check right: isBSTUtil(20, 10, INT\_MAX).  
  * isBSTUtil(5, INT\_MIN, 10): 5 is in range. Left/Right are NULL (true). Returns true.  
  * isBSTUtil(20, 10, INT\_MAX): 20 is in range. Check left: isBSTUtil(15, 10, 20). Check right: isBSTUtil(NULL, 20, INT\_MAX).  
  * isBSTUtil(15, 10, 20): 15 is in range. Left/Right are NULL (true). Returns true.  
  * isBSTUtil(NULL, 20, INT\_MAX): Base case, returns true.  
  * Since all checks return true, the tree is a BST.

2\. Get Elements in Range \[k1, k2\] (printRange)

* Problem: Given a BST and a range \[k1, k2\], print all elements within that range (inclusive).  
* Function: void printRange(btNode\* root, int k1, int k2)  
* Logic: This uses a modified inorder traversal, leveraging the BST property to prune unnecessary branches.  
  1. Base Case: If root is NULL, do nothing and return.  
  2. Check Left: If the current root-\>data is greater than k1, it's possible that nodes in the left subtree could be within the range \[k1, k2\]. Recursively call printRange on the left child. (If root-\>data \<= k1, the entire left subtree must also be \<= k1, so we don't need to explore it).  
  3. Check Current: If the current root-\>data is within the range \[k1, k2\] (i.e., root-\>data \>= k1 && root-\>data \<= k2), print root-\>data.  
  4. Check Right: If the current root-\>data is less than k2, it's possible that nodes in the right subtree could be within the range \[k1, k2\]. Recursively call printRange on the right child. (If root-\>data \>= k2, the entire right subtree must also be \>= k2, so we don't need to explore it).  
* Example: Tree {20, 10, 30, 5, 15}, Range \[12, 25\].  
  * printRange(20, 12, 25): 20 \> 12 (Check left). 20 is in range (Print 20). 20 \< 25 (Check right).  
  * printRange(10, 12, 25): 10 is not \> 12 (Skip left). 10 is not in range. 10 \< 25 (Check right).  
  * printRange(15, 12, 25): 15 \> 12 (Check left \- NULL). 15 is in range (Print 15). 15 \< 25 (Check right \- NULL). Returns.  
  * Back to node 10's right call. Returns.  
  * Back to node 20's right call: printRange(30, 12, 25).  
  * printRange(30, 12, 25): 30 \> 12 (Check left \- NULL). 30 is not in range. 30 is not \< 25 (Skip right). Returns.  
  * Output: 20 15 (or 15 20 depending on exact print order relative to recursive calls \- the code prints 15 20 because it checks left, then prints current, then checks right).

3\. Check if Two BSTs Contain Same Information (haveSameInfo)

* Problem: Given two BSTs (which might have different structures), check if they contain the exact same set of values.  
* Functions: int haveSameInfo(btNode\* root1, btNode\* root2), void storeInorder(btNode\* root, int arr\[\], int\* index), int countNodes(btNode\* root)  
* Logic: The key property is that the inorder traversal of any BST yields its elements in sorted order. Therefore, two BSTs contain the same set of elements if and only if their inorder traversals are identical.  
  1. Count Nodes: First, count the number of nodes in both trees using countNodes (a simple recursive function: 1 \+ count(left) \+ count(right)). If the counts differ, they cannot contain the same information. Return 0\. If both counts are 0 (empty trees), return 1\.  
  2. Store Inorder: Allocate two arrays, one for each tree, of size equal to the node count. Use the storeInorder function (standard recursive inorder traversal) to fill each array with the elements of the respective tree.  
  3. Compare Arrays: Iterate through the two arrays. Since the inorder traversals of BSTs are sorted, if the trees contain the same elements, the arrays should be identical element by element. If any mismatch is found (arr1\[i\] \!= arr2\[i\]), return 0\.  
  4. Return: If the loop completes without finding any mismatch, the trees contain the same information. Return 1\. Remember to free the allocated arrays.  
* Example:  
  * T1: {10, 5, 15} \-\> Inorder: \[5, 10, 15\]  
  * T2: {15, 10, \#, 5} \-\> Inorder: \[5, 10, 15\]  
  * Counts are equal (3). Arrays are identical. Returns 1\.

4\. Check if Height Balanced (isHeightBalanced)

* Problem: Determine if a binary tree is height-balanced (for every node, the height difference between its left and right subtrees is at most 1).  
* Functions: int isHeightBalanced(btNode\* root), int checkBalanceAndHeight(btNode\* root, bool\* isBalanced)  
* Logic: A naive approach would calculate the height of left and right subtrees for every node, which is inefficient (O(n^2)). The implemented approach calculates height and checks balance simultaneously in a single traversal (O(n)).  
  1. checkBalanceAndHeight (Recursive Helper):  
     * Base Case: If root is NULL, its height is \-1 (by convention for balance calculation). Return \-1.  
     * Early Exit: If the isBalanced flag has already been set to false by a deeper recursive call, stop processing and return \-1 (or any value, as the result is already determined).  
     * Recursive Calls: Recursively call checkBalanceAndHeight for the left and right children. This obtains their heights and updates the isBalanced flag if unbalance is found deeper down.  
     * Check Current Node: After the recursive calls return (and provided isBalanced is still true), calculate the absolute difference between the leftHeight and rightHeight. If the difference is greater than 1, set \*isBalanced \= false.  
     * Return Height: If the node is balanced so far, return its height (max(leftHeight, rightHeight) \+ 1). If it became unbalanced at this node, the return value doesn't strictly matter, but returning \-1 is consistent.  
  2. isHeightBalanced (Wrapper): Initializes a boolean variable isBalanced to true. Calls checkBalanceAndHeight starting from the root, passing the address of the isBalanced flag. The helper function modifies this flag if any unbalance is detected. Returns the final value of the flag (converted to 1 or 0).  
* Example: Tree {10, 5, 20, \#, \#, 15, 30, \#, \#, \#, 25}  
  * Check(25): returns height 0\.  
  * Check(30): needs Check(25). Gets leftHeight=-1, rightHeight=0. Diff=1. Balanced. Returns height 1\.  
  * Check(15): returns height 0\.  
  * Check(20): needs Check(15), Check(30). Gets leftHeight=0, rightHeight=1. Diff=1. Balanced. Returns height 2\.  
  * Check(5): returns height 0\.  
  * Check(10): needs Check(5), Check(20). Gets leftHeight=0, rightHeight=2. Diff=2. Unbalanced\! Sets isBalanced \= false. Returns \-1 (or some value).  
  * isHeightBalanced returns 0\.

5\. Remove Elements Outside Range \[a, b\] (removeOutsideRange)

* Problem: Given a BST and a range \[a, b\], remove all nodes whose values fall outside this range, modifying the tree in place.  
* Function: btNode\* removeOutsideRange(btNode\* root, int a, int b)  
* Logic: This uses a post-order traversal approach. We need to process children before the parent, because removing a parent might disconnect children that need processing.  
  1. Base Case: If root is NULL, return NULL.  
  2. Recursive Calls: Recursively call removeOutsideRange on the left and right children. This ensures that the subtrees are already "cleaned" before processing the current node. The assignments (root-\>left \= ..., root-\>right \= ...) update the child pointers in case the recursive call returned a different node (e.g., if the original child was removed).  
  3. Process Current Node: After processing children:  
     * Case 1: root-\>data \< a: The current node's value is too small. Since it's a BST, its entire left subtree must also be too small. The only potentially valid part of the tree rooted here is the (already cleaned) right subtree. So, we free the current root node and return root-\>right to replace it in the parent's link.  
     * Case 2: root-\>data \> b: The current node's value is too large. Its entire right subtree must also be too large. The only potentially valid part is the (already cleaned) left subtree. free the current root and return root-\>left.  
     * Case 3: root-\>data \>= a && root-\>data \<= b: The current node is within the valid range. Keep it. Return the root pointer itself.  
* Example: Tree {20, 10, 30, 5, 15}, Range \[10, 25\].  
  * Calls go down to leaves. remove(5, 10, 25): 5 \< 10, free(5), return NULL. Node 10's left becomes NULL.  
  * remove(15, 10, 25): 15 is in range. Returns 15\. Node 10's right remains 15\.  
  * remove(10, 10, 25): Children processed. 10 is in range. Returns 10\. Node 20's left remains 10\.  
  * remove(NULL, 10, 25\) (left of 30): returns NULL.  
  * remove(NULL, 10, 25\) (right of 30): returns NULL.  
  * remove(30, 10, 25): Children processed. 30 \> 25, free(30), return root-\>left (which is NULL). Node 20's right becomes NULL.  
  * remove(20, 10, 25): Children processed. 20 is in range. Returns 20\.  
  * Final tree: {20, {10, NULL, 15}, NULL}.

6\. Create Sum Tree (createSumTree)

* Problem: Create a *new* binary tree where each node's value is the sum of the corresponding node's value in the original tree plus the sum of all values in its original left and right subtrees.  
* Functions: btNode\* createSumTree(btNode\* root), int sumTreeValues(btNode\* root)  
* Logic:  
  1. sumTreeValues (Helper): A standard recursive function to calculate the sum of all node values in a tree (or subtree). Base case: sum of NULL tree is 0\. Recursive step: root-\>data \+ sumTreeValues(root-\>left) \+ sumTreeValues(root-\>right).  
  2. createSumTree (Main Logic):  
     * Base Case: If the original root is NULL, the corresponding sum tree node is also NULL. Return NULL.  
     * Calculate Sum: Calculate the sum for the current node using root-\>data \+ sumTreeValues(root-\>left) \+ sumTreeValues(root-\>right).  
     * Create New Node: Create a new node (sumNode) for the sum tree and store the calculated sum in it.  
     * Recursive Calls: Recursively call createSumTree on the original tree's left and right children to build the left and right subtrees of the sumNode. Assign the results to sumNode-\>left and sumNode-\>right.  
     * Return: Return the newly created sumNode.  
* Example: Original Tree {10, 5, 15}  
  * createSumTree(10):  
    * sum \= 10 \+ sumTreeValues(5) \+ sumTreeValues(15) \= 10 \+ 5 \+ 15 \= 30\.  
    * Create sumNode(30).  
    * sumNode-\>left \= createSumTree(5).  
    * createSumTree(5): sum \= 5 \+ sum(NULL) \+ sum(NULL) \= 5\. Create node(5). Left/Right are NULL. Return node(5).  
    * sumNode-\>right \= createSumTree(15).  
    * createSumTree(15): sum \= 15 \+ sum(NULL) \+ sum(NULL) \= 15\. Create node(15). Left/Right are NULL. Return node(15).  
    * Return sumNode(30).  
  * Final Sum Tree: {30, 5, 15}.

7\. Convert Binary Tree to BST (convertBTtoBST)

* Problem: Given an arbitrary binary tree, create a new BST that contains the same set of values.  
* Functions: btNode\* convertBTtoBST(btNode\* root), storeInorder(...), countNodes(...), qsort(...), btNode\* sortedArrayToBST(int arr\[\], int start, int end)  
* Logic: This leverages the fact that the inorder traversal of the desired BST must be the sorted version of the elements present in the original BT.  
  1. Count Nodes: Determine the number of nodes (n) in the original BT using countNodes.  
  2. Store Inorder: Perform an inorder traversal of the original BT using storeInorder and store all the node values into an integer array arr of size n. Note that this array will contain the elements but not necessarily in sorted order.  
  3. Sort Array: Sort the array arr using qsort (or any other sorting algorithm). Now arr contains the elements in the order they should appear in an inorder traversal of the target BST.  
  4. Build Balanced BST: Use the sortedArrayToBST helper function to construct a height-balanced BST from the sorted array.  
     * sortedArrayToBST Logic:  
       * Base Case: If start \> end, return NULL.  
       * Find the middle element of the current array segment (mid \= start \+ (end \- start) / 2).  
       * Create a new node with the value arr\[mid\]. This node becomes the root of the current subtree.  
       * Recursively build the left subtree using the left half of the array (sortedArrayToBST(arr, start, mid \- 1)). Assign the result to the root's left child.  
       * Recursively build the right subtree using the right half of the array (sortedArrayToBST(arr, mid \+ 1, end)). Assign the result to the root's right child.  
       * Return the created root node.  
  5. Return & Cleanup: Return the root of the newly constructed BST (bstRoot) and free the temporary array arr.  
* Example: BT {10, 20, 5}  
  * Count \= 3\.  
  * Inorder (BT): \[20, 10, 5\]. Store in arr.  
  * Sort arr: \[5, 10, 20\].  
  * sortedArrayToBST(\[5, 10, 20\], 0, 2):  
    * Mid \= 1\. Create root node(10).  
    * Left: sortedArrayToBST(\[5\], 0, 0). Mid=0. Create node(5). Left/Right NULL. Return node(5). Root's left is 5\.  
    * Right: sortedArrayToBST(\[20\], 2, 2). Mid=2. Create node(20). Left/Right NULL. Return node(20). Root's right is 20\.  
    * Return node(10).  
  * Final BST: {10, 5, 20}.

8\. Convert BST to Sorted Doubly Linked List (convertBSTtoDLL)

* Problem: Convert a BST into a sorted Doubly Linked List (DLL) in-place. The DLL should use the left pointer as prev and the right pointer as next.  
* Functions: btNode\* convertBSTtoDLL(btNode\* root), void convertBSTtoDLLUtil(btNode\* root, btNode\*\* headRef, btNode\*\* prevRef)  
* Logic: This is done using an inorder traversal. During the traversal, when a node is "visited" (after its left subtree has been processed but before its right subtree is processed), we link it to the previously visited node.  
  1. convertBSTtoDLLUtil (Recursive Helper):  
     * Parameters: Takes the current root, a pointer to the DLL head (headRef), and a pointer to the previously visited node (prevRef).  
     * Base Case: If root is NULL, return.  
     * Recurse Left: Recursively call convertBSTtoDLLUtil on the left child. This processes the entire left subtree and sets prevRef to the rightmost node of the left subtree (the inorder predecessor).  
     * Process Current Node:  
       * If \*prevRef is NULL, it means this is the first node being visited in the inorder traversal (the leftmost node of the entire tree). Set \*headRef \= root.  
       * If \*prevRef is not NULL, link the previous node to the current node: (\*prevRef)-\>right \= root (previous node's next points to current) and root-\>left \= \*prevRef (current node's prev points to previous).  
       * Update \*prevRef \= root so that the current node becomes the "previous" node for the next node visited in the inorder sequence.  
     * Recurse Right: Recursively call convertBSTtoDLLUtil on the right child.  
  2. convertBSTtoDLL (Wrapper): Initializes head \= NULL and prev \= NULL. Calls the utility function convertBSTtoDLLUtil. Returns the final head of the DLL.  
* Example: BST {10, 5, 15}  
  * Util(10, \&h, \&p): Calls Util(5, \&h, \&p).  
  * Util(5, \&h, \&p): Calls Util(NULL, \&h, \&p) (returns). Process 5\. p is NULL. h becomes node 5\. p becomes node 5\. Calls Util(NULL, \&h, \&p) (returns). Returns.  
  * Back to Util(10, \&h, \&p): Process 10\. p is node 5\. Link: p-\>right=10 (5-\>10), 10-\>left=p (10\<-5). p becomes node 10\. Calls Util(15, \&h, \&p).  
  * Util(15, \&h, \&p): Calls Util(NULL, \&h, \&p) (returns). Process 15\. p is node 10\. Link: p-\>right=15 (10-\>15), 15-\>left=p (15\<-10). p becomes node 15\. Calls Util(NULL, \&h, \&p) (returns). Returns.  
  * Back to Util(10, \&h, \&p). Returns.  
  * convertBSTtoDLL returns h (node 5). DLL: 5 \<-\> 10 \<-\> 15\.

9\. Sum of Values in BST (sumBSTValues)

* Problem: Calculate the sum of all node values in a BST.  
* Function: int sumBSTValues(btNode\* root)  
* Logic: This is identical to calculating the sum of values in any binary tree. The BST property doesn't provide a shortcut here. The code reuses the sumTreeValues function implemented for Problem 6\.  
  1. Base Case: If root is NULL, the sum is 0\.  
  2. Recursive Step: Return root-\>data \+ sumBSTValues(root-\>left) \+ sumBSTValues(root-\>right).  
* Example: Tree {10, 5, 15}. Sum \= 10 \+ sum(5) \+ sum(15) \= 10 \+ (5 \+ 0 \+ 0\) \+ (15 \+ 0 \+ 0\) \= 30\.

10\. Modify BST based on value m (modifyBST)

* Problem: Given a BST and a value m, modify the tree in-place such that all values less than or equal to m are incremented by 5, and all values greater than m are decremented by 5\.  
* Function: void modifyBST(btNode\* root, int m)  
* Logic: Perform a simple traversal (preorder, inorder, or postorder all work) of the tree. At each node, check its data against m and apply the modification.  
  1. Base Case: If root is NULL, return.  
  2. Modify Current Node: Check root-\>data: if \<= m, add 5; otherwise, subtract 5\.  
  3. Recursive Calls: Recursively call modifyBST on the left and right children.  
* Important Note: This operation will very likely destroy the BST property of the tree.  
* Example: Tree {10, 5, 15}, m \= 12\.  
  * modifyBST(10, 12): 10 \<= 12, data becomes 15\. Calls modifyBST(5, 12). Calls modifyBST(15, 12).  
  * modifyBST(5, 12): 5 \<= 12, data becomes 10\. Calls on NULL children. Returns.  
  * modifyBST(15, 12): 15 \> 12, data becomes 10\. Calls on NULL children. Returns.  
  * Final Tree (structure unchanged, data modified): {15, 10, 10}. This is no longer a valid BST.

11\. Find m-th Largest Element in BST (findMthLargest)

* Problem: Find the m-th largest element in a BST (e.g., m=1 is the largest, m=2 is the second largest).  
* Functions: int findMthLargest(btNode\* root, int m), void findMthLargestUtil(btNode\* root, int m, int\* count, int\* result)  
* Logic: The key is to use a *reverse inorder traversal* (Right \-\> Node \-\> Left). This visits nodes in descending order. We keep a count of visited nodes. When the count reaches m, the current node is the m-th largest.  
  1. findMthLargestUtil (Recursive Helper):  
     * Parameters: Current root, target rank m, pointer to a count, pointer to store the result.  
     * Base Cases: Return immediately if root is NULL or if the m-th largest has already been found (\*count \>= m).  
     * Recurse Right: First, recursively call on the right child (findMthLargestUtil(root-\>right, ...)). This explores larger values first.  
     * Process Current Node: After returning from the right subtree call, check if the m-th largest has been found yet (\*count \< m). If not:  
       * Increment the \*count.  
       * If \*count now equals m, we've found the desired node. Store root-\>data in \*result and return (no need to check left).  
     * Recurse Left: If the m-th largest hasn't been found after processing the current node (\*count \< m), recursively call on the left child (findMthLargestUtil(root-\>left, ...)).  
  2. findMthLargest (Wrapper): Initializes count \= 0 and result \= INT\_MIN (or another indicator for "not found"). Calls the utility function. Checks if m was valid and if the result was found (comparing result against the initial "not found" value or checking if count \< m). Returns the found result or an error indicator.  
* Example: Tree {20, 10, 30, 5, 15}, m \= 2 (second largest).  
  * Util(20, 2, \&c=0, \&r=MIN): Calls Util(30, 2, \&c, \&r).  
  * Util(30, 2, \&c=0, \&r=MIN): Calls Util(NULL) (right). Process 30\. c becomes 1\. c \!= m. Calls Util(NULL) (left). Returns.  
  * Back to Util(20,...): Process 20\. c becomes 2\. c \== m. Set r \= 20\. Return. (Doesn't need to call on left child 10).  
  * findMthLargest returns r (which is 20).

12\. BST based on Word Length and Frequency (buildFreqBSTFromFile, etc.)

* Problem: Read words from a file. Create a BST where each node stores a unique word *length* and the *frequency* (count) of words having that length.  
* Functions: freqNode\* buildFreqBSTFromFile(const char\* filename), freqNode\* insertFreqBST(freqNode\* root, int length), freqNode\* createFreqNode(int length), void displayFreqBST(freqNode\* root), void freeFreqTree(freqNode\* root)  
* Data Structure: Uses a separate freqNode struct { int length; int freq; struct freqNode \*left, \*right; }.  
* Logic:  
  1. buildFreqBSTFromFile:  
     * Opens the specified file.  
     * Reads words one by one using fscanf.  
     * For each word, calculates its strlen.  
     * Calls insertFreqBST to add the length to the frequency BST.  
     * Closes the file and returns the root of the built frequency BST.  
  2. insertFreqBST:  
     * Base Case: If root is NULL, create a new freqNode for this length (using createFreqNode, which initializes freq to 1\) and return it.  
     * Recursive Step:  
       * If length \< root-\>length, recursively insert into the left subtree (root-\>left \= insertFreqBST(root-\>left, length)).  
       * If length \> root-\>length, recursively insert into the right subtree (root-\>right \= insertFreqBST(root-\>right, length)).  
       * If length \== root-\>length, a node for this length already exists. Simply increment its frequency (root-\>freq++).  
     * Return: Return the root pointer.  
  3. displayFreqBST: Performs a standard inorder traversal of the freqNode tree, printing the length and freq at each node. This displays the frequencies sorted by word length.  
  4. freeFreqTree: Standard post-order traversal to free all nodes in the frequency tree.  
* Example: File: "a cat dog cat"  
  * Read "a": len=1. insert(NULL, 1\) creates node(len=1, freq=1). Root is node(1,1).  
  * Read "cat": len=3. insert(root, 3). 3 \> 1\. root-\>right \= insert(NULL, 3). Creates node(3,1). Tree: { (1,1), NULL, (3,1) }.  
  * Read "dog": len=3. insert(root, 3). 3 \> 1\. insert(node(3,1), 3). 3 \== 3\. Increment freq. Node becomes node(3,2). Tree: { (1,1), NULL, (3,2) }.  
  * Read "cat": len=3. insert(root, 3). 3 \> 1\. insert(node(3,2), 3). 3 \== 3\. Increment freq. Node becomes node(3,3). Tree: { (1,1), NULL, (3,3) }.  
  * Display (inorder): "Length: 1, Frequency: 1", "Length: 3, Frequency: 3".

This covers the logic behind the implementations for Practice Set 2\.