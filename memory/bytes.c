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
// PARSE MEMORY REGION MAP
/***********************************************************************/
int parse_maps(pid_t pid, Memo_Region *regions, int max_regions) {
    char path[PATH];
    snprintf(path, sizeof(path), "/proc/%d/maps", pid);

    FILE *file = fopen(path, "r");
    if (file == NULL) {
        fprintf(stderr, "Failed to open file\n");
        return 0;
    }

    char line[MAX_LINE];
    int num_regions = 0;

    while (fgets(line, sizeof(line), file) != NULL && num_regions < max_regions) {
        char *start = line;
        char *end = strchr(line, '-');
        if (end != NULL) {
            *end = '\0';
            regions[num_regions].start = strtoul(start, NULL, 16);
            regions[num_regions].end = strtoul(end + 1, NULL, 16);
            regions[num_regions].readable = 1;
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
        return;
    }

    for (int i = 0; i < region_count; i++) {
        if (!regions[i].readable)
            continue;

        uintptr_t start = regions[i].start;
        uintptr_t end = regions[i].end;
        size_t size = end - start;

        uint8_t *buffer = malloc(size);

        if (!buffer) 
            continue;
        
        ssize_t bytes_read = pread(fd, buffer, size, start);

        if (bytes_read > 0) {
            printf("0x%lx - 0x%lx (%ld bytes)\n", start, end, bytes_read);
            for (ssize_t x = 0; x < bytes_read; x++) {
                printf("%02x ", buffer[x]);
                if ((x + 1) % 16 == 0)
                    printf("\n");
            }
            printf("\n");
        }
        free(buffer);
    }
    close(fd);
}