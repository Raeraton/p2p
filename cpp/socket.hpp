#ifndef SOCKET_HPP
#define SOCKET_HPP

#include <string>
#include <cerrno>

#include <bits/stdc++.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 



namespace socket_tool{


inline in_port_t port_from_int( int port ){
    return htons(port);
}
inline in_addr_t ip_from_str( const std::string& ip ){
    return inet_addr(ip.c_str());
}


struct Error{
    std::string message;
    int code = 0;
    Error( const std::string& _message="unknown error", int _code=0 ) : message{_message}, code{_code} {}
};

struct Exception{
    std::string message;
    int code = 0;
    Exception( const std::string& _message="unknown exception", int _code=0 ) : message{_message}, code{_code} {}
};

struct Timeout_excpetion: public Exception{
    Timeout_excpetion() : Exception("Timeout") {}
};





struct Address{
    in_addr_t ip=0;
    in_port_t port=0;
    Address() = default;
    Address( in_addr_t _ip, in_port_t _port ) : ip{_ip}, port{_port} {}
    Address( const std::string& _ip, int _port ) : ip{ip_from_str(_ip)}, port{port_from_int(_port)} {}
    sockaddr_in to_sockaddr_in() const {
        sockaddr_in out;
        out.sin_family = AF_INET;
        out.sin_addr.s_addr = ip;
        out.sin_port = port;
        return out;
    }
    inline bool operator==( const Address& oth ){
        return ip==oth.ip && port==oth.port;
    }
};


class UDP_socket{
    int socket_fd=-1; // socket descriptor
    sockaddr_in addr={0};

public:

    UDP_socket( const Address& _addr ){

        // creating socket
        socket_fd = socket( AF_INET, SOCK_DGRAM, 0 );
        if( socket_fd < 0 )
            throw Error{ "creating socket", socket_fd };
        
        addr.sin_family    = AF_INET; // IPv4 
        addr.sin_addr.s_addr = _addr.ip; 
        addr.sin_port = _addr.port;

        // binding
        int res = bind(socket_fd, (const sockaddr*)&addr, sizeof(addr));
        if( res < 0 )
            throw Error{ "binding socket", res };

    }

    UDP_socket( const UDP_socket& ) = default;

    Address recv_from( char* buffer, size_t* size_io ){
        sockaddr_in target_addr = {0};
        socklen_t target_len = sizeof(target_addr);
        
        *size_io = recvfrom(   socket_fd,
                                        buffer, *size_io,
                                        MSG_WAITALL, ( struct sockaddr *) &target_addr,
                                        &target_len );
        
        if( *size_io == -1 ){
            if( errno == EAGAIN || errno == EWOULDBLOCK ){
                throw Timeout_excpetion{};
            }else{
                throw Exception{"recving"};
            }
        }
        
        return Address{ target_addr.sin_addr.s_addr, target_addr.sin_port };

    }

    void send_to( const char* buffer, size_t send_amount, const Address& _target_addr ){
        sockaddr_in target_addr = {0};
        target_addr.sin_family = AF_INET;
        target_addr.sin_addr.s_addr = _target_addr.ip;
        target_addr.sin_port = _target_addr.port;

        ssize_t res = sendto(socket_fd, buffer, send_amount, MSG_CONFIRM, (const struct sockaddr *) &target_addr, sizeof(target_addr));
        if( res == (ssize_t)-1 ){
            throw Exception{"some error in sending"};
        }

    }


    void set_timeout( double secs ){
        timeval tv={0};
        tv.tv_sec = (int)secs;
        secs -= (double)tv.tv_sec;
        tv.tv_usec = (int)(secs * 1000000);

        int ret = setsockopt( socket_fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv) );
        if( ret < 0 )
            throw Error{"timeout set error"};
    }


    // carefuly, because its fuck up every copy
    void close(){
        if( socket_fd >= 0 ){
            ::close(socket_fd);
            socket_fd = -1;
        }
    }




};




}



#endif