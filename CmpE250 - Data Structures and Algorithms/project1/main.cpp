#include "Character.h"
#include <iostream>
#include <fstream>
#include <vector>


using namespace std;

	// There are two communities in the battlefield.
	// Community 1 attacks first as a convention.

	// Damage = Attack point of attacker - defense point of defender
	// Negative health scores are considered as 0.

void Sort(vector<Character> &community);
int Find(const vector<Character> &community, int i);
void Simulation(vector<Character> &_attacker, vector<Character> &_defender, string special_skill, string attacker_name, string defender_name, 
	int &attacker_lastKilled, int &defender_lastKilled, bool &attacker_win, bool &defender_win, int &attacker_casualty, int &defender_casualty);




int main(int argc, char* argv[]) {
	
	// argv[0] is always reserved for the name of the program itself.
	string infile_name = argv[1];
	string outfile_name = argv[2];

	ifstream infile;
	ofstream outfile;
	infile.open(infile_name);


	vector<Character> community1;
	vector<Character> community2;

	// Stores the given order of characters (we need to record them to print out the results in correct order)
	vector<string> names1;
	vector<string> names2;


	int max_number_of_rounds;
	infile >> max_number_of_rounds;

	string name, type;
	int attack, defense, health;
	// first community
	for(int i=0; i<5; i++) {
		infile >> name >> type >> attack >> defense >> health;
		Character character(name, type, attack, defense, health, max_number_of_rounds);
		community1.push_back(character);
		names1.push_back(name);
	}

	// second community
	for(int i=0; i<5; i++) {
		infile >> name >> type >> attack >> defense >> health;
		Character character(name, type, attack, defense, health, max_number_of_rounds);
		community2.push_back(character);
		names2.push_back(name);
	}

	// Sorts the communities according to the alphabetic order
	Sort(community1);
	Sort(community2);


	int com1_lastKilled = -1, com2_lastKilled = -1, com1_casualty = 0, com2_casualty = 0;
	int round = 1;
	bool com1_win = false, com2_win = false;
	string attacker, defender, special_skill;
	// Battle Time
	for(round; round<=max_number_of_rounds && !com1_win && !com2_win; round++) {   // i=0 before the war
		// All updates will be done here.

		infile >> attacker >> defender >> special_skill;

		// runs the simulation according to the attacker and defender communities
		if(round%2 == 0) Simulation(community2, community1, special_skill, attacker, defender, com2_lastKilled, com1_lastKilled, com2_win, com1_win, com2_casualty, com1_casualty); 
		else Simulation(community1, community2, special_skill, attacker, defender, com1_lastKilled, com2_lastKilled, com1_win, com2_win, com1_casualty, com2_casualty);

		// round is ended, time to update the healthHistory and nRoundsSinceSpecial
		for(int i=0; i<community1.size(); i++) {
			community1[i].healthHistory[round] = community1[i].remainingHealth;
			community2[i].healthHistory[round] = community2[i].remainingHealth;

			community1[i].nRoundsSinceSpecial++;
			community2[i].nRoundsSinceSpecial++;
		}
	}


	// writing the output
	string result;
	if(com1_win) result = "Community-1";
	else if(com2_win) result = "Community-2";
	else result = "Draw";
	int casualties = com1_casualty + com2_casualty;



	outfile.open(outfile_name);

	outfile << result << "\n" << (round-1) << "\n" << casualties << endl;

	// write the output in the given order of characters
	for(int j=0; j<names1.size(); j++) {
		for(int i=0; i<community1.size(); i++) {
			if(community1[i].name.compare(names1[j]) == 0) {
						outfile << community1[i].name << " ";
						for(int r = 0; r<round; r++) outfile << community1[i].healthHistory[r] << " ";
							outfile << endl;
			}
		}
	}

	// write the output in the given order of characters
	for(int j=0; j<names2.size(); j++) {
		for(int i=0; i<community2.size(); i++) {
			if(community2[i].name.compare(names2[j]) == 0) {
						outfile << community2[i].name << " ";
						for(int r = 0; r<round; r++) outfile << community2[i].healthHistory[r] << " ";
							outfile << endl;
			}
		}
	}


	// at the end
	infile.close();
	outfile.close();

	return 0;
}

// Sorts the community in alphabetical order
void Sort(vector<Character> &community) {
	for(int i=0; i<community.size() - 1; i++) {
		if(community[i+1] < community[i]) {
			// swap
			Character ref = community[i+1];
			community[i+1] = community[i];
			community[i] =  ref;

			i = (i == 0) ? (-1) : (i-2);			
		}
	}

}

// if the current character is dead, it finds the next character according to the given rules
int Find(const vector<Character> &community, int i) {
	int index = i;
	// i - to the end
	for(index; index < community.size() && !community[index].isAlive; index++) {}

	// if found, return	
	if(community[index].isAlive) return index;

	index = i;
	// i - to the beginning
	for(index; index  >= 0 && !community[index].isAlive; index--) {}

		return index;
	

}
// Whole simulation runs here. It takes the attacker and defender communities as a reference since we want to make permanent changes on them.
// Takes special skill, attacker name and defender name. It also takes casualty list of attacker and defender communities. It takes boolean values
// that indicate the win conditions.
void Simulation(vector<Character> &_attacker, vector<Character> &_defender, string special_skill, string attacker_name, string defender_name, 
	int &attacker_lastKilled, int &defender_lastKilled, bool &attacker_win, bool &defender_win, int &attacker_casualty, int &defender_casualty) {


	for(int i = 0; i < _attacker.size(); i++) {
	    if(_attacker[i].name == attacker_name) {   // we found our attacker
	        i = Find(_attacker, i);           // in case attacker is dead
	        for(int j=0; j<_defender.size(); j++) {
	                if(_defender[j].name == defender_name) {   // if not alive, just go on
	                	j = Find(_defender, j);


	                	int damage = _attacker[i].attack - _defender[j].defense;
			            	// Special skill check		    
	                	if(special_skill.compare("SPECIAL") == 0) {
	                		if(_attacker[i].type.compare("Elves") == 0 && _attacker[i].nRoundsSinceSpecial >= 10) {
	                			int transfer = _attacker[i].remainingHealth / 2;
	                			_attacker[i].remainingHealth = _attacker[i].remainingHealth - transfer;



			            		int k;	// we need to find the hobbit
			            		for(k=0; k<_attacker.size() && _attacker[k].type.compare("Hobbit") != 0; k++) {}
			            				_attacker[k].remainingHealth += transfer;    // hobbit cannot be dead. If he was, then simulation would end.
			            			    _attacker[i].nRoundsSinceSpecial = -1;   // it will be zero at the end, no worries.

			            			} else if (_attacker[i].type.compare("Dwarfs") == 0  && _attacker[i].nRoundsSinceSpecial >= 20) {
			            				// doubles the damage
			            				damage = damage * 2;
			            				_attacker[i].nRoundsSinceSpecial = -1;

			            			} else if (_attacker[i].type.compare("Wizards") == 0 && _attacker[i].nRoundsSinceSpecial >= 50 && attacker_lastKilled != -1) {
			            				_attacker[i].nRoundsSinceSpecial = -1;
			            				_attacker[attacker_lastKilled].remainingHealth = _attacker[attacker_lastKilled].healthHistory[0]; 

			            				if(!_attacker[attacker_lastKilled].isAlive) {   // so, member is actually alive.
			            				attacker_casualty--;
			            				_attacker[attacker_lastKilled].isAlive = true;  // resurrected
			            				_attacker[attacker_lastKilled].nRoundsSinceSpecial = 0;


			            			}
			            		}
			            	}

			            		// attack
			            	if(damage > 0 ) {
			            			// if damage is bigger then the health of defender, he dies. Otherwise update the health.
			            		_defender[j].remainingHealth = (_defender[j].remainingHealth - damage > 0) ? (_defender[j].remainingHealth - damage) : (0);

			            				if(_defender[j].remainingHealth == 0) {  // he is dead
			            					defender_casualty++;
			            					_defender[j].isAlive = false;
			            					// take the dead character to the graveyard
			            					defender_lastKilled = j;

			            					// If dead character is a hobbit, game ends. Also, if number of casualties reaches 4, then again : game ends, attacker wins.
			            					if(_defender[j].type.compare("Hobbit") == 0 || defender_casualty == 4) attacker_win = true;

			            				}
			            			}
			            			break;
			            		}
			            	}
			            	break;
			            }
			        }
			    }
			