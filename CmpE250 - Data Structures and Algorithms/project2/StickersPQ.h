#include "DeluxePQ.h"



#ifndef STICKERSPQ_H
#define STICKERSPQ_H


class StickersPQ : public DeluxePQ<Hacker> {
public:
	StickersPQ(int capacity = 20000);
	StickersPQ(const vector<Hacker>& v);
	int compare(const Hacker& item1, const Hacker& item2);
};

#endif // STICKERSPQ_H