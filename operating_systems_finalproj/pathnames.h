/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 */

#ifndef _PATHNAMES_H
#define _PATHNAMES_H

void getNextComponent(char *path, char *component);
void stripFirstComponent(char *path, char *remainder);
int extractComponents(char *path, char *components[]);

extern char rootPath[];

#endif /* "./pathnames.h" included */
