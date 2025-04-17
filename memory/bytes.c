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
#define MAX_REGION_SIZE 16384
#define BLOCK_SIZE 4096


typedef struct {
    uintptr_t start;
    uintptr_t end;
    int readable;
} Memo_Region;

/**********************************************************************/
// PARSE MEMORY REGION MAP
/***********************************************************************/
int parse_maps(pid_t pid, Memo_Region *regions, int max_regions) {
    char path[PATH];
    snprintf(path, sizeof(path), "/proc/%d/maps", pid);

    FILE *file = fopen(path, "r");
    if (file == NULL) {
        fprintf(stderr, "Failed to open %s: %s\n", path, strerror(errno));
        return 0;
    }

    char line[MAX_LINE];
    int num_regions = 0;

    while (fgets(line, sizeof(line), file) != NULL && num_regions < max_regions) {
        char *start = line;
        char *end = strchr(line, '-');
        char perms[5];

        if (end != NULL) {
            *end = '\0';
            regions[num_regions].start = strtoul(start, NULL, 16);
            regions[num_regions].end = strtoul(end + 1, NULL, 16);
            if (sscanf(end + 1, "%*x %4s", perms) == 1) {
                regions[num_regions].readable = (perms[0] == 'r');
            } else {
                regions[num_regions].readable = 0;
            }
            num_regions++;
        }
    }

    fclose(file);
    return num_regions;
}

/**********************************************************************/
// I DONT FUCKING KNOW WHAT IM DOING HERE, BUT IT WORKS(I GUESS...)
/***********************************************************************/

void read_memory(pid_t pid, Memo_Region *regions, int region_count) {
    char memo_path[PATH];
    snprintf(memo_path, sizeof(memo_path), "/proc/%d/mem", pid);

    int fd = open(memo_path, O_RDONLY);
    if (fd == -1) {
        perror("open");
        fprintf(stderr, "Needed root privileges\n");
        return;
    }

    for (int i = 0; i < region_count; i++) {
        if (!regions[i].readable)
            continue;

        uintptr_t start = regions[i].start;
        uintptr_t end = regions[i].end;
        size_t size = end - start;
        size_t to_read = size > MAX_REGION_SIZE ? MAX_REGION_SIZE : size;

        uint8_t *buffer = malloc(to_read);

        if (!buffer) 
            continue;
        
        ssize_t bytes_read = pread(fd, buffer, to_read, start);

        if (bytes_read > 0) {
            printf("0x%lx - 0x%lx (%ld bytes)\n", start, start + to_read, bytes_read);
            for (ssize_t i = 0; i < bytes_read; i += 16) {
                printf("0x%016lx: ", start + i);
                for (int j = 0; j < 16 && i + j < bytes_read; j++) {
                    printf("%02x ", buffer[i + j]);
                }
                printf("\n");
            }
        }
        free(buffer);
    }
    close(fd);
}

void monitor_changes(pid_t pid, Memo_Region *regions, int region_count) {
    char memo_path[PATH];
    snprintf(memo_path, sizeof(memo_path), "/proc/%d/mem", pid);
    int fd = open(memo_path, O_RDONLY);
    if (fd == -1) {
        perror("open");
        return;
    }

    for (int i = 0; i < region_count; i++) {
        if (!regions[i].readable) 
            continue;

        uintptr_t start = regions[i].start;
        uintptr_t end = regions[i].end;
        size_t size = end - start;


        uint8_t *buffer = malloc(size);
        uint8_t *previous = malloc(size);
        if (!buffer || !previous) 
            continue;

        if (pread(fd, previous, size, start) <= 0) 
            continue;

        printf("Monitoring regions: 0x%lx - 0x%lx...\n", start, end);

        while (1) {
            usleep(50000);

            if (pread(fd, buffer, size, start) <= 0) 
                continue;

            for (size_t j = 0; j < size; j++) {
                if (buffer[j] != previous[j]) {
                    printf("Changes at 0x%lx: 0x%02x -> 0x%02x\n",
                           start + j, previous[j], buffer[j]);
                    previous[j] = buffer[j];
                }
            }
        }

        free(buffer);
        free(previous);
    }

    close(fd);
}
