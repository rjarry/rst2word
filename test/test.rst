.. |Authors| replace:: Robin Jarry, Gregory Boissinot
.. |Company| replace:: AB LogiX
.. |Date| date:: 
.. |Title| replace:: RST 2 Word
.. |Subject| replace:: Yeah
.. |Doc_id| replace:: 46655 54684621 1321354

--------------------------------

.. contents:: Table of Contents
   :depth: 2

.. raw:: excel
    :file: super.xls



One of the more useful and complex |Doc_id| features of C is its use of pointers. With pointers, 
you can create complex data structures like linked lists and trees. Figure 17-1 
illustrates some of these data structures. 

.. figure:: img/fig17-1.jpg
    :align: center

    Figure 17-1. How pointers may be used



Up to now, all of our data structures have been allocated by the compiler as either 
permanent or temporary variables. With pointers, we can create and allocate 
dynamic data structures that can grow or shrink as needed. In this chapter, you will 
learn how to use some of the more common dynamic data structures. 

========  ========  =========
Colonne1  Colonne1  Colonne1
========  ========  =========
klsjd     slkdjf    flskdj
mlsk      msdlkfm   mldskfms
mlsk      msdlkfm   mldskfms
mlsk      msdlkfm   mldskfms
mlsk      msdlkfm   mldskfms
mlsk      msdlkfm   mldskfms
========  ========  =========


Pointers and Structures
#######################

Structures can contain pointers, even a pointer to another instance of the same 
structure. In the following example: ::

    struct node {  
        struct node *next_ptr;    /* Pointer to the next node */ 
        int value;                /* Data for this node */ 
    }

the structure ``node`` is illustrated in Figure 17-2. This structure contains two fields, 
one named ``value``, shown here as the section containing the number 2. The other is 
a pointer to another structure. The field ``next_ptr`` is shown as an arrow. 

.. figure:: img/fig17-2.jpg
    :align: center

    Figure 17-2. Node

The question is: how do we create ``nodes``? We could declare them explicitly: ::

    struct node *node_1; 
    struct node *node_2; 

and so on. The problem with this structure is that we can declare only a limited 
number of nodes. What we need is a procedure to which we can say, "I want a new 
node", and then have the procedure create the node for us.

The malloc function
===================

The procedure ``malloc`` does the job. It allocates storage for a variable and then 
returns a pointer. It is used to create new things out of thin air (actually out of an 
area of memory called the *heap*). Up to now, we've used pointers solely to point to 
named variables. So if we used a statement like: ::

    int data;  
    int *number_ptr;  
    number_ptr = &data; 

the thing that we are pointing to has a name (``data``). The function ``malloc`` creates a 
new, unnamed variable and returns a pointer to it. The "things" created by ``malloc`` 
can be referenced only through pointers, never by name. 

The definition of ``malloc`` is: ::

    void *malloc(unsigned int); 

The function ``malloc`` takes a single argument: the number of bytes to allocate. If 
``malloc`` runs out of memory, it returns a null pointer.  

In the declaration, ``void *`` is used to indicate that malloc returns a generic pointer
(a pointer that can point to any type of thing). So C uses void for two purposes: 

+ When used as a type in a function declaration, ``void`` indicates that the 
  function returns no value.
+ When used in a pointer declaration, ``void`` defines a generic pointer.

We will start using ``malloc`` by allocating space for simple structures. As we go on, we
will see how to create bigger structures and link them together to form very complex
data structures. Example 17-1 allocates storage for a character string 80 bytes long
(``'\0'`` included). The variable ``string_ptr`` points to this storage. 

Allocating Memory for a String 
""""""""""""""""""""""""""""""
::

    [#include <stdlib.h>] 
    main()  
    {  
        /* Pointer to a string that will be allocated from the heap */ 
        char *string_ptr; 
        
        string_ptr = malloc(80); 


Allocating Memory for a structure
"""""""""""""""""""""""""""""""""

Suppose we are working on a complex database that contains (among other things) 
a mailing list. The structure person is used to hold the data for each person: ::

    struct person {
        char    name[30];           /* name of the person */
        char    address[30];        /* where he lives */
        char    city_state_zip[30]; /* Part 2 of address */
        int     age;                /* his age */
        float   height;             /* his height in inches */
    }

We could use an array to hold our mailing list, but an ar ray is an inefficient use of 
memory. Every entry takes up space, whether or not it is used. What we need is a 
way to allocate space for only those entries that are used. We can use ``malloc`` to 
allocate space on an as-needed basis.

To create a new person, we use the code: ::

    /* Pointer to a person structure to be allocated from the heap */ 
    struct person *new_item_ptr;
    
    new_item_ptr = malloc(sizeof(struct person)); 

Allocation Errors
"""""""""""""""""

We determine the number of bytes to allocate by using the expression 
``sizeof(struct person)``. Without the ``sizeof`` operator, we would have to count the 
number of bytes in our structure, a difficult and error-prone operation.   
The size of the heap, although large, is finite. When ``malloc`` runs out of room, it will 
return a ``NULL`` pointer. Good programming practice tells you to check the return 
value of each ``malloc`` call to ensure that you really got the memory. :: 

    new_item_ptr = malloc(sizeof(struct person));  
    if (new_item_ptr == NULL) { 
        fprintf(stderr, "Out of memory\n"); 
        exit (8); 
    } 

Although checking the return value of ``malloc`` is good programming practice, far too 
often the check is omitted and the programmer assumes that he got the memory 
whether on not he really did. The result is that far too many programs crash when 
they run out of memory.

The problem has gotten so bad that when C++ was designed, it contained a special 
error handling mechanism for out-of-memory conditions. 

free Function
=============

The function ``malloc`` gets memory from the heap. To free that memory after you are 
done with it, use the function ``free``. The general form of the ``free`` function is: ::

    free(pointer);
    pointer = NULL;

where pointer is a pointer previously allocated by ``malloc``. (We don't have to set 
pointer to ``NULL`` ; however, doing so prevents us from trying to used freed memory.) 

The following is an example that uses ``malloc`` to get storage and ``free`` to dispose of 
it: ::

    const int DATA_SIZE = (16 * 1024); /* Number of bytes in the buffer */ 
    void copy(void)  
    {  
        char *data_ptr;        /* Pointer to large data buffer */  
        data_ptr = malloc(DATA_SIZE);        /* Get the buffer */  
        /*  
         * Use the data buffer to copy a file   
         */   
        free(data_ptr);  
        data_ptr = NULL; 
    } 

But what happens if we forget to free our pointer? The buffer becomes dead. That is, 
the memory management system thinks that the buffer is being used, but no one is 
using it. If the ``free`` statement was removed from the function ``copy``, then each 
successive call would eat up another 16K of memory. Do this often enough and your 
program will run out of memory.

The other problem that can occur is using memory that has been freed. When ``free`` 
is called, the memory is returned to the memory pool and can be reused. Using a 
pointer after a ``free`` call is similar to an out-of-bounds error for an index to an array. 
You are using memory that belongs to someone else. This error can cause 
unexpected results or program crashes.  

Linked List
###########

Suppose you are writing a program that displays a series of flash cards as a teaching 
drill. The problem is that you don't know ahead of time how many cards the user will 
supply. One solution is to use a linked-list data structure. In that way, the list can 
grow as more cards are added. Also, as we will see later, linked lists may be 
combined with other data structures to handle extremely complex data. 

A *linked list* is a chain of items in which each item points to the next one in the chain. 
Think about the treasure hunt games you played when you were a kid. You were 
given a note that said, "Look in the mailbox." Racing to the mailbox you found your 
next clue, "Look in the big tree in the back yard," and so on until you found your 
treasure (or you got lost). In a treasure hunt, each clue points to the next one.

A linked list is shown in Figure 17-3.

.. figure:: img/fig17-3.jpg
    :align: center

    Figure 17-3. Linked list

Data Structures
===============

The structure declarations for a linked list are: ::

    struct linked_list {
        char    data[30];             /* data in this element */
        struct linked_list *next_ptr; /* pointer to next element */
    };

    struct linked_list *first_ptr = NULL;

The variable ``first_ptr`` points to the first element of the list. In the beginning, 
before we insert any elements into the list (the list is empty), this variable is 
initialized to ``NULL``.  

Insert an element in the list
=============================

In Figure 17-4, a new element is created and then inserted at the beginning of an 
existing list. To insert a new element into a linked list in C, we execute the following 
steps:   

1. Create a structure for the item: ``new_item_ptr = malloc(sizeof(struct linked_list));``
2. Store the item in the new element: ``(*new_item_ptr).data = item;``
3. Make the first element of the list point to the new element: ``(*new_item_ptr).next_ptr = first_ptr;`` 
4. The new element is now the first element: ``first_ptr = new_item_ptr;`` 

.. figure:: img/fig17-4.jpg
    :align: center

    Figure 17-4. Adding new element to beginning of list

The code for the actual program is: ::

    void add_list(char *item)  
    {  
        /* pointer to the next item in the list */  
        struct linked_list *new_item_ptr;   
     
        new_item_ptr = malloc(sizeof(struct linked_list));  
        strcpy((*new_item_ptr).data, item);   
        (*new_item_ptr).next_ptr = first_ptr;   
        first_ptr = new_item_ptr;  
    }

To see if the name is in the list, we must search each element of the list until we 
either find the name or run out of data. Example 17-2 contains the ``find`` program, 
which searches through the items in the list.   

Example: find/find.c
"""""""""""""""""""""

::

    #include <stdio.h> 
    #include <string.h> 
     
    struct linked_list { 
       struct linked_list *next_ptr;        /* Next item in the list */ 
       char *data;                          /* Data for the list */ 
    }; 
     
    struct linked_list *first_ptr; 
    /******************************************************** 
     * find ## Looks for a data item in the list.           * 
     *                                                      * 
     * Parameters                                           * 
     *      name ## Name to look for in the list.           * 
     *                                                      * 
     * Returns                                              * 
     *      1 if name is found.                             * 
     *      0 if name is not found.                         * 
     ********************************************************/ 
    int find(char *name) 
    { 
        /* current structure we are looking at */ 
        struct linked_list *current_ptr; 
     
        current_ptr = first_ptr; 
     
        while ((strcmp(current_ptr->data, name) != 0) && 
               (current_ptr != NULL)) 
            current_ptr = (*current_ptr)->next_ptr; 
     
        /* 
         * If current_ptr is null, we fell off the end of the list and 
         * didn't find the name 
         */ 
        return (current_ptr != NULL); 
    }

**Question 17-1:** Why does running this program sometimes result in a bus error? 
Other times, it will return "1" for an item that is not in the list. (Click here for the 
answer `Section 17.11`_)

Structure Pointer Operator
##########################

In our ``find`` program, we had to use the cumbersome notation 
``(*current_ptr).data`` to access the data field of the structure. C provides a 
shorthand for this construct using the structure pointer (``->``) operator. The dot (``.``) 
operator indicates the field of a structure. The ``->`` indicates the field of a structure 
pointer.  

The following two expressions are equivalent: :: 

    (*current_ptr).data = value;  
    current_ptr->data = value; 

Ordered Linked Lists
####################

So far, we have added new elements only to the head of a linked list. Suppose we 
want to add elements in order. `Figure 17-5`_ is an example of an ordered linked list.  

.. _`Figure 17-5`:
.. figure:: img/fig17-5.jpg
    :align: center

    Figure 17-5. Ordered list

The subroutine in `the following example`_ implements this function. The first step is to locate
the insert point. ``head_ptr`` points to the first element of the list. The program moves
the variable ``before_ptr`` along the list until it finds the proper place for the insert. 
The variable  ``after_ptr`` is set to point to the element that follows the insertion. The
new element will be inserted between these elements. 

.. _`the following example`: Example_

Example
=======

::

    void enter(struct item *first_ptr, const int value)
    {
        struct item *before_ptr;            /* Item before this one */
        struct item *after_ptr;             /* Item after this one */
        struct item *new_item_ptr;          /* Item to add */
        
        /* Create new item to add to the list */
        
        before_ptr = first_ptr;             /* Start at the beginning */
        after_ptr =  before_ptr->next_ptr;
        
        while (1) {
            if (after_ptr == NULL || after_ptr->value >= value)
                /* insert point located */                /* [1] */
                break;
            
            /* Advance the pointers */
            after_ptr = after_ptr->next_ptr;
            before_ptr = before_ptr->next_ptr;
        }
        
        /* create a new item */
        new_item_ptr = malloc(sizeof(struct item));       /* [2] */
        new_item_ptr->value = value;
        
        /* new item insertion */
        before_ptr->next_ptr = new_item_ptr;              /* [3] */
        new_item_ptr->next_ptr = after_ptr;               /* [4] */
    }

In `Figure 17-6`_, we have positioned ``before_ptr`` so that it points to the element 
before the insert point. The variable ``after_ptr`` points to the element after the 
insert. In other words, we are going to put our new element in between ``before_ptr`` 
and ``after_ptr``.

.. _`Figure 17-6`:
.. figure:: img/fig17-6.jpg
    :align: center

    Figure 17-6. Ordered list insert

Double-Linked Lists
###################

A double-linked list contains two links. One link points forward to the next element; 
the other points backward to the previous element.  

The structure for a double-linked list is: ::

    struct double_list {  
        int data;                          /* data item */
        struct  double_list *next_ptr;     /* forward link */
        struct  double_list *previous_ptr; /* backward link */
    };

A double-linked list is illustrated in `Figure 17-7`_. This is very similar to the 
single-linked list, except that there are two links: one forward and one backward. 
The four steps required to insert a new element into the list are illustrated later in 
`Figure 17-8`_, `Figure 17-9`_, `Figure 17-10`_, and in `this figure`_. 

.. _`this figure`: `Figure 17-11`_

.. _`Figure 17-7`:
.. figure:: img/fig17-7.jpg
    :align: center

    Figure 17-7. Double-linked list

Insert an element in the list
=============================

The code to insert a new element in this list is: ::

    void double_enter(struct double_list *head_ptr, int item)  
    {  
        struct list *insert_ptr; /* insert before this element */   
        /*  
         * Warning: This routine does not take  
         *   care of the case in which the element is  
         *   inserted at the head of the list  
         *   or the end of the list  
         */   
        insert_ptr = head_ptr;  
        while (1) {  
            insert_ptr = insert_ptr->next;  
            /* have we reached the end */  
            if (insert_ptr == NULL)  
                break;   
            /* have we reached the right place */  
            if (item >= insert_ptr->data)  
                break;   
        } 

Let's examine this in detail. First we set up the forward link of our new element with 
the code: ::

    new_item_ptr->next_ptr = insert_ptr; 

This is illustrated in `Figure 17-8`_.

.. _`Figure 17-8`:
.. figure:: img/fig17-8.jpg
    :align: center

    Figure 17-8. Double-linked list insert, part 1

Now we need to take care the backward pointer (``new_item_ptr->previous_ptr``). 
This is accomplished with the statement: ::

    new_item_ptr->previous_ptr = insert_ptr->previous_ptr; 

Note that unlike the single-linked list, we have no ``before_ptr`` to point to the 
element in front of the insert point. Instead, we use the value of 
``insert_ptr->previous_ptr`` to point to this element. Our linked list now looks like 
`Figure 17-9`_. 

.. _`Figure 17-9`:
.. figure:: img/fig17-9.jpg
    :align: center

    Figure 17-9. Double-linked list insert, part 2

We've set up the proper links in our new element; however, the links of the old 
elements (numbers 11 and 36) still need to be adjusted. We first adjust the field 
``next_ptr`` in element 11. Getting to this element requires a little work. We start at 
``insert_ptr`` (element 36) and follow the link ``previous_ptr`` to element 11. We want 
to change the field next_ptr in this element. The code for this is: ::

    insert_ptr->previous_ptr->next_ptr = new_ptr;

Our new link is illustrated in `Figure 17-10`_. 

.. _`Figure 17-10`:
.. figure:: img/fig17-10.jpg
    :align: center

    Figure 17-10. Double-linked list insert, part 3

We have three out of four links done. The final link is ``previous_ptr`` of element 36. 
This is set with code: ::

    insert_ptr->previous_ptr = new_item_ptr; 

The final version of our double link is illustrated in `Figure 17-11`_. 

.. _`Figure 17-11`:
.. figure:: img/fig17-11.jpg
    :align: center

    Figure 17-11. Double-linked list insert, part 4

Trees
#####

Suppose we want to create an alphabetized list of the words that appear in a file. We 
could use a linked list ; however, searching a linked list is slow because we must 
check each element until we find the correct insertion point. By using a data type 
called a *tree*, we can cut the number of compares down tremendously. A *binary tree 
structure* is shown in `Figure 17-12`_.  

.. _`Figure 17-12`:
.. figure:: img/fig17-12.jpg
    :align: center

    Figure 17-12. Tree

Each box is called a *node* of the tree. The box at the top is the *root*, and the boxes 
at the bottom are the *leaves*. Each node contains two pointers, a left pointer and a 
right pointer, that point to the left and right subtrees.

Data Structures
===============

The structure for a tree is: ::

    struct node {  
        char   *data;           /* word for this tree */  
        struct node *left;      /* tree to the left */   
        struct node *right;     /* tree to the right */  
    }; 

Trees are often used for storing a *symbol table*, a list of variables used in a program. 
In this chapter, we will use a tree to store a list of words and then print the list 
alphabetically. The advantage of a tree over a linked list is that searching a tree 
takes considerably less time.

In this example, eac h node stores a single word. The left subtree stores all words 
less than the current word, and the right subtree stores all the words greater than 
the current word.  

For example, `Figure 17-13`_ shows how we descend the tree to look for the word 
"orange." We would start at the root "lemon." Because "orange" > "lemon," we 
would descend to the right link and go to "pear." Because "orange" < "pear," we 
descend to the left link and  we have "orange." 

.. _`Figure 17-13`:
.. figure:: img/fig17-13.jpg
    :align: center

    Figure 17-13. Tree search

Recursion
=========

Recursion is extremely useful with trees. Our rules for recursion are:

1. The function must make things simpler. Th is rule is satisfied by trees, 
   because as you descend the hierarchy there is less to search. 
2. There must be some endpoint. A tree offers two endpoints, either you find a 
   match, or you reach a null node.  

Insert an element
=================

The algorithm for inserting a word in a tree is: 

1. If this is a null tree (or subtree), create a one-node tree with this word in it.  
2. If the current node contains the word, do nothing. 
3. Otherwise, perform a recursive call to "insert word" to insert the word in the 
   left or right subtree, depending on the value of the word. 

To see how this algortithm works, consider what happens when we insert the word 
"fig" into the tree as shown in `Figure 17-13`_. First, we check the word "fig" against 
"lemon." "Fig" is smaller, so we go to "apple." Because "fig" is bigger, we go to 
"grape." Because "fig" is smaller than "grape," we try the left link. It is ``NULL``, so we 
create a new node. The function to enter a value into a tree is: ::

    void enter(struct node **node, char *word)  
    {  
        int  result;                /* result of strcmp */   
        char *save_string();        /* save a string on the heap */  
        void memory_error();        /* tell user no more room */  
         
        /* 
         * If the current node is null, then we have reached the bottom 
         * of the tree and must create a new node 
         */ 
        if ((*node) == NULL) {  
        
            /* Allocate memory for a new node */ 
            (*node) = malloc(sizeof(struct node));   
            if ((*node) == NULL)   
                memory_error();  
        
            /* Initialize the new node */ 
            (*node)->left = NULL;  
            (*node)->right = NULL;   
            (*node)->word = save_string(word);  
            return; 
        }
        
        /* Check to see where our word goes */ 
        result = strcmp((*node)->word, word);  
        
        /* The current node  
         * already contains the word,  
         * no entry necessary */ 
        if (result == 0)  
            return;  
        
        /* The word must be entered in the left or right subtree */ 
        if (result < 0)  
            enter(&(*node)->right, word);  
        else  
            enter(&(*node)->left, word);  
    }

This function is passed a pointer to the root of the tree. If the root is ``NULL``, it creates 
the node. Because we are changing the value of a pointer, we must pass *a pointer 
to the pointer*. (We pass one level of pointer because that's the variable type outside 
the function; we pass the second level because we have to change it.) 

Printing a Tree
###############

Despite the complex nature of a tree structure, it is easy to print. Again, we use 
recursion. The printing algorithm is: 

1. For the null tree, print nothing.
2. Print the data that comes before this node (left tree), then print this node 
   and print the data that comes after this node (right tree). 

The code for ``print_tree`` is: :: 

    void print_tree(struct node *top)  
    {  
        if (top == NULL)  
            return;                 /* short tree */ 
        print_tree(top->left);  
        printf("%s\n", top->word);  
        print_tree(top->right);  
    } 

Rest of Program
###############

Now that we have defined the data structure, all we need to complete the p rogram 
is a few more functions.

The main function checks for the correct number of arguments and then calls the 
scanner and the ``print_tree`` routine.

The scan function reads the file and breaks it into words. It uses the standard macro 
``isalpha``. This macro, defined in the standard header file *ctype.h*, returns nonzero if 
its argument is a letter and otherwise. The macro is defined in the standard include 
file *ctype.h*. After a word is found, the function ``enter`` is called to put it in the tree.  

``save_string`` creates the space for a string on the heap, then returns the pointer to 
it.

``memory_error`` is called if a ``malloc`` fails. This program handles the out-of-memory 
problem by writing an error message and quitting.

Example 17-4 is a listing of *words.c*.  

Example: words/words.c
======================

:: 

    /******************************************************** 
     * words ## Scan a file and print out a list of words   * 
     *              in ASCII order.                         * 
     *                                                      * 
     * Usage:                                               * 
     *      words <file>                                    * 
     ********************************************************/ 
    #include <stdio.h>
    #include <ctype.h>
    #include <string.h>
    #include <stdlib.h>
     
    struct node { 
        struct node    *left;       /* tree to the left */ 
        struct node    *right;      /* tree to the right */ 
        char           *word;       /*  word for this tree */ 
    }; 
     
    /* the top of the tree */ 
    static struct node *root = NULL; 
     
    /******************************************************** 
     * memory_error ## Writes error and dies.               *  
     ********************************************************/ 
    void memory_error(void) 
    { 
        fprintf(stderr, "Error:Out of memory\n"); 
        exit(8); 
    } 
     
    /******************************************************** 
     * save_string ## Saves a string on the heap.           * 
     *                                                      * 
     * Parameters                                           * 
     *      string ## String to save.                       * 
     *                                                      * 
     * Returns                                              * 
     *      pointer to malloc-ed section of memory with     * 
     *      the string copied into it.                      * 
     ********************************************************/ 
    char *save_string(char *string) 
    { 
        char *new_string;   /* where we are going to put string */ 
     
        new_string = malloc((unsigned) (strlen(string) + 1)); 
     
        if (new_string == NULL) 
            memory_error(); 
     
        strcpy(new_string, string);   350 
        return (new_string); 
    } 
    /******************************************************** 
     * enter ## Enters a word into the tree.                * 
     *                                                      * 
     * Parameters                                           * 
     *      node ## Current node we are looking at.         * 
     *      word ## Word to enter.                          * 
     ********************************************************/ 
    void enter(struct node **node, char *word) 
    { 
        int  result;        /* result of strcmp */ 
     
        char *save_string(char *);  /* save a string on the heap */ 
     
        /*  
         * If the current node is null, we have reached the bottom 
         * of the tree and must create a new node. 
         */ 
        if ((*node) == NULL) { 
     
            /* Allocate memory for a new node */ 
            (*node) = malloc(sizeof(struct node)); 
            if ((*node) == NULL) 
                 memory_error(); 
     
            /* Initialize the new node */ 
            (*node)->left = NULL; 
            (*node)->right = NULL; 
            (*node)->word = save_string(word); 
            return; 
        } 
        /* Check to see where the word goes */ 
        result = strcmp((*node)->word, word); 
     
        /* The current node already contains the word, no entry necessary */ 
        if (result == 0) 
            return; 
     
        /* The word must be entered in the left or right subtree */ 
        if (result < 0) 
            enter(&(*node)->right, word); 
        else 
            enter(&(*node)->left, word);   351 
    } 
    /******************************************************** 
     * scan ## Scans the file for words.                    * 
     *                                                      * 
     * Parameters                                           * 
     *      name ## Name of the file to scan.               * 
     ********************************************************/ 
    void scan(char *name) 
    { 
        char word[100];     /* word we are working on */ 
        int  index;         /* index into the word */ 
        int  ch;            /* current character */ 
        FILE *in_file;      /* input file */ 
     
        in_file = fopen(name, "r"); 
        if (in_file == NULL) { 
            fprintf(stderr, "Error:Unable to open %s\n", name); 
            exit(8); 
        } 
        while (1) { 
            /* scan past the whitespace */ 
            while (1) { 
                ch = fgetc(in_file); 
     
                if (isalpha(ch) || (ch == EOF)) 
                    break; 
            } 
     
            if (ch == EOF) 
                break; 
     
            word[0] = ch; 
            for (index = 1; index < sizeof(word); ++index) { 
                ch = fgetc(in_file); 
                if (!isalpha(ch)) 
                    break; 
                word[index] = ch; 
            } 
            /* put a null on the end */ 
            word[index] = '\0'; 
     
            enter(&root, word); 
        } 
        fclose(in_file);   352 
    } 
    /******************************************************** 
     * print_tree ## Prints out the words in a tree.        * 
     *                                                      * 
     * Parameters                                           * 
     *      top ## The root of the tree to print.           *  
     ********************************************************/ 
    void print_tree(struct node *top) 
    { 
        if (top == NULL) 
            return;                 /* short tree */ 
     
        print_tree(top->left); 
        printf("%s\n", top->word); 
        print_tree(top->right); 
    } 
     
    int main(int argc, char *argv[]) 
    { 
        if (argc != 2) { 
            fprintf(stderr, "Error:Wrong number of parameters\n"); 
            fprintf(stderr, "      on the command line\n"); 
            fprintf(stderr, "Usage is:\n"); 
            fprintf(stderr, "    words 'file'\n"); 
            exit(8); 
        } 
        scan(argv[1]); 
        print_tree(root); 
        return (0); 
    }

Question 17-2
=============

*I once made a program that read the dictionary into memory using 
a tree structure, and then used the structure in a program that searched for 
misspelled words. Although trees are supposed to be fast, this program was so slow 
that you would think I used a linked list. Why?* 

.. hint::
    Graphically construct a tree using the words "able," "baker," "cook," "delta," 
    and "easy," and look at the result. (Click here for the answer `Section 17.11`_) 


.. warning::
    gaubert est moche


Data Structures for a Chess Program
###################################

One of the classic problems in artificial intelligence is the game of chess. As this 
book goes to press, the Grandmaster who beat the world's best chess-playing 
computer last year has lost to the computer this year (1997).

We are going to design a data structure for a chess-playing program. In chess, you 
have several possible moves that you can make. Your opponent has many 
responses to which you have many answers, and so on, back and forth, for several 
levels of moves.  

Our data structure is beginning to look like a tree. This structure is not a binary tree 
because we have more than two branches for each node, as shown in `Figure 17-14`_.

.. _`Figure 17-14`:
.. figure:: img/fig17-14.jpg
    :align: center

    Figure 17-14. Chess tree

We are tempted to use the following data structure: ::

    struct chess {  
        struct board board;    /* Current board position */  
        struct next {  
            struct move;       /* Our next move */  
            struct *chess_ptr; /* Pointer to the resulting position */  
        } next[MAX_MOVES];  
    }; 

The problem is that the number of moves from any given position can vary 
dramatically. For example, in the beginning you have lots of pieces running 
around. [#]_ Things like rooks, queens, and bishops can move any number of squares 
in a straight line. When you reach the end game (in an evenly matched game), each 
side probably has only a few pawns and one major piece. The number of possible 
moves has been greatly reduced. 

.. [#] Trivia question:
    What are the 21 moves that you can make in chess from the starting position? You can move 
    each pawn up one (8 moves) or two (8 more), and the knights can move out to the left and right (4 more: 
    8+8+4=20). What's the 21st move?

We want to be as efficient in our storage as possible, because a chess program will 
stress the limits of our machine. We can reduce our storage requirements by 
changing the next-move array into a linked list. Our resulting structure is: ::

    struct next {  
        struct move this_mode;     /* Our next move */   
        struct *chess_ptr;         /* Pointer to the resulting position */  
    };  
    struct chess {  
        struct board board;        /* Current board position */  
        struct next *list_ptr;     /* List of moves we can make from here */  
        struct move this_move;     /* The move we are making */  
    }; 

This is shown graphically in Figure 17-15. 

.. _`Figure 17-15`:
.. figure:: img/fig17-15.jpg
    :align: center

    Figure 17-15. Revised chess structure

The new version adds a little complexity, but saves a great deal of storage. In the
first version, we must allocate storage for pointers to all possible moves. If we have
only a few possible moves, we waste a lot of storage for pointers to unused moves.
Using a linked list, we allocate storage on an on-demand basis. So if there are 30 
possible moves, our list is 30 long; but if there are only 3 possible moves, our list is
3 long. The list grows only as needed, resulting in a more efficient use of storage.  

.. _`Section 17.11`:

Answers
#######

Answer 17-1
===========

The problem is with the statement: ::

    while ((strcmp(current_ptr->data, name) != 0) &&  
           (current_ptr != NULL))

``current_ptr->data`` is checked before we check to see if ``current_ptr`` is a valid 
pointer (``!= NULL``). If the pointer is ``NULL``, we can easily check a random memory 
location that could contain anything. The solution is to check ``current_ptr`` before 
checking what it is pointing to: ::

    while (current_ptr != NULL) {   
        if (strcmp(current_ptr->data, name) == 0)  
            break; 
    } 

Answer 17-2
===========

The problem was that because the first word in the dictionary was 
the smallest, every other word used the right-hand link. In fact, because the entire 
list was ordered, only the right-hand link was used. Although this structure was 
defined as a tree structure, the result was a linked list, as shown in `Figure 17-16`_. 
Some of the more advanced books on data structures, like Niklaus Wirth's book 
*Algorithms + Data Structures = Programs*, discuss ways of preventing this error by 
balancing a binary tree.

.. _`Figure 17-16`:
.. figure:: img/fig17-16.jpg
    :align: center

    Figure 17-16. An imbalanced tree

**Trivia Answer:** You give up. That's right; the 21st move is to resign.

Programming Exercises  
#####################

Exercise 17-1
=============

Write a cross-reference program.

Exercise 17-2
=============

Write a function to delete an element of a linked list.  

Exercise 17-3
=============

Write a function to delete an element of a double-linked list.

Exercise 17-4
=============

Write a function to delete an element of a tree. 
