.. _`Chapter 20`:

Chapter 20. Portability Problems   
================================

..

    | Wherein I spake of most disastrous changes,
    | Of moving accidents by flood and field, 
    | Of hair-breath 'scapes i' the imminent deadly breath...

    -- Shakespeare, on program porting [Othello, Act 1, Scene III] 

You've just completed work on your great masterpiece, a ray -tracing program that 
renders complex three-dimensional shaded graphics on a Cray supercomputer 
using 300MB of memory and 50GB of disk space. What do you do when someone 
comes in and asks you to port this program to an IBM PC with 640K of memory and 
100MB of disk space? Killing him is out; not only is it illegal, but it is considered 
unprofessional. Your only choice is to whimper and start the port. During this 
process, you will find that your nice, working program exhibits all sorts of strange 
and mysterious problems.   

C programs are supposed to be portable; however, C contains many 
machine-dependent features. Also, because of the vast difference between UNIX 
and MS-DOS/Windows, system deficiencies can frequently cause portability 
problems with many programs. 

This chapter discusses some of the problems associated with writing truly portable 
programs as well as some of the traps you might encounter. 

20.1 Modularity   
---------------

One of the tricks to writing portable programs is to put all the nonportable code into 
a separate module. For example, screen handling differs greatly on 
MS-DOS/Windows and UNIX. To design a portable program, you'd have to write 
machine-specific modules that update the screen. 

For example, the HP-98752A terminal has a set of function keys labeled F1 to F8. 
The PC terminal also has a set of function keys. The problem is that they don't send 
out the same set of codes. The HP terminal sends "<esc>p<return>" for F1 and the 
PC sends "<NULL>;". In this case, you would want to write a ``get_code`` routine that 
gets a character (or function-key string) from the keyboard and translates function 
keys. Because the translation is different for both machines, a machine-dependent 
module would be needed for each one. For  the HP machine, you would put together 
the program with *main.c* and *hp-tty.c*, while for the PC you would use *main.c* and 
*pc-tty.c*. 

20.2 Word Size   
--------------

A **long** int is 32 bits, a **short** int is 16 bits, and a normal **int** 
can be 16 or 32 bits, depending on the machine. 
This disparity can lead to some unexpected problems. For example, 
the following code works on a 32-bit UNIX system, but fails when 
ported to MS-DOS/Windows: ::

    int zip;  
    zip = 92126;  
    printf("Zip code %d\n", zip); 

The problem is that on MS-DOS/Windows, ``zip`` is only 16 bits-too-small for 92126. 
To fix the problem, we declare ``zip`` as a 32-bit integer: ::

    long int zip;  
    zip = 92126;  
    printf("Zip code %d\n", zip); 

Now ``zip`` is 32 bits and can hold 92126.  

**Question 20-1:** Why do we still have a problem? ``zip`` does not print correctly on a 
PC. (Click here for the answer `Section 20.9`_) 

20.3 Byte Order Problem   
-----------------------

A **short** int consists of 2 bytes. Consider the number 0x1234. The 2 bytes have the 
values 0x12 and 0x34. Which value is stored in the first byte? The answer is 
machine dependent.  

This uncertainty can cause considerable trouble when you are trying to write 
portable binary files. The Motorola 68000-series machines use one type of byte 
order (ABCD), while Intel and Digital Equipment Corporation machines use another 
(BADC). 

One solution to the problem of portable binary files is to avoid them. Put an option 
in your program to read and write ASCII files. ASCII offers the dual advantages of 
being far more portable and human readable. 

The disadvantage is that text files are larger. Some files may be too big for ASCII. 
In that case, the magic number at the beginning of a file may be useful. Suppose the 
magic number is 0x11223344 (a bad magic number, but a goo d example). When 
the program reads the magic number, it can check against the correct number as
well as the byte -swapped version (0x22114433). The program can automatically fix 
the file problem: ::

    const long int MAGIC      = 0x11223344L /* file identification number*/  
    const long int SWAP_MAGIC = 0x22114433L /* magic-number byte swapped */  
     
    FILE *in_file;                /* file containing binary data */   
    long int magic;               /* magic number from file */  
     
    in_file = fopen("data", "rb");  
    fread((char *)&magic, sizeof(magic), 1, in_file);  
    switch (magic) {  
        case MAGIC:  
            /* No problem */   
            break;   
        case SWAP_MAGIC:  
            printf("Converting file, please wait\n");  
            convert_file(in_file);   
            break;   
        default:  
            fprintf(stderr, "Error:Bad magic number %lx\n", magic);  
            exit (8);  
    }

20.4 Alignment Problems
-----------------------






.. _`Section 20.9`:

