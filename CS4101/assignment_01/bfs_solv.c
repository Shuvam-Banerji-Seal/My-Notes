#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define JUG1_CAP 3
#define JUG2_CAP 4
#define MAX_STATES 100
#define TARGET 2


typedef struct {
    int x, y;
    int parent_index;
    const char* action;
} State;

// A big ol' array to store every state we discover.
State all_states[MAX_STATES];
int state_count = 0;

// The mighty Queue! First-in, first-out, like a civilized line in a bakery shop
typedef struct {
    int items[MAX_STATES];
    int front, rear;
} Queue;

void init_queue(Queue* q) { q->front = 0; q->rear = -1; }
int is_queue_empty(Queue* q) { return q->rear < q->front; }
void enqueue(Queue* q, int value) { q->items[++q->rear] = value; }
int dequeue(Queue* q) { return q->items[q->front++]; }

// This is the brain of the operation, containing all the rules.
void generate_next_states(int current_index, int visited[][JUG2_CAP + 1], Queue* q) {
    State current = all_states[current_index];
    int x = current.x;
    int y = current.y;

    // Rule 1: Fill 3L jug
    if (!visited[JUG1_CAP][y]) {
        visited[JUG1_CAP][y] = 1;
        all_states[state_count] = (State){JUG1_CAP, y, current_index, "Fill 3L jug"};
        printf("  -> Discovered new state: (%d, %d). Adding to queue.\n", JUG1_CAP, y);
        enqueue(q, state_count++);
    }
    // Rule 2: Fill 4L jug
    if (!visited[x][JUG2_CAP]) {
        visited[x][JUG2_CAP] = 1;
        all_states[state_count] = (State){x, JUG2_CAP, current_index, "Fill 4L jug"};
        printf("  -> Discovered new state: (%d, %d). Adding to queue.\n", x, JUG2_CAP);
        enqueue(q, state_count++);
    }
    // Rule 3: Empty 3L jug
    if (!visited[0][y]) {
        visited[0][y] = 1;
        all_states[state_count] = (State){0, y, current_index, "Empty 3L jug"};
        printf("  -> Discovered new state: (%d, %d). Adding to queue.\n", 0, y);
        enqueue(q, state_count++);
    }
    // Rule 4: Empty 4L jug
    if (!visited[x][0]) {
        visited[x][0] = 1;
        all_states[state_count] = (State){x, 0, current_index, "Empty 4L jug"};
        printf("  -> Discovered new state: (%d, %d). Adding to queue.\n", x, 0);
        enqueue(q, state_count++);
    }
    // Rule 5: Pour from 3L to 4L
    int pour = (x < JUG2_CAP - y) ? x : (JUG2_CAP - y);
    if (!visited[x - pour][y + pour]) {
        visited[x - pour][y + pour] = 1;
        all_states[state_count] = (State){x - pour, y + pour, current_index, "Pour 3L to 4L"};
        printf("  -> Discovered new state: (%d, %d). Adding to queue.\n", x - pour, y + pour);
        enqueue(q, state_count++);
    }
    // Rule 6: Pour from 4L to 3L
    pour = (y < JUG1_CAP - x) ? y : (JUG1_CAP - x);
    if (!visited[x + pour][y - pour]) {
        visited[x + pour][y - pour] = 1;
        all_states[state_count] = (State){x + pour, y - pour, current_index, "Pour 4L to 3L"};
        printf("  -> Discovered new state: (%d, %d). Adding to queue.\n", x + pour, y - pour);
        enqueue(q, state_count++);
    }
}


// The BFS solver!
void solve_bfs() {
    int visited[JUG1_CAP + 1][JUG2_CAP + 1] = {0}; // A map to keep track of where we've been.
    Queue q;
    init_queue(&q);

    // Let's start at the very beginning, a very good place to start. I wanna be the best like I ever was to be the best is my cause
    printf("Starting BFS...\n");
    all_states[state_count++] = (State){0, 0, -1, "Initial State"};
    visited[0][0] = 1;
    printf("Adding initial state (0,0) to queue.\n\n");
    enqueue(&q, 0);

    // Keep going as long as there are states in our to-do list (the queue).
    while (!is_queue_empty(&q)) {
        int current_index = dequeue(&q);
        State current = all_states[current_index];

        printf("Processing state from queue: (%d, %d)\n", current.x, current.y);

        // Did we win?
        if (current.y == TARGET) {
            printf("\nGoal Found! State is (%d, %d).\n", current.x, current.y);
            // In a later step, we'll call the function to print the path here.
            return;
        }

        // If not, let's generate all possible next moves.
        printf("Generating next possible states...\n");
        generate_next_states(current_index, visited, &q);
    }

    printf("Solution not found!\n");
}

// --- main function and other solve_ function stubs ---
void solve_dfs() { printf("DFS function called.\n"); }
void solve_iddfs() { printf("ID-DFS function called.\n"); }

void menu()
{
    int choice;
    int r;
    printf("OPTIONS AVAILABLE:\n");
    printf("1. Breadth First Search (BFS)\n");
    printf("2. Depth First Search (DFS)\n");
    printf("3. Iterative Deepening Depth First Search (ID-DFS)\n");
    printf("4. Exit\n\n");
    printf("Please select an option from above: ");

    r = scanf("%d", &choice);
    if (r!= 1)
    {
        printf("\n You have entered some random stuff");
        getchar(); // Clear the invalid input
        menu();
    }
    switch (choice) {
        case 1:
            solve_bfs();
            break;
        case 2:
            solve_dfs();
            break;
        case 3:
            solve_iddfs();
            break;
        case 4:
            printf("Exiting program.\n");
            break;
        default:
            printf("Invalid choice.\n");
            break;
    }
}


// The main function
int main() {
    menu();
    return 0;
}

