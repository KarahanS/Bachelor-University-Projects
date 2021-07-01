#include "Writer.h"
#include <iostream>


Writer::Writer()
{
    tempVarCounter = 1;
    ifCounter = 0;
    whileCounter = 0;
    regCounter = 1;
}



void Writer::writeToFile(string moduleID, unordered_set<string>& variableSet)
{
    //Write file header
    if (fileMounted())
    {
        outputFile  << "; ModuleID = '" << moduleID << "'" << endl
                    << "declare i32 @printf(i8*, ...)" << endl
                    << "@print.str = constant [4 x i8] c\"%d\\0A\\00\"" << endl << endl;

        outputFile  << "define i32 @choose(i32 %expr1, i32 %expr2, i32 %expr3, i32 %expr4) {" << endl
                    << "entry:" << endl
                    << "    %t1 = icmp eq i32 %expr1, 0" << endl
                    << "    br i1 %t1, label %equal, label %not_equal" << endl
                    << "equal:" << endl
                    << "    ret i32 %expr2" << endl
                    << "not_equal:" << endl
                    << "    %t2 = icmp sgt i32 %expr1, 0" << endl
                    << "    br i1 %t2, label %greater, label %smaller" << endl
                    << "greater:" << endl
                    << "    ret i32 %expr3" << endl
                    << "smaller:" << endl
                    << "    ret i32 %expr4" << endl << "}" << endl << endl
                    << "define i32 @main() {" << endl;

        for (auto& v: variableSet)
        {
            outputFile << "    %_" << v << " = alloca i32" << endl;
        }
        outputFile << endl;

        for (auto& v: variableSet)
        {
            outputFile << "    store i32 0, i32* %_" << v << endl;
        }
        outputFile << endl;

        outputFile << stream.str();
        outputFile << "    ret i32 0" << endl << "}";

    }
    else 
    {
        cout << "ERROR: No file mounted." << endl;
        cout << "AT   :  Writer::writeToFile()" << endl;
    }
}

void Writer::writeErrorToFile(string moduleID, int line)
{
    outputFile  << "; ModuleID = '" << moduleID << "'" << endl
                << "declare i32 @printf(i8*, ...)" << endl
                << "@print.str = constant [23 x i8] c\"Line %d: syntax error\\0A\\00\"" << endl << endl
                << "define i32 @main() {" << endl

                << "    call i32 (i8*, ...)* @printf(i8* getelementptr ([23 x i8]* @print.str, i32 0, i32 0), i32 "
                << line
                << " )" << endl

                << "    ret i32 0" << endl << "}";
                
}

//memory writer functions

// allocates 32 bit memory for a variable
void Writer::allocate(string varName)
{
    stream  << "    "
            << varName
            << " = alloca i32" << endl;
}

// stores a value in a 32 bit variable, initally value of the each variable is assigned to zero
void Writer::store(string varName, string value)
{
    stream  << "    store i32 "
            << value
            << ", i32* "
            << varName << endl;
}

void Writer::load(string loadTo, string loadFrom)
{
    stream  << "    "
            << loadTo
            << " = load i32* "
            << loadFrom << endl;
}

//arithmetic writer functions
//sub instruction: https://llvm.org/docs/LangRef.html#sub-instruction
//mul instruction: https://llvm.org/docs/LangRef.html#mul-instruction
//There are two choices for integer division: udiv and sdiv.
//See the link: //https://llvm.org/docs/LangRef.html#udiv-instruction
//opcodes:
//add, sub, sdiv, mul, icmp ne, icmp sgt, icmp eq
void Writer::arithmetic(string saveTo, string opcode, string operandOne, string operandTwo)
{
    stream  << "    "
            << saveTo
            << " = "
            << opcode
            << " i32 "
            << operandTwo
            << ", "
            << operandOne << endl;
}

//Other Writer Functions
void Writer::ret(string ret)
{
    stream  << "    "
            << "ret i32 "
            << ret << endl;
}

void Writer::brConditional(string condition, string blockOne, string blockTwo)
{
    // cout << "CHECK br: " << endl << stream.str() << endl;
    stream  << "    br i1 "
            << condition
            << ", label %"
            << blockOne
            << ", label %"
            << blockTwo << endl << endl;
}

void Writer::brUnconditional(string block)
{
    stream  << "    br label %"
            << block << endl << endl;
}

void Writer::choose(string& saveTo, vector<string>& operands)
{
    stream  << "    "
            << saveTo
            << " = call i32 @choose( i32 "
            << operands[0];

    for (int i=1; i<4; i++)
    {
        stream << ", i32 " << operands[i];
    }
    stream << ")" << endl;
}

void Writer::writeLine(string line)
{
    stream << line << endl;
}

bool isOp(string& string)
{
    return (string[0] == '+' || string[0] == '-' || string[0] == '*' || string[0] == '/');
}

void Writer::writeExpression(vector<string>& postFix)
{
    stack<string> bin;

    for (auto s: postFix)
    {
        if (isOp(s))
        {

            string operandOne = bin.top();
            bin.pop();
            string operandTwo = bin.top();
            bin.pop();
            char op = s[0];
            string opCode;
            if (op == '*') {opCode = "mul";}
            else if (op == '/') {opCode = "sdiv";}
            else if (op == '+') {opCode = "add";}
            else if (op == '-') {opCode = "sub";}
            else {cout << "Something went wrong." << endl;}

            string saveTo = "%t" + to_string(tempVarCounter++);
            arithmetic(saveTo, opCode, operandOne, operandTwo);
            bin.push(saveTo);
        }
        else
        {
            bin.push(s);
        }
    }
}

void Writer::print(string& toWrite)
{
    stream  << "    call i32 (i8*, ...)* @printf(i8* getelementptr ([4 x i8]* @print.str, i32 0, i32 0), i32 "
            << toWrite
            << " )" << endl;
}

//file functions
void Writer::mountFile(string filePath)
{
    outputFile.open(filePath);
}

// closes the file
void Writer::dismountFile()
{
    outputFile.close();
}

bool Writer::fileMounted()
{
    return outputFile.is_open();
}