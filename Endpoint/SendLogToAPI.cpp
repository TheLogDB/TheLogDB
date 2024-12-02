#include <iostream>
#include <string>
#include <curl/curl.h>

size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

void sendLogToAPI(const std::string &serverAddress, const std::string &projectId, const std::string &logData) {
    CURL *curl;
    CURLcode res;
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (curl) {
        std::string url = serverAddress + "/api/logs";  // 假设 API 路径是这个
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        
        // 设置 POST 数据
        std::string data = "project_id=" + projectId + "&log=" + logData;
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());

        // 捕获响应
        std::string response;
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << "\n";
        } else {
            std::cout << "Response: " << response << "\n";
        }

        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();
}

int main() {
    std::string serverAddress = "http://localhost:8080";
    std::string projectId = "12345";
    std::string logData = "This is a test log";

    sendLogToAPI(serverAddress, projectId, logData);

    return 0;
}