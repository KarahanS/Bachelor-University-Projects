#include "StickersPQ.h"

StickersPQ::StickersPQ(int capacity){

	this->capacity = capacity;
	this->array.reserve(this->capacity);
	this->noItems = 0;
}
StickersPQ::StickersPQ(const vector<Hacker>& v) {

	// cout << " StickersPQ is initialized" << endl;
	this->capacity = v.size() + 1;
	this->array.reserve(v.capacity());  // NO COPY CONSTRUCTOR CALL
	
	for(int i=1; i<this->capacity; i++) {
		this->array[i] = v[i-1];
	}
	this->noItems = v.size();

	// heapify - O(n)
	for(int i= this->noItems / 2; i>0; i--) sink(i);
} 


int StickersPQ::compare(const Hacker& item1, const Hacker& item2) {
	// cout << " StickerPQ comparison called " << endl;

	float float1 = item1.arrivalTimeStickers;
	float float2 = item2.arrivalTimeStickers;

	if(float1 - float2 > 0.00001) return 1;
	else if (float2 - float1 > 0.00001) return -1;
	else {
		if(item1.ID > item2.ID) return 1;
		else if (item1.ID < item2.ID) return -1;
		else return 0;
	}
}


