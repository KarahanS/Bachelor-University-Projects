#include "Event.h"

Event::Event() {
	// cout << "Event constructor is called - something is wrong" << endl;
} 
Event::Event(const Type& type, int ID, const float& time, const int& commit) {
	this->type = type;
	this->ID = ID;
	this->time = time;
	this->commit = commit;
	// this->print();

}
void Event::print() {

	string type;
	int t = this->type;
	switch(t) {
		case 0: 
		type = "Arrival";
		break;
		case 1:
		type = "Commit";
		break;
		case 2:
		type = "Sticker queue enter attempt";
		break;
		case 3:
		type = "Sticker desk leave";
		break;
		case 4:
		type = "Hoodie queue enter attempt";
		break;
		case 5:
		type= "Hoodie desk leave";
		break;

	}
	cout << "Event --> " << type << " | time --> " << this->time << " | hacker ID --> " << this->ID << endl;
}
bool Event::operator>(const Event& other) const {
	float float1 = this->time;
	float float2 = other.time;
	float res = float1 - float2;


	if(res > 0.00001) return true;
	else if(-res > 0.00001) return false;
	else {
		if(this->ID > other.ID) return true;
		else if(this->ID < other.ID) return false;
		else return false;  // not going to run anyways
	}
}
Event& Event::operator=(const Event& event) {
	if(this==&event) {
		return *this;
	} else {
		this->ID = event.ID;
		this->type = event.type;
		this->commit = event.commit;
		this->time = event.time;
		return *this;
	}
}