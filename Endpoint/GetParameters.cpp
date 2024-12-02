#include <iostream>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int opt;
    std::string serverAddress;
    std::string projectId;
    
    while ((opt = getopt(argc, argv, "s:p:")) != -1) {
        switch (opt) {
            case 's':
                serverAddress = optarg;  // 获取服务器地址
                break;
            case 'p':
                projectId = optarg;      // 获取项目ID
                break;
            default:
                std::cerr << "Usage: " << argv[0] << " -s server_address -p project_id\n";
                return 1;
        }
    }

    std::cout << "Server: " << serverAddress << "\n";
    std::cout << "Project ID: " << projectId << "\n";

    return 0;
}