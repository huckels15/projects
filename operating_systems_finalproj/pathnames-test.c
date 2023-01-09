/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 */

#include <stdio.h>
#include <string.h>
#include "./grayfs.h"
#include "./pathnames.h"

char rootPath[GRAY_MAX_PATHLENGTH];

/*
 * test - used for testing
 */
void test(char *pathname) {
    char *componentArray[GRAY_MAX_DEPTH];
    int depth = 0;
    int d = 0;
    char path1[GRAY_MAX_PATHLENGTH];

    printf("Testing: %s\n", pathname);

    for(d = 0; d < GRAY_MAX_DEPTH; d++) componentArray[d] = 0;
    strncpy(path1, pathname, GRAY_MAX_PATHLENGTH);

    printf("  Printing the components of the path:\n");
    depth = extractComponents(path1, componentArray);
    printf("    Depth = %d\n", depth);
    for (d = 0; d < depth && componentArray[d] != NULL; d++) {
        printf("    components[%d] = %s\n", d, componentArray[d]);
    }

}
/*
 * main -- this is used only for testing
 */
int main(int argc, char *argv[]) {
    char path[1024];

    strcpy(rootPath, "/maria/gfs/");


    strcpy(path, "/usr/local/bin");
    test(path);

    strcpy(path, "usr/local/bin/");
    test(path);

    strcpy(path, "/");
    test(path);

    strcpy(path, "/folder");
    test(path);

    // The following correctly asserts!
    //strcpy(path, "./foo");
    //test(path);
    return(0);
}
