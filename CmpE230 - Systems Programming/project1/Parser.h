#ifndef PARSER_H
#define PARSER_H

#include "Writer.h"

#include <unordered_set>
#include <unordered_map>
#include <stack>
#include <vector>


using namespace std;
class Parser {
private:
	unordered_set<string> variableSet;
	int lineCount;
	Writer writer;
	bool chooseFound;
	
	bool validateVariable(string& var);
	bool validateNumber(string& var);
	void syntaxError();
	bool assignmentParser(string& line);
	bool expressionParser(string& expr);
	bool validateExpression(string& expr, vector<string>& tokens, vector<string>& varNames);
	bool replaceChoose(string& expr);

	
public:
	Parser(string writeToFile);
	~Parser();
	void read(vector<string>& lines);

};
#endif