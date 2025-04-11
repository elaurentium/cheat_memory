#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
#include <string.h>
#include <dirent.h>
#include <ctype.h>

#define MAX_PATH_LENGTH 256
#define MAX_NAME_LENGTH 1024
#define MAX_PROCESSES 1024

typedef struct {
    char pid[16];           
    char pname[MAX_NAME_LENGTH];
} ProcessInfo;

int is_number(const char *s) {
    if (s == NULL || *s == '\0') {
        return 0; 
    }
    
    while (*s) {
        if (!isdigit(*s)) {
            return 0; 
        }
        s++;
    }
    
    return 1; 
}

char* process_pid(const char *pid, char *buffer, size_t buffer_size) {
    if (buffer == NULL || buffer_size == 0) {
        return NULL;
    }
    
    // clean buffer
    memset(buffer, 0, buffer_size);

    char cmdline_path[MAX_PATH_LENGTH];
    snprintf(cmdline_path, sizeof(cmdline_path), "/proc/%s/cmdline", pid);
    
    FILE *cmdline_file = fopen(cmdline_path, "r");
    if (cmdline_file == NULL) {
        strcpy(buffer, "[unknown]");
        return buffer;
    }
    
    size_t bytes_read = fread(buffer, 1, buffer_size - 1, cmdline_file);
    fclose(cmdline_file);
    
    if (bytes_read == 0) {
        strcpy(buffer, "[unknown]");
    } else {
        buffer[bytes_read] = '\0'; 
    }
    
    return buffer;
}

int collect_processes(ProcessInfo *processes_array, int max_processes) {
    DIR *dir = opendir("/proc");
    if (dir == NULL) {
        fprintf(stderr, "Erro /proc\n");
        return 0;
    }
    
    int count = 0;
    struct dirent *entry;
    
    while ((entry = readdir(dir)) != NULL && count < max_processes) {
        if (entry->d_type && is_number(entry->d_name)) {
            strncpy(processes_array[count].pid, entry->d_name, sizeof(processes_array[count].pid) - 1);
            processes_array[count].pid[sizeof(processes_array[count].pid) - 1] = '\0';
            
            process_pid(entry->d_name, processes_array[count].pname, sizeof(processes_array[count].pname));
            
            count++;
        }
    }
    
    closedir(dir);
    return count;
}

int search_processes_by_name(ProcessInfo *processes_array, int num_processes, 
                             const char *search_term, ProcessInfo *results, int max_results) {
    int count = 0;
    
    char search_lower[MAX_NAME_LENGTH];
    strncpy(search_lower, search_term, sizeof(search_lower) - 1);
    search_lower[sizeof(search_lower) - 1] = '\0';
    
    for (int i = 0; i < strlen(search_lower); i++) {
        search_lower[i] = tolower(search_lower[i]);
    }
    
    for (int i = 0; i < num_processes && count < max_results; i++) {
        char name_lower[MAX_NAME_LENGTH];
        strncpy(name_lower, processes_array[i].pname, sizeof(name_lower) - 1);
        name_lower[sizeof(name_lower) - 1] = '\0';
        
        for (int j = 0; j < strlen(name_lower); j++) {
            name_lower[j] = tolower(name_lower[j]);
        }

        if (strstr(name_lower, search_lower) != NULL) {
            memcpy(&results[count], &processes_array[i], sizeof(ProcessInfo));
            count++;
        }
    }
    
    return count;
}

int search_process_by_pid(ProcessInfo *processes_array, int num_processes, 
                          const char *pid, ProcessInfo *result) {
    for (int i = 0; i < num_processes; i++) {
        if (strcmp(processes_array[i].pid, pid) == 0) {
            memcpy(result, &processes_array[i], sizeof(ProcessInfo));
            return 1;
        }
    }
    
    return 0;
}

void print_processes(ProcessInfo *processes_array, int num_processes) {
    if (num_processes == 0) {
        printf("No one find.\n");
        return;
    }
    
    for (int i = 0; i < num_processes; i++) {
        printf("PID: %s | Name: %s\n", 
               processes_array[i].pid, 
               processes_array[i].pname);
    }
    
    printf("Total : %d\n", num_processes);
}

int main() {
    ProcessInfo processes[MAX_PROCESSES];
    ProcessInfo search_results[MAX_PROCESSES];
    ProcessInfo single_result;
    
    int num_processes = collect_processes(processes, MAX_PROCESSES);

    char search_term[MAX_NAME_LENGTH];
    char pid[16];

    printf(" _____________________________________________________________________________________ \n");
    printf("|                                                                                       |\n");
    printf("|   ██████╗██╗  ██╗███████╗ █████╗ ████████╗    ███╗   ███╗███████╗███╗   ███╗ ██████╗  |\n");
    printf("|  ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝    ████╗ ████║██╔════╝████╗ ████║██╔═══██╗ |\n");
    printf("|  ██║     ███████║█████╗  ███████║   ██║       ██╔████╔██║█████╗  ██╔████╔██║██║   ██║ |\n");
    printf("|  ██║     ██╔══██║██╔══╝  ██╔══██║   ██║       ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║ |\n");
    printf("|  ╚██████╗██║  ██║███████╗██║  ██║   ██║       ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝ |\n");
    printf("|   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝  |\n");
    printf("|_______________________________________________________________________________________| \n\n");

    

    printf("Type process name: ");
    fgets(search_term, sizeof(search_term), stdin);
    search_term[strcspn(search_term, "\n")] = 0;

    if (is_number(search_term)) {
        int result = search_process_by_pid(processes, num_processes, search_term, &single_result);
        print_processes(&single_result, result);
    } else {
        int results_count = search_processes_by_name(processes, num_processes, 
                                                    search_term, search_results, MAX_PROCESSES);
        print_processes(search_results, results_count);
    }
    
         
    return 0;
}