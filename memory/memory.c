#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/sysinfo.h>
#include <sys/mman.h>
#include <unistd.h>


void* memo_map(size_t lenght) {
    void* ptr;
    // Linux/macOS/Unix: usage mmap
    ptr = mmap(NULL, lenght, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (ptr == MAP_FAILED) {
        perror("Erro to try map memory on Linux/macOS");
        return NULL;
    }

    return ptr;
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
    void* ptr = memo_map(lenght);

    printf("-----------------------------------------------------------------------------------------\n");
    printf("/                                   CHEAT MEMORY                                        /\n");
    printf("-----------------------------------------------------------------------------------------\n");

    memo_map(lenght);
    free_memo(ptr, lenght);
}