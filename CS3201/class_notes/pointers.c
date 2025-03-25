#include<stdio.h>
#include<string.h>



int main()
{
    int x = 5, y;
    int *p;

    p = &x;

    //y = *p;
    
    /*printf("%d %d\n", x, *p);

    printf("x = %d is stored at address &x = %u\n", x, &x);
    
    printf("x = %d is stored at address &x = %u\n", *&x, &x);
    printf("Using p: x = %d is stored at address &x = %u\n", *p, p);
    
    printf("Using p, y: x = %d is stored at address &x = %u\n", y, &*p);
    //printf("p = %u is stored at address &p = %u\n", p, &p);
    //printf("y = %d is stored at address &y = %u\n", y, &y);*/

    printf("Changing the value of x via p...\n\n");

	//x++;
    //*p = *p + 1;
    (*p)++;
    //y++;

    printf("x = %d is stored at address &x = %u\n", x, &x);
    //printf("x = %d is stored at address &x = %u\n", *p, p);
    

	return 0;
}
