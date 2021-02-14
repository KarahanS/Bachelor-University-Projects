#include "Event.h"

using namespace std;

#ifndef DELUXEPQ_H
#define DELUXEPQ_H

template <class T>
class DeluxePQ 
{
public:
	int capacity; // capacity of the vector (it includes 0)
	int noItems; 
	vector<T> array;
	DeluxePQ<T>(int capacity = 20000);
	DeluxePQ<T>(const vector<T>& v);
	void swim(int index);
	void sink(int index);
	T& next();
	bool pop();
	bool add(const T& item);
	int size();
	virtual int compare(const T& item1,const T& item2);   // virtual means it is going to be overridden
	bool isEmpty();
};

#endif // DELUXEPQ_H