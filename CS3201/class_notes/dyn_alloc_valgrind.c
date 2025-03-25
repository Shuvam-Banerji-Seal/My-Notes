#include<stdio.h>
#include<stdlib.h>

void main()
{
	int **marks;
	
	
	//********************1-D case********************
	int *x, *y;
	
	int n, m, i, j;
	
	printf("The value of n? ");
	scanf("%d", &n);
	
	printf("\nThe value of m? ");
	scanf("%d", &m);
	
	x = (int*)malloc(n*sizeof(int));
	
	printf("%u\n", x);
	
	//free(x);
	
	//x = (int*)malloc(n*sizeof(int));
	
	//printf("%u\n", x);
	
	y = (int*)malloc(m*sizeof(int));

	free(x);
	free(y);
	
	//************************2-D case***********************
	
	/*marks = (int**)malloc(n*sizeof(int*));
	
	for(i = 0; i < n; i++)
	{
		marks[i] = (int*)malloc(m*sizeof(int));
	}
	
	for(i = 0; i < n; i++)
	{
		for(j = 0; j < m; j++)
		{
			marks[i][j] = i+j;
		}
	
	}
	
	for(i = 0; i < n; i++)
	{
		for(j = 0; j < m; j++)
		{
			printf("%d ", marks[i][j]);
		}
		printf("\n");
	
	}
	
	//FREEing (in this order recommended)
	
	for(i = 0; i < n; i++)
	{
		free(marks[i]);
	}*/
	

	//free(marks);
}
