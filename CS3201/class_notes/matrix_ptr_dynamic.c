#include<stdio.h>
#include<string.h>
#include<stdlib.h>


void display2D(int arr[][3], int rows) //int (*arr)[3] also works
{
	int i, j;
	
	printf("\nThe matrix, in array notation:\n\n");
	
	for(i = 0; i < rows; i++)
	{
		for(j = 0; j < 3; j++)
		{
			printf("%d ", arr[i][j]);
			//printf("%d ", *(arr + i*5 + j));
		}
		printf("\n");
	}

}


void display1Dptr(int *arr, int rows, int cols) 
{
	int i, j;
	
	printf("\nThe matrix, in pointer notation:\n\n");
	
	for(i = 0; i < rows; i++)
	{
		for(j = 0; j < cols; j++)
		{
			//printf("%d ", arr[i][j]);
			printf("%d %u ", *(arr + i*cols + j), arr + i*cols + j);
		}
		printf("\n");
	}

}

void display1Dptr2ptr(int **arr, int rows, int cols) 
{
	int i, j;
	
	printf("\nThe matrix, in pointer to pointer notation:\n\n");
	
	for(i = 0; i < rows; i++)
	{
		for(j = 0; j < cols; j++)
		{
			//printf("%u %d ", &arr[i][j], arr[i][j]);
			printf("%u %d ", (*(arr+i) + j), *(*(arr+i) + j));
		}
		printf("\n");
	}

}



void main()
{
	int arr[2][3] = {{1, 2, 3}, {4, 5, 6}}; //Reference matrix
	int **arr_dyn;
	
	int no_r, no_c, j, l;
	
	printf("How many rows?\n");
	
	scanf("%d", &no_r);
	
	printf("How many columns?\n");
	
	scanf("%d", &no_c);
	
	arr_dyn = (int**)malloc(no_r*sizeof(int*));
	
	
	printf("Address of arr_dyn[0] = %u arr_dyn[1]=%u\n\n", &arr_dyn[0], &arr_dyn[1]);
	
	//**********************CONTIGUOUS********************
	
	arr_dyn[0] = (int*) malloc(no_r*no_c*sizeof(int));
	
	for(j = 1; j < no_r; j++)
	{
		arr_dyn[j] = arr_dyn[0] + j*no_c;
	} 
	
	for(j = 0; j < no_r; j++)
	{
		
		
		for(l = 0; l < no_c; l++)
		{
			printf("Element - (%d, %d)? ", j, l);
		
			scanf("%d", &arr_dyn[j][l]);
		}
		
		printf("\n");
		
		
		
		
	}
	
	//***********************NON CONTIGUOUS**********************
		
	/*for(j = 0; j < no_r; j++)
	{
		arr_dyn[j] = (int*)malloc(no_c*sizeof(int));
		
		for(l = 0; l < no_c; l++)
		{
		
		
			printf("Element - (%d, %d)? ", j, l);
		
			scanf("%d", &arr_dyn[j][l]);
		}	
		
		
	}*/
	
	//**************************************************
	
	
	for(j = 0; j < no_r; j++)
	{
		
		
		for(l = 0; l < no_c; l++)
		{
			printf("%d %lu\t", arr_dyn[j][l], &arr_dyn[j][l]);
		}
		
		printf("\n");
		
		
		
		
	}
	
	printf("\n\n");
	
	
	for(j = 0; j < no_r; j++)
	{
		
		
		for(l = 0; l < no_c; l++)
		{
			printf("%d %lu\t", *(*(arr_dyn+j)+l), *(arr_dyn+j)+l);
		}
		
		printf("\n");
		
		
		
		
	}
	
	//display2D(arr_dyn, 2);

	//display1Dptr(&arr[0][0], 2, 3);	
	//display1Dptr(arr_dyn, 2, 3);	
	//display1Dptr2ptr(arr_dyn, 2, 3); 
	
	//********************CONTIGUOUS**********************
	
	free(arr_dyn[0]);
	free(arr_dyn);
	
	
	//********************NON CONTIGUOUS*****************
	
	/*for(j = 0; j < no_r; j++)
	{
		free(arr_dyn[j]);
	}
	
	free(arr_dyn);*/
	
	
	
	
	
}
