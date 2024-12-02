#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>

void readConfigFile(const std::string &filename, std::unordered_map<std::string, std::string> &config) {
    std::ifstream configFile(filename);
    std::string line;
    
    while (std::getline(configFile, line)) {
        std::istringstream ss(line);
        std::string key, value;
        if (std::getline(ss, key, '=') && std::getline(ss, value)) {
            config[key] = value;
        }
    }
}

int main() {
    std::unordered_map<std::string, std::string> config;
    readConfigFile("config.ini", config);

    std::cout << "Server Address: " << config["server_address"] << "\n";
    std::cout << "Project ID: " << config["project_id"] << "\n";

    return 0;
}