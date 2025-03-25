#include<stdio.h>
#include<string.h>



int main()
{
    int a[] = {5, 6, 1, 2, 9}, *p, i;

    /*printf("Sizeof int = %zu\n", sizeof(int));

    printf("Accessing using array indices:\n\n");

    for(i = 0; i < 5 ; i++)
    {
        printf("Value = %d at address = %u\n", a[i], &a[i]);
    }*/

    p = &a[0]; //p = a also works
    //p = p - 1;

    i = 0;

    printf("Accessing using pointers:\n\n");

    while(i < 4)
    {
        printf("Pointer *p: Value = %d address = %u\n", *p, p);

        p++;


        i++;
    }



	return 0;
}
