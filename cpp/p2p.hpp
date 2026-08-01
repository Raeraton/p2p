#ifndef P2P_HPP
#define P2P_HPP

#include "socket.hpp"

namespace p2p{

    

    class P2P_connection{

        socket_tool::Address m_target_addr;
        socket_tool::UDP_socket* m_sock=nullptr;
        bool m_owned=false;

    public:

        P2P_connection( int _port, const socket_tool::Address& _target_addr )
                    : m_target_addr{ _target_addr },
                      m_sock{ new socket_tool::UDP_socket{
                        socket_tool::Address{ socket_tool::ip_from_str("0.0.0.0"), socket_tool::port_from_int(_port) }
                      }},
                      m_owned{true} {}
        
        P2P_connection( socket_tool::UDP_socket* _sock, const socket_tool::Address& _target_addr )
                    : m_target_addr{_target_addr},
                      m_sock{_sock},
                      m_owned{false} {}
                      
        ~P2P_connection(){
            m_sock->close();
            if( m_owned ) delete m_sock;
        }

        void punch_hole();
        void send( const char* buff, size_t buff_size );
        void recv( char* buff, size_t* len_io, float timeout=1 );

    };


}


#endif