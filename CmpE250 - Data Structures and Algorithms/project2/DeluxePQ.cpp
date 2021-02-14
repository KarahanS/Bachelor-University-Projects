#include "DeluxePQ.h"


template<class T>
void DeluxePQ<T>::swim(int index) {
	int parentID = index / 2;
	if(parentID == 0) return;  // we are at the root

	bool isHeapified = false;
	while (!isHeapified) {
		if(parentID == 0 || compare(this->array[index], this->array[parentID]) >= 0) {    // Comparison 1
			isHeapified = true;
			break;
		}

		// swap
		swap(this->array[index], this->array[parentID]);
		index = parentID;
		parentID = index / 2;
	}
} 

template<class T>
void DeluxePQ<T>::sink(int index) {
	int childID = 2 * index;
	if(childID > this->noItems) return;  // we are at the end 


	bool isHeapified = false;
	while(!isHeapified) {
		if(childID + 1 <= this->noItems && compare(array[childID], array[childID+1]) > 0) childID++;  // Comparison 2

		if(childID > this->noItems || compare(this->array[index], this->array[childID]) <= 0) {  // Comparison 3
			isHeapified = true;
			break;
		}

		// swap
		swap(this->array[index], this->array[childID]);

		index = childID;
		childID = 2 * index;

	}
}

// Don't know how to use capacity
template<class T>
DeluxePQ<T>::DeluxePQ(int capacity) {
	this->capacity = capacity;
	this->array.reserve(this->capacity);
	this->noItems = 0;
}

template<class T>
DeluxePQ<T>::DeluxePQ(const vector<T>& v) {

	this->capacity = v.size() + 1;
	this->array.reserve(v.capacity());  // NO COPY CONSTRUCTOR CALL
	
	for(int i=1; i<capacity; i++) {
		this->array[i] = v[i-1];
	}
	this->noItems = v.size();

	// heapify - O(n)
	for(int i= this->noItems / 2; i>0; i--) sink(i);
} 


// returns the next event, or hacker according to the implementation
template<class T>
T& DeluxePQ<T>::next() {
	return this->array[1];
}

template<class T>
bool DeluxePQ<T>::pop() {
	if(this->noItems == 0) return false; // nothing inside the vector

	// swap
	swap(this->array[1], this->array[this->noItems]);

	// this->array[this->noItems] = 0; --> this line doesn't work with Hacker, Event data type

	this->noItems--;  // popped
	this->sink(1);
	return true;
}

template<class T>
bool DeluxePQ<T>::add(const T& item) {

	if(this->noItems + 1 >= this->capacity) return false;
	this->noItems++;


	this->array[this->noItems] = item;  // DO NOT USE PUSH_BACK!
	swim(this->noItems);

	return true;
}

// return the number of elements in the pq
template<class T>
int DeluxePQ<T>::size() {
	return this->noItems;
}

template<class T>
bool DeluxePQ<T>::isEmpty() {
	return this->noItems == 0;
}



template<class T>
int DeluxePQ<T>::compare(const T& item1, const T& item2) {
	if(item1 > item2) return 1;
	else if (item2 > item1) return -1;
	else return 0;

}
template class DeluxePQ<int>;
template class DeluxePQ<Event>;
template class DeluxePQ<Hacker>;






