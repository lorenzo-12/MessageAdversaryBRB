/*
Copyright 2022

This file is part of QUANTAS.
QUANTAS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
QUANTAS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with QUANTAS. If not, see <https://www.gnu.org/licenses/>.
*/

#ifndef ExamplePeer_hpp
#define ExamplePeer_hpp

#include <iostream>
#include <vector>
#include "../Common/Peer.hpp"
#include "../Common/Simulation.hpp"

namespace quantas{

    using std::string; 
    using std::ostream;
    using std::vector;

    //
    // Example of a message body type
    //
    struct ExampleMessage{
        
        int id;
        long sender_id;
        
    };

    //
    // Example Peer used for network testing
    //
    class ExamplePeer : public Peer<ExampleMessage>{
    public:

        long senderId;
        int msgToSend = 0;
        bool byzantine = false;
        int maPower;
        int msgSent = 0;
        string corr_behavior_type = "normal";

        map<long,int> resend_coin_flip;
        vector<int> delivered;
        map<string,vector<int>>* termination_time;
        

        // methods that must be defined when deriving from Peer
        ExamplePeer                             (long);
        ExamplePeer                             (long, map<string,vector<int>>&, long, int, bool, int );
        ExamplePeer                             (long, map<string,vector<int>>&, long, int, bool, int, string );
        ExamplePeer                             (const ExamplePeer &rhs);
        ~ExamplePeer                            ();

        // perform one step of the Algorithm with the messages in inStream
        void                 performComputation ();
        void                 correctBehavior();
        void                 byzantineBehavior();
        void                 correctBehavior_coin_flip();
        void                 correctBehavior_repeater();
        // perform any calculations needed at the end of a round such as determine throughput (only ran once, not for every peer)
        void                 endOfRound         (const vector<Peer<ExampleMessage>*>& _peers);

        // addintal method that have defulte implementation from Peer but can be overwritten
        void                 log()const { printTo(*_log); };
        ostream&             printTo(ostream&)const;
        friend ostream& operator<<         (ostream&, const ExamplePeer&);
    };

    Simulation<quantas::ExampleMessage, quantas::ExamplePeer>* generateSim();
}
#endif /* ExamplePeer_hpp */
