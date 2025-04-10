#include <iostream>
#include <dirent.h>
#include <cstring>
#include <fstream>
#include <sstream>
#include <algorithm> 

bool is_number(const std::string& s) {
    return !s.empty() && std::all_of(s.begin(), s.end(), ::isdigit);
}

std::string get_process_name(const std::string& pid) {
    std::ifstream cmdline("/proc/" + pid + "/cmdline");
    std::string name;
    if (cmdline.is_open()) {
        std::getline(cmdline, name, '\0');
    }
    return name.empty() ? "[unknowned]" : name;
}

int main() {
    DIR* dir = opendir("/proc");
    if (dir == nullptr) {
        std::cerr << "Erro at /proc\n";
        return 1;
    }

    struct dirent* entry;
    while ((entry = readdir(dir)) != nullptr) {
        if (entry->d_type == DT_DIR && is_number(entry->d_name)) {
            std::string pid = entry->d_name;
            std::string pname = get_process_name(pid);
            std::cout << "PID: " << pid << " | Name: " << pname << "\n";
        }
    }

    closedir(dir);
    return 0;
}
