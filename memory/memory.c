#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
    #include <windows.h>
#else
    #include <sys/mman.h>
    #include <unistd.h>
#endif

void* memo_map(size_t tamanho) {
    void* ptr;
    
#ifdef _WIN32
    // Windows: VirtualAlloc
    ptr = VirtualAlloc(NULL, tamanho, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (ptr == NULL) {
        printf("Erro ao alocar memória no Windows: %d\n", GetLastError());
        return NULL;
    }
#else
    // Linux/macOS/Unix: usage mmap
    ptr = mmap(NULL, tamanho, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (ptr == MAP_FAILED) {
        perror("Erro ao mapear memória no Linux/macOS");
        return NULL;
    }
#endif
    
    return ptr;
}

void free_memo(void* ptr, size_t tamanho) {
#ifdef _WIN32
    VirtualFree(ptr, 0, MEM_RELEASE);
#else
    munmap(ptr, tamanho);
#endif
}

int main() {
    size_t tamanho_memoria = 4096;
    char* memoria_mapeada;
    char* ponteiro;
    
    memoria_mapeada = (char*)memo_map(tamanho_memoria);
    if (memoria_mapeada == NULL) {
        return 1;
    }
    
    printf("Memória mapeada em: %p\n", (void*)memoria_mapeada);
    
    ponteiro = memoria_mapeada;
    const char* mensagem = "Teste de escrita na memória mapeada!";
    strcpy(ponteiro, mensagem);
    
    printf("Conteúdo escrito: %s\n", ponteiro);
    
    ponteiro += 6;
    printf("Conteúdo a partir do offset 6: %s\n", ponteiro);
    
    free_memo(memoria_mapeada, tamanho_memoria);
    
    return 0;
}