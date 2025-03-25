#include<stdio.h>
#include<string.h>



int main()
{
    int a[] = {5, 6, 1, 2, 9}, *p, i;

    //printf("Sizeof int = %zu\n", sizeof(int));

    printf("Accessing using array indices:\n\n");

    for(i = 0; i < 5 ; i++)
    {
        printf("Value = %d at address = %u\n", a[i], &a[i]);
    }

    p = a; //p = a also works

    i = 0;

    printf("Accessing using pointers:\n\n");

    while(i < 1)
    {
        printf("Array: Value = %d at address = %u\n", a[i], &a[i]);
        printf("Pointer *(p + i): Value = %d at address = %u\n", *(p + i), p + i);
        printf("Pointer *(i + p): Value = %d at address = %u\n", *(i + p), i + p);
        //printf("Pointer *p: Value = %d at address = %u\n", *p, p);
        printf("Pointer *(a + i): Value = %d at address = %u\n", *(a + i), (a + i));
        printf("Pointer *(i + a): Value = %d at address = %u\n", *(i + a), (i + a));
        printf("Pointer i[a]: Value = %d at address = %u\n", i[a], &i[a]);

        printf("\n=========================================================\n");

        //p++;
        i++;
    }



	return 0;
}
