.. _`Chapter 18`:

Chapter 18. Modular Programming
===============================

.. 

    Many hands make light work.

    --John Heywood 

All along, we have been dealing with small programs. As programs grow larger and 
larger, it is more desirable to split them into sections or modules. C allows programs 
to be split into multiple files, compiled separately, and then combined (linked) to 
form a single program.  

In this chapter, we will go through a programming example, discussing the C 
techniques needed to create good modules. You will be shown how to use *make* to 
put these modules together to form a program. 

18.1 Modules   
------------

A module is a collection of functions that perform related tasks. For example, a 
module could exist to handle database functions such as ``lookup``, ``enter``, and ``sort``. 
Another module could handle complex numbers, and so on. 

Also, as programming problems get bigger, more and more programmers are 
needed to finish them. An efficient way of splitting up a large project is to assign 
each programmer a different module. In this manner, each programmer only 
worries about the internal details of a particular module.  

In this chapter, we will discuss a module to handle *infinite arrays*. The functions in 
this package allow the user to store data into an array without worrying about its 
size. The infinite array grows as needed (limited only by the amount of memory in 
the computer). The array will be used to store data for a histogram, but can be used 
to store things like line numbers from a cross-reference program or other types of 
data.  

18.2 Public and Private  
-----------------------

Modules are divided into two parts: *public* and *private*. The public part tells the user 
how to call the functions in the module. It contains the definition of data structures 
and functions that are to be used outside the module. These definitions are put in a 
header file, and the file must be included  in any program that depends on that 
module. In our infinite array example, we have put the public declarations in the file 
*ia.h*, which we will look at shortly. Figure 18-1 illustrates the relationship between 
the various parts of the infinite array package.  

.. _`Figure 18-1`:
.. figure:: img/fig18-1.jpg
    :align: center

    Figure 18-1. Definition, implementation, and use of the infinite array 

Anything that is internal to the module is private. Everything that is not directly 
usable by the outside world should be kept private.

One of the advantages of C++ over C is that you can explicitly declare what is public 
and what is private, and prevent unauthorized modification of private data.  

18.3 The extern Modifier
------------------------

The extern **modifier** is used to indicate that a variable or function is defined outside 
the current file. For example, look at the contents of two files, *main.c* and *count.c*. 

File main.c
~~~~~~~~~~~

::

    #include <stdio.h>  
    /* number of times through the loop */  
    extern int counter;  
     
    /* routine to increment the counter */  
    extern void inc_counter(void);  
     
    main()  
    {  
        int   index; /* loop index */  
     
        for (index = 0; index < 10; index++)  
            inc_counter();  
        printf("Counter is %d\n", counter);    359 
        return (0);  
    } 

File count.c
~~~~~~~~~~~~
::

    /* number of times through the loop */  
    int     counter = 0;  
     
    /* trivial example */  
    void    inc_counter(void)  
    {  
        ++counter;  
    } 

In this example, the function ``main`` uses the variable ``counter``. The **extern** 
declaration is used by *main.c* to indicate that ``counter`` is declared outside the 
function; in this case, counter is defined in the file *counter.c*. The modifier **extern** is 
not used in *counter.c* because it contains the "real" declaration of the variable. 

There are three modifiers that can be used to indicate where a variable is defined, as 
shown in the following table.   

========== ==================================================================================
Modifier   Meaning
========== ==================================================================================
**extern** Variable/function is defined in another file.
*"none"*   Variable/function is defined in this file (public) and can be used in other files.
**static** Variable/function is local to this file (private).
========== ==================================================================================

Notice that the word **static** has two meanings. For data defined globally, **static** 
means "private to this file." For data defined inside a function, it means "variable is 
allocated from static memory (instead of the temporary stack)."

C is very liberal in its use of the rules for the **static** and **extern** modifiers. You can 
declare a variable **extern** at the beginning of a program and later define it with no 
modifier: ::

    extern sam;  
    int sam = 1;    /* this is legal */ 

This method is useful when you have all of your external variables defined in a 
header file. The pr ogram includes the header file (and defines the variables as 
extern), then defines the variable for real. 

Another problem concerns declaring a variable in two different files:  

File main.c
~~~~~~~~~~~

::

    int     flag  = 0;      /* flag is off */ 
    main() 
    { 
    printf("Flag is %d\n", flag); 
    } 

File sub.c
~~~~~~~~~~
::

    int     flag = 1;       /* flag is on */ 

What happens in this case?

1. ``flag`` will be initialized to because *main.c* is loaded first.  
2. ``flag`` will be initialized to 1 because the entry in sub.c will overwrite the one 
   in *main.c*. 
3. The compiler will very carefully analyze both programs, then pick out the 
   value that is most likely to be wrong.  

There is only one global variable ``flag``, and it will be initialized to either 1 or 
depending on the whims of the compiler. Some of the more advanced compilers will 
issue an error message when a global is declared twice, but most compilers will 
silently ignore this error. It is entirely possible for the program ``main`` to print out: 

>>> flag is 1 

even though we initialized flag to and did not change it before printing. To avoid the 
problem of hidden initializations, use the keyword **static** to limit the scope of each 
variable to the file in which it is declared.  

If we had written:  

File main.c
~~~~~~~~~~~

:: 

    static int      flag  = 0;      /* flag is off */   
    main()  
    {  
            printf("Flag is %d\n", flag);  
    }

File sub.c
~~~~~~~~~~

::

    static int      flag = 1;       /* flag is on */ 

then ``flag`` in *main.c* is an entirely different variable from ``flag`` in *sub.c*. However, 
you should still give the variables different names to avoid confusion.  

18.4 Headers   
------------

Information that is shared between modules should be put in a header file. By 
convention, all header filenames end with *.h*. In our infinite array example, we use 
the file *ia.h*. 

The header should contain all the public information, such as: 

+ A comment section describing clearly what the module does and what is 
  available to the user  
+ Common constants 
+ Common structures 
+ Prototypes of all the public functions 
+ **extern** declarations for public variables  

In our infinite array example, over half of the file *ia.h* is devoted to comments. This 
level of comment is not excessive; the real guts of the coding are hidden in the 
program file *ia.c*. The *ia.h* file serves both as a program file and as documentation to 
the outside world.  

Notice there is no mention in the *ia.h* comments about how the infinite array is 
implemented. At this level, we don't care about how something is done; we just 
want to know what functions are available. Look through the file *ia.h* (see Example 
18-1).  

Example 18-1. File ia.h
~~~~~~~~~~~~~~~~~~~~~~~

::

    /******************************************************** 
     * Definitions for the infinite array (ia) package.     *  
     *                                                      * 
     * An infinite array is an array whose size can grow    *  
     * as needed.  Adding more elements to the array        * 
     * will just cause it to grow.                          *  
     *------------------------------------------------------* 
     * struct infinite_array                                * 
     *      Used to hold the information for an infinite    *
     *      array.                                          * 
     *------------------------------------------------------* 
     * Routines                                             * 
     *                                                      * 
     *      ia_init -- Initializes the array.               * 
     *      ia_store -- Stores an element in the array.     * 
     *      ia_get -- Gets an element from the array.       *  
     ********************************************************/ 
     
    /* number of elements to store in each cell of the infinite array */ 
    #define BLOCK_SIZE      10 
             
    struct infinite_array { 
        /* the data for this block */ 
        float   data[BLOCK_SIZE];        
     
        /* pointer to the next array */ 
        struct infinite_array *next; 
    }; 
     
    /******************************************************** 
     * ia_init -- Initializes the infinite array.           * 
     *                                                      * 
     * Parameters                                           * 
     *      array_ptr -- The array to initialize.           *  
     ********************************************************/ 
    #define ia_init(array_ptr)      {(array_ptr)->next = NULL;} 
     
    /******************************************************** 
     * ia_get -- Gets an element from an infinite array.    *  
     *                                                      * 
     * Parameters                                           * 
     *      array_ptr -- Pointer to the array to use.       *  
     *      index   -- Index into the array.                *  
     *                                                      * 
     * Returns                                              * 
     *      The value of the element.                       *  
     *                                                      * 
     * Note: You can get an element that                    * 
     *      has not previously been stored. The value       *  
     *      of any uninitialized element is zero.           *  
     ********************************************************/ 
    extern int ia_get(struct infinite_array *array_ptr, int index); 

    /******************************************************** 
     * ia_store -- Store an element in an infinite array.   *  
     *                                                      * 
     * Parameters                                           * 
     *      array_ptr -- Pointer to the array to use.       *  
     *      index   -- index into the array.                *  
     *      store_data -- Data to store.                    *  
     ********************************************************/ 
    extern void  ia_store(struct infinite_array * array_ptr,  
                          int index, int store_data);

A few things should be noted about this file. Three functions are documented: 
``ia_get``, ``ia_store``, and ``ia_init``. ``ia_init`` isn't really a function, but is a macro. For 
the most part, people using this module do not need to know if a function is really a 
function or only a macro.

The macro is bracketed in curly braces (``{}``), so it will not cause syntax problems 
when used in something like an **if**/**else** sequence. The code: ::

    if (flag)  
        ia_init(&array);  
    else  
        ia_store(&array, 0, 1.23); 

will work as expected. 

Everything in the file is a constant definition, a data structure definition, or an 
external definition. No code or storage is defined.

18.5 The Body of the Module   
---------------------------

The body of the module contains all the functions and data for that module. Private 
functions that will not be called from outside the module should be declared **static**. 
Variables declared outside of a function that are not used outside the module are 
declared **static**.  

18.6 A Program to Use Infinite Arrays  
-------------------------------------

The program uses a simple linked list to store the elements of the array, as shown 
in Figure 18-2. A linked list can grow longer as needed (until we run out of room). 
Each list element or bucket can store 10 numbers. To find element 38, the program 
starts at the beginning, skips past the first three buckets, then extracts element 8 
from the data in the current bucket.

.. _`Figure 18-2`:
.. figure:: img/fig18-2.jpg
    :align: center

    Figure 18-2. Infinite array structure

The code for the module *ia.c* is shown as Example 18-2.

Example 18-2. a/ia.c
~~~~~~~~~~~~~~~~~~~~

::

    /********************************************************
     * infinite-array -- routines to handle infinite arrays *
     *                                                      *
     * An infinite array is an array that grows as needed.  *
     * There is no index too large for an infinite array    *
     * (unless we run out of memory).                       *
     ********************************************************/
    #include "ia.h"               /* get common definitions */
    #include <memory.h>
    #include <stdio.h>
    #include <stdlib.h>

    /********************************************************
     * ia_locate -- Gets the location of an infinite array  *
     *              element.                                *
     *                                                      *
     * Parameters                                           *
     *      array_ptr -- Pointer to the array to use.       *
     *      index   -- Index into the array.                *
     *      current_index -- Pointer to the index into this *
     *              bucket (returned).                      *
     *                                                      *
     * Returns                                              *
     *      pointer to the current bucket                   *
     ********************************************************/
    static struct infinite_array *ia_locate(
            struct infinite_array *array_ptr, int index,
            int *current_index_ptr)
    {
        /* pointer to the current bucket */
        struct infinite_array *current_ptr;

        current_ptr = array_ptr;
        *current_index_ptr = index;

        while (*current_index_ptr >= BLOCK_SIZE) {
            if (current_ptr->next == NULL) {

                current_ptr->next = malloc(sizeof(struct infinite_array));

                if (current_ptr->next == NULL) {
                    fprintf(stderr, "Error:Out of memory\n");
                    exit(8);
                }

                memset(current_ptr->next, '\0', 
                       sizeof(struct infinite_array));
            }
            current_ptr = current_ptr->next;
            *current_index_ptr -= BLOCK_SIZE;
        }
        return (current_ptr);
    }
    /********************************************************
     * ia_store -- Stores an element into an infinite array.*
     *                                                      *
     * Parameters                                           *
     *      array_ptr -- Pointer to the array to use.       *
     *      index   -- Index into the array.                *
     *      store_data -- Data to store.                    *
     ********************************************************/
    void  ia_store(struct infinite_array * array_ptr,
        int index, int store_data)
    {
        /* pointer to the current bucket */
        struct infinite_array *current_ptr;
        int   current_index;        /* index into the current bucket */
        current_ptr = ia_locate(array_ptr, index, &current_index);
        current_ptr->data[current_index] = store_data;
    }
    /********************************************************
     * ia_get -- Gets an element from an infinite array.    *
     *                                                      *
     * Parameters                                           *
     *      array_ptr -- Pointer to the array to use.       *
     *      index   -- Index into the array.                *
     *                                                      *
     * Returns                                              *
     *      the value of the element                        *
     *                                                      *
     * Note: You can get an element that                    *
     *      has not previously been stored. The value       *
     *      of any uninitialized element is zero.           *
     ********************************************************/
    int ia_get(struct infinite_array *array_ptr, int index)
    {
        /* pointer to the current bucket */
        struct infinite_array *current_ptr;

        int   current_index;        /* index into the current bucket */

        current_ptr = ia_locate(array_ptr, index, &current_index);
        return (current_ptr->data[current_index]);
    }

This program uses an internal routine, ``ia_locate``. Because this routine is not used 
outside the module, it is defined as **static**. The routine is also not put in the header 
*ia.h*.   

18.7 The Makefile for Multiple Files  
------------------------------------

The program ``make`` is designed to aid the programmer in compiling and linking 
programs. Before ``make``, the user had to explicitly type in compile commands for 
every change in the program. For example:

>>> cc -g -o hello hello.c  

As programs grow, the number of commands needed to create them grows. Typing 
a series of 10 or 20 commands can be tiresome and error prone, so programmers 
started writing shell scripts (or .BAT files on MS-DOS.) All the programmer had to 
type was a script name such as ``do-it``, and the computer would compile everything.

This method can be overkill, however, because all the files are recompiled whether 
or not they need to be.  

As the number of files in a project grows, so does the time required for a recompile. 
Making changes in one small file, starting the compilation, and then having to wait 
until the next day while the computer executes severa l hundred compile commands 
can be frustrating, especially when only one compile was really needed. 

The program  make was created to make compilation dependent upon whether a file 
has been updated since the last compilation. The program allows you to specify the 
dependencies of the program file and the source file, and the command that 
generates the program from its source.  

The file Makefile (case sensitivity is important in UNIX) contains the rules used by 
make to decide how to build the program. 

The Makefile contains the following sections:  

+ Comments 
+ Macros 
+ Explicit rules 
+ Default rules 

Any line beginning with a hash mark (``#``) is a comment. 

A macro has the format: :: 

    name = data

where ``name`` is any valid identifier and data is the text that will be substituted 
whenever ``make`` sees ``$(name)``. 

For example: :: 

    #  
    # Very simple Makefile  
    #  
    MACRO=Doing All  
    all:  
        echo $(MACRO) 

Explicit rules tell make what commands are needed to create the program. They can 
take several forms. The most common of these is: :: 

    target: source [source2] [source3] 
        command
        [command] 
        [command]
        ... 

where  target  is the name of a file to create. It is "made" or created out of the source 
file source. If the  target  is created out of several files, they are all listed. This list 
should include any header files included by the source file. The  command that 
generates the target is specified on the next line. Sometimes you need more than 
one command to create the target. Commands are listed one per line. Each is 
indented by a tab.

For example, the rule: ::

    hello: hello.c  
        cc -g -ohello hello.c

tells make to create the file hello from the file hello.c using the command: 

>>> cc -g -ohello hello.c 

make will create hello only if necessary. The files used in the creation of hello,  
arranged in chronological order (by modification times), are shown in the following table. 

========= ========= ================
Age       UNIX      MS-DOS/Windows 
========= ========= ================
oldest    hello.c   HELLO.C
old       hello.o   HELLO.OBJ
newest    hello     HELLO.EXE
========= ========= ================

If the programmer changes the source file  hello.c, its modification time will be out of 
date with respect to the other files. make will recognize that and re-create the other 
files. 

Another form of the explicit rule is:  ::

    source: 
        command 
        [command] 

In this case, the commands are unconditionally executed each time ``make`` is run. If 
the commands are omitted from an explicit rule, ``make`` will use a set of built -in rules 
to determine what command to e xecute. For example, the rule:  ::

    hist.o: ia.h hist.c 

tells make to create hist.o from *hist.c* and *ia.h*, using the standard suffix rule for 
making *file.o* from *file.c*. This rule is: ::

    $(CC) $(CFLAGS) -c file.c  

(make  predefines the macros ``$(CC)`` and ``$(CFLAGS)``.) 

We are going to create a main program hist.c that calls functions in the module *ia.c*. 
Both files include the header *ia.h*, so they depend on it. The UNIX Makefile that 
creates the program hist from *hist.c* and *ia.c* is: ::

    CFLAGS = -g  
    OBJ=ia.o hist.o  
     
    all: hist  
               
    hist: $(OBJ)  
            $(CC) $(CFLAGS) -o hist $(OBJ)  
     
    hist.o:ia.h hist.c  
     
    ia.o:ia.h ia.c 

The macro ``OBJ`` is a list of all the object (*.o*) files. The lines: ::

    hist: $(OBJ)  
        $(CC) $(CFLAGS) -o hist $(OBJ)

tell ``make`` to create *hist* from the object files. If any of the object files are out of date, 
``make`` will re-create them. 

The line: :: 

    hist.o:hist.c ia.h 

tells ``make`` to create *hist.o* from *ia.h* and  *hist.c*. Because no command is specified, the 
default is used.  

One big drawback exists with ``make``. It checks to see only if the files have changed, 
not the rules. If you have compiled all of your program with ``CFLAGS=-g`` for 
debugging and need to produce the production version (``CFLAGS=-O``), ``make`` will not  
recompile. 

The command ``touch`` changes the modification date of a file. (It doesn't change the 
file, it just makes the operating system think that it did.) If you ``touch`` a source file 
such as hello.c and then run ``make``, the program will be re -created. This feature is 
useful if you have changed the compile-time flags and want to force a recompilation.  

``make`` provides you with a rich set of commands for creating programs. Only a  few 
have been discussed here. [#]_

.. [#] If you are going to create programs that require more than 10 or 20 source files, 
    read the Nutshell Handbook Managing Projects with make, by Andy Oram and Steve Talbott.


18.8 Using the Infinite Array
-----------------------------

The histogram program, ``hist``, is designed to use the infinite array package. (A 
histogram is a graphic representation of the frequency with which data items recur.) 
It takes one file as its argument. The file contains a list of numbers from to 99. Any 
number of entries can be used. The program prints a histogram showing how many 
times each number appears. 

A typical line of output from our program looks like: :: 

    5 (   6): *************************** 

The first number (5) is the line index. In our sample data, there are six entries with 
the value 5. The line of asterisks graphically represents our six entries. 

Some data fall out of range and are not represented in our histogram. S uch data are 
counted and listed at the end of the printout. Here is a sample printout: ::

    1  (   9): ************************ 
    2  (  15): **************************************** 
    3  (   9): ************************ 
    4  (  19): *************************************************** 
    5  (  13): *********************************** 
    6  (  14): ************************************** 
    7  (  14): ************************************** 
    8  (  14): ************************************** 
    9  (  20): ****************************************************** 
    10 (  13): *********************************** 
    11 (  14): ************************************** 
    12 (   9): ************************ 
    13 (  13): *********************************** 
    14 (  12): ******************************** 
    15 (  14): ************************************** 
    16 (  16): ******************************************* 
    17 (   9): ************************ 
    18 (  13): *********************************** 
    19 (  15): **************************************** 
    20 (  11): ****************************** 
    21 (  22): ************************************************************ 
    22 (  14): ************************************** 
    23 (   9): ************************ 
    24 (  10): *************************** 
    25 (  15): **************************************** 
    26 (  10): *************************** 
    27 (  12): ******************************** 
    28 (  14): ************************************** 
    29 (  15): **************************************** 
    30 (   9): ************************
    104 items out of range 

The program uses the library routine ``memset`` to initialize the ``counters`` array. This 
routine is highly efficient for setting all values of an array to 0. The line: :: 

    memset(counters, '\0', sizeof(counters)); 

zeroes out the entire array ``counters``. 

The ``sizeof(counters)`` makes sure that all of the array is zeroed. Example 18-3 
contains the full listing of hist.c.

Example 18-3. ia/hist.c
~~~~~~~~~~~~~~~~~~~~~~~

::

    /******************************************************** 
     * hist -- Generates a histogram of an array of numbers.* 
     *                                                      * 
     * Usage                                                * 
     *      hist <file>                                     * 
     *                                                      * 
     * Where                                                * 
     *      file is the name of the file to work on.        *  
     ********************************************************/ 
    #include "ia.h" 
    #include <stdio.h> 
    #include <stdlib.h>      
    #include <memory.h> 
    /* 
     * Define the number of lines in the histogram 
     */ 
    #define NUMBER_OF_LINES 30      /* Number of lines in the histogram */ 
    const int DATA_MIN = 1;         /* Number of the smallest item */ 
    const int DATA_MAX = 30;        /* Number of the largest item */ 
    /* 
     * WARNING: The number of items from DATA_MIN to DATA_MAX (inclusive) 
     * must match the number of lines. 
     */ 
     
    /* number of characters wide to make the histogram */ 
    const int WIDTH = 60; 
     
    static struct infinite_array data_array; 
    static int data_items; 
     
    int main(int argc, char *argv[]) 
    { 
        /* Function to read data */ 
        void read_data(const char name[]); 
     
        /* Function to print the histogram */ 
        void  print_histogram(void); 
     
        if (argc != 2) { 
            fprintf(stderr, "Error:Wrong number of arguments\n"); 
            fprintf(stderr, "Usage is:\n");
            fprintf(stderr, "  hist <data-file>\n"); 
            exit(8); 
        } 
        ia_init(&data_array); 
        data_items = 0; 
     
        read_data(argv[1]); 
        print_histogram(); 
        return (0); 
    } 
    /******************************************************** 
     * read_data -- Reads data from the input file into     *  
     *              the data_array.                         *  
     *                                                      * 
     * Parameters                                           * 
     *      name -- The name of the file to read.           *  
     ********************************************************/ 
    void read_data(const char name[]) 
    { 
        char  line[100];    /* line from input file */ 
        FILE *in_file;      /* input file */ 
        int data;           /* data from input */ 
     
        in_file = fopen(name, "r"); 
        if (in_file == NULL) { 
            fprintf(stderr, "Error:Unable to open %s\n", name); 
            exit(8); 
        } 
        while (1) { 
            if (fgets(line, sizeof(line), in_file) == NULL) 
                break; 
     
            if (sscanf(line, "%d", &data) != 1) { 
                fprintf(stderr, 
                  "Error: Input data not integer number\n"); 
                fprintf(stderr, "Line:%s", line); 
            } 
            ia_store(&data_array, data_items, data); 
            ++data_items; 
        } 
        fclose(in_file); 
    } 
    /******************************************************** 
     * print_histogram -- Prints the histogram output.      *
     ********************************************************/ 
    void  print_histogram(void) 
    { 
        /* upper bound for printout */ 
        int   counters[NUMBER_OF_LINES];     
     
        int   out_of_range = 0;/* number of items out of bounds */ 
        int   max_count = 0;/* biggest counter */ 
        float scale;        /* scale for outputting dots */ 
        int   index;        /* index into the data */ 
     
        memset(counters, '\0', sizeof(counters)); 
     
        for (index = 0; index < data_items; ++index) { 
            int data;/* data for this point */ 
     
            data = ia_get(&data_array, index); 
     
            if ((data < DATA_MIN) || (data > DATA_MAX)) 
                ++out_of_range; 
            else { 
                ++counters[data - DATA_MIN]; 
                if (counters[data - DATA_MIN] > max_count) 
                    max_count = counters[data  - DATA_MIN]; 
            } 
        } 
     
        scale = ((float) max_count) / ((float) WIDTH); 
     
        for (index = 0; index < NUMBER_OF_LINES; ++index) { 
            /* index for outputting the dots */ 
            int   char_index; 
            int   number_of_dots;   /* number of * to output */ 
     
            printf("%2d (%4d): ", index + DATA_MIN, counters[index]); 
     
            number_of_dots = (int) (((float) counters[index]) / scale); 
            for (char_index = 0;   
                 char_index < number_of_dots; 
                 ++char_index) { 
                printf("*"); 
            } 
            printf("\n"); 
        }
        printf("%d items out of range\n", out_of_range); 
    }

Makefile for Free Software Foundation's gcc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    #-----------------------------------------------# 
    #       Makefile for UNIX systems               # 
    #    using a GNU C compiler.                    # 
    #-----------------------------------------------# 
    CC=gcc 
    CFLAGS=-g -Wall -D__USE_FIXED_PROTOTYPES__ -ansi 
     
    all:    hist 
      
    hist: hist.o ia.o  
            $(CC) $(CFLAGS) -o  hist hist.o ia.o 
     
    hist.o: hist.c ia.h 
     
    ia.o: ia.c ia.h 
     
    clean: 
            rm -f hist hist.o ia.o

18.9 Dividing a Task into Modules   
---------------------------------

Unfortunately, computer programming is more of an art than a science. There are 
no hard and fast rules that tell you how to divide a task into modules. Knowing what 
makes a good module and what doesn't comes with experience and practice.

This section describes some general rules for module division and how they can be 
applied to real-world programs. The techniques described here have worked well for 
me. You should use whatever works for you.  

Information is a key part of any program. The key to any program is deciding what 
information is being used and what processing you want to perform on it. 
Information flow should be analyzed before the design begins. 

Modules should be designed to minimize the amount of information that has to pass 
between them. If you look at the organization of an army, you'll see that  it is divided 
up into modules. There is the infantry, artillery, tank corps, and so on. The amount 
of information that passes between these modules is minimized. For example, an 
infantry sergeant who wants the artillery to bombard an enemy position calls u p the 
artillery command and says, "There's a pillbox at location Y-94. Get rid of it." 

The artillery commander handles all the details of deciding which battery is to be 
used, how much fire power to allocate based on the requirements of other fire 
missions, keeping the guns supplied, and many more details [#]_.
  
.. [#] 
    This is a very general diagram of the chain of command for an ideal army. 
    The system used by the United States Army is more complex and so highly classified 
    that even the army commanders don't know how it works.

Programs should be organized in the same way. Information hiding is key to good 
programming. A module should make public only the minimum number of functions 
and data needed to do the job. The smaller the interface, the simpler the interface. 
The simpler the interface, the easier it is to use. Also, a simple interface is less risky 
and less error prone than a complex one.

Small, simple interfaces are also easier to design, test, and maintain. Data hiding 
and good interface design are key to making good modules.

18.10 Module Division Example: Text Editor   
------------------------------------------

You are already familiar with using a  text editor. It is a program that allows the user 
to display and change text files. Most editors are display oriented and continually 
display about 25 lines of the current file on the screen. The text editor must also 
interpret commands that are typed in by the user. This information must be parsed
so that the computer can understand it and act accordingly. The individual 
commands are small and perform similar functions ("delete line" is very much like 
"delete character"). Imposing a standard structure on the command execution 
modules improves readability and reliability.

The different modules that form a text editor are illustrated in `Figure 18-3`_. 

.. _`Figure 18-3`:
.. figure:: img/fig18-3.jpg
    :align: center

    Figure 18-3. Text editor modules

Minimal communication exists between the modules. The display manager needs to 
know only two things: where the cursor is and what the file currently looks like. All 
the file handler needs to do is read the file, write the file, and keep track of changes. 
Even the work involved in making changes can be minimized. All editing commands, 
no matter how complex, can be broken down into a series of inserts and deletes. 
The command module must take complex user commands and turn them into 
simple inserts and deletes that the file handler can process. 

The information passing between the modules is minimal. In fact, no information 
passes between the command decoder and the display manager. 

A word processor is just a fancy text editor. Where a simple editor only has to worry 
about ASCII characters (one font, one size), a word processor must be able to 
handle many different sizes and shapes.

18.11 Compiler  
--------------

In a compiler, the information being processed is C code. The job of the compiler is 
to transform that information from C source to machine-dependent object code. 
Several stages comprise this process. First, the code is run through the 
preprocessor to expand macros, take care of conditional compilation, and read 
include files. Next, the processed file is passed to the first stage of the compiler, the 
lexical analyzer. 

The lexical analyzer takes as its input a stream of characters and returns a series of 
tokens . A token is a word or operator. For example, let's look at the English 
command: ::

    Open the door.

There are 14 characters in this command. Lexical analysis would recognize three 
words and a period. These tokens are then passed to the parser, where they are 
assembled into sentences. At this stage, a symbol table is generated so that the 
parser can have some idea of what variables are being used by the program. 

Now the compiler knows what the program is supposed to do. The optimizer looks at 
the instructions and tries to figure out how to make them more efficient. This step 
is optional and is omitted unless the ``-O`` flag is specified on the command line.  

The code generator turns the high-level statements into machine-specific assembly 
code. In assembly language, each assembly language statement corresponds to 
one machine instruction. The assembler turns assembly language into binary code 
that can be executed by the machine. 

The general information flow of a compiler is shown in `Figure 18-4`_.

.. _`Figure 18-4`:
.. figure:: img/fig18-4.jpg
    :align: center

    Figure 18-4. Compiler modules

One of the contributing factors to C popularity is the ease with which a C compiler 
can be created for a new machine. The Free Software Foundation distributes the 
source to a C compiler (gcc). Because the source is written in modular fashion, you 
can port it to a new machine by changing the code generator and writing a new 
assembler. Both of these are relatively simple tasks (see the quote at the beginning 
of Chapter 7).

Lexical analysis and parsing are very common and used in a wide variety of 
programs. The utility ``lex`` generates the lexical analyzer module for a program, 
given a description of the tokens used by the program. Another utility, ``yacc``, 
can be used to generate the parser module [#]_.
 
.. [#] 
    For descriptions of these programs, see the Nutshell Handbook  lex & yacc, 
    by John Levine, Tony Mason, and Doug Brown.

18.12 Spreadsheet   
-----------------

A simple spreadsheet takes a matrix of numbers and equations and displays the 
results on the screen. This program manages equations and data.  

The core of a spreadsheet is its set of equations. To change the equations into 
numbers, we need to go through lexical analysis and parsing, just like a compiler. 
But unlike a compiler, we don't generate machine code; instead, we interpret  the 
equations and compute the results. 

These results are passed off to the display manager, which puts them on the screen. 
Add to this an input module that allows the user to edit and change the equations 
and you have a spreadsheet, as shown in `Figure 18-5`_.

.. _`Figure 18-5`:
.. figure:: img/fig18-5.jpg
    :align: center

    Figure 18-5. Spreadsheet modules

18.13 Module Design Guidelines   
------------------------------

There  are no hard and fast rules when it comes to laying out the modules for a 
program. Some general guidelines are:

- The number of public functions in a module should be small. 
- The information passed between modules should be limited. 
- All the functions in a module should perform related jobs.

18.14 Programming Exercises
---------------------------

Exercise 18-1
~~~~~~~~~~~~~

Write a module that will handle page formatting. It should contain 
the following functions:

=================================== ========================
Function                            Description
=================================== ========================
``open_file(char *name)``           Open print file. 
``define_header(char *heading)``    Define heading text. 
``print_line(char *line)``          Send line to file.  
``page(void)``                      Start new page. 
``close_file(void)``                Close printer file.
=================================== ========================

Exercise 18-2
~~~~~~~~~~~~~

Write a module called ``search_open`` that is given an array of 
filenames, searches until it finds one file that exists, and then opens the file. 

Exercise 18-3
~~~~~~~~~~~~~

Write a symbol table program consisting of the following functions: 

=============================== =================================================
Function                        Description
=============================== =================================================
``void enter(char *name)``      Enter name into symbol table. 
``int lookup(char *name)``      Return 1 if name is in table; return 0 otherwise.  
``void delete(char *name)``     Remove name from symbol table. 
=============================== =================================================

Exercise 18-4
~~~~~~~~~~~~~

Take the ``words`` program from `Chapter 17`_, and combine it with the 
infinite array module to create a cross-reference program. (As an added bonus, 
teach it about C comments and strings to create a C cross-referencer.) 

