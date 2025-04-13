#include <stdio.h>
#include <stdlib.h>
#include <string.h>
///////////////////////////////////////////////////////////////////////////////////////////////
// function prototypes
void menu();
void insert(Node **root, int data);
void delete(Node **root, int data);
void search(Node *root, int data);
void preorder(Node *root);
void inorder(Node *root);
void postorder(Node *root);
void display(Node *root, int level);
void display_tree(Node *root);
void free_tree(Node *root);
///////////////////////////////////////////////////////////////////////////////////////////////
// structure definition

typedef struct btnode {
    int data;
    struct btnode *left;
    struct btnode *right;
} Node;


void menu() {   
    Node *root = NULL;
    int choice, r, data;
    while (1) {
        printf("\n1. Insert\n");
        printf("2. Delete\n");
        printf("3. Search\n");
        printf("4. Preorder\n");
        printf("5. Inorder\n");
        printf("6. Postorder\n");
        printf("7. Display\n");
        printf("8. Display Tree\n");
        printf("9. Free Tree\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        r = scanf("%d", &choice);
        if (r != 1) {
            printf("Invalid input\n");
            menu();
        }

        switch (choice) {
            case 1:
                printf("Enter the data to insert: ");
                scanf("%d", &data);
                insert(&root, data);
                break;
            case 2:
                printf("Enter the data to delete: ");
                scanf("%d", &data);
                delete(&root, data);
                break;
            case 3:
                printf("Enter the data to search: ");
                scanf("%d", &data);
                search(root, data);
                break;
            case 4:
                preorder(root);
                break;
            case 5:
                inorder(root);
                break;
            case 6:
                postorder(root);
                break;
            case 7:
                display(root, 0);
                break;
            case 8:
                display_tree(root);
                break;
            case 9:
                free_tree(root);
                break;
            case 0:
                free_tree(root);
                exit(0);
            default:
                printf("Invalid choice\n");
        }
    }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int main() {
    Node *root = (Node *)malloc(sizeof(Node));
    menu();
    return 0;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// function to insert a node in the tree
void insert(Node **root, int data) {
    if (*root == NULL) {
        *root = (Node *)malloc(sizeof(Node));
        (*root)->data = data;
        (*root)->left = NULL;
        (*root)->right = NULL;
    } else {
        if (data < (*root)->data) {
            insert(&(*root)->left, data);
        } else {
            insert(&(*root)->right, data);
        }
    }
}   

// function to delete a node from the tree  
void delete(Node **root, int data) {
    if (*root == NULL) {
        return;
    } else {
        if (data < (*root)->data) {
            delete(&(*root)->left, data);   
}}




// function to search a node in the tree
void search(Node *root, int data) {
    if (root == NULL) {
        printf("Data not found\n");
    } else {
        if (data < root->data) {
            search(root->left, data);
        } else if (data > root->data) {
            search(root->right, data);
        } else {
            printf("Data found\n");
        }
    }
}

// function to traverse the tree in preorder
void preorder(Node *root) {
    if (root != NULL) {
        printf("%d ", root->data);
        preorder(root->left);
        preorder(root->right);
    }
}

// function to traverse the tree in inorder
void inorder(Node *root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->data);
        inorder(root->right);
    }
}

// function to traverse the tree in postorder
void postorder(Node *root) {
    if (root != NULL) {
        postorder(root->left);
        postorder(root->right);
        printf("%d ", root->data);
    }  
}
