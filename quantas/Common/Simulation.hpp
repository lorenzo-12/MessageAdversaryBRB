/*
Copyright 2022

This file is part of QUANTAS.
QUANTAS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
QUANTAS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with QUANTAS. If not, see <https://www.gnu.org/licenses/>.
*/
//
// This class handles reading in a configuration file, setting up log files for the simulation, 
// initializing the network class, and repeating a simulation according to the configuration file 
// (i.e., running multiple experiments with the same configuration).  It is templated with a user 
// defined message and peer class, used for the underlaying network instance. 

#ifndef Simulation_hpp
#define Simulation_hpp

#include <chrono>
#include <thread>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <map>
#include <string>
#include <iostream>
#include <typeinfo>
#include <numeric>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <cstdio>

using json = nlohmann::json;

#include "Network.hpp"
#include "LogWriter.hpp"
#include "BS_thread_pool.hpp"


using std::ofstream;
using std::thread;
using std::map;
using std::string;
using std::vector;
using namespace std;


template<class type_value>
inline string vec_to_string(std::vector<type_value> v){
	std::ostringstream oss;
	oss << "[";
	for (size_t i = 0; i < v.size(); ++i) {
		oss << v[i];
		if (i != v.size() - 1)
			oss << ",";  // or any separator
	}
	oss << "]";
	std::string str = oss.str();
	return str;
}

class TestInfo {
    public:
		long senderId;
		string maType;
		int maPower;
        double avgDeliveryTime;
        int maxDeliveryTime;
		double avgDeliveryNodes;
		int totalMsgsSent;
		vector<int> byzantineNodes;
		vector<int> disconnectedNodes;
		map<string,vector<string>>  peersDelivery;
		map<string,int> recapMsgDelivered;
		map<string,vector<int>> msgDelivered;
	
		void computeAvgDeliveryNode(map<string,vector<int>> d, vector<int> byzantineNodes){
			double sum = 0;
			vector<double> list_avg;
			for (auto [msgId, deliveryVector] : d){
				sum = 0;
				for (auto val : deliveryVector){
					if (val>=0) sum += 1;
				}
				int byz_numb = byzantineNodes.size();
				double avg = sum/ (deliveryVector.size()-byz_numb);
				if (maType == "ma2") avg = sum/ (deliveryVector.size()-byz_numb-maPower);
				list_avg.push_back(avg);
				//cout << "[stats] t:" << byz_numb << " d:" << maPower << " sum:" << sum << " avg:" << avg << endl;
			}

			sum = 0;
			for (auto avg : list_avg){
				sum += avg;
			}
			avgDeliveryNodes =  (sum/list_avg.size()) * 100;
		}
		
		void computeAvgDeliveryTime(map<string,vector<int>> d){
			double sum = 0;
			double counter = 0;
			double avg = 0;
			vector<double> list_avg;
			for (auto [msgId, deliveryVector] : d){
				sum = 0;
				counter = 0;
				for (auto val : deliveryVector){
					if (val>0) {
						sum += val;
						counter += 1;
					}
				}
				if (counter!=0){
					avg = (sum/counter);
					list_avg.push_back(avg);
				}
			}

			sum = 0;
			for (auto avg : list_avg){
				sum+= avg;
			}
			avgDeliveryTime = (sum/list_avg.size());
		}
		
		void computeMaxDeliveryTime(map<string,vector<int>> d){
			int globalMax = 0;
			for (auto [msgId, deliveryVector] : d){
				int localMax = *std::max_element(deliveryVector.begin(), deliveryVector.end());
				if (localMax > globalMax) globalMax = localMax;
			}
			maxDeliveryTime = globalMax;
		}
		
		void computeRecapMsgDelivered(map<string,vector<int>> d){
			map<string,int> m;
			for (auto [msgId, deliveryVector] : d){
				m[msgId] = 0;
				for (auto val : deliveryVector){
					if (val>0) m[msgId]++;
				}
			}
			recapMsgDelivered = m;
		}

		void computePeersDelivery(map<string,vector<int>> d){
			map<string,vector<string>> m;

			for (int i = 0; i < d["0"].size(); ++i) {
				m[std::to_string(i)] = {};  // ensure every node has a key
			}

			for (auto [msgId,deliveryVector] : d){
				for (int peerId=0; peerId<deliveryVector.size(); peerId++){
					if (deliveryVector[peerId]>=0){
						m[std::to_string(peerId)].push_back(msgId);
					}
				}
			}
			peersDelivery = m;
		}
		
		void computeDisconnectedNodes(json topology){
			vector<long> r;
			r.push_back(senderId);
			int i = 0;
			while (i<r.size()){
				for (auto node : topology[to_string(r[i])]){
					if (find(byzantineNodes.begin(),byzantineNodes.end(),node) == byzantineNodes.end()){
						if (find(r.begin(),r.end(),node) == r.end()){
							r.push_back(node);
						}
					}
				}
				i++;
			}
			for (int i=0; i<topology.size(); i++){
				if (find(r.begin(),r.end(),i) == r.end()){
					if (find(byzantineNodes.begin(),byzantineNodes.end(),i) == byzantineNodes.end()){
						disconnectedNodes.push_back(i);
					}
				}
			}			
		}
    
	TestInfo() = default;
    TestInfo(map<string,vector<int>> msg_delivered, vector<int> byz, int ma_p, string ma_t, long sender, int tms): 
			msgDelivered(msg_delivered), 
			byzantineNodes(byz), 
			maPower(ma_p), 
			maType(ma_t),
			senderId(sender),
			totalMsgsSent(tms) {
	};

	void computeInfo(){
		computeAvgDeliveryTime(msgDelivered);
		computeMaxDeliveryTime(msgDelivered);
		computeRecapMsgDelivered(msgDelivered);
		computeAvgDeliveryNode(msgDelivered, byzantineNodes);
		computePeersDelivery(msgDelivered);
	}
	
};

inline void to_json(json& j, const TestInfo& t) {
    j = json{
		{"senderId", t.senderId},
		{"totalMsgsSent", t.totalMsgsSent},
		{"disconnectedNodes", t.disconnectedNodes},
		{"byzantineNodes", t.byzantineNodes},
		{"MessageAdversaryPower", t.maPower},
        {"avgDeliveryTime", t.avgDeliveryTime},
        {"maxDeliveryTime", t.maxDeliveryTime},
		{"avgDeliveryNodes", t.avgDeliveryNodes},
		//{"recapMsgDelivered", t.recapMsgDelivered},
		//{"peersDeliveredMsg", t.peersDelivery},
        //{"msgDelivered", t.msgDelivered}
    };
}


namespace quantas {
	class SimWrapper {
	public:
    	virtual void run(json) = 0;
	};

	template<class type_msg, class peer_type>
    class Simulation : public SimWrapper{
    private:
        Network<type_msg, peer_type> 		system;
        ostream                             *_log;
    public:
        // Name of log file, will have Test number appended
        void 				run			(json);

        // logging functions
        ostream& 			printTo		(ostream &out)const;
        friend ostream&     operator<<  (ostream &out, const Simulation &sim)      {return sim.printTo(out);};

    };

	template<class type_msg, class peer_type>
	ostream& Simulation<type_msg, peer_type>::printTo(ostream& out)const {
		return out;
	}

	template<class type_msg, class peer_type>
	void Simulation<type_msg, peer_type>::run(json config) {
		ofstream out;
		if (config["logFile"] == "cout") {
			LogWriter::instance()->setLog(cout); // Set the log file to the console
		}
		else {
			string file = config["logFile"];
			//std::cout << "[DEBUG] Attempting to open log file at path: " << file << std::endl;
			out.open(file);
			if (out.fail()) {
				//cout << "Error: could not open file " << file << ". Writing to console" << endl;
				LogWriter::instance()->setLog(cout); // If the file doesn't open set the log file to the console
			}
			else {
				//cout << "Log file opened at path: " << file << endl;
				LogWriter::instance()->setLog(out); // Otherwise set the log file to the user given file
			}
		}

		std::chrono::time_point<std::chrono::high_resolution_clock> startTime, endTime; // chrono time points
   		std::chrono::duration<double> duration; // chrono time interval
		startTime = std::chrono::high_resolution_clock::now();

		std::chrono::time_point<std::chrono::high_resolution_clock> startTimeTest, endTimeTest; // chrono time points
   		std::chrono::duration<double> durationTest; // chrono time interval

		int _threadCount = thread::hardware_concurrency(); // By default, use as many hardware cores as possible
		//if (config.contains("threadCount") && config["threadCount"] > 0) {
		//	_threadCount = config["threadCount"];
		//}
		cout << "[simulation] Using " << _threadCount << " threads for the simulation." << endl;
		if (_threadCount > config["topology"]["totalPeers"]) {
			_threadCount = config["topology"]["totalPeers"];
		}
		int networkSize = static_cast<int>(config["topology"]["totalPeers"]);
		

		// dictionary that will contain, for each test i, all the results of test i
		map<string,TestInfo> testInfoDict;

		// maps (msgId, deliveryVector)
		map<string,vector<int>> terminationTime;
		
		srand(time(0));

		string status_file = config["outFile"];
		string end_file = ".txt";
		string start_file = "results_status/";
		string file = start_file + status_file + end_file;
		std::freopen(file.c_str(), "a+", stdout);

		BS::thread_pool pool(_threadCount);
		for (int i = 0; i < config["tests"]; i++) {
			startTimeTest = std::chrono::high_resolution_clock::now();
			LogWriter::instance()->setTest(i);

			// Configure the delay properties and initial topology of the network
			system.setDistribution(config["distribution"]);
			system.initNetwork(config["topology"], config["rounds"]);
			if (config.contains("parameters")) {
				system.initParameters(config["parameters"]);
			}
						
			//cout << "Test " << i + 1 << endl;
			for (int j = 0; j < config["rounds"]; j++) {
				//cout << "ROUND " << j << endl;
				LogWriter::instance()->setRound(j); // Set the round number for logging

				// do the receive phase of the round

				BS::multi_future<void> receive_loop = pool.parallelize_loop(networkSize, [this](int a, int b){system.receive(a, b);});
				receive_loop.wait();

				BS::multi_future<void> compute_loop = pool.parallelize_loop(networkSize, [this](int a, int b){system.performComputation(a, b);});
				compute_loop.wait();

				system.endOfRound(); // do any end of round computations

				BS::multi_future<void> transmit_loop = pool.parallelize_loop(networkSize, [this](int a, int b){system.transmit(a, b);});
				transmit_loop.wait();
			}

			
			terminationTime = system.term_time;
			json termTimeJson = terminationTime;
			//cout << "[simulation] " << termTimeJson << endl;

			
			vector<int> byzantine;
			for (int i=0; i<system.byz_vec.size(); i++){
				if (system.byz_vec[i]==true) byzantine.push_back(i);
			}

			int maPower = config["topology"]["messageAdversary"]["power"];
			string maType = config["topology"]["messageAdversary"]["behavior"];
			int senderId = system.sender_id;
			int totalBitSent = 0;
			for (auto peer_ptr : system.peers()) {
				auto casted_peer = dynamic_cast<peer_type*>(peer_ptr);
				if (casted_peer) {
					//cout << "Peer ID: " << casted_peer->id() << " sent " << casted_peer->bits_sent << " bytes.\n";
					totalBitSent += casted_peer->msgs_sent;

				}
			}

			TestInfo test(terminationTime,byzantine,maPower,maType,senderId,totalBitSent);
			test.computeDisconnectedNodes(config["topology"]["list"]);
			test.computeInfo();
			testInfoDict[std::to_string(i)] = test;

			endTimeTest = std::chrono::high_resolution_clock::now();
   			durationTest = endTimeTest - startTimeTest;

			cout << endl << "End test " << i << "  tot_bits_sent: " << totalBitSent << "   time:" << durationTest.count(); 
			
			
			/* cout << "totalMsgSent: " << totalMsgSent << endl;
			cout << "avgDeliveryTime: " << test.avgDeliveryTime << endl;
			cout << "maxDeliveryTime: " << test.maxDeliveryTime << endl;
			cout << "avgDeliveryNodes: " << test.avgDeliveryNodes << endl;
			cout << "totalMsgSent: " << test.totalMsgSent << endl;
			cout << "byzantineNodes: " << vec_to_string(byzantine) << endl;
			cout << vec_to_string(terminationTime["0"]) << endl;  */
			

		}
		
		endTime = std::chrono::high_resolution_clock::now();
   		duration = endTime - startTime;
		LogWriter::instance()->data["RunTime"] = duration.count();

		json test_info_dict_json = testInfoDict;
		string str = test_info_dict_json.dump();
		LogWriter::instance()->data["tests"] = test_info_dict_json;


		LogWriter::instance()->print();
		out.close();
	}

	
}

#endif /* Simulation_hpp */
