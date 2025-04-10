#ifndef PROCESS_H
#define PROCESS_H

#include <iostream>
#include <dirent.h>
#include <cstring>
#include <fstream>
#include <sstream>
#include <algorithm> 


bool is_number(const std::string& s);

std::string get_process_name(const std::string& pid);

#endif
