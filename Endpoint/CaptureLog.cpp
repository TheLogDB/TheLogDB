#include <iostream>
#include <string>

void captureLog() {
    std::string logInput;
    
    // 从标准输入读取日志
    while (std::getline(std::cin, logInput)) {
        std::cout << "Log from Stdin: " << logInput << std::endl;
    }
    
    // 捕获标准错误
    std::string errorInput;
    while (std::getline(std::cerr, errorInput)) {
        std::cerr << "Error from Stderr: " << errorInput << std::endl;
    }
}

int main() {
    captureLog();
    return 0;
}