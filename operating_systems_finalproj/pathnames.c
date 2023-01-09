/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 */

/*
 * This file contains helpers specifically to help manage pathnames.
 * You should NOT need to make changes here.
 */

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include "./grayfs.h"
#include "./gfs-helper.h"
#include "./pathnames.h"

/*
 * getNextComponent - return the next component of the specified path
 *
 * -- Requires that the path not be NULL
 * -- Requires that the first character of path NOT be a '/' or a '.'.
 * -- Is NOT destructive to path.
 */
void getNextComponent(char *path, char *component) {
    char workingPath[GRAY_MAX_PATHLENGTH];
    int containsNul = 0;
    int i;

    assert(path != NULL);
    assert(path[0] != '/');
    assert(path[0] != '.');
    for (i = 0; i <= strlen(path) && i < GRAY_MAX_PATHLENGTH; i++) {
        if (path[i] == '\0') {
            containsNul = 1;
        }
    }
    assert(containsNul == 1);
    strncpy(workingPath, path, GRAY_MAX_PATHLENGTH);
    char *separatorLocation = strtok(workingPath, SEPARATOR);
    if (separatorLocation != NULL) {
        strncpy(component, separatorLocation, GRAY_NAME_SIZE);
    } else {
        component = NULL;
    }
    assert(strlen(component) < GRAY_NAME_SIZE);
}

/*
 * stripFirstComponent -- return the path without the first component
 *
 * -- Skips over leading "/".
 * -- Is NOT destructive to path.
 */
void stripFirstComponent(char *path, char *remainder) {
    int i = 0;
    int j = 0;
    int pathLength = (int)strlen(path);

    assert(pathLength < GRAY_MAX_PATHLENGTH);

    remainder[0] = '\0';

    // Skip over leading TOKEN (aka /)
    if (path[0] == TOKEN) i++;

    // Skip over characters until we reach the next TOKEN
    for ( ; i < pathLength; i++) {
        if (path[i] == TOKEN) break;
        if (path[i] == '\0') {
            printf("path[%d] is null\n", i);
            assert(1 == 0);
            break;
        }
    }

    // Copy the remaining characters into remainder
    assert((i < (pathLength-1) || (path[i] == '\0')));
    i++; // Skip the separating TOKEN
    for (j = 0; j < GRAY_MAX_PATHLENGTH && i < pathLength; j++, i++) {
        remainder[j] = path[i];
    }
    assert(j < (GRAY_MAX_PATHLENGTH-1));
    remainder[j] = '\0';
}

/*
 * extractComponents - separate the elements of path by /, placing each component
 *                     into the appropriate components[i] pointer.
 *
 * Components must be an array of character pointers of length GRAY_MAX_DEPTH.
 * This function is NOT destructive of path, but is destructive of components[].
 */
int extractComponents(char *path, char *components[]) { // FIX? Assert on spacing of /'s?
    char workingPath[GRAY_MAX_PATHLENGTH];
    char component[GRAY_NAME_SIZE];
    char remainder[GRAY_MAX_PATHLENGTH];
    int depth = 0;
    int d = 0;
    int pathlen = (int)strlen(path);

    assert(path != NULL);
    assert(pathlen < GRAY_MAX_PATHLENGTH);
    // Strip any trailing '/'
    if ((pathlen > 1) && (path[pathlen-1] == TOKEN)) {
        path[pathlen-1] = '\0';
    }
    if (path[0] == TOKEN) {
        strncpy(workingPath, path+1, GRAY_MAX_PATHLENGTH);
        d = 1;
        components[0] = malloc(GRAY_NAME_SIZE);
        memzero(components[0], GRAY_NAME_SIZE);
        strncpy(components[0], SEPARATOR, GRAY_NAME_SIZE);
    } else {
        strncpy(workingPath, path, GRAY_MAX_PATHLENGTH);
        d = 0;
    }

    strncpy(remainder, workingPath, GRAY_MAX_PATHLENGTH);
    depth = d;
    for ( ; d < GRAY_MAX_DEPTH && remainder[0] != 0; d++) {
        strncpy(workingPath, remainder, GRAY_MAX_PATHLENGTH);
        getNextComponent(workingPath, component);
        stripFirstComponent(workingPath, remainder);
        if (component[0] != 0) {
            assert(strlen(component) > 0);
            components[d] = malloc(GRAY_NAME_SIZE);
            strncpy(components[d], component, GRAY_NAME_SIZE);
            assert(strlen(components[d]) > 0);
            assert(strlen(components[d]) <= GRAY_NAME_SIZE);
            depth = d+1;
        } else {
            break;
        }
    }
    assert(depth <= GRAY_MAX_DEPTH);
    return depth;
}
