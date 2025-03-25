#include<stdio.h>


int add(int a, int b)
{
	printf("add is called!\n");
    return (a + b);
}
 
int  printSum(int (*f)(), int a, int b)
{
	printf("printSum called!\n");
    return ((*f)(a,b) + 1);

}
int main()
{
    int (*f)();

    f = add;
    
    printf("%u\n", f);

    //printf("Sum = %d\n", (*f)(4, 5));
    //printf("Sum = %d\n", f(4, 5));
    //printf("Sum = %d\n", printSum(add, 4, 5));
    printf("Sum = %d\n", printSum(f, 4, 5));


	return 0;
}
