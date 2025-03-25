/*Find pairs with given sum in a sorted doubly linked list*/

#include<stdio.h>
#include<stdlib.h>

struct node
{
	struct node *prev;
	int info;
	struct node *next;
};

struct node *create_list(struct node *start);
void display(struct node *start);
struct node *addtoempty(struct node *start,int data);
struct node *addatbeg(struct node *start,int data);
struct node *addatend(struct node *start,int data);
struct node *addafter(struct node *start,int data,int item);
struct node *addbefore(struct node *start,int data,int item);
struct node *del(struct node *start,int data);
struct node *reverse(struct node *start);
void pairSum(struct node* start, int sum);
void pairSum_unsorted(struct node* start, int sum);

main()
{
	int choice,data,item;
	struct node *start=NULL;
	/*while(1)
	{
		printf("1.Create List\n");
		printf("2.Display\n");
		printf("3.Add to empty list\n");
		printf("4.Add at beginning\n");
		printf("5.Add at end\n");
		printf("6.Add after\n");
		printf("7.Add before\n");
		printf("8.Delete\n");
		printf("9.Reverse\n");
		printf("10.Quit\n");
		printf("Enter your choice : ");
		scanf("%d",&choice);
		switch(choice)
		{
		 case 1:
			start=create_list(start);
			break;
		 case 2:
			display(start);
			break;
		 case 3:
			printf("Enter the element to be inserted : ");
			scanf("%d",&data);
			start=addtoempty(start,data);
			break;
		 case 4:
	        printf("Enter the element to be inserted : ");
			scanf("%d",&data);
			start=addatbeg(start,data);
			break;
		 case 5: 
			printf("Enter the element to be inserted : ");
			scanf("%d",&data);
			start=addatend(start,data);
			break;
		 case 6:
			printf("Enter the element to be inserted : ");
			scanf("%d",&data);
			printf("Enter the element after which to insert : ");
			scanf("%d",&item);
			start=addafter(start,data,item);
			break;
		 case 7:
			printf("Enter the element to be inserted : ");
			scanf("%d",&data);
			printf("Enter the element before which to insert : ");
			scanf("%d",&item);
			start=addbefore(start,data,item);
			break;
		 case 8:
			printf("Enter the element to be deleted : ");
			scanf("%d",&data);
			start=del(start,data);
	   		break;
		 case 9:
		 	start=reverse(start);
			break;
		 case 10:
			exit(1);
		 default:
			printf("Wrong choice\n");
	}/*End of switch
   }/*End of while*/
   
   start=create_list(start);
   pairSum(start, 7);
   //pairSum_unsorted(start, 7);
   
}/*End of main()*/

struct node *create_list(struct node *start)
{
	int i,n,data;
	printf("Enter the number of nodes : ");
	scanf("%d",&n);
	start=NULL;
	if(n==0)
		return start;
	printf("Enter the element to be inserted : ");
	scanf("%d",&data);
	start=addtoempty(start,data);
		
	for(i=2;i<=n;i++)
	{
		printf("Enter the element to be inserted : ");
		scanf("%d",&data);
		start=addatend(start,data);	
	}
	return start;
}/*End of create_list()*/

void pairSum_unsorted(struct node* start, int sum)
{
	struct node *head1 = start, *head2, *beg = start;
	
	while(head1 != NULL)
	{
		head2 = beg;
		while(head2 != NULL)
		{
			if(head1 != head2 && head1->info + head2->info == sum)
			{
				printf("Sum found! ==> %d %d\n\n", head1->info, head2->info);
				//return;
			}
			head2 = head2->next;
		}
		head1 = head1->next;
	}
}

void pairSum(struct node* start, int sum)
{
	struct node* head = start, *tail = start;
	
	while(tail->next != NULL)
	{
		tail = tail->next;
	}
	
	while(head != NULL && tail != NULL && head != tail)
	{
	
		if(head->info + tail->info == sum)
		{
			printf("Sum found! ==> %d %d\n\n", head->info, tail->info);
			//head = head->next;
			//tail = tail->prev;
			return;
		}
		else
		{
			if(head->info + tail->info < sum)
			{
				head = head->next;
			}
			else
			{
				tail = tail->prev;
			}
		}
	}
	
}




void display(struct node *start)
{
	struct node *p;
	if(start==NULL)
	{
		printf("List is empty\n");
		return;
	}
	p=start;
	printf("List is :\n");
	while(p!=NULL)
	{
		printf("%d ",p->info);
		p=p->next;
	}
	printf("\n");
}/*End of display() */

struct node *addtoempty(struct node *start,int data)
{
	struct node *tmp;
	tmp=(struct node *)malloc(sizeof(struct node));
	tmp->info=data;
	tmp->prev=NULL;
	tmp->next=NULL;
	start=tmp;
	display(start);
	return start;
}/*End of addtoempty( )*/

struct node *addatbeg(struct node *start,int data)
{
	struct node *tmp;
	tmp = (struct node *)malloc(sizeof(struct node));
	tmp->info=data;
	tmp->prev=NULL;
	tmp->next=start;
	start->prev=tmp;
	start=tmp;
	display(start);
	return start;
}/*End of addatbeg( )*/

struct node *addatend(struct node *start,int data)
{
	struct node *tmp,*p;
	tmp=(struct node *)malloc(sizeof(struct node));
	tmp->info=data;
	p=start;
	while(p->next!=NULL)
		p=p->next;
	p->next=tmp;
	tmp->next=NULL;
	tmp->prev=p;
	display(start);
	return start;
}/*End of addatend( )*/

struct node *addafter(struct node *start,int data,int item)
{
	struct node *tmp,*p;
	tmp=(struct node *)malloc(sizeof(struct node));
	tmp->info=data;
	p=start;
	while(p!=NULL)
	{
		if(p->info==item)
		{
			tmp->prev=p;
			tmp->next=p->next;
			if(p->next!=NULL) 
				p->next->prev=tmp;
			p->next=tmp;
			display(start);
			return start;	
		}
		p=p->next;
	}
	printf("%d not present in the list\n\n",item);
	return start;
}/*End of addafter()*/

struct node *addbefore(struct node *start,int data,int item)
{
	struct node *tmp,*q;
	if(start==NULL )
	{
		printf("List is empty\n");
		return start;
	}
	if(start->info==item)
	{
		tmp = (struct node *)malloc(sizeof(struct node));
		tmp->info=data;
		tmp->prev=NULL;
		tmp->next=start;
		start->prev=tmp;
		start=tmp;
		display(start);
		return start;
	}
	q=start;
	while(q!=NULL)
	{
		if(q->info==item)
		{
			tmp=(struct node *)malloc(sizeof(struct node));
			tmp->info=data;
			tmp->prev=q->prev;
			tmp->next = q;
			q->prev->next=tmp;
			q->prev=tmp;
			display(start);
			return start;
		}	
		q=q->next;
	}
	printf("%d not present in the list\n",item);
	return start;
}/*End of addbefore()*/		

struct node *del(struct node *start,int data)
{
	struct node *tmp;
	if(start==NULL)
	{
		printf("List is empty\n");
		return start;
	}
	if(start->next==NULL)	/*only one node in the list*/
		if(start->info==data) 
		{
			tmp=start;
			start=NULL;
			free(tmp);
			display(start);
			return start;
		}
		else
		{
			printf("Element %d not found\n",data);
			return start;
		}
	/*Deletion of first node*/
	if(start->info==data)
	{
		tmp=start;
		start=start->next;  
		start->prev=NULL;
		free(tmp);
		display(start);
		return start;
	}
	/*Deletion in between*/
	tmp=start->next;
	while(tmp->next!=NULL )
	{
		if(tmp->info==data)     
		{
			tmp->prev->next=tmp->next;
			tmp->next->prev=tmp->prev;
			free(tmp);
			display(start);
			return start;
		}
		tmp=tmp->next;
	}
	/*Deletion of last node*/
	if(tmp->info==data)
	{
		tmp->prev->next=NULL;
		free(tmp);
		display(start);
		return start;
	}
	printf("Element %d not found\n",data);
	return start;
}/*End of del()*/

struct node *reverse(struct node *start)
{
	struct node *p1,*p2;
	p1=start;
	p2=p1->next;
	p1->next=NULL;
	p1->prev=p2;
	while(p2!=NULL)
	{
		p2->prev=p2->next;
		p2->next=p1;
		p1=p2;
		p2=p2->prev; 
	}
	start=p1;
	printf("List reversed\n");
	return start;
}/*End of reverse()*/
