#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include <string.h>
#include <sys/sysinfo.h>

#define LINE_LEN 256
#define MAX_READ_SIZE 64

void map_memo(pid_t pid) {
    char map_path[64], mem_path[64];

    snprintf(map_path, sizeof(map_path), "/proc/%d/maps", pid);
    snprintf(mem_path, sizeof(mem_path), "/proc/%d/mem", pid);

    FILE *file = fopen(map_path, "r");

    if (!file) {
        printf("Cannot open file");
        return;
    }

    int mem_fd = open(mem_path, O_RDONLY);

    if (mem_fd < 0) {
        fclose(file);
        return;
    }

    printf("Map of process: %d: \n\n", pid);
    char line[LINE_LEN];
    while (fgets(line, LINE_LEN, file)) {
        unsigned long start, end;
        char perms[5];

        if (sscanf(line, "%lx-%lx %4s", &start, &end, perms) != 3)
            continue;

        if (perms[0] != 'r')
            continue;

        unsigned long size = end - start;
        size_t to_read = size > MAX_READ_SIZE ? MAX_READ_SIZE : size;

        unsigned char *buffer = malloc(to_read);

        if (!buffer)
            continue;

        if (lseek(mem_fd, start, SEEK_SET) == -1) {
            free(buffer);
            continue;
        }

        ssize_t bytes_read = read(mem_fd, buffer, to_read);

        if (bytes_read <= 0) {
            free(buffer);
            continue;
        }

        printf("Region: 0x%lx - 0x%lx (%s), read %zd bytes\n", start, end, perms, bytes_read);

        for (int i = 0; i < bytes_read; i += sizeof(uint64_t)) {
            if (i + sizeof(uint64_t) > bytes_read)
                break;

            uint64_t ptr;
            memcpy(&ptr, buffer + i, sizeof(uint64_t));
            printf("  [%2d] possible pointer: 0x%016lx\n", i / 8, ptr);
        }

        printf("\n");

        free(buffer);
    }

    fclose(file);
    close(mem_fd);
}

//size_t memo_lenght() {
   // struct sysinfo info;

    //if (sysinfo(&info) == 0) {
      //  size_t total = (size_t)info.totalram * info.mem_unit / (1024 * 1024);
       // return total;
    //}
//}

int main() {
    //size_t lenght = memo_lenght();
    pid_t pid;

    printf("-----------------------------------------------------------------------------------------\n");
    printf("/                                   CHEAT MEMORY                                        /\n");
    printf("-----------------------------------------------------------------------------------------\n");

    printf("Type process PID: \n");
    scanf("%d", &pid);

    map_memo(pid);

    return 0;
}