/*P4.2 Program of stack using linked list*/

#include<stdio.h>
#include<stdlib.h>

struct node
{
	int info;
	struct node *link;
};

void push(int item, struct node **top);
int pop(struct node **top);
int peek(struct node *top);
int isEmpty(struct node *top);
void display(struct node *top);

main()
{
	int choice,item;
	struct node *top = NULL;
	
	while(1)
	{      	
		printf("1.Push\n");
		printf("2.Pop\n");
		printf("3.Display item at the top\n");
		printf("4.Display all items of the stack\n");
		printf("5.Quit\n");
		printf("Enter your choice : ") ;
		scanf("%d", &choice);

		switch(choice)
		{
		case 1:
			printf("Enter the item to be pushed : ");
			scanf("%d",&item);
			push(item, &top);
			break;
		case 2:
			item=pop(&top);
			printf("Popped item is : %d\n",item);
			break;
		case 3:
			printf("Item at the top is %d\n",peek(top));
			break;
		case 4:
			display(top);
			break;
		case 5:
			exit(1);
		default :
			printf("Wrong choice\n");
		}/*End of switch */
	}/*End of while */
}/*End of main() */

void push(int item, struct node** top)
{
	struct node *tmp;
	tmp=(struct node *)malloc(sizeof(struct node));
	if(tmp==NULL)
	{
		printf("Stack Overflow\n");
		return;
	}
	tmp->info=item;
	tmp->link=*top;
	*top=tmp;
}/*End of push()*/

int pop(struct node** top)
{
	struct node *tmp;
	int item;
	if( isEmpty(*top) )
	{
		printf("Stack Underflow\n");
		exit(1);
	}
	tmp=*top;
	item=tmp->info;
	*top=(*top)->link;
	free(tmp);
	return item;
}/*End of pop()*/

int peek(struct node* top)
{
	if( isEmpty(top) )
	{
		printf("Stack Underflow\n");
		exit(1);
	}
	return top->info;
}/*End of peek() */

int isEmpty(struct node* top)
{
	if(top == NULL)
		return 1;
	else
		return 0;
}/*isEmpty()*/


void display(struct node *top)
{       
	struct node *ptr;
	ptr=top;
	/*if(isEmpty(top))
	{	
		printf("Stack is empty\n");
		return;
	}*/
	printf("Stack elements :\n\n");
	while(ptr!=NULL)
	{
		printf(" %d\n",ptr->info);
		ptr=ptr->link;
	}
	printf("\n");
}/*End of display()*/
