#include "socket.hpp"
#include "p2p.hpp"
#include <iostream>
#include <cerrno>


int main(int argc, char** argv){

    using namespace socket_tool;
    using namespace p2p;

    Address server_addr;

    if( argc >= 3 ){
        char* ip = argv[0];
        int port = std::atoi(argv[1]);
        std::cout << "connecting to " << ip << ":" << port << "\n";
        server_addr = Address{ ip, port };
    }else{
        std::cout << "connecting to default 127.0.0.1:50020 \n";
        server_addr = Address{ "127.0.0.1", 50020 };
    }

    
    UDP_socket sock{ Address{ "0.0.0.0", 0 } };
    Address target_addr;
    while( 1 ){
        sleep(1);
        try{
            constexpr size_t buff_size = 1200;
            char buffer[buff_size] = {0};
            size_t len = buff_size;

            sock.send_to(buffer, 1, server_addr);
            auto recv_from_addr = sock.recv_from(buffer, &len);

            std::cout << "recv from server: " << buffer << '\n';

            if( buffer[0] == 'O' && buffer[1] == 'K' )
                continue;
            break;            

        }catch(Exception e){
            std::cerr << "[EXCEPTION] " << e.message << " code: " << e.code << " cerrno: " << strerror(errno) << "\n";
        }
    }

    



}