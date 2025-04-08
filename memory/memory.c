#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/sysinfo.h>
#include <sys/mman.h>
#include <unistd.h>


void map_memo(pid_t pid) {
    char path[256];

    snprintf(path, sizeof(path), "/proc/%d/maps", pid);

    FILE* file = fopen(path, 'r');

    if (!file) {
        printf("Cannot open file");
        return;
    }

    printf("Map of process: %d: \n\n", pid);
    char line[1024];
    while (fgets(line, sizeof(line), file)) {
        printf("%s", line);
    }

    fclose(file);
}

void free_memo(int* ptr, size_t lenght) {
    munmap(ptr, lenght);
}

size_t memo_lenght() {
    struct sysinfo info;

    if (sysinfo(&info) == 0) {
        size_t total = (size_t)info.totalram * info.mem_unit / (1024 * 1024);
        return total;
    }
}

int main() {
    size_t lenght = memo_lenght();
    pid_t pid;

    printf("-----------------------------------------------------------------------------------------\n");
    printf("/                                   CHEAT MEMORY                                        /\n");
    printf("-----------------------------------------------------------------------------------------\n");

    printf("Type process PID: \n");
    scanf("%d", &pid);

    void map = map_memo(pid);

    if (map) {
        free_memo((int)pid, lenght)
    }
}