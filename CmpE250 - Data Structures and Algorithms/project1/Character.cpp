#include "Character.h"

Character::Character(string _name, string _type, int _attack, int _defense, int _remainingHealth, int _nMaxRounds) {
	name = _name;
	type = _type;
	attack = _attack;
	defense = _defense;
	remainingHealth = _remainingHealth;
	nMaxRounds = _nMaxRounds;
	healthHistory = new int[nMaxRounds+1]{0};  // if there are 100 rounds, this variable should store 101 values.
	healthHistory[0] = remainingHealth;
	nRoundsSinceSpecial = 0;                  // at the beginning, roundsSinceSpecial is assigned to 0.

}

Character::Character(const Character& character) {
	name = character.name;
	type = character.type;
	attack = character.attack;
	defense = character.defense;
	remainingHealth = character.remainingHealth;
	nMaxRounds = character.nMaxRounds;
	healthHistory = new int[nMaxRounds + 1];
	nRoundsSinceSpecial = character.nRoundsSinceSpecial;

	// copy the content of the array
	for(int i=0; i < nMaxRounds + 1; i++) {
		healthHistory[i] = character.healthHistory[i];
	}	

}

// parameter is the right hand side character
Character& Character::operator=(const Character& character) {
	// this is a pointer
	if(this == &character) {
		return *this;   // return the object itself 
	} else {
		name = character.name;
		type = character.type;
		attack = character.attack;
		defense = character.defense;
		remainingHealth = character.remainingHealth;
		nMaxRounds = character.nMaxRounds;
		nRoundsSinceSpecial = character.nRoundsSinceSpecial;

		for(int i=0; i < nMaxRounds + 1; i++) {
			healthHistory[i] = character.healthHistory[i];
		}
		return *this;
	}


}

bool Character::operator<(const Character& other) {
	if(this->name.compare(other.name) < 0) return true;  // this comes first in alphabetical order
	else return false;
}

Character::~Character() {
	// delete the dynamic memory
	delete[] healthHistory;

}
