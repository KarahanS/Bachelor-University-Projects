#include <vector>
#include <string>
#include <iostream>  // included for debug
#include "Hacker.h"


#ifndef  EVENT_H
#define EVENT_H

class Event 
{
public:


	enum Type {
		ARRIVAL, COMMIT, STICKER_QUEUE_ENTER, STICKER_DESK_LEAVE, HOODIE_QUEUE_ENTER, HOODIE_DESK_LEAVE
	};
	// ARRIVAL = 0
	// COMMIT = 1
	// STICKER_QUEUE_ENTER = 2
	// STICKER_DESK_LEAVE = 3
	// HOODIE_QUEUE_ENTER = 4
	// HOODIE_DESK_LEAVE = 5

	Event();
	Event(const Type& type, int ID, const float& time,const int& commit = 0);
	int ID;
	Type type;
	int commit;
	float time;
	void print();
	bool operator>(const Event& other) const;
	Event& operator=(const Event& event);
};
#endif // EVENT_H