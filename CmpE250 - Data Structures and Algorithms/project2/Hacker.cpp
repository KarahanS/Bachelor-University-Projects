#include "Hacker.h"

int Hacker::invalidQueue = 0;
int Hacker::invalidGift = 0;
float Hacker::totalGift = 0;
Hacker::Hacker(int ID, float arrivalTime) {
	this->ID = ID;
	this->arrivalTime = arrivalTime;


}

Hacker& Hacker::operator=(const Hacker& hacker) {
	if(this==&hacker) {
		return *this;
	} else {
		ID = hacker.ID;
		arrivalTime = hacker.arrivalTime;
		arrivalTimeHoodies = hacker.arrivalTimeHoodies;  // arrival time to the queue
		arrivalTimeStickers = hacker.arrivalTimeStickers;  // arrival time to the queue
		leaveTimeHoodies = hacker.leaveTimeHoodies;
		leaveTimeStickers = hacker.leaveTimeStickers;
		gift = hacker.gift;
		inStickerQueue = hacker.inStickerQueue;
		inHoodieQueue = hacker.inHoodieQueue;
		noValidCommits = hacker.noValidCommits; // valid commits (number of commits not length)
		totalLength = hacker.totalLength; // whole commits
		deskNumber = hacker.deskNumber;
		return *this;
	}
}

void Hacker::addCommit(const int& commit, const float& commitTime) {
	// DEBUG
	// cout << "Hacker with the ID " << ID << " made a commit = " << commit << " in timestamp " << commitTime  <<  endl;
	// DEBUG
	if(commit >= 20) this->noValidCommits++;
	totalLength += commit;

}
void Hacker::print() {
	cout << "Hacker ID -> " << this->ID << endl;
}
bool Hacker::operator>(const Hacker& other) const{
	// cout << " This function shouldn't be called. Hacker operator overload." << endl;
	return 1;
}
bool Hacker::isValid() {  // isValid for queue

	if(this->noValidCommits < 3) {
		invalidQueue++;
		// cout << " Hacker with ID " << this->ID << " tries to enter a queue but he has " << noValidCommits << " valid commits. Invalid Attempt" << endl;
		return false;
	}
	if(this->gift == 3) {  // 3 hoodies + 3 stickers  --> 4th attempt to enter the queue
		invalidGift++;
		// cout << " Hacker with ID " << this->ID << " tries to enter a queue but he has 3 hoodies and stickers. 4th attempt -- Invalid Attempt" << endl;
		return false;
	}
	if(this->inStickerQueue) {
		// cout << " Hacker with ID " << this->ID << " tries to enter a queue but he is already in sticker queue. Invalid Attempt" << endl;
		return false;
	}
	if(this->inHoodieQueue) {
		// cout << " Hacker with ID " << this->ID << " tries to enter a queue but he is already in hoodie queue. Invalid Attempt" << endl;
		return false;
	}
	return true;  // it is in queue then


}