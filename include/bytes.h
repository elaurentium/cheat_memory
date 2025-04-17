#ifndef BYTES_H
#define BYTES_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>

#define MAX_LINE 256
#define MAX_BUF 4096
#define PATH 64
#define MAX_REGIONS 1024


typedef struct {
    uintptr_t start;
    uintptr_t end;
    int readable;
} Memo_Region;

/**********************************************************************/
// MAKE PARSE MEMORY REGION MAP
/***********************************************************************/
int parse_maps(pid_t pid, Memo_Region *regions, int max_regions);

/**********************************************************************/
// READ MEMORY
/***********************************************************************/
void read_memory(pid_t pid, Memo_Region *regions, int region_count);

/**********************************************************************/
// MONITOR CHANGES MEMORY
/***********************************************************************/
void monitor_changes(pid_t pid, Memo_Region *regions, int region_count);

#endif