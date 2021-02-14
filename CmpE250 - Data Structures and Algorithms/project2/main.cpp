#include "DeluxePQ.h"
#include "Hacker.h"
#include "Event.h"
#include "HoodiesPQ.h"
#include "StickersPQ.h"

#include <iomanip>
#include <string>
#include <fstream>

int main(int argc, char* argv[]) {
    int maxSticker = 0, maxHoodie = 0, invalidQueue = 0, invalidGift = 0;  
    float averageGift = 0, waitSQ = 0, waitHQ = 0, totalCommit = 0, totalLines = 0, totalTurnArounds = 0;

	struct Desk {
		float serviceTime;
		bool available;
	};

	string infile_name = argv[1];
	string outfile_name = argv[2];

	ifstream infile;
	ofstream outfile;
	infile.open(infile_name);

	int N;
	infile >> N;   // N denotes the total number of hackers
	vector<Hacker> hackers;
	hackers.reserve(N);
	vector<Event> events;


	// Create hacker objects and store them in the vector.
	for(int i=0; i<N; i++) {
		float arrivalTime;
		infile >> arrivalTime;

		Hacker h(i+1, arrivalTime);
		hackers.push_back(h);


		Event event(Event::Type::ARRIVAL, i+1, arrivalTime);
		events.push_back(event);
	}


	int C;
    infile >> C;

    
    for(int i=0; i<C; i++) {
    	int ID, length;
    	float time;

    	infile >> ID >> length >> time;
    	Event event(Event::Type::COMMIT, ID, time, length);
    	events.push_back(event);
    
    }


    int Q;
    infile >> Q;
    for(int i=0; i<Q; i++) {
    	int ID;
    	float time;

    	infile >> ID >> time;
    	Event event(Event::Type::STICKER_QUEUE_ENTER, ID, time);
    	events.push_back(event);
    }

    int Ds;  // Desks for stickers
    infile >> Ds;

    Desk serviceSticker[Ds];
    float serviceTime;

    for(int i=0; i<Ds; i++) {
    	infile >> serviceTime;
    	Desk desk = {};
    	desk.serviceTime = serviceTime;
    	desk.available = true;
    	serviceSticker[i] = desk;
    }


    int Dh;  // Desks for hoodies
    infile >> Dh;

    Desk serviceHoodie[Dh];

    for(int i=0; i<Dh; i++) {
    	infile >> serviceTime;
    	Desk desk = {};
    	desk.serviceTime = serviceTime;
    	desk.available = true;
    	serviceHoodie[i] = desk;
    } 
	

    // SHOW TIME

    DeluxePQ<Event> DES = DeluxePQ<Event>(events);   // Complexity = O(n)


    StickersPQ StickersQ = StickersPQ(hackers.size()+1);  // Maximum length for the sticker queue can be number of hackers (0 included)
    HoodiesPQ HoodiesQ = HoodiesPQ(hackers.size()+1); // Maximum length for the hoodies queue can be number of hackers (0 included)

    // hacker vector -->  0 1 2 3 4 5 6      capacity = 7   noItems = 6

    int maximumSticker, maximumHoodie;
    float time;

    while(!DES.isEmpty()) {
    	Event nextEvent = DES.next();
     	DES.pop();
     	int ID, commit;
     	time;

     	if(nextEvent.type == Event::Type::ARRIVAL) { /* do nothing */  }
     	else if (nextEvent.type == Event::Type::COMMIT) {
     		ID = nextEvent.ID;
     		commit = nextEvent.commit;
     		time = nextEvent.time;

            totalCommit++;
            totalLines += commit;
     		hackers[ID-1].addCommit(commit, time);    		
     	}
     	else if(nextEvent.type == Event::Type::STICKER_QUEUE_ENTER) {
     		ID = nextEvent.ID;
     		time = nextEvent.time;

     		if(hackers[ID-1].isValid()) {
     			// cout << " Hacker with ID " << ID << " has an attempt to enter the sticker queue in timestamp " << time << endl;

     			// first we need to see if there is any available desk
     			// if there is no available desk, put it to the queue

                int d = 0;
                for(d=0; d < Ds && !serviceSticker[d].available; d++) {}

                d = (d >= Ds) ? (0) : (d);
                if(serviceSticker[d].available) {   // We found an available desk
                    // cout << " Available desk is found! Hacker with ID " << ID << " enters the sticker desk " << endl;

                    float t =  time + serviceSticker[d].serviceTime;
                    Event event(Event::Type::STICKER_DESK_LEAVE, ID, t);
                    DES.add(event);
                    serviceSticker[d].available = false;  // not available from now on
                    hackers[ID - 1].deskNumber = d;       // hacker is in the desk d
                    hackers[ID - 1].arrivalTimeStickers = time;  // TO COMPUTE TOTAL TURNAROUND TIME IT IS NECESSARY

 
                } else {    // No available desk, put it to the queue
                    // cout << " No available desk right now. Hacker with ID " << ID << " enters sticker queue" << endl;

                    hackers[ID - 1].arrivalTimeStickers = time;
                    StickersQ.add(hackers[ID-1]);
                    hackers[ID - 1].inStickerQueue = true;
                    if(StickersQ.size() > maxSticker) maxSticker = StickersQ.size();
                }

     		}
     	}
        // There cannot be a sticker desk leave event if hacker is not in the desk
     	else if(nextEvent.type == Event::Type::STICKER_DESK_LEAVE) {
            ID = nextEvent.ID;
            time = nextEvent.time;

            // cout << " Hacker with ID " << ID << " leaves the sticker desk in timestamp " << time <<  endl;

            // WHAT TO DO?   
            // 1- If there is anyone in the sticker queue, he gets to the available desk
            // 2- Hacker attempts to enter the hoodie queue

            serviceSticker[hackers[ID-1].deskNumber].available = true;   // available from now on
            int d = hackers[ID-1].deskNumber;

            // hackers[ID-1].deskNumber=0;  --> I don't know if this is necessary

            if(!StickersQ.isEmpty()) {

                int otherID = StickersQ.next().ID;
                hackers[otherID - 1].inStickerQueue = false;
                // cout << " A desk is empty and the hacker with the ID " << otherID << " enter that sticker desk leaving the queue " << endl;

                float t =  time + serviceSticker[d].serviceTime;
                Event event(Event::Type::STICKER_DESK_LEAVE, otherID, t);
                DES.add(event);
                serviceSticker[d].available = false;  // not available from now on
                hackers[otherID - 1].deskNumber = d;       // hacker is in the desk d
                StickersQ.pop();

                hackers[otherID - 1].wait += (time - hackers[otherID - 1].arrivalTimeStickers);
                waitSQ += (time - hackers[otherID - 1].arrivalTimeStickers);


            }

            if(hackers[ID - 1].isValid()) {
                // cout << " Hacker with ID " << ID << " has an attempt to enter the hoodie queue in timestamp " << time << endl;

                int d = 0;
                for(d=0; d < Dh && !serviceHoodie[d].available; d++) {}

                d = (d >= Dh) ? (0) : (d);
                if(serviceHoodie[d].available) {   // We found an available desk
                    // cout << " Available desk is found! Hacker with ID " << ID << " enters the hoodie desk " << endl; 

                    float t =  time + serviceHoodie[d].serviceTime;
                    Event event(Event::Type::HOODIE_DESK_LEAVE, ID, t);
                    DES.add(event);
                    serviceHoodie[d].available = false;  // not available from now on
                    hackers[ID - 1].deskNumber = d;       // hacker is in the desk d

 
                } else {    // No available desk, put it to the queue
                    // cout << " No available desk right now. Hacker with ID " << ID << " enters hoodie queue" << endl;

                    hackers[ID - 1].arrivalTimeHoodies = time;
                    HoodiesQ.add(hackers[ID-1]);
                    hackers[ID - 1].inHoodieQueue = true;
                    if(HoodiesQ.size() > maxHoodie) maxHoodie = HoodiesQ.size();
                }

            }

        }
     	else if(nextEvent.type == Event::Type::HOODIE_DESK_LEAVE) {
            ID = nextEvent.ID;
            time = nextEvent.time;

            // cout << " Hacker with ID " << ID << " leaves the hoodie desk in timestamp " << time <<  endl;
            totalTurnArounds += (time - hackers[ID -1].arrivalTimeStickers);

            // 1- Hacker gets a sticker gift   gift++
            // 2- If there is anyone in the hoodie queue, he gets to the available desk

            serviceHoodie[hackers[ID-1].deskNumber].available = true;   // available from now on
            hackers[ID-1].gift++;  // hoodie is taken
            hackers[ID-1].totalGift++;
            int d = hackers[ID-1].deskNumber;

            // hackers[ID-1].deskNumber=0;  --> I don't know if this is necessary

            if(!HoodiesQ.isEmpty()) {

                int otherID = HoodiesQ.next().ID;
                hackers[otherID - 1].inHoodieQueue = false;
                // cout << " A desk is empty and the hacker with the ID " << otherID << " enter that hoodie desk leaving the queue " << endl;

                float t =  time + serviceHoodie[d].serviceTime;
                Event event(Event::Type::HOODIE_DESK_LEAVE, otherID, t);
                DES.add(event);
                serviceHoodie[d].available = false;  // not available from now on
                hackers[otherID - 1].deskNumber = d;       // hacker is in the desk d
                HoodiesQ.pop();

                hackers[otherID - 1].wait += (time - hackers[otherID - 1].arrivalTimeHoodies);
                waitHQ += (time - hackers[otherID - 1].arrivalTimeHoodies);


            }
        }
     	else if(nextEvent.type == Event::Type::HOODIE_QUEUE_ENTER) { /* maybe just delete this ? */ }
    }  

    invalidGift = hackers[0].invalidGift;
    invalidQueue = hackers[0].invalidQueue;
    averageGift = hackers[0].totalGift / N;
    float averageWaitSQ = waitSQ / (hackers[0].totalGift); 
    float averageWaitHQ = waitHQ / (hackers[0].totalGift);
    float averageCommit = totalCommit / N;
    float averageLine = totalLines / totalCommit;
    float averageTurnAround = totalTurnArounds / (hackers[0].totalGift);

    float maxWaiting = -1, leastWaiting = time+1;
    int maxWID = 0, minWID = -1;

    for(int i=0; i<hackers.size(); i++) {
        float float1 = hackers[i].wait;
        float float2 = maxWaiting;
        float float3 = leastWaiting;
        if(float1 - float2 > 0.00001) {
            maxWaiting = hackers[i].wait;
            maxWID = i+1;
        }

        if(hackers[i].gift == 3 && float3 - float1 > 0.00001) {
            leastWaiting = hackers[i].wait;
            minWID = i+1;
        }
    }
    leastWaiting = (leastWaiting == time+1) ? (-1) : (leastWaiting);

    outfile.open(outfile_name);
    outfile << std::setprecision(3) << std::fixed;
    outfile << maxSticker << endl;
    outfile << maxHoodie  << endl;
    outfile << averageGift << endl;
    outfile << averageWaitSQ << endl;
    outfile << averageWaitHQ << endl;
    outfile << averageCommit << endl;
    outfile << averageLine << endl;
    outfile << averageTurnAround << endl;
    outfile << invalidQueue << endl;
    outfile << invalidGift << endl;
    outfile << maxWID << " " << maxWaiting << endl;
    outfile << minWID << " " << leastWaiting << endl;
    outfile << time;

	infile.close();
	outfile.close();

	return 0;
}