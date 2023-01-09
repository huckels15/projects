#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h> 
#include <unistd.h>
#include "uthash.h"
#include <pthread.h>

long fsize; //length
char *file_arr; //input str
long THREAD_COUNT; //num threads
pthread_mutex_t MUTEX;

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

void add_state(char *name, int local_ap){
    struct info *s;
    HASH_FIND_STR(bins, name, s); 
    if (s == NULL) {
        s = (struct info*)malloc(sizeof(struct info));
        strcpy(s->state, name);
        HASH_ADD_STR(bins, state, s);  
        s->appearances = local_ap;
    }
    else if (s != NULL) {
        s->appearances += local_ap;
    }
}

void add_state_p(char *name, struct info **ahash){
    struct info *s;
    HASH_FIND_STR(*ahash, name, s); 
    if (s == NULL) {
        s = (struct info*)malloc(sizeof(struct info));
        strcpy(s->state, name);
        HASH_ADD_STR(*ahash, state, s);  
        s->appearances = 1;
    }
    else if (s != NULL) {
        s->appearances ++;
    }
}

struct starts{
    int start_num;
    int end;
};

struct starts *starts_and_stops;

void *start_stop(void * rank) {
    long myrank = (long)rank;
    long chunk = fsize / THREAD_COUNT;
    int start = myrank * chunk;
    int end = (myrank + 1) * chunk;  
    if (myrank != 0) {
        while((file_arr[start] > '9' || file_arr[start] < '0' || (file_arr[start - 1]) != '\n')){
            start --;
        }
    }
    while (file_arr[end] != '\n'){
        end--;
    }
    if (myrank == THREAD_COUNT - 1){
        end = fsize;
    }
    if (start <= starts_and_stops[myrank - 1].end && myrank != 0){
        start = starts_and_stops[myrank - 1].end + 1;
    }
    starts_and_stops[myrank].start_num = start;
    starts_and_stops[myrank].end = end;
    return NULL;
}

// Matthews, Newhall, Webb. 2020. Dive into Systems. 1st Edition. Dive Into Systems LLC. Section 14.6.
// My implementation for my tok_it_up function used the countsElemsStr_p_v2.c file as a skeleton, most of the
// function is very similar to the one written in that example.

void *tok_it_up(void * rank){
    long myrank = (long)rank;

    char *rest;

    struct info *myhash = NULL;
    char *token;
    long end = starts_and_stops[myrank].end;

    file_arr[end] = 0;
    strtok_r(file_arr + starts_and_stops[myrank].start_num, ",", &rest);
    strtok_r(NULL, ",", &rest);
    strtok_r(NULL, ",", &rest);
    token = strtok_r(NULL, "\n", &rest);
    while (token != NULL){
        add_state_p(token, &myhash);
        strtok_r(NULL, ",", &rest);
        strtok_r(NULL, ",", &rest);
        strtok_r(NULL, ",", &rest);
        token = strtok_r(NULL, "\n", &rest);
    }
    pthread_mutex_lock(&MUTEX);
    struct info *s;
    for (s = myhash; s != NULL; s = (struct info*)(s->hh.next)) {
        add_state(s->state, s->appearances);
    }
    pthread_mutex_unlock(&MUTEX);
    free(myhash);
    return NULL;
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
    if (argc != 5){
        fprintf(stderr, "usage for %s \nfirst input: <filename.csv>\n", argv[0]);
        fprintf(stderr, "second input: n for the number of cities you wish to view.\n");
        fprintf(stderr, "third input: n for the number of threads you wish to use.\n");
        fprintf(stderr, "fourth input: 1 or 0 for if you would like the result printed or not.\n");
        return 1;
    }
    FILE *fp = fopen(argv[1], "r");
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

    THREAD_COUNT = atoi(argv[3]);
    if (THREAD_COUNT < 1 || THREAD_COUNT > 8){
        fprintf(stderr, "You need between 0 and 8 threads.\n");
        return 4;
    }

    int print_bool = atoi(argv[4]);
    if (print_bool != 0 && print_bool != 1){
        fprintf(stderr, "Select if you would like the output printed by using 1 or 0 in the 4th argument position.\n");
        return 5;
    }

    // user529758. C Programming: How to read the whole file contents into a buffer. Stackoverflow.com. [Accessed 5 Decemeber 2021].
    // https://stackoverflow.com/questions/14002954/c-programming-how-to-read-the-whole-file-contents-into-a-buffer 
    // I did not know how to read an entire file into a single string, only how to read it line by line. This stackoverflow
    // entry provided me with how to read an entire file into a single buffer.
    fseek(fp, 0, SEEK_END);
    fsize = ftell(fp);
    rewind(fp);
    file_arr = malloc(fsize);
    fread(file_arr, 1,  fsize, fp);

    long thread;
    pthread_t *thread_handles = malloc(THREAD_COUNT* sizeof(pthread_t));
    starts_and_stops = malloc(THREAD_COUNT * sizeof(struct starts));
    int t;
    for (t = 0; t < THREAD_COUNT; t++){
        starts_and_stops[t].start_num = 0;
        starts_and_stops[t].end = 0;
    }


    //Sacheen. Conditional wait and signal in multi-threading. GeeksForGeeks.com. [Accessed 9 December 2021].
    //https://www.geeksforgeeks.org/condition-wait-signal-multi-threading/.
    // For my start_stop function, the start points for each thread are contingent on the end values of the thread
    // before it. As a result, if they do not run in sequence, there would be an error with how the file was strtoked.
    // This article spoke of the sleep function as well as it's header file which I implemented to make the threads run
    // in order.
    for (thread = 0; thread < THREAD_COUNT; thread ++){
        pthread_create(&thread_handles[thread], NULL, start_stop, (void*)thread);
        sleep(0.05);
    }

    for (thread = 0; thread < THREAD_COUNT; thread ++){
        pthread_join(thread_handles[thread], NULL);
    }

    
    pthread_mutex_init(&MUTEX, NULL);
    for (thread = 0; thread < THREAD_COUNT; thread ++){
        pthread_create(&thread_handles[thread], NULL, tok_it_up, (void*)thread);
    }

    for (thread = 0; thread < THREAD_COUNT; thread ++){
        pthread_join(thread_handles[thread], NULL);
    }
    pthread_mutex_destroy(&MUTEX);

    free(thread_handles);
    free(file_arr);
    free(starts_and_stops);
    sort_by_state();
    sort_by_appearances();
    if (print_bool == 1){
        print_bins(atoi(argv[2]));
    }
    fclose(fp);
    free(bins);
    return 0;
}