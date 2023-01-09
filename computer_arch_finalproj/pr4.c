#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h> 
#include "uthash.h"

#define LINE_MAX 200

// Troy D. Hanson, Arthur O'Dwyer. uthash User Guide. Github. [Accessed 2021 November 20].
// https://troydhanson.github.io/uthash/userguide.html#_string_keys  
// This structure follows the same format and was adapted from the structure in the 
// "Defining a structure that can be hashed" section in the uthash User Guide.
struct info {
    char state[50];
    int appearances;
    UT_hash_handle hh; 
};

// Troy D. Hanson, Arthur O'Dwyer. uthash User Guide. Github. [Accessed 2021 November 20].
// https://troydhanson.github.io/uthash/userguide.html#_string_keys  
// This variable was adapted from the "Declare the hash" section 
// in the uthash user guide.
struct info *bins = NULL;

// Troy D. Hanson, Arthur O'Dwyer. uthash User Guide. Github. [Accessed 2021 November 20].
// https://troydhanson.github.io/uthash/userguide.html#_string_keys  
// This add_state function was adapted from the add_user function in the Add item section,
// Checking uniqueness subsection. I modified it to be able to work with a string key and to
// increment the value by one if a duplicate was detected.
void add_state(char *name, int appearance){
    struct info *s;
    HASH_FIND_STR(bins, name, s);  
    if (s == NULL) {
        s = (struct info*)malloc(sizeof(struct info));
        strcpy(s->state, name);
        HASH_ADD_STR(bins, state, s);  
        s->appearances = appearance;
    }
    else if (s != NULL) {
        s->appearances ++;
    }
}

// Troy D. Hanson, Arthur O'Dwyer. uthash User Guide. Github. [Accessed 2021 November 20].
// https://troydhanson.github.io/uthash/userguide.html#_string_keys  
// My print_bins function was adapted from the print_users function in the Iterating and Sorting
// section in the uthash user guide. I modified it to work for the print format I needed and to 
// print only as many bins as the user wanted. 
void print_bins(int limit) {
    struct info *s;
    for (s = bins; s != NULL; s = (struct info*)(s->hh.next)) {
        if (limit > 0){
            printf("%s %d\n", s->state, s->appearances);
            limit -= 1;
        }
        else {
            return;
        }
    }
}

// Troy D. Hanson, Arthur O'Dwyer. uthash User Guide. Github. [Accessed 2021 November 20].
// https://troydhanson.github.io/uthash/userguide.html#_string_keys  
// My state_sort, appearance_sort, sort_by_state, and sort_by_appearance functions were adapted
// from the functions in the "Sorting items in the hash" section of the uthash user guide. state_sort
// is the same code as name_sort in the user guide because it needed to serve the same exact function.
// appearance_sort is the same as id_sort execpt with the subtraction flipped to sort the states from 
// highest frequenecy to lowest frequency. sort_by_state and sort_by_appearance are the same as sort_by_name
// and sort_by_id respectively in order to be able to implement my sort functions described above to work in 
// the hash table.
int state_sort(struct info *a, struct info *b){
    return strcmp(a->state, b->state);
}

int appearance_sort(struct info *a, struct info *b){
    return (b-> appearances - a-> appearances);
}

void sort_by_state(){
    HASH_SORT(bins, state_sort);
}

void sort_by_appearances(){
    HASH_SORT(bins, appearance_sort);
}

int main(int argc, char **argv){
    int fp_checker = 1;
    int digit_checker = 1;
    if (argc != 3){
        fprintf(stderr, "usage for %s \nfirst input: <filename.csv>\n", argv[0]);
        fprintf(stderr, "second input: n for the number of cities you wish to view.\n");
        return 1;
    }
    char line[LINE_MAX];
    FILE *fp = fopen(argv[1], "r");
    char *name;
    if (!fp){
        fp_checker = 0;
    }

    int len = strlen(argv[2]);
    int i;
    char argument[20];
    strcpy(argument, argv[2]);

    // C isdigit(). Programiz.com. [Accessed 20 November 2021]. https://www.programiz.com/c-programming/library-function/ctype.h/isdigit.
    // This article was used to figure out how to use the isdigit() function we see in 
    // other programming languages in C. This article provided the header file that needed to be used
    // as well as what the function takes and returns. This function allowed me to make sure the second user
    // input is an integer like it needs to be.
    for (i = 0; i < len; i++){
        if (isdigit(argument[i]) == 0){ 
            digit_checker = 0;
        }
    }

    if (digit_checker == 0 && fp_checker == 0){
        fprintf(stderr, "This file does not exist. Additionally, your second argument must be an integer!\n");
        return 1;
    }
    else if (digit_checker == 0 && fp_checker == 1){
        fprintf(stderr, "Make sure your second argument is a positive integer!\n");
        return 2;
    }
    else if (fp_checker == 0 && digit_checker == 1){
        fprintf(stderr, "Error opening file.\n");
        return 3;
    }

    while(fgets(line, LINE_MAX, fp) != NULL) {
        strtok(line, ",");
        strtok(NULL, ",");
        strtok(NULL, ",");
        name = strtok(NULL, "\n");
        add_state(name,1);
    }
    sort_by_state();
    sort_by_appearances();
    print_bins(atoi(argv[2]));
    fclose(fp);
    free(bins);
    return 0;
}