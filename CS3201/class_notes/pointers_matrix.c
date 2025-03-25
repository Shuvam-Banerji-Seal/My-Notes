#include<stdio.h>
#include<string.h>

int main()
{
    int a[2][3] = {{5, 6, 1}, {2, 9, 7}}, *p, (*q)[3], *r, i , j, noOfRows = 2, noOfCols = 3;

    

    printf("Printing the element-wise addresses:\n");

    for(i = 0; i < noOfRows; i++)
    {
        for(j = 0; j < noOfCols; j++)
        {
            printf("%u ", &a[i][j]);
        }
        printf("\n");
    }

    printf("\n\n");

    printf("Pointers to 0th row, 1st row: %u %u\n", &a[0][0], &a[1][0]);//Pointers to the 0th row, 1st row
    printf("Pointers to 0th row, 1st row: %u %u\n", *a, *(a + 1));
    
    printf("Pointers to the (0,0)th, (1,0)th elements: %u %u\n", &a[0][0], &a[1][0]);//Pointers to the (0,1)th, (1,1)th elements
    printf("Pointers to the (0,0)th, (1,0)th elements: %u %u\n", *(a + 0) + 0, *(a + 1) + 0);

    //printf("Pointers to the (0,1)th, (1,1)th elements: %u %u\n", &a[0][1], &a[1][1]);//Pointers to the (0,1)th, (1,1)th elements
    //printf("Pointers to the (0,1)th, (1,1)th elements: %u %u\n", *(a + 0) + 1, *(a + 1) + 1);
    //printf("Pointers to the %u\n", *(*(a+1)+1));
	
    printf("\n\n");

    //p = (int*)a;
    p = a;

    printf("Using a in pointer form...\n\n");

    for(i = 0; i < noOfRows; i++)
    {
        for(j = 0; j < noOfCols; j++)
        {
            printf("%d ", *(*(a + i) + j));
        }
        printf("\n");
    }


    printf("\n\n");

    printf("Using p...\n\n");

    for(i = 0; i < noOfRows; i++)
    {
        for(j = 0; j < noOfCols; j++)
        {
            //printf("%d ", *(p + i*noOfCols + j));
            printf("%u ", (p + i*noOfCols + j));
        }
        printf("\n");
    }
/*
    printf("\n\n");
    
    printf("Using q..\n\n");

    q = a;

    for(i = 0; i < noOfRows; i++)
    {
        r = q + i;
        for(j = 0; j < noOfCols; j++)
        {
            printf("%d ", *(r + j));
        }
        printf("\n");
    }

    printf("\n\n");

    */



	return 0;
}
