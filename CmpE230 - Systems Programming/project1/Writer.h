#ifndef WRITER_H
#define WRITER_H

#include <fstream>
#include <string>
#include <vector>
#include <stack>
#include <sstream>
#include <unordered_set>
using namespace std;

class Writer
{
private:    
    ofstream outputFile;
    ostringstream stream;
    
    //arithmetic writer functions

    
    
public:
    Writer();
    int tempVarCounter;
    int ifCounter;
    int whileCounter;
    int regCounter;

    //file functions
    void mountFile(string filePath);
    void dismountFile();
    bool fileMounted();

    //memory writer functions
    void allocate(string varName);
    void store(string varName, string value);

    void load(string loadTo, string loadFrom);
    void arithmetic(string saveTo, string opcode, string operandOne, string operandTwo);
    void choose(string& saveTo, vector<string>& operands);

    //other writer functions
    void ret(string ret);
    void brConditional(string condition, string blockOne, string blockTwo);
    void brUnconditional(string block);

    //void writeFile(Content content, string moduleID);
    //hypothetical Content object that contains all the data about the
    //LLVM file. fileContent function then uses this content to call
    //private printer functions.
    //Defined a test function for now:
    void writeToFile(string moduleID, unordered_set<string>& variableSet);
    void writeErrorToFile(string moduleID, int line);
    void writeLine(string line);
    void print(string& toWrite);
    void writeExpression(vector<string>& postFix);
};

#endif