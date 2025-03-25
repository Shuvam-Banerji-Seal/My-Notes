#include<stdio.h>
#include<string.h>

void swap_value(int a, int b)
{
    int t;

    t = a;
    a = b;
    b = t;

    printf("In swap_value: address of a = %u, address of b = %u\n\n", &a, &b);
}

int swap_ref(int* a, int* b)
{
    int t;

    t = *a;
    *a = *b;
    *b = t;

    printf("In swap_ref: address of a = %u, address of b = %u\n\n", a, b);
}


int main()
{
    int a = 5, b = 10;

    printf("In main: address of a = %u, address of b = %u\n\n", &a, &b);

    printf("Call by value:\n\n");
    printf("Before swap: a = %d b = %d\n", a, b);
    swap_value(a, b);
    printf("After swap: a = %d b = %d\n", a, b);

    printf("\nCall by reference:\n\n");
    printf("Before swap: a = %d b = %d\n", a, b);
    swap_ref(&a, &b);
    printf("After swap: a = %d b = %d\n", a, b);

	return 0;
}
