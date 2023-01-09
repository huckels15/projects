/*
 * Long Gray Line File System
 * Copyright (C) 2022 Maria R. Ebling, Ph.D <maria.ebling@westpoint.edu>
 */

#include <string.h>
#include "./utils.h"

/*
 * Utilities
 */
void memzero(char *addr, int size) {
    memset(addr, 0, size);
}
