#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define JUG1_CAP 3
#define JUG2_CAP 4
#define TARGET 2
#define MAX_STATES 100

typedef struct {
    int x, y;           // x: water in 3L jug, y: water in 4L jug
    int parent_index;   // Index of the parent state in the all_states array
    const char* action; // The action taken to reach this state
    int depth;          // Depth of the state in the search tree (for ID-DFS)
} State;

// --- Global array to store all unique states discovered ---
State all_states[MAX_STATES];
int state_count = 0;

// --- Queue for BFS ---
typedef struct {
    int items[MAX_STATES];
    int front, rear;
} Queue;

void init_queue(Queue* q) { q->front = 0; q->rear = -1; }
int is_queue_empty(Queue* q) { return q->rear < q->front; }
void enqueue(Queue* q, int value) { q->items[++q->rear] = value; }
int dequeue(Queue* q) { return q->items[q->front++]; }

// --- Stack for DFS/ID-DFS ---
typedef struct {
    int items[MAX_STATES];
    int top;
} Stack;

void init_stack(Stack* s) { s->top = -1; }
int is_stack_empty(Stack* s) { return s->top == -1; }
void push(Stack* s, int value) { s->items[++s->top] = value; }
int pop(Stack* s) { return s->items[s->top--]; }


// GNUuuuuuuuuuuuuuuuuu PLot

// Generates a PNG image for a given state using gnuplot
void plot_state(int x, int y, int step) {
    char filename[50];
    sprintf(filename, "step_%02d.png", step);

    FILE *gnuplot_pipe = popen("gnuplot -persistent", "w");
    if (gnuplot_pipe) {
        fprintf(gnuplot_pipe, "set terminal pngcairo size 400,400 enhanced font 'Verdana,10'\n");
        fprintf(gnuplot_pipe, "set output '%s'\n", filename);
        fprintf(gnuplot_pipe, "set title 'Water Jug State (%d, %d)'\n", x, y);
        fprintf(gnuplot_pipe, "set boxwidth 0.5\n");
        fprintf(gnuplot_pipe, "set style fill solid 0.5\n");
        fprintf(gnuplot_pipe, "set yrange [0:%d]\n", JUG2_CAP + 1);
        fprintf(gnuplot_pipe, "set xrange [-1:2]\n");
        fprintf(gnuplot_pipe, "set xtics ('%dL Jug' 0, '%dL Jug' 1)\n", JUG1_CAP, JUG2_CAP);
        fprintf(gnuplot_pipe, "set ylabel 'Liters'\n");
        fprintf(gnuplot_pipe, "unset key\n");
        fprintf(gnuplot_pipe, "plot '-' with boxes\n");
        fprintf(gnuplot_pipe, "0 %d\n", x);
        fprintf(gnuplot_pipe, "1 %d\n", y);
        fprintf(gnuplot_pipe, "e\n");
        fflush(gnuplot_pipe);
        pclose(gnuplot_pipe);
    } else {
        printf("Error: Could not open gnuplot.\n");
    }
}

// Creates an animated GIF from the generated PNGs using ImageMagick
void create_animation() {
    printf("\n--- Creating Animation (solution.gif) ---\n");
    // Using ImageMagick's 'convert' command for higher quality GIF.
    // Sorry as I couldn't find a better way to make the animation of the water jug problem. Python has got many modules but in C a lot of the things need
    // frrom scratch
    char command[] = "convert -delay 100 -loop 0 step_*.png solution.gif";

    int result = system(command);

    if (result == 0) {
        printf("Animation 'solution.gif' created successfully using ImageMagick.\n");
    } else {
        printf("Error: Could not create animation.\n");
        printf("Please ensure ImageMagick is installed (e.g., 'sudo apt-get install imagemagick').\n");
    }
}

// Prints the solution path and triggers plotting
void print_and_plot_path(int goal_index) {
    int path[MAX_STATES];
    int count = 0;
    int current_index = goal_index;

    while (current_index != -1) {
        path[count++] = current_index;
        current_index = all_states[current_index].parent_index;
    }

    printf("\n-----------------------------------------------------\n");
    printf("Goal Found! Following are the steps to follow:\n");
    printf("Initial State: (0, 0)\n");

    // Print path in correct order and generate plots
    plot_state(0, 0, 0); // Plot initial state
    int step_count = 1;
    for (int i = count - 1; i >= 0; i--) {
        State s = all_states[path[i]];
        // Only print the action if it's not the initial state (parent_index is -1)
        if (s.parent_index != -1) {
            printf("%s : (%d, %d)\n", s.action, s.x, s.y);
        }
        // Plot every state in the path except for the duplicate initial one
        if(s.parent_index != -1 || i == count -1) {
             plot_state(s.x, s.y, step_count++);
        }
    }
    printf("-----------------------------------------------------\n");
    create_animation();
}



// Adds a new state to the global list if it's unique
int add_state(int x, int y, int parent_index, const char* action, int depth) {
    if (state_count >= MAX_STATES) {
        printf("Max states reached!\n");
        return -1;
    }
    all_states[state_count] = (State){x, y, parent_index, action, depth};
    return state_count++;
}

// Generates all possible next states from a given state
void generate_next_states(int current_index, int visited[][JUG2_CAP + 1], void* data_structure, const char* type, int depth_limit) {
    State current = all_states[current_index];
    int x = current.x;
    int y = current.y;
    int new_depth = current.depth + 1;

    // For ID-DFS, don't generate states beyond the depth limit
    if (depth_limit != -1 && new_depth > depth_limit) {
        return;
    }

    // Operation 1: Fill 3L jug
    if (!visited[JUG1_CAP][y]) {
        int new_index = add_state(JUG1_CAP, y, current_index, "Fill 3L jug from faucet", new_depth);
        visited[JUG1_CAP][y] = 1;
        if (strcmp(type, "queue") == 0) enqueue((Queue*)data_structure, new_index);
        else push((Stack*)data_structure, new_index);
    }
    // Operation 2: Fill 4L jug
    if (!visited[x][JUG2_CAP]) {
        int new_index = add_state(x, JUG2_CAP, current_index, "Fill 4L jug from faucet", new_depth);
        visited[x][JUG2_CAP] = 1;
        if (strcmp(type, "queue") == 0) enqueue((Queue*)data_structure, new_index);
        else push((Stack*)data_structure, new_index);
    }
    // Operation 3: Empty 3L jug
    if (!visited[0][y]) {
        int new_index = add_state(0, y, current_index, "Empty 3L jug down drain", new_depth);
        visited[0][y] = 1;
        if (strcmp(type, "queue") == 0) enqueue((Queue*)data_structure, new_index);
        else push((Stack*)data_structure, new_index);
    }
    // Operation 4: Empty 4L jug
    if (!visited[x][0]) {
        int new_index = add_state(x, 0, current_index, "Empty 4L jug down drain", new_depth);
        visited[x][0] = 1;
        if (strcmp(type, "queue") == 0) enqueue((Queue*)data_structure, new_index);
        else push((Stack*)data_structure, new_index);
    }
    // Operation 5: Pour from 3L to 4L
    int pour = (x < JUG2_CAP - y) ? x : (JUG2_CAP - y);
    if (!visited[x - pour][y + pour]) {
        int new_index = add_state(x - pour, y + pour, current_index, "Fill 4L jug using water from 3L jug", new_depth);
        visited[x - pour][y + pour] = 1;
        if (strcmp(type, "queue") == 0) enqueue((Queue*)data_structure, new_index);
        else push((Stack*)data_structure, new_index);
    }
    // Operation 6: Pour from 4L to 3L
    pour = (y < JUG1_CAP - x) ? y : (JUG1_CAP - x);
    if (!visited[x + pour][y - pour]) {
        int new_index = add_state(x + pour, y - pour, current_index, "Fill 3L jug using water from 4L jug", new_depth);
        visited[x + pour][y - pour] = 1;
        if (strcmp(type, "queue") == 0) enqueue((Queue*)data_structure, new_index);
        else push((Stack*)data_structure, new_index);
    }
}

// --- Solver Functions ---

void solve_bfs() {
    int visited[JUG1_CAP + 1][JUG2_CAP + 1] = {0};
    Queue q;
    init_queue(&q);

    int initial_index = add_state(0, 0, -1, "Initial State", 0);
    visited[0][0] = 1;
    enqueue(&q, initial_index);

    while (!is_queue_empty(&q)) {
        int current_index = dequeue(&q);
        State current = all_states[current_index];

        // *** CORRECTED GOAL CHECK ***
        if (current.y == TARGET) {
            print_and_plot_path(current_index);
            return;
        }
        generate_next_states(current_index, visited, &q, "queue", -1);
    }
    printf("Solution not found!\n");
}

void solve_dfs() {
    int visited[JUG1_CAP + 1][JUG2_CAP + 1] = {0};
    Stack s;
    init_stack(&s);

    int initial_index = add_state(0, 0, -1, "Initial State", 0);
    visited[0][0] = 1;
    push(&s, initial_index);

    while (!is_stack_empty(&s)) {
        int current_index = pop(&s);
        State current = all_states[current_index];

    
        if (current.y == TARGET) {
            print_and_plot_path(current_index);
            return;
        }
        generate_next_states(current_index, visited, &s, "stack", -1);
    }
    printf("Solution not found!\n");
}

void solve_iddfs() {
    for (int depth_limit = 0; ; depth_limit++) {
        printf("Trying with depth limit: %d\n", depth_limit);
        int visited[JUG1_CAP + 1][JUG2_CAP + 1] = {0};
        Stack s;
        init_stack(&s);
        
        // Reset global state for each iteration
        state_count = 0; 
        int initial_index = add_state(0, 0, -1, "Initial State", 0);
        visited[0][0] = 1;
        push(&s, initial_index);
        
        int found_at_this_depth = 0;

        while (!is_stack_empty(&s)) {
            int current_index = pop(&s);
            State current = all_states[current_index];

            // *** CORRECTED GOAL CHECK ***
            if (current.y == TARGET) {
                print_and_plot_path(current_index);
                return; // Solution found, exit completely
            }
            
            if (current.depth < depth_limit) {
                 generate_next_states(current_index, visited, &s, "stack", depth_limit);
            } else {
                 found_at_this_depth = 1;
            }
        }
        
        // If no solution was found and no nodes were left to expand at the limit,
        // it means the entire tree has been explored.
        if (!found_at_this_depth && is_stack_empty(&s)) {
            break;
        }
    }
    printf("Solution not found!\n");
}


// --- Main Function ---

int main() {
    int choice;
    printf("****************************************\n");
    printf("        Water Jug Problem Solver        \n");
    printf("****************************************\n");
    printf("OPTIONS AVAILABLE:\n");
    printf("1. Breadth First Search (BFS)\n");
    printf("2. Depth First Search (DFS)\n");
    printf("3. Iterative Deepening Depth First Search (ID-DFS)\n");
    printf("4. Exit\n\n");
    printf("Please select an option from above: ");
    scanf("%d", &choice);

    // Clean up old image files before starting
    system("rm -f step_*.png solution.gif");

    switch (choice) {
        case 1:
            printf("\nYou have selected BFS. Following are the steps to follow.\n");
            solve_bfs();
            break;
        case 2:
            printf("\nYou have selected DFS. Following are the steps to follow.\n");
            solve_dfs();
            break;
        case 3:
            printf("\nYou have selected ID-DFS. Following are the steps to follow.\n");
            solve_iddfs();
            break;
        case 4:
            printf("Exiting program.\n");
            break;
        default:
            printf("Invalid choice. Please run the program again.\n");
            break;
    }

    return 0;
}
