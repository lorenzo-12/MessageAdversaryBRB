/*
Copyright 2022

This file is part of QUANTAS.
QUANTAS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
QUANTAS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with QUANTAS. If not, see <https://www.gnu.org/licenses/>.
*/

#include "ExamplePeer.hpp"
#include <algorithm>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

using namespace std;


namespace quantas {

	//
	// Example Channel definitions
	//
	ExamplePeer::~ExamplePeer() {

	}

	ExamplePeer::ExamplePeer(const ExamplePeer& rhs) : Peer<ExampleMessage>(rhs) {
		
	}

	ExamplePeer::ExamplePeer(long id) : Peer(id) {
	}

	ExamplePeer::ExamplePeer(long id, map<string,vector<int>>& term_time, long send_id, int msg_to_send, bool byz, int ma_power):
		Peer(id),
		byzantine(byz),
		termination_time(&term_time),
		maPower(ma_power),
		senderId(send_id),
		msgToSend(msg_to_send){
	}

	ExamplePeer::ExamplePeer(long id, map<string,vector<int>>& term_time, long send_id, int msg_to_send, bool byz, int ma_power, string corr_behavior):
		Peer(id),
		byzantine(byz),
		termination_time(&term_time),
		maPower(ma_power),
		senderId(send_id),
		msgToSend(msg_to_send),
		corr_behavior_type(corr_behavior){
	}

	// correct behavior can be defined here
	void ExamplePeer::correctBehavior() {
		/* std::ofstream outFile("output.txt", std::ios::app);
        std::streambuf* originalCoutBuffer = std::cout.rdbuf();
        std::cout.rdbuf(outFile.rdbuf()); */

		// each nodes print if they are correct 
		if (getRound() == 0) {
			//cout << "[node_" << std::to_string(id()) << "] is Correct " << endl;
		}

		// for the sender only
		if (id() == senderId && getRound() == 0){
			//cout << "[node_" << id() << "] starting broadcast as sender" << endl;
			for (int i=0; i<msgToSend; i++){
				ExampleMessage msg;
				msg.id = i;
				msg.sender_id = id();
				Packet<ExampleMessage> newMsg(getRound(), id(), id());
				newMsg.setMessage(msg);

				// broadcast the message with the Message Adversary option
				// update the number of messages sent
				int ms = broadcast_MA(msg,maPower,{id()});
				msgSent += ms;

				// we are the sender so we can deliver immediately
				(*termination_time)[std::to_string(msg.id)][id()] = getRound();
				//term_time_vecter->at(id()) = getRound();
			}
			//cout << endl;
		}

		while (!inStreamEmpty()){
			// if we are the sender we don't do anything
			if (id() == senderId) return;

			Packet<ExampleMessage> MSG = popInStream();
			ExampleMessage msg = MSG.getMessage();

			// If not already delivered
			if (find(delivered.begin(),delivered.end(),msg.id) == delivered.end()){
				delivered.push_back(msg.id);
				//cout << "[node_" << id() << "][delivered] " << msg.id << " from: " << MSG.sourceId() << " " << vec_to_string(delivered) << endl;

				// update the value in your position in the termination vector with the current round
				// so if and when know when each node delivered the message
				(*termination_time)[std::to_string(msg.id)][id()] = getRound();
				//term_time_vec->at(id()) = getRound();
				Packet<ExampleMessage> newMsg(getRound());
				newMsg.setMessage(msg);

				// broadcast the message with the Message Adversary option
				// update the number of messages sent
				int ms = broadcast_MA(msg, maPower,{senderId,MSG.sourceId()});
				msgSent += ms;
				//cout << endl;
			}
		}

		/* std::cout.rdbuf(originalCoutBuffer);
        outFile.close(); */
	}

	// correct behavior can be defined here
	void ExamplePeer::correctBehavior_coin_flip() {
		/* std::ofstream outFile("output.txt", std::ios::app);
        std::streambuf* originalCoutBuffer = std::cout.rdbuf();
        std::cout.rdbuf(outFile.rdbuf()); */
		
		
		// each nodes print if they are correct 
		if (getRound() == 0) {

			// initialize coin flip count for each message
			for (int i=0; i<msgToSend; i++){
				resend_coin_flip[i] = 0;
			}
			//cout << "[node_" << std::to_string(id()) << "] is Correct " << endl;
		}

		// for the sender only
		if (id() == senderId && getRound() == 0){
			//cout << "[node_" << id() << "] starting broadcast as sender" << endl;
			for (int i=0; i<msgToSend; i++){
				ExampleMessage msg;
				msg.id = i;
				msg.sender_id = id();
				Packet<ExampleMessage> newMsg(getRound(), id(), id());
				newMsg.setMessage(msg);

				// broadcast the message with the Message Adversary option
				// update the number of messages sent
				int ms = broadcast_MA(msg,maPower,{id()});
				msgSent += ms;

				// we are the sender so we can deliver immediately
				(*termination_time)[std::to_string(msg.id)][id()] = getRound();
				//term_time_vecter->at(id()) = getRound();
			}
			//cout << endl;
		}

		while (!inStreamEmpty()){
			// if we are the sender we don't do anything
			if (id() == senderId) return;

			Packet<ExampleMessage> MSG = popInStream();
			ExampleMessage msg = MSG.getMessage();

			if (resend_coin_flip[msg.id] == 0){
				delivered.push_back(msg.id);
				//cout << "[node_" << id() << "][delivered] " << msg.id << " from: " << MSG.sourceId() << " " << vec_to_string(delivered) << endl;

				resend_coin_flip[msg.id] += 1;
				// update the value in your position in the termination vector with the current round
				// so if and when know when each node delivered the message
				(*termination_time)[std::to_string(msg.id)][id()] = getRound();
				//term_time_vec->at(id()) = getRound();
				Packet<ExampleMessage> newMsg(getRound());
				newMsg.setMessage(msg);

				// broadcast the message with the Message Adversary option
				// update the number of messages sent
				int ms = broadcast_MA(msg, maPower,{senderId,MSG.sourceId()});
				msgSent += ms;
				//cout << endl;
			}
			else {
			    // Flip x coins
			    int x = resend_coin_flip[msg.id];
			    bool resend = true;
				//cout << "[node_" << id() << "] starting " << x << " coin flips: ";
			    for (int i = 0; i < x; ++i) {
			        if (rand() % 2 == 0) { // 0 = tails, 1 = heads
			            resend = false;
						//cout << " tail ";
			            break;
			        }
					//cout << " head" ;
			    }
				//cout << endl;

			    if (resend) {
					//cout << "[node_" << id() << "][resend] " << msg.id << "\n" << endl;
			        Packet<ExampleMessage> newMsg(getRound());
			        newMsg.setMessage(msg);
			        int ms = broadcast_MA(msg, maPower, {senderId, MSG.sourceId()});
			        msgSent += ms;
			    }

				resend_coin_flip[msg.id] += 1;
			}
			
		}
		/* std::cout.rdbuf(originalCoutBuffer);
        outFile.close(); */
		//cout << "[node_" << id() << "] msgSent: " << msgSent << endl;

	}

	// correct behavior can be defined here
	void ExamplePeer::correctBehavior_repeater() {
		/* std::ofstream outFile("output.txt", std::ios::app);
        std::streambuf* originalCoutBuffer = std::cout.rdbuf();
        std::cout.rdbuf(outFile.rdbuf()); */

		// each nodes print if they are correct 
		if (getRound() == 0) {
			//cout << "[node_" << std::to_string(id()) << "] is Correct " << endl;
		}

		// for the sender only
		if (id() == senderId && getRound() == 0){
			//cout << "[node_" << id() << "] starting broadcast as sender" << endl;
			for (int i=0; i<msgToSend; i++){
				ExampleMessage msg;
				msg.id = i;
				msg.sender_id = id();
				Packet<ExampleMessage> newMsg(getRound(), id(), id());
				newMsg.setMessage(msg);

				// broadcast the message with the Message Adversary option
				// update the number of messages sent
				int ms = broadcast_MA(msg,maPower,{id()});
				msgSent += ms;

				// we are the sender so we can deliver immediately
				(*termination_time)[std::to_string(msg.id)][id()] = getRound();
				//term_time_vecter->at(id()) = getRound();
			}
			//cout << endl;
		}

		vector<int> round_msgs;
		for (int i=0; i<msgToSend; i++){
			round_msgs.push_back(0);
		}
		while (!inStreamEmpty()){
			// if we are the sender we don't do anything
			if (id() == senderId) return;

			Packet<ExampleMessage> MSG = popInStream();
			ExampleMessage msg = MSG.getMessage();

			// If not already delivered
			if (find(delivered.begin(),delivered.end(),msg.id) == delivered.end()){
				delivered.push_back(msg.id);
				//cout << "[node_" << id() << "][delivered] " << msg.id << " from: " << MSG.sourceId() << " " << vec_to_string(delivered) << endl;

				// update the value in your position in the termination vector with the current round
				// so if and when know when each node delivered the message
				(*termination_time)[std::to_string(msg.id)][id()] = getRound();
			}

			// resend the message at most once (otherwise infinite messages)
			if (round_msgs[msg.id] == 0){
				round_msgs[msg.id] = 1;
				Packet<ExampleMessage> newMsg(getRound());
				newMsg.setMessage(msg);

				// broadcast the message with the Message Adversary option
				// update the number of messages sent
				int ms = broadcast_MA(msg, maPower,{senderId,MSG.sourceId()});
				msgSent += ms;
				//cout << endl;
			}
		}

		/* std::cout.rdbuf(originalCoutBuffer);
        outFile.close(); */
	}

	// Byzantine behavior can be defined here
	void ExamplePeer::byzantineBehavior() {
		// stay silent
		//cout << "[node_" << id() << "] ..." << endl;
	}

	void ExamplePeer::performComputation() {

		if (byzantine == true){
			byzantineBehavior();
		}
		else{
			if (corr_behavior_type == "normal"){
				correctBehavior();
			}
			else if (corr_behavior_type == "coin_flip"){
				correctBehavior_coin_flip();
			}
			else if (corr_behavior_type == "repeater"){
				correctBehavior_repeater();
			}
			else{
				cout << "Error: correct behavior not defined" << endl;
			}
			
		}
		
	}

	void ExamplePeer::endOfRound(const vector<Peer<ExampleMessage>*>& _peers) {
		//cout << "End of round " << getRound() << endl;
		/* std::ofstream outFile("output.txt", std::ios::app);
        std::streambuf* originalCoutBuffer = std::cout.rdbuf();
        std::cout.rdbuf(outFile.rdbuf());
		cout << "End of round " << getRound() << endl;
		std::cout.rdbuf(originalCoutBuffer);
        outFile.close(); */
	}

	ostream& ExamplePeer::printTo(ostream& out)const {
		Peer<ExampleMessage>::printTo(out);

		/* out << id() << endl;
		out << "counter:" << getRound() << endl;

		out << "delivered: [";
		for (auto val : delivered){
			out << val << ", ";
		}
		out << "]" << endl; */

		return out;
	}

	ostream& operator<< (ostream& out, const ExamplePeer& peer) {
		peer.printTo(out);
		return out;
	}

	Simulation<quantas::ExampleMessage, quantas::ExamplePeer>* generateSim() {
        
        Simulation<quantas::ExampleMessage, quantas::ExamplePeer>* sim = new Simulation<quantas::ExampleMessage, quantas::ExamplePeer>;
        return sim;
    }
}