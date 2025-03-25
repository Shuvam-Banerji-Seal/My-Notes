#include<stdio.h>

void main()
{
	int x;
	float sum = 0.0;
	
	int i;
	
	for(i = 5; i >  -2; i--)
	{
		sum += 100/i;
	} 
	
	printf("%f\n", sum);

}
