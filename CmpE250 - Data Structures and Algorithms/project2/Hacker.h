#include <iostream>

using namespace std;

#ifndef HACKER_H
#define HACKER_H

class Hacker
{
public:
	static int invalidQueue;
	static int invalidGift;
	static float totalGift;
	int ID;
	float arrivalTime;
	float arrivalTimeHoodies;  // arrival time to the queue
	float arrivalTimeStickers;  // arrival time to the queue
	float leaveTimeHoodies;
	float leaveTimeStickers;
	int gift = 0;
	bool inStickerQueue = false;
	bool inHoodieQueue = false;
	float wait = 0;
	int noValidCommits = 0; // valid commits (number of commits not length)
	int totalLength = 0; // whole commits
	int deskNumber = 0;
	Hacker(int ID, float arrivalTime);
	void addCommit(const int& commit, const float& commitTime) ;
	void print();
	bool operator>(const Hacker& other) const;
	bool isValid();
	Hacker& operator=(const Hacker& hacker);

};

#endif // HACKER