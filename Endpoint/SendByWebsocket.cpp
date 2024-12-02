#include <iostream>
#include <string>
#include <websocketpp/client.hpp>
#include <websocketpp/config/asio_no_tls_client.hpp>
#include <websocketpp/lib/json.hpp>

typedef websocketpp::client<websocketpp::config::asio_client> client;
typedef websocketpp::lib::shared_ptr<websocketpp::lib::asio::io_service> io_service_ptr;

client c;

void on_open(websocketpp::connection_hdl hdl) {
    std::cout << "Connection Opened!" << std::endl;
}

void on_message(websocketpp::connection_hdl hdl, client::message_ptr msg) {
    std::cout << "Received message: " << msg->get_payload() << std::endl;
}

void send_log(const std::string& log, const std::string& server_url) {
    websocketpp::lib::error_code ec;
    websocketpp::client<websocketpp::config::asio_client>::connection_ptr con = c.get_connection(server_url, ec);

    if (ec) {
        std::cerr << "Could not create connection: " << ec.message() << std::endl;
        return;
    }

    // 设置事件处理
    con->set_open_handler(&on_open);
    con->set_message_handler(&on_message);

    // 发起连接
    c.connect(con);

    // 运行客户端事件循环
    c.run();
}

int main() {
    try {
        // 初始化客户端
        c.init_asio();

        // 设置 WebSocket 服务器 URL
        std::string server_url = "ws://localhost:8080";

        // 日志内容
        std::string log = "This is a test log";

        // 发送日志
        send_log(log, server_url);

    } catch (websocketpp::exception const & e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }

    return 0;
}