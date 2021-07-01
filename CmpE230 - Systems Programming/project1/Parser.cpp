#include "Parser.h"
#include <iostream>
using namespace std;
// Creates a Parser object and a Writer object associated with it
Parser::Parser(string writeToFile) {
    lineCount = 0;
    writeToFile.replace(writeToFile.rfind("."), writeToFile.size(), ".ll");
    writer.mountFile(writeToFile);
    chooseFound = false;
}
// Destructor dismounts the file 
Parser::~Parser()
{
    writer.dismountFile();
}

/*
A variable name starts wtih an alphabetic character followed by alphanumeric characters.
*/
bool Parser::validateVariable(string& var) {
    if (var[0] == '#') return true;
    if(!isalpha(var[0])) return false;
    for(int i = 0; i <(int)var.size(); i++) {
        if(!isalnum(var[i])) return false;
    }
    if(var == "if" || var == "while" || var == "print" || var == "choose") return false;

    this->variableSet.insert(var);
    return true;
}

// If a "variable" do not satisfy the conditions to be a "variable" in an expression.
// It may be a number. We have to check it, if it doesn't also satisfy the conditions to be a number, syntax error.
bool Parser::validateNumber(string& var) {
    for(int i=0; i<(int)var.size(); i++) {
        if(!isdigit(var[i])) return false;
    }
    return true;
}

void Parser::syntaxError() {
    writer.writeErrorToFile("mylang2ir", this->lineCount);
}

// line parser is used for the assignment statements
// left hand side = lhs    right hand side = rhs (expression)
bool Parser::assignmentParser(string& line) {

    size_t index = line.find("=");
    string lhs = line.substr(0, index);
    string rhs = line.substr(index + 1);

    if(!validateVariable(lhs) || !expressionParser(rhs)) return false;
    // rhs will be checked under the expressionParser

    if (validateNumber(rhs))
    {
        writer.store("%_"+lhs, rhs);
    }
    else
    {
        writer.store("%_"+lhs, "%t"+to_string(writer.tempVarCounter-1));
    }

    return true;
}

/*
Expression parser sends the expression to validateExpression(). If expression is valid,
it transforms the expression from infix to postfix and sends it to the writer.
*/
bool Parser::expressionParser(string& expr) {
    expr = expr + "+0";
    vector<string> tokens;
    vector<string> varNames;
    if(!validateExpression(expr, tokens, varNames)) return false;

    unordered_map<string, int> map;
    map.insert(pair<string, int>("*", 3));
    map.insert(pair<string, int>("/", 3));
    map.insert(pair<string, int>("+", 2));
    map.insert(pair<string, int>("-", 2));
    map.insert(pair<string, int>("(", 1));

    stack<string> opStack;
    vector<string> postfix;

    for(int i=0; i<tokens.size(); i++) {
        if(validateVariable(tokens[i]) || validateNumber(tokens[i])) postfix.push_back(tokens[i]);
        else if(tokens[i] == "(") opStack.push(tokens[i]);
        else if(tokens[i] == ")") {
            string topToken = opStack.top();
            opStack.pop();

            while(topToken != "(") {
                postfix.push_back(topToken);
                topToken = opStack.top();
                opStack.pop();
            }
        } else {
            while(!opStack.empty() && map[opStack.top()] >= map[tokens[i]]) {
                postfix.push_back(opStack.top());
                opStack.pop();
            }
            opStack.push(tokens[i]);
        }
    }

    while(!opStack.empty()){
        postfix.push_back(opStack.top());
        opStack.pop();
    }

    // RETURN POSTFIX TO WRITER/CONTENT
    
    for (auto& v: varNames)
    {
        string loadTo = "%t" + to_string(writer.tempVarCounter++);
        writer.load(loadTo, "%_" + v);
        for (auto& t: postfix)
        {
            if (v.compare(t) == 0)
            {
                t = loadTo;   
            }
        }
    }

    for (auto& t: postfix)
    {
        if (t[0] == '#')
        {
            t = t.substr(1,t.size()-2);
        }
    }

    writer.writeExpression(postfix);


    return true;
}

// Checks if the given expression is valid
bool Parser::validateExpression(string& expr, vector<string>& tokens, vector<string>& varNames) {
    /*
    We evaluate statements without if, while, print() or choose() as "expression".
    We check if these are still existent in our expression, if so we raise a Syntax error.

    Keep in mind that, some other errors like unmatched parenthesis can be present.
    You need to check it under expressionParser.
    */
    if(expr.find("choose(") != string::npos ||
        expr.find("print(") != string::npos ||
        expr.find("}") != string::npos ||
        expr.find("{") != string::npos ||
        expr.find("=") != string::npos)  {
         return false;

    }
       

    int unmatched_parenthesis = 0;
    // name is tricky, variables can include numbers.
    vector<string> variables;


    string var = "";
    char last = '+';
    bool lastChoose = false; 

    /*
    There cannot be consecutive operators
    Before "(" = operator or "(" (no alphanumeric - no ")")
    After "(" = operand or "("   (no operator - no ")")
    Before ")" = operand or ")"  (no operator - no "(")
    After ")" = operator or ")"  (no alphanumeric - no "(")

    An operand can come after an operator or "(", but not ")".

    parenthesis with no content is also syntax error -->  ()
    This is also syntax error --> )(   There should be an operator in between


    */


    for(int i=0; i<(int)expr.size(); i++) {
        if(isalnum(expr[i])) {
            var.push_back(expr[i]);
            if(last == ')') return false;
        } else {
            if(!var.empty()) {
                variables.push_back(var);
                tokens.push_back(var);
            }

            var = "";
            string s(1, expr[i]);
            if (expr[i] != '#')
            {
                tokens.push_back(s);
            }

            if(expr[i] == '(') {
                if(isalnum(last) || last == ')') return false;  // there cannot be a variable before '('.
                unmatched_parenthesis++;
            } else if(expr[i] == ')') {
                if(last == '*' || last == '/' || last == '+' || last == '-' || last == '(' || unmatched_parenthesis == 0) return false;
                unmatched_parenthesis--; 
            } else if(expr[i] == '*' || expr[i] == '/' || expr[i] == '+' || expr[i] == '-') {
                if(last == '(' || last == '*' || last == '/' || last == '+' || last == '-' ) return false;
            } else if (expr[i] == '#') {
                if(isalnum(last) || last == ')') return false;
                string str;
                lastChoose = true;
                while (expr[++i] != '#') 
                {
                    str.push_back(expr[i]);
                }
                tokens.push_back("#"+str+"#");
                last = ')';
            } else {
                
                // there shouldn't be characters in an expression apart from alphanumeric and "()+-*/".
                return false;
            }
        }
        if (lastChoose)
        {
            last = ')';
            lastChoose = false;
        }
        else
        {
            last = expr[i];
        }
        

    }

    if(!var.empty()) {
        variables.push_back(var);
        tokens.push_back(var);
    }
    // Last character shouldn't be an operator and there shouldn't be unmatched parenthesis left.
    if(unmatched_parenthesis > 0 || last == '(' || last == '*' || last == '/' || last == '+' || last == '-' ) return false;

    // If an operand is neither variable nor number, it is a syntax error.
    for(int i=0; i<(int)variables.size(); i++) {
        if(!validateVariable(variables[i]) && !validateNumber(variables[i])) return false;
    }

    for (auto v: variables)
    {
        if (validateVariable(v)) {varNames.push_back(v);}
    }

    return true;
}

// Replaces choose() functions in the expressions with temporary variables
bool Parser::replaceChoose(string& line) {


    int length = (int) line.size();
    int startingIndex = line.find("choose(");
    int endingIndex = -1;
    int left_parenthesis = 0;
    int noComma = 0;
    chooseFound = true;

    vector<string> expressions;

    
    int expr_start = startingIndex + 7;

    for(int i = startingIndex + 6; i < length; i++) {
        if(i==startingIndex + 6) continue; // do not take first "(" into account.

        if(line[i] == ',' && left_parenthesis == 0)  {
            noComma++;
            expressions.push_back(line.substr(expr_start, i - expr_start));
            expr_start = i + 1;
        }
        else if(line[i] == '(') left_parenthesis++;
        else if(line[i] == ')') {
            if(left_parenthesis == 0 && noComma == 3) {
                expressions.push_back(line.substr(expr_start, i - expr_start));
                expr_start = i + 1;
                endingIndex = i;
                break;              
            } else {
                left_parenthesis--;
                if(left_parenthesis < 0) return false;
            }
        }
        else if(noComma > 3) return false;
           
    }


    if(endingIndex == -1) return false;

    bool expressionValidate = true;


    vector<string> chooseOperands;
    // Send each parameter of choose() function to expression parsers
    for(int i=0; i<4; i++) {

        while(expressions[i].find("choose(") != string::npos) {
            if(!replaceChoose(expressions[i])) return false;
        }
        expressionValidate = expressionParser(expressions[i]);

        if (validateNumber(expressions[i])) {chooseOperands.push_back(expressions[i]);}
        else {chooseOperands.push_back("%t" + to_string(writer.tempVarCounter-1));}
        if(!expressionValidate) return false; // invalid expression
    }
    
    string saveTo = "%t"+to_string(writer.tempVarCounter++);
    writer.choose(saveTo, chooseOperands);
    line.replace(startingIndex, endingIndex - startingIndex + 1, "#"+saveTo+"#");


    return true;

    
}

/*
Main function of Parser object.
It iterates through the lines and tries to identify each line.
A line can be an if/while conditional, assignment statement, print(), closing curly bracket or empty line.
It keeps a lineCount variable to print out the index of the current line in case of a syntax error.
*/
void Parser::read(vector<string>& lines) {



    bool openBlock = false;
    this->lineCount = 0;
    string line;
    
    while(this->lineCount < lines.size()) {
        line = lines[this->lineCount];
        int length = (int)line.size();

        bool lastWasIf;

        if(line.find("{") != string::npos) {
            
            // IF or WHILE statements
           if(line.rfind("if", 0) == 0) {

                // Ok, this is an if statement
                if(line[length - 1] != '{' || line[length - 2] != ')' || line[2] != '(' || openBlock) {
                    syntaxError();
                    return;
                }

                openBlock = true;
                while(line.find("choose(") != string::npos) {
                    if(!replaceChoose(line)) {
                        syntaxError();
                        return;
                    }
                }

                string expression = line.substr(3, line.size() - 5);

                // We know that statement is something like this -->   if(***){
                // We don't know the expression inside the parenthesis yet.

                // HERE --> Parse the expression
                // Print "IF" here.
                lastWasIf = true;
                string nextBody = "regbody" + to_string(writer.regCounter++);
                string conditionBody = "ifcond" + to_string(++writer.ifCounter);
                writer.brUnconditional(conditionBody);
                writer.writeLine(conditionBody + ":");

                if(!expressionParser(expression)) {
                    syntaxError();
                    return;
                }

                string ifBody = "ifbody" + to_string(writer.ifCounter);
                string saveTo = "%t"+to_string(writer.tempVarCounter++);
                string compareWith;
                if (validateNumber(expression)) {compareWith = expression;}
                else {compareWith = "%t"+to_string(writer.tempVarCounter-2);}
                writer.arithmetic(saveTo, "icmp ne", compareWith, "0");
                writer.brConditional(saveTo, ifBody, nextBody);

                writer.writeLine(ifBody + ":");

            } else if (line.rfind("while", 0) == 0) {
                // Ok, this is a while statement

                if(line[length - 1] != '{' || line[length - 2] != ')' || line[5] != '(' || openBlock) {
                    syntaxError();
                    return;
                }

                openBlock = true;
                while(line.find("choose(") != string::npos) {
                    if(!replaceChoose(line)) {
                        syntaxError();
                        return;
                    }
                }
                string expression = line.substr(6, line.size()- 8);

                // We know that statement is something like this -->  while(***){
                // We don't know the expression inside the parenthesis yet.

                // HERE --> Parse the expression
                lastWasIf = false;
                string nextBody = "regbody" + to_string(writer.regCounter++);
                string conditionBody = "whcond" + to_string(++writer.whileCounter);
                writer.brUnconditional(conditionBody);
                writer.writeLine(conditionBody + ":");

                if(!expressionParser(expression)) {
                    syntaxError();
                    return;
                }
                
                string whBody = "whbody" + to_string(writer.whileCounter);
                string saveTo = "%t"+to_string(writer.tempVarCounter++);
                string compareWith;
                if (validateNumber(expression)) {compareWith = expression;}
                else {compareWith = "%t"+to_string(writer.tempVarCounter-2);}
                writer.arithmetic(saveTo, "icmp ne", compareWith, "0");
                writer.brConditional(saveTo, whBody, nextBody);

                writer.writeLine(whBody + ":");

            } else {
                // We said, it is either IF or WHILE statement. If not both, syntax error!
                syntaxError();
                return;
            }
        }

        else if(line.find("print(") != string::npos) {
            /* This is definitely print statement.
            We check it with "print(", because there can be a variable whose name includes "print", but not "(".
            print() cannot be an expression. So it cannot be used in an assignment statement, function, if or while statement.
            */

            if(line.rfind("print", 0) != 0 ||  line[length - 1] != ')' || line[5] != '(') {
                syntaxError();
                return;
            }

            // We know that statement is something like this --> print(**)
            // We don't know the expression inside the prenthesis yet.

            while(line.find("choose(") != string::npos) {
                if(!replaceChoose(line)) {
                    syntaxError();
                    return;
                }
            }

            string expression = line.substr(6, line.size()- 7);

            if(!expressionParser(expression)) {
                syntaxError();
                return;
            }

            // Now, it is time to print out the variable
            string toPrint;
            if (validateNumber(expression)) {toPrint = expression;}
            else {toPrint = "%t" + to_string(writer.tempVarCounter-1);}
            writer.print(toPrint);
        } 


        else if (line.find("=") != string::npos) {

            // No if statement, no while statement, no choose() function or print() function.
            while(line.find("choose(") != string::npos) {
                if(!replaceChoose(line)) {
                    syntaxError();
                    return;
                }
            }

            if(!assignmentParser(line)) {
                syntaxError();
                return;
            }

        } else if(line.find("}") != string::npos) {

            if(line.size() > 1 || !openBlock) {
                syntaxError();
                return;
            }
            else openBlock = false;

            string newBody;
            if (lastWasIf)
            {
                newBody = "regbody" + to_string(writer.regCounter-1);
                writer.brUnconditional(newBody);
                writer.writeLine(newBody + ":");
            }
            else 
            {
                writer.brUnconditional("whcond" + to_string(writer.whileCounter));
                writer.writeLine("regbody" + to_string(writer.regCounter-1) + ":");
            }
            

        } else {
            /*
            It is not a print, if or while statement.
            It is not an assignment statement.
            Syntax error

            If it is not an empty line, syntax error.
            */
            if(line.size() != 0) {
                syntaxError();
                return;
            }
        }
        this->lineCount++;
    }

    // Unmatched parenthesis

    if(openBlock) {
        this->lineCount--;
        syntaxError();
        return;
    }

    writer.writeToFile("mylang2ir", variableSet);
}