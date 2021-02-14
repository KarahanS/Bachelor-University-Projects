#include "DeluxePQ.h"

#ifndef HOODIESPQ_H
#define HOODIESPQ_H


class HoodiesPQ : public DeluxePQ<Hacker> {
public:
	HoodiesPQ(int capacity = 20000);
	HoodiesPQ(const vector<Hacker>& v);
	int compare(const Hacker& item1, const Hacker& item2);
};

#endif // HOODIESPQ_H