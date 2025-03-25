#include<stdio.h>

void display2D(int arr[][5], int rows) //int (*arr)[5] also works
{
	int i, j;
	
	for(i = 0; i < rows; i++)
	{
		for(j = 0; j < 5; j++)
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
	
	for(i = 0; i < rows; i++)
	{
		for(j = 0; j < cols; j++)
		{
			//printf("%d ", arr[i][j]);
			printf("%d ", *(arr + i*cols + j));
		}
		printf("\n");
	}

}

void update2D(int arr[][5], int rows) //int (*arr)[5] also works
{
	int i, j;
	
	for(i = 0; i < rows; i++)
	{
		for(j = 0; j < 5; j++)
		{
			//printf("%d ", arr[i][j]);
			//printf("%d ", *(arr + i*5 + j));
			if(arr[i][j] < 5)
			{
				arr[i][j] += 2;
			}
		}
		printf("\n");
	}

}


void update1Dptr(int *arr, int rows, int cols) 
{
	int i, j;
	
	for(i = 0; i < rows; i++)
	{
		for(j = 0; j < cols; j++)
		{
			//printf("%d ", arr[i][j]);
			//printf("%d ", *(arr + i*cols + j));
			if(*(arr + i*cols + j) < 5)
			{
				*(arr + i*cols + j) += 2;
			}
			
			
		}
		printf("\n");
	}

}

void main()
{
	int array[2][5] = {{1, 2, 3, 4, 6}, 
			 {9, 10, 11, 12, 15}};
			 
			 
	display2D(array, 2);	
	display1Dptr(&array[0][0], 2, 5);		 
	//update2D(array, 2);
	//display2D(array, 2);
	//update1Dptr(&array[0][0], 2, 5);
	//display1Dptr(&array[0][0], 2, 5);
	
	

}
