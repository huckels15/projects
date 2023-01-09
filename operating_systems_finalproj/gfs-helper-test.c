/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 */


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "./gfs-helper.h"

struct gray_fobj root;

int testGrayChild(char *path) {
    char pathname[GRAY_MAX_PATHLENGTH];
    char lastComponent[GRAY_NAME_SIZE];
    struct gray_fobj *object;
    char separator = '/';

    strncpy(pathname, path, GRAY_MAX_PATHLENGTH);
    strncpy(lastComponent, (char *)(rindex(path, separator)+1), GRAY_NAME_SIZE);
    printf("testing %s with lastComponent *%s* [0]=<%c>/<%d>\n", path, lastComponent, lastComponent[0], (int)lastComponent[0]);
    if (lastComponent[0] == '\0') {
        printf("******copying / in there\n");
        strcpy(lastComponent, "/");
    }
    object = gray_child(&root, pathname);
    if ((object) && (strncmp(object->name, lastComponent, GRAY_NAME_SIZE) == 0)) {
        printf("Yeah! We found the proper child\n");
        return 0;
    } else {
        printf("Uh oh...\n");
        return -1;
    }
}

int main(int argc, char *argv[]) {

    struct gray_fobj *element1 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *element2 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *element3 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *dir1 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *dir2 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *file11 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *file21 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *file22 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *file23 = malloc(sizeof(struct gray_fobj));
    struct gray_fobj *file24 = malloc(sizeof(struct gray_fobj));
    char pathname[GRAY_MAX_PATHLENGTH];

	printf("  Initializing the file system objects...\n");
    init_fobj(&root, GrayDir, "/");
    init_fobj(element1, GrayFile, "File1");
    init_fobj(element2, GrayFile, "File2");
    init_fobj(element3, GrayFile, "File3");
    init_fobj(dir1, GrayDir, "Dir1");
    init_fobj(file11, GrayFile, "Dir1File1");
    init_fobj(dir2, GrayDir, "Dir2");
    init_fobj(file21, GrayFile, "Dir2File1");
    init_fobj(file22, GrayFile, "Dir2File2");
    init_fobj(file23, GrayFile, "Dir2File3");
    init_fobj(file24, GrayFile, "Dir2File4");

	printf("  Inserting the file objects into a structure 1...\n");
    gray_insert(&root, element3);
    gray_insert(&root, dir1);
    gray_insert(&root, element1);
    gray_insert(&root, element2);

    gray_insert(dir1, file11);
    gray_insert(&root, dir2);
    gray_insert(dir2, file22);
    gray_insert(dir2, file21);
    gray_insert(dir2, file23);
    gray_insert(dir2, file24);

	printf("File System Initialised. Begin testing...\n");
    printDirFull(&root);

    /*
    printObject(&root);
    printObject(&file21);
    sleep(5);
    gray_truncate(&file21, 100);
    printObject(&file21);
    */

    printf("Testing read and write\n:");
    printf("Before Write Value: *%s*\n", gray_read(file21, 0, 33));
    printObjectContent(file21);
    char myContent[128];
    strcpy(myContent, "Hello world");
    gray_write(file21, 0, myContent);
    printf("After write:\n");
    printObjectContent(file21);
    printf("Read: %s\n", gray_read(file21, 2, 33));

    printf("\nTesting gray_child\n");
    strcpy(pathname, "/Dir1/Dir1File1");
    assert(testGrayChild(pathname) == 0);

    strcpy(pathname, "/Dir2");
    assert(testGrayChild(pathname) == 0);

    strcpy(pathname, "/");
    assert(testGrayChild(pathname) == 0);

    strcpy(pathname, "/Dir2/Foo");
    assert(testGrayChild(pathname) == -1);

    strcpy(pathname, "/Dir3/Foo");
    assert(testGrayChild(pathname) == -1);

	printf("File System Status at the beginning of testing remove...\n");
    printDirFull(&root);
    printf("  Removing child in the middle of the list.\n");
    gray_remove(element1);
//    printDirFull(&root);
    printf("  Removing child at the front of the list.\n");
    gray_remove(element3);
//    printDirFull(&root);
    printf("  Removing first child in a subdirectory.\n");
    gray_remove(file22);
//    printDirFull(&root);
    printf("  Removing middle child in a subdirectory.\n");
    gray_remove(file23);
//    printDirFull(&root);
    printf("  Removing last element in children list in a subdirectory.\n");
    gray_remove(file24);
//    printDirFull(&root);
    printf("  Removing last child in a subdirectory.\n");
    gray_remove(file21);
//    printDirFull(&root);

    printf("  Removing an empty subdirectory.\n");
    gray_remove(dir2);
//    printDirFull(&root);
    printf("State of file system after all the removals:\n");
    printDirFull(&root);

    return 0;
}
