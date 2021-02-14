#include "HoodiesPQ.h"

HoodiesPQ::HoodiesPQ(int capacity){

	this->capacity = capacity;
	this->array.reserve(this->capacity);
	this->noItems = 0;
}
HoodiesPQ::HoodiesPQ(const vector<Hacker>& v){


	this->capacity = v.size() + 1;
	this->array.reserve(v.capacity());  // NO COPY CONSTRUCTOR CALL
	
	for(int i=1; i<this->capacity; i++) {
		this->array[i] = v[i-1];
	}
	this->noItems = v.size();

	// heapify - O(n)
	for(int i= this->noItems / 2; i>0; i--) sink(i);
} 
int HoodiesPQ::compare(const Hacker& item1, const Hacker& item2) {
	// cout << " HoodiesPQ comparison called " << endl;
	float float1 = item1.arrivalTimeHoodies;
	float float2 = item2.arrivalTimeHoodies;


	if(item1.noValidCommits > item2.noValidCommits) return -1; // -1 --> minimum (first out)
	else if(item1.noValidCommits < item2.noValidCommits) return 1;
	else {
		if(float1 - float2 > 0.00001) return 1;
		else if (float2 - float1 > 0.00001) return -1;
		else {
			if(item1.ID > item2.ID) return 1;
			else if(item1.ID < item2.ID) return -1;
			else return 0;
		}
	}
}
