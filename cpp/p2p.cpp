#include "p2p.hpp"



using namespace p2p;
using namespace socket_tool;

void P2P_connection::punch_hole(){
    m_sock->set_timeout(1);
    
    while(true){
        try{
            char buffer[1200];
            size_t len = 1200;
            Address client_addr = m_sock->recv_from(buffer, &len);

            if( client_addr == m_target_addr ) break;

        }catch(Timeout_excpetion _){

            const char* msg = "\0";
            m_sock->send_to( msg, 1, m_target_addr );

        }
    }

}
void P2P_connection::send( const char* buff, size_t buff_size ){
    m_sock->send_to( buff, buff_size, m_target_addr );
}
void P2P_connection::recv( char* buff, size_t* len_io, float timeout ){
    m_sock->set_timeout(timeout);
    while(true){
        Address client_addr = m_sock->recv_from(buff, len_io);
        if( client_addr == m_target_addr ){
            break;
        }else{
            std::cout << "wtf\n";
        }
    }
}


