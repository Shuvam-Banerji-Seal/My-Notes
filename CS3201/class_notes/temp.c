#include <stdio.h>


int main()
{
  int i,j, n;
  printf("Enter the number of row:\n");
  scanf("%d",&i);
  printf("Enter the number of column:\n");
  scanf("%d",&j);
  int a[i][j];
  printf("Enter the elements of the matrix:\n");
  for(n=0; n<i; n++)
  {
    for(int m=0; m<j; m++)
    {
      scanf("%d",&a[n][m]);
    }
  }
  for(n=0; n<i; n++)
  {
    for(int m=0; m<j; m++)
    {
      printf("%d\t",a[n][m]);
    }
    printf("\n");
  }
  return 0;
}

