/*
Copyright 2022

This file is part of QUANTAS.
QUANTAS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
QUANTAS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with QUANTAS. If not, see <https://www.gnu.org/licenses/>.
*/

#ifndef BRBPeer_hpp
#define BRBPeer_hpp

#include <iostream>
#include <sstream>
#include "../Common/Peer.hpp"
#include "../Common/Simulation.hpp"
using namespace std;

namespace quantas{

    using std::string; 
    using std::ostream;

    //
    // Example of a message body type
    //
    struct ExampleMessage{

        string id;
        interfaceId source = -1;
        interfaceId destination = -1;
        string type;

        //bracha
        string value;
        
        //opodis
        string C = "";
        string frag_a = "_";
        string frag_b = "_";
        vector<interfaceId> signs = {};

    };

    inline string br_str(const ExampleMessage& msg){
        stringstream ss;
        ss << "( id:" << msg.id << ",  source:" << msg.source << ",  type:" << msg.type << ",  value:" << msg.value << ")";
        return ss.str();
    }

    inline string op_str(const ExampleMessage& msg){
        stringstream ss;
        string s;
        string f;
        if (msg.signs.size() == 1) s = "[" + to_string(msg.signs[0]) + "]";
        if (msg.signs.size() == 2) s = "[" + to_string(msg.signs[0]) + "," + to_string(msg.signs[1]) + "]";
        if (msg.frag_a != "_" && msg.frag_b == "_") f = "[" + msg.frag_a + "]";
        if (msg.frag_a != "_" && msg.frag_b != "_") f = "[" + msg.frag_a + "," + msg.frag_b + "]";
        ss <<   "(source: " <<  msg.source << 
                ",  id: " <<    msg.id << 
                ",  C: " <<     msg.C << 
                ",  frag:" <<  f << 
                ", signs:" << s << ")";
        return ss.str();
    };

    //
    // Example Peer used for network testing
    //
    class BRBPeer : public Peer<ExampleMessage>{
    public:

        bool print = false;
        long senderId;
        int msgToSend = 0;
        int msgs_sent = 0;
        int msgs_sent_prev = 0;
        int n = 0;
        
        bool im_byzantine = false;
        string algorithm = "bracha";
        map<string,vector<int>>* termination_time;

        //common
        bool delivered = false;
        vector<string> received_msgs = {};

        //bracha
        int echo_threshold = 0;
        int ready_threshold = 0;
        int deliver_threshold = 0;

        vector<string> send_list = {};
        vector<string> echo_list = {};
        vector<string> ready_list = {};
        bool sent_echo = false;
        bool sent_ready = false;

        //opodis 
        string commit = "";
        int signature_threshold = 0;
        int fragments_threshold = 0;
        vector<string> signatures;
        vector<string> fragments;
        bool enough_signature = false;
        bool sent_forward_ps = false;
        bool sent_forward = false;
        bool sent_boundle = false;

        // methods that must be defined when deriving from Peer
        BRBPeer                             (long);
        BRBPeer                             (const BRBPeer &rhs);
        ~BRBPeer                            ();

        // initialize the configuration of the system
        void                    initParameters(const vector<Peer<ExampleMessage>*>& _peers, json parameters, map<string,vector<int>>& term_time);
        // perform one step of the Algorithm with the messages in inStream
        void                    performComputation ();
        void                    byzantineBehavior();
        void                    rc_broadcast(ExampleMessage msg);

        //bracha
        void                    bracha();
        void                    bracha_propagate(ExampleMessage msg);
        void                    bracha_rc_deliver(ExampleMessage msg);
        void                    bracha_broadcast(string val);
        void                    bracha_deliver(string val);

        void                    echo_check();
        void                    ready_check();
        void                    deliver_check();

        //opodis
        void                    opodis();
        void                    opodis_propagate(ExampleMessage msg);
        void                    opodis_rc_deliver(ExampleMessage msg);
        void                    opodis_broadcast(string val);
        void                    opodis_deliver(string val);

        void                    signature_check();


        // perform any calculations needed at the end of a round such as determine throughput (only ran once, not for every peer)
        void                    endOfRound(const vector<Peer<ExampleMessage>*>& _peers);
    };

    Simulation<quantas::ExampleMessage, quantas::BRBPeer>* generateSim();
}
#endif /* BRBPeer_hpp */