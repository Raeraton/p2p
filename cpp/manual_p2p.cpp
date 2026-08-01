#include "p2p.hpp"
#include <iostream>
#include <string>
#include <time.h>
#include <chrono>
#include <map>

using namespace std;
using namespace p2p;
using namespace socket_tool;

inline chrono::system_clock::time_point time_now(){
    return chrono::system_clock::now();
}

inline int duration_ms( chrono::system_clock::time_point t1, chrono::system_clock::time_point t2 ){
    return ( chrono::duration<double>(t2 - t1).count() * 1000 );
}

int main(){

    srand(time(NULL));
    int my_port = 50000 + (rand()%1000);
    cout << "listening on 0.0.0.0:" << my_port << "\n";

    string target_ip;
    int target_port;

    cout << "enter ip:  ";
    cin >> target_ip;
    cout << "enter port:";
    cin >> target_port;

    try{

        P2P_connection connection{my_port, Address{target_ip, target_port}};

        connection.punch_hole();

        chrono::system_clock::time_point time_point_table[100] = {};
        int echo_num;

        char buff[1201]={0};

        size_t idx = 0;

        while (1){ try{

            int random_num = rand() % 100;
            time_point_table[random_num] = time_now();
            size_t n = snprintf( buff, 1200, "%d %d", random_num, echo_num);
            

            connection.send( buff, n );

            n=1200;
            connection.recv( buff, &n );
            buff[n] = '\0';
            sscanf( buff, "%d %d", &echo_num, &random_num);

            cout << ++idx << ".: key num: " << random_num << "\t echo num: " << echo_num << " \t\t round tripp time: " << duration_ms( time_now(), time_point_table[random_num%100] ) << "\tus\n";

        }catch(Timeout_excpetion _){
            connection.punch_hole();
        }catch(Exception e){
            cerr << "cauth exception " << e.message << "\n";
        }
        }


    }catch( Exception e ){
        cerr << "uncouth exception " << e.message << "\n";
    }catch( Error e ){
        cerr << "error " << e.message << "\n";
    }catch(...){
        cerr << "unknown \n";
    }


}