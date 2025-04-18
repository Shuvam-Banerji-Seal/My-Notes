#include <stdio.h>
#include <stdlib.h>
#include <time.h>   // For srand, rand
#include <limits.h> // For INT_MIN/MAX checks if needed

#include "utils.h"
#include "binary_tree.h"
#include "binary_search_tree.h"

// --- Function Prototypes for Main ---
void displayMainMenu();
void displayPracticeSet1Menu();
void displayPracticeSet2Menu();
btNode* createRandomTree(int n);
btNode* createTreeFromUserInput();
btNode* createHardcodedTree();
void generateUniqueRandoms(int arr[], int n, int range_max); // Helper for random tree

// --- Main Function ---
int main() {
    btNode *root = NULL; // The main tree root pointer
    btNode *root2 = NULL; // Second root for comparison functions (isIdentical, isMirror)
    freqNode *freqRoot = NULL; // Separate root for Problem 12 of Set 2
    int choice, subChoice, n, data, parentData, k1, k2, m;
    char direction;
    bool keepRunning = true;

    srand(time(NULL)); // Seed random number generator

    printf("Welcome to the Binary Tree Practice Program!\n");

    while (keepRunning) {
        displayMainMenu();
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Please enter a number.\n");
            while (getchar() != '\n'); // Clear input buffer
            choice = -1; // Set invalid choice to loop again
        }
         while (getchar() != '\n'); // Consume trailing newline

        // Free existing trees before creating a new one
        if (choice >= 1 && choice <= 3) {
             if (root) {
                printf("Freeing existing main tree...\n");
                freeTree(root);
                root = NULL;
             }
              if (root2) {
                printf("Freeing existing second tree...\n");
                freeTree(root2);
                root2 = NULL;
             }
             // Keep freqRoot separate, it's only built/freed in its specific option
        }


        switch (choice) {
            case 1: // Create Random Tree
                printf("Enter the number of nodes for the random tree: ");
                 if (scanf("%d", &n) != 1 || n <= 0) {
                     printf("Invalid number of nodes. Please enter a positive integer.\n");
                     while (getchar() != '\n'); // Clear input buffer
                     break;
                 }
                 while (getchar() != '\n'); // Consume trailing newline
                root = createRandomTree(n);
                displayTree(root);
                break;

            case 2: // Create Tree from User Input (Manual Insertion)
                root = createTreeFromUserInput();
                displayTree(root);
                break;

            case 3: // Create Hardcoded Example Tree
                root = createHardcodedTree();
                printf("Hardcoded example tree created.\n");
                displayTree(root);
                break;

            case 4: // Display Current Tree
                printf("\n--- Current Main Tree ---\n");
                displayTree(root);
                printf("\n--- Current Second Tree (for comparison) ---\n");
                displayTree(root2);
                 printf("\n--- Current Frequency Tree (Set 2, Prob 12) ---\n");
                 if (freqRoot) {
                    displayFreqBST(freqRoot);
                 } else {
                    printf("(Not built yet)\n");
                 }
                 printf("------------------------\n");
                break;

            case 5: // Practice Set 1 Menu
                if (!root && subChoice != 18) { // Allow building tree even if root is NULL
                   printf("Please create a tree first (Options 1-3).\n");
                   if (subChoice == 18) printf("Except for option 18 (Build Complete Tree).\n");
                   else break;
                }
                displayPracticeSet1Menu();
                printf("Enter Set 1 choice: ");
                 if (scanf("%d", &subChoice) != 1) {
                    printf("Invalid input.\n");
                    while (getchar() != '\n'); break;
                 }
                 while (getchar() != '\n'); // Consume newline

                // --- Handle Set 1 Choices ---
                switch(subChoice) {
                    case 1: // Manual Insert (can add to existing tree)
                        printf("Enter data for new node: "); scanf("%d", &data);
                        printf("Enter data of parent node (-1 for root): "); scanf("%d", &parentData);
                        if (parentData != -1) {
                             printf("Insert as Left ('L') or Right ('R') child: "); scanf(" %c", &direction); // Space before %c to skip whitespace
                        } else {
                            direction = ' '; // Not needed for root
                        }
                        while (getchar() != '\n'); // Consume newline
                        root = insertNodeManual(&root, data, parentData, direction); // Pass address of root
                        displayTree(root);
                        break;
                    case 2: displayTree(root); break;
                    case 3: inorder_nonrecursive(root); break;
                    case 4: postorder_nonrecursive(root); break;
                    case 5:
                        data = findMax(root);
                        if (data == INT_MIN) printf("Tree is empty.\n");
                        else printf("Maximum value: %d\n", data);
                        break;
                    case 6:
                        printf("Enter value to search for: "); scanf("%d", &data); while (getchar() != '\n');
                        if (isExists(root, data)) printf("%d exists in the tree.\n", data);
                        else printf("%d does not exist in the tree.\n", data);
                        break;
                    case 7: printf("Height of the tree: %d\n", getHeight(root)); break;
                    case 8:
                        printf("Enter value to find level for: "); scanf("%d", &data); while (getchar() != '\n');
                        n = getLevel(root, data);
                        if (n == -1) printf("Value %d not found in the tree.\n", data);
                        else printf("Level of %d is: %d\n", data, n);
                        break;
                    case 9: levelorder(root); break;
                    case 10: zigzag(root); break;
                    case 11: printf("Number of leaf nodes: %d\n", getLeafCount(root)); break;
                    case 12: printf("Number of full nodes: %d\n", getFullNodeCount(root)); break;
                    case 13: printf("Number of half nodes: %d\n", getHalfNodeCount(root)); break;
                    case 14: // isIdentical - Needs a second tree
                        printf("Creating a second tree for comparison (hardcoded example).\n");
                        if(root2) freeTree(root2); // Free previous second tree if exists
                        root2 = createHardcodedTree(); // Create the same example
                        // You might want an option to create a *different* second tree
                        displayTree(root2);
                        if (isIdentical(root, root2)) printf("The two trees ARE identical.\n");
                        else printf("The two trees ARE NOT identical.\n");
                        break;
                    case 15: // isMirror - Needs a second tree
                         printf("Creating a second tree for comparison (mirrored hardcoded example).\n");
                         if(root2) freeTree(root2);
                         // Manually create a mirror of the hardcoded tree
                         root2 = createNode(49);
                         root2->left = createNode(73);
                         root2->right = createNode(34);
                         root2->left->left = createNode(79);
                         root2->left->right = createNode(60);
                         root2->right->left = createNode(40);
                         root2->right->right = createNode(12);
                         root2->right->left->left = createNode(55); // Mirrored position
                         root2->right->left->right = createNode(38);// Mirrored position
                         root2->right->right->right = createNode(13); // Mirrored position
                         displayTree(root2);
                         if (isMirror(root, root2)) printf("The two trees ARE mirror images.\n");
                         else printf("The two trees ARE NOT mirror images.\n");
                         break;
                    case 16:
                        printf("Enter data of node to find ancestors for: "); scanf("%d", &data); while (getchar() != '\n');
                        printf("Ancestors of %d: ", data);
                        if (!printAncestors(root, data)) {
                             printf("(Node %d not found or is root)\n", data);
                        } else {
                             printf("\n");
                        }
                        break;
                    case 17: printf("Breadth (Maximum Width) of the tree: %d\n", getBreadth(root)); break;
                    case 18: // Build Complete Tree from Input
                        if (root) { freeTree(root); root = NULL; } // Clear existing tree
                        root = buildCompleteTreeFromInput();
                        displayTree(root);
                        break;
                    default: printf("Invalid choice for Set 1.\n"); break;
                }
                break; // End of case 5 (Practice Set 1)

            case 6: // Practice Set 2 Menu
                 if (!root) {
                   printf("Please create a tree first (Options 1-3).\n");
                   // Allow Prob 7 (BT->BST) and Prob 12 (Freq BST) even if main root is NULL
                   if (subChoice != 7 && subChoice != 12) break;
                 }
                displayPracticeSet2Menu();
                printf("Enter Set 2 choice: ");
                 if (scanf("%d", &subChoice) != 1) {
                    printf("Invalid input.\n");
                    while (getchar() != '\n'); break;
                 }
                 while (getchar() != '\n'); // Consume newline

                // --- Handle Set 2 Choices ---
                 switch(subChoice) {
                    case 0: // Helper: Insert into BST (useful for testing other functions)
                        printf("Enter value to insert into BST: "); scanf("%d", &data); while (getchar() != '\n');
                        root = insertBST(root, data); // Assumes 'root' should behave like a BST now
                        displayTree(root);
                        break;
                    case 1: // isBST
                        if (isBST(root)) printf("The current tree IS a Binary Search Tree.\n");
                        else printf("The current tree IS NOT a Binary Search Tree.\n");
                        break;
                    case 2: // Print Range
                        printf("Enter range start (k1): "); scanf("%d", &k1);
                        printf("Enter range end (k2): "); scanf("%d", &k2); while (getchar() != '\n');
                        if (!isBST(root)) printf("Warning: Tree might not be a BST, results may be incorrect.\n");
                        printf("Elements in range [%d, %d]: ", k1, k2);
                        printRange(root, k1, k2);
                        printf("\n");
                        break;
                    case 3: // Have Same Info
                        printf("Creating/Using a second tree for comparison (hardcoded example).\n");
                        if(!root2) root2 = createHardcodedTree(); // Create if doesn't exist
                        // Optional: Add way to create a different second tree
                        displayTree(root2);
                        if (!isBST(root) || !isBST(root2)) printf("Warning: One or both trees might not be BSTs.\n");
                        if (haveSameInfo(root, root2)) printf("The two trees contain the same information.\n");
                        else printf("The two trees DO NOT contain the same information.\n");
                        break;
                    case 4: // isHeightBalanced
                        if (isHeightBalanced(root)) printf("The tree IS height-balanced.\n");
                        else printf("The tree IS NOT height-balanced.\n");
                        break;
                    case 5: // Remove Outside Range
                        printf("Enter valid range start (a): "); scanf("%d", &k1); // Reuse k1
                        printf("Enter valid range end (b): "); scanf("%d", &k2); while (getchar() != '\n'); // Reuse k2
                        if (!isBST(root)) printf("Warning: Tree might not be a BST, operation assumes BST properties.\n");
                        printf("Removing nodes outside range [%d, %d]...\n", k1, k2);
                        root = removeOutsideRange(root, k1, k2);
                        displayTree(root);
                        break;
                    case 6: // Create Sum Tree
                        printf("Creating a new Sum Tree based on the current tree...\n");
                        btNode* sumRoot = createSumTree(root);
                        printf("Original Tree:\n");
                        displayTree(root);
                        printf("Sum Tree:\n");
                        displayTree(sumRoot);
                        // Remember to free the sum tree if you don't need it anymore
                        printf("Freeing the Sum Tree...\n");
                        freeTree(sumRoot);
                        break;
                    case 7: // Convert BT to BST
                        printf("Converting the current Binary Tree structure to a BST...\n");
                        btNode* bstRoot = convertBTtoBST(root);
                        printf("Original Tree (remains unchanged):\n");
                        displayTree(root);
                        printf("New Binary Search Tree:\n");
                        displayTree(bstRoot);
                        printf("Replacing current main tree with the new BST.\n");
                        freeTree(root); // Free the old BT structure
                        root = bstRoot; // Update root to point to the new BST
                        break;
                    case 8: // Convert BST to DLL
                         if (!isBST(root)) printf("Warning: Tree might not be a BST, DLL conversion assumes BST for sorted order.\n");
                         printf("Converting BST to sorted Doubly Linked List...\n");
                         btNode* dllHead = convertBSTtoDLL(root);
                         printDLL(dllHead);
                         // IMPORTANT: The original tree structure is modified (left/right pointers are reused).
                         // To use tree functions again, you'd need to rebuild the tree or restore pointers.
                         printf("Original tree structure modified. Setting root to NULL to avoid invalid operations.\n");
                         root = NULL; // Set root to NULL as tree structure is now a DLL
                         // Optional: Add code here to free the DLL nodes if needed immediately
                         // freeDLL(dllHead); // You'd need to implement freeDLL
                         break;
                    case 9: // Sum BST Values
                         if (!isBST(root)) printf("Warning: Tree might not be a BST.\n");
                         printf("Sum of all values in the tree: %d\n", sumBSTValues(root));
                         break;
                    case 10: // Modify BST
                         printf("Enter threshold value m: "); scanf("%d", &m); while (getchar() != '\n');
                         if (!isBST(root)) printf("Warning: Tree might not be a BST, operation assumes BST properties.\n");
                         printf("Modifying tree: values <= %d add 5, values > %d subtract 5...\n", m, m);
                         modifyBST(root, m);
                         displayTree(root);
                         // Check if it's still a BST (it likely won't be)
                         if (isBST(root)) printf("Modified tree is still a BST.\n");
                         else printf("Modified tree is NO LONGER a BST.\n");
                         break;
                    case 11: // Find m-th Largest
                         printf("Enter rank m (1 for largest, 2 for second largest, etc.): "); scanf("%d", &m); while (getchar() != '\n');
                         if (!isBST(root)) printf("Warning: Tree might not be a BST, result depends on inorder traversal.\n");
                         data = findMthLargest(root, m);
                         if (data != INT_MIN) { // Check if found
                             printf("%d-th largest element: %d\n", m, data);
                         } // Error message printed inside findMthLargest if not found
                         break;
                    case 12: // Build and display Frequency BST from file
                        if (freqRoot) {
                            printf("Freeing previous frequency tree...\n");
                            freeFreqTree(freqRoot);
                            freqRoot = NULL;
                        }
                        // NOTE: Requires a file named "input_words.txt"
                        freqRoot = buildFreqBSTFromFile("input_words.txt");
                        if (freqRoot) {
                            printf("\n--- Frequency BST (Inorder Display) ---\n");
                            displayFreqBST(freqRoot);
                             printf("--------------------------------------\n");
                        }
                        break;
                    default: printf("Invalid choice for Set 2.\n"); break;
                 }
                 break; // End of case 6 (Practice Set 2)

            case 0: // Exit
                printf("Exiting program. Freeing trees...\n");
                if(root) freeTree(root);
                if(root2) freeTree(root2);
                if(freqRoot) freeFreqTree(freqRoot);
                keepRunning = false;
                break;

            default:
                printf("Invalid choice. Please try again.\n");
                break;
        } // End of main switch
        if (keepRunning) {
            printf("\nPress Enter to continue...");
            getchar(); // Wait for user before showing menu again
        }

    } // End of while loop

    printf("Goodbye!\n");
    return 0;
}

// --- Menu Display Functions ---

void displayMainMenu() {
    printf("\n===== Main Menu =====\n");
    printf("1. Create Random Tree\n");
    printf("2. Create Tree from User Input (Manual Insert)\n");
    printf("3. Create Hardcoded Example Tree\n");
    printf("4. Display Current Trees\n");
    printf("5. Go to Practice Set 1 Menu (Binary Tree)\n");
    printf("6. Go to Practice Set 2 Menu (Binary Search Tree)\n");
    printf("0. Exit\n");
    printf("=====================\n");
}

void displayPracticeSet1Menu() {
    printf("\n--- Practice Set 1: Binary Tree Operations ---\n");
    printf(" 1. Insert Node Manually (Prob 1)\n");
    printf(" 2. Display Tree (Prob 2)\n");
    printf(" 3. Inorder Traversal (Non-Recursive) (Prob 3)\n");
    printf(" 4. Postorder Traversal (Non-Recursive) (Prob 4)\n");
    printf(" 5. Find Maximum Value (Prob 5)\n");
    printf(" 6. Check if Value Exists (Prob 6)\n");
    printf(" 7. Get Tree Height (Prob 7)\n");
    printf(" 8. Get Level of Node (Prob 8)\n");
    printf(" 9. Level Order Traversal (Prob 9)\n");
    printf("10. Zigzag Level Order Traversal (Prob 10)\n");
    printf("11. Count Leaf Nodes (Prob 11)\n");
    printf("12. Count Full Nodes (Prob 12)\n");
    printf("13. Count Half Nodes (Prob 13)\n");
    printf("14. Check if Identical (compares with 2nd tree) (Prob 14)\n");
    printf("15. Check if Mirror (compares with 2nd tree) (Prob 15)\n");
    printf("16. Print Ancestors of Node (Prob 16)\n");
    printf("17. Get Tree Breadth (Max Width) (Prob 17)\n");
    printf("18. Build Complete Binary Tree from Input (Prob 18)\n");
    printf("--------------------------------------------\n");
}

void displayPracticeSet2Menu() {
    printf("\n--- Practice Set 2: Binary Search Tree Operations ---\n");
    printf(" 0. Insert Value (Standard BST Insert - Helper)\n"); // Added helper
    printf(" 1. Check if Tree is BST (Prob 1)\n");
    printf(" 2. Print Elements in Range [k1, k2] (Prob 2)\n");
    printf(" 3. Check if Two Trees Have Same Info (Prob 3)\n");
    printf(" 4. Check if Height Balanced (Prob 4)\n");
    printf(" 5. Remove Elements Outside Range [a, b] (Prob 5)\n");
    printf(" 6. Create Sum Tree (Prob 6)\n");
    printf(" 7. Convert Binary Tree to BST (Prob 7)\n");
    printf(" 8. Convert BST to Sorted Doubly Linked List (Prob 8)\n");
    printf(" 9. Sum of Values in BST (Prob 9)\n");
    printf("10. Modify BST (<= m add 5, > m subtract 5) (Prob 10)\n");
    printf("11. Find m-th Largest Element (Prob 11)\n");
    printf("12. Build/Display Word Length Frequency BST from File (Prob 12)\n");
    printf("----------------------------------------------------\n");
}


// --- Tree Creation Functions ---

/**
 * @brief Generates unique random integers within a specified range.
 * Simple approach: generate random numbers and check for duplicates.
 * For larger 'n' or smaller 'range_max', this can be inefficient.
 */
void generateUniqueRandoms(int arr[], int n, int range_max) {
    if (n > range_max) {
        fprintf(stderr, "Warning: Cannot generate %d unique numbers from range [1, %d].\n", n, range_max);
        // Fill with non-unique numbers as fallback
         for (int i = 0; i < n; i++) {
             arr[i] = (rand() % range_max) + 1;
         }
        return;
    }

    bool *used = (bool*)calloc(range_max + 1, sizeof(bool)); // Track used numbers
    if (!used) {
        perror("Failed to allocate memory for uniqueness check");
        // Fallback to non-unique
        for (int i = 0; i < n; i++) {
             arr[i] = (rand() % range_max) + 1;
         }
        return;
    }


    for (int i = 0; i < n; i++) {
        int num;
        do {
            num = (rand() % range_max) + 1; // Generate number in [1, range_max]
        } while (used[num]); // Repeat if number is already used
        arr[i] = num;
        used[num] = true; // Mark number as used
    }
    free(used);
}


/**
 * @brief Creates a random binary tree with n unique nodes.
 * Uses level order insertion for a relatively balanced structure.
 */
btNode* createRandomTree(int n) {
    if (n <= 0) return NULL;

    // Generate n unique random numbers (e.g., in range 1 to 10*n for sparseness)
    int range = n * 10; // Adjust range as needed
    int* values = (int*)malloc(n * sizeof(int));
    if (!values) {
        perror("Failed to allocate memory for random values");
        return NULL;
    }
    generateUniqueRandoms(values, n, range);

    printf("Generated unique values: ");
    for(int i=0; i<n; ++i) printf("%d ", values[i]);
    printf("\n");


    // Create tree using level order insertion
    btNode* root = createNode(values[0]);
    if (!root) { free(values); return NULL; }

    Queue* q = createQueue();
    if (!q) { free(values); freeTree(root); return NULL; }
    enqueue(q, root);

    int i = 1; // Index for the next value in the 'values' array
    while (i < n) {
        btNode* currentParent = dequeue(q);
         if (!currentParent) break; // Should not happen if n > 0

        // Add left child if available
        if (i < n) {
            currentParent->left = createNode(values[i]);
            if (currentParent->left) {
                enqueue(q, currentParent->left);
            } else {
                 break; // Node creation failed
            }
            i++;
        } else {
            break; // No more values left
        }


        // Add right child if available
        if (i < n) {
            currentParent->right = createNode(values[i]);
             if (currentParent->right) {
                enqueue(q, currentParent->right);
             } else {
                 break; // Node creation failed
             }
            i++;
        } else {
            break; // No more values left
        }
    }

    free(values);
    freeQueue(q);
    printf("Random tree created using level order insertion.\n");
    return root;
}


/**
 * @brief Creates a tree based on user input using manual insertion (Problem 1, Set 1).
 */
btNode* createTreeFromUserInput() {
    btNode* root = NULL;
    int data, parentData;
    char direction;
    char cont = 'y';

    printf("\n--- Create Tree via Manual Insertion ---\n");
    printf("Insert root node first (use parent data -1).\n");

    while (cont == 'y' || cont == 'Y') {
         printf("\nEnter data for new node: ");
         if (scanf("%d", &data) != 1) { printf("Invalid data.\n"); while(getchar()!='\n'); continue;}

         printf("Enter data of parent node (-1 if this is the root): ");
         if (scanf("%d", &parentData) != 1) { printf("Invalid parent data.\n"); while(getchar()!='\n'); continue;}

         direction = ' '; // Default
         if (parentData != -1) {
             printf("Insert as Left ('L') or Right ('R') child: ");
             if (scanf(" %c", &direction) != 1 || (direction != 'L' && direction != 'l' && direction != 'R' && direction != 'r')) {
                 printf("Invalid direction.\n"); while(getchar()!='\n'); continue;
             }
         }
         while (getchar() != '\n'); // Consume trailing newline

         // Perform insertion
         insertNodeManual(&root, data, parentData, direction); // Function prints success/error

         printf("\nAdd another node? (y/n): ");
         scanf(" %c", &cont);
         while (getchar() != '\n'); // Consume trailing newline
    }

    printf("Manual tree creation finished.\n");
    return root;
}


/**
 * @brief Creates a predefined hardcoded example tree (based on the PDF diagram).
 */
btNode* createHardcodedTree() {
    btNode* root = createNode(49);
    if (!root) return NULL;

    root->left = createNode(34);
    root->right = createNode(73);

    if (root->left) {
        root->left->left = createNode(12);
        root->left->right = createNode(40);
         if (root->left->left) {
            root->left->left->right = createNode(13); // Node 13 is right child of 12
         }
         if (root->left->right) {
             root->left->right->left = createNode(38);
             root->left->right->right = createNode(55); // Node 55 is right child of 40 (Error in PDF diagram?) - Assuming 55 is child of 60 based on level order
             // Correction: PDF diagram shows 55 as child of 60. Let's follow the diagram structure.
             // Let's redo based on structure visual + level order: 49 34 73 12 40 60 79 13 38 55
             free(root->left->right->right); // Remove the wrongly placed 55
             root->left->right->right = NULL;
         }
    }

     if (root->right) {
        root->right->left = createNode(60);
        root->right->right = createNode(79);
         if (root->right->left) {
             root->right->left->left = createNode(55); // 55 is left child of 60
         }
     }


    // Verify structure based on diagram:
    // Level 0: 49
    // Level 1: 34, 73
    // Level 2: 12, 40, 60, 79
    // Level 3: 13(R of 12), 38(L of 40), 55(L of 60)

    // Re-create based on this structure:
    freeTree(root); // Clear previous attempt
    root = createNode(49);
    root->left = createNode(34);
    root->right = createNode(73);
    root->left->left = createNode(12);
    root->left->right = createNode(40);
    root->right->left = createNode(60);
    root->right->right = createNode(79);
    root->left->left->right = createNode(13); // R child of 12
    root->left->right->left = createNode(38); // L child of 40
    root->right->left->left = createNode(55); // L child of 60


    return root;
}
