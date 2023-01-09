/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 */

#ifndef _GRAYFS_H
#define _GRAYFS_H 1

#define SEPARATOR "/"
#define TOKEN '/'

#define GRAY_NAME_SIZE 128
#define GRAY_MAX_FILESIZE 1024
#define GRAY_MAX_DEPTH 10
#define GRAY_MAX_PATHLENGTH (GRAY_NAME_SIZE*GRAY_MAX_DEPTH)+1

#endif /* "./grayfs.h" included. */