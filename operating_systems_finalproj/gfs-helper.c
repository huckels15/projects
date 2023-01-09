/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 */

/*
 * This file contains helper functions so that you don't have to write
 * the C code to maintain the data structures needed to maintain your
 * file system data.
 */

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>

#include <libgen.h>
#include <assert.h>
#include <time.h>
#include <errno.h>
#include "./grayfs.h"
#include "./pathnames.h"
#include "./gfs-helper.h"
#include "./utils.h"

/*
 * getTypeChar - takes a FileType as input and returns a single character.
 */
char getTypeChar(enum FileType t) {
    char typeChar = '!';
    switch(t) {
        case GrayDir:  typeChar = 'd'; break;
        case GrayFile: typeChar = 'f'; break;
        case GrayLink: typeChar = 'l'; break;
        case GrayDev:  typeChar = 'v'; break;
        default:
            typeChar = '?';
            printf("Received a file type value of %d\n", (int)t);
            break;
    }
    return typeChar;
}

char *gray_dirname(char *path) {
    char *returnValue = NULL;
    int isSlash = strcmp(path, "/");
    int startsDot = (path[0] == '.');
    char originalPath[GRAY_MAX_PATHLENGTH];
    int pathLen = strlen(path);
    int isEmpty = strcmp(path, "");

    strcpy(originalPath, path);
    returnValue = dirname(path);
    if (isEmpty == 0) {
        printf("gray_dirname on %s is empty, returning %s\n", originalPath, returnValue);
    }
    if ((isSlash == 0) && (pathLen == 1)) {
        printf("gray_dirname on %s returning %s\n", originalPath, returnValue);
    }
    if (startsDot) {
        printf("gray_dirname starts with . returning %s\n", returnValue);
    }
    return returnValue;
}

char *gray_basename(char *path) {
    char *returnValue = NULL;
    int isSlash = strcmp(path, "/");
    int startsDot = (path[0] == '.');
    int pathLen = strlen(path);
    char originalPath[GRAY_MAX_PATHLENGTH];
    int isEmpty = strcmp(path, "");

    strcpy(originalPath, path);
    returnValue = basename(path);
    if (isEmpty == 0) {
        printf("gray_dirname on %s is empty, returning %s\n", originalPath, returnValue);
    }
    if ((isSlash == 0) && (pathLen == 1)) {
        printf("gray_basename on %s returning %s\n",  originalPath, returnValue);
    }
    if (startsDot) {
        printf("gray_basename starts with . returning %s\n", returnValue);
    }
    return returnValue;
}


/*
 * init_fobj - Initializes a file object for GrayFS
 */
void init_fobj(struct gray_fobj* obj, enum FileType type, char *name) {
    time_t now = time(0);

    memzero((char *)obj, sizeof(struct gray_fobj));
    obj->type = type;
    strncpy(obj->name, name, GRAY_NAME_SIZE);
    switch (type) {
        case GrayDir:
            obj->mode = S_IFDIR | 0755;
            obj->nlink = 2;
            //obj->dev = 0;
            break;
        case GrayFile:
            obj->mode = S_IFREG | 0444;
            obj->nlink = 1;
            //obj->dev = 0;
            break;
        case GrayLink:
            obj->mode = S_IFLNK | 0777;
            obj->nlink = 1;
            //obj->dev = 0;
            break;
        case GrayDev:
            obj->mode = S_IFCHR | 0660;
            obj->nlink = 1;
            //obj->dev = 5;
            break;
        default:
            assert(false);
    }
    obj->user_id = getuid();
    obj->group_id = getgid();
    obj->atime = now;
    obj->mtime = now;
    obj->ctime = now;
    obj->extended_attr = NULL;
    memzero(obj->content, GRAY_MAX_FILESIZE);
    obj->length = 0;
    obj->parent = NULL;
    obj->children = NULL;
    obj->sibling = NULL;
}

/*
 * updateTimes - updates the accessed, modified, and status changed attributes
 *               of a grayfs file object
 */
void updateTimes(struct gray_fobj *object, bool accessed, bool modified, bool status) {
    assert(object != NULL);
    time_t now = time(0);
    if (accessed) {
        object->atime = now;
    }
    if (modified) {
        object->mtime = now;
    }
    if (status) {
        object->ctime = now;
    }
}

/*
 * gray_stat - Returns an fstat object based on the attributes of a file object
 *
 * We can ignore the st_dev, st_blksize, and st_ino.
 */
void gray_stat(struct gray_fobj *object, struct stat *stat_buf) {
    memzero((char *)stat_buf, sizeof(struct stat));
    stat_buf->st_mode = object->mode;
    stat_buf->st_nlink = 2;
    stat_buf->st_uid = object->user_id;
    stat_buf->st_gid = object->group_id;
    stat_buf->st_size = strlen(object->content);
    stat_buf->st_atime = object->atime;
    stat_buf->st_mtime = object->mtime;
    stat_buf->st_ctime = object->ctime;
}

/*
 * getFileObject - Get the file object referenced by path
 */
struct gray_fobj *getFileObject(struct gray_fobj *root, char *path) {
    char workingPath[GRAY_MAX_PATHLENGTH];

    strncpy(workingPath, path, GRAY_MAX_PATHLENGTH);
    printf("getFileObject calling gray_child with *%s* and *%s*\n", workingPath, path);
    return gray_child(root, workingPath);
}

/*
 * match_child - Traverses a list of children, returning the file object with
 *               the matching name or NULL, if no match exists.
 */
struct gray_fobj *matchChild(struct gray_fobj *children, char *name) {
    struct gray_fobj *child = children;

    while (child != NULL) {
        if (strncmp(child->name, name, GRAY_NAME_SIZE) == 0) {
            break;
        } else {
            child = child->sibling;
        }
    }
    return child;
}

/*
 * gray_child - Given a path, crawl the path, element by element, and return
 *              the file object associated with the final component of the path
 */
struct gray_fobj *gray_child(struct gray_fobj *start, char *path) {
    struct gray_fobj *object = start;
    struct gray_fobj *child = NULL;
    char *componentArray[GRAY_MAX_DEPTH];
    int depth = 0;
    int d = 0;
    char workingPath[GRAY_MAX_PATHLENGTH];
    int foundChild = 0;

    assert(start != NULL);

    // Make sure every component in componentArray is empty
    for (d = 0; d < GRAY_MAX_DEPTH; d++) componentArray[d] = 0;

    strncpy(workingPath, path, GRAY_MAX_PATHLENGTH);
    depth = extractComponents(workingPath, componentArray);
    printf("gray_child: depth = %d, path = %s\n", depth, path);
    for (d = 0; d < depth; d++) {
        printf("component[%d] = %s\n", d, componentArray[d]);
    }
    printf("Start->name = %s\n", start->name);
    if ((depth == 1) && (strncmp(start->name, path, GRAY_NAME_SIZE) == 0)) {
            printf("Child is root\n");
            child = object;
            return child;
    }
    for (d = 0; d < depth-1; d++) {
        assert(object != NULL); // MRE: new 7/7
        assert(object->type == GrayDir); // MRE: new 7/7
        assert(strncmp(object->name,componentArray[d], GRAY_NAME_SIZE) == 0);

        object = object->children;
        foundChild = 0;
        while (object != NULL) {
            if (strncmp(object->name, componentArray[d+1], GRAY_NAME_SIZE) == 0) {
                // Found the next component of the path
                child = object;
                foundChild = 1;
                break;
            } else {
                object = object->sibling;
            }
        }
        if (!foundChild) {
            break;
        }
    }

    // Free the memory that extractComponents allocated!
    for (d = 0; d < depth; d++) {
        free(componentArray[d]);
    }

    if ((child != NULL) && (strncmp(child->name, componentArray[d-1], GRAY_NAME_SIZE) != 0)) {
        child = NULL;
    }

    return child;
}

/*
 * Directory hierarchy
 */
struct gray_fobj* gray_findLastSibling(struct gray_fobj *parent) {
    assert(parent != NULL);

    struct gray_fobj *nextChild = parent->children;
    struct gray_fobj *lastChild = NULL;
    while (nextChild != NULL) {
        lastChild = nextChild;
        nextChild = nextChild->sibling;
    }
    return lastChild;
}

/*
 * gray_findOlderSibling - return the older sibling of child
 *
 * Returns NULL if there are no older children.
 */
struct gray_fobj* gray_findOlderSibling(struct gray_fobj *parent, struct gray_fobj *child) {
    assert(parent != NULL);
    assert(parent->children != NULL);
    assert(child != NULL);
    assert(child->parent == parent);

    struct gray_fobj *nextChild = parent->children;
    struct gray_fobj *olderSibling = NULL;
    while ((nextChild != NULL) && (nextChild != child)) {
        olderSibling = nextChild;
        nextChild = nextChild->sibling;
    }
    return olderSibling;
}

/*
 * gray_insert - Insert a child object into the parent object
 */
void gray_insert(struct gray_fobj *parent, struct gray_fobj *child) {
    assert(parent != NULL);
    assert(child != NULL);
    assert(child->sibling == NULL);
    assert(child->parent == NULL);
    assert(child->children == NULL);

    /* Set up the directory hierarchy */
    child->parent = parent;

    /* Insert this child in the proper location */
    if (parent->children == NULL) {
        /* Add the first child */
        parent->children = child;
    } else {
        /* Add this child to the end of the list of children */
        struct gray_fobj *lastSibling;
        lastSibling = gray_findLastSibling(parent);
        assert(lastSibling->sibling == NULL);
        lastSibling->sibling = child;
    }
}

/*
 * gray_remove - Remove a child object from the parent object
 */
void gray_remove(struct gray_fobj *object) {
    assert(object != NULL);
    if (object->parent == NULL) { printf("Removing root illegal\n"); }
    assert(object->parent != NULL);

    struct gray_fobj *parent = object->parent;
    struct gray_fobj *olderSibling = gray_findOlderSibling(parent, object);

    if (object->type == GrayDir) {
        assert(object->children == NULL);
    }

    if (olderSibling == NULL) {
        /*
         * There are no older siblings.
         * We just need to set the parent's children pointer to point at the
         * next younger child, which may be NULL.
         */
        parent->children = object->sibling;
    } else {
        /*
         * There is an older sibling.
         * We need to set the older sibling's sibling pointer to point at
         * the object's sibling pointer (the next younger child), which may
         * be NULL.
         */
        olderSibling->sibling = object->sibling;
    }

    // Free the object's memory
    free(object);
}

struct gray_fobj *find(struct gray_fobj *directory, char *name) {
    struct gray_fobj *thisObject;
    int nameLength = strlen(name);

    assert(directory != NULL);
    assert(nameLength != 0);
    thisObject = directory->children;
    while ((thisObject != NULL) && strncmp(name, thisObject->name, GRAY_NAME_SIZE)) {
        thisObject = thisObject->sibling;
    }
    return thisObject;
}

void printDirElements(struct gray_fobj *directory) {
    struct gray_fobj *child = NULL;

    assert(directory != NULL);
    assert(directory->type == GrayDir);


    printf("%s:\n", directory->name);

    child = directory->children;
    while (child != NULL) {
        printf("  %s: %c\n", child->name, getTypeChar(child->type));
        child = child->sibling;
    }
    printf("\n");
}

void printDirFull(struct gray_fobj *directory) {
    struct gray_fobj *child = NULL;

    printDirElements(directory);
    child = directory->children;
    while (child != NULL) {
        if (child->type == GrayDir) {
            printDirFull(child);
        }
        child = child->sibling;
    }

}

void printObject(struct gray_fobj *object) {
    char timeBuffer[20];
    assert(object != NULL);
    strftime(timeBuffer, 20, "%Y-%m-%d %H:%M:%S", localtime(&object->mtime));
    printf("%c %d %d %d %s %s\n", getTypeChar(object->type), object->user_id, object->group_id, object->length, timeBuffer, object->name);
}

void printObjectContent(struct gray_fobj *object) {
    assert(object != NULL);
    assert(object->name != NULL);
    assert(object->type == GrayFile);
    assert(object->content != NULL);

    printf("Object name: %s\n", object->name);
    printf("Object content: *%s*\n", object->content);
}

/*
 * gray_read - Read length bytes starting at offset in the specified file
 */
char *gray_read(struct gray_fobj *file, int offset, int length, char * readBuffer) {

    assert(file != NULL);
    assert(offset >= 0);
    assert(length >= 0);
    assert((offset + length) < GRAY_MAX_FILESIZE);
    if (file->type == GrayDir) {
        errno = -EISDIR;
        return NULL;
    }
    if (file->type == GrayLink) {
        errno = -EISNAM;
        return NULL;
    }

    if ((offset + length) >= file->length) {
        length = file->length - offset;
    }

    memzero(readBuffer, GRAY_MAX_FILESIZE);
    strncpy(readBuffer, &(file->content[offset]), length);
    updateTimes(file, true, false, false);
    return readBuffer;
}

/*
 * gray_write - Write buffer to the specified file starting at offset
 */
int gray_write(struct gray_fobj *file, int offset, char *buffer) {
    int length = -1;
    int bufferLength = strlen(buffer);
    bool lengthChanged = false;

    assert(file != NULL);
    if (file->type == GrayDir) {
        return -EISDIR;
    }
    if (file->type == GrayLink) {
        return -EISNAM;
    }

    assert(offset <= GRAY_MAX_FILESIZE);
    length = offset + bufferLength;
    assert(length <= GRAY_MAX_FILESIZE);
    if (file->length < length) { // MRE: Should this be !=? What if it is longer?
        file->length = length;
        lengthChanged = true;
    }
    strncpy(&(file->content[offset]), buffer, bufferLength);
    updateTimes(file, true, true, lengthChanged);
    return bufferLength;
}

/*
 * gray_truncate - Truncate the file to the specified length
 */
void gray_truncate(struct gray_fobj *file, int length) {
    int i = 0;

    assert(file != NULL);
    assert(length < GRAY_MAX_FILESIZE);
    int startZeroing = length;
    int startLength = file->length;

    if (file->length < length) {
        startZeroing = file->length;
        file->length = length;
    }

    for (i = startZeroing; i < GRAY_MAX_FILESIZE; i++) {
        file->content[i] = '\0';
    }

    if (startLength != file->length) {
        updateTimes(file, false, true, true);
    }
}

