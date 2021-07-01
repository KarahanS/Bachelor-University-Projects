#include "Writer.h"
#include "Parser.h"

#include <vector>
#include <algorithm>

using namespace std;


int main(int argc, char* argv[])
{
	// argv[0] is always reserved for the name of the program itself.
	string infile_name =  argv[1];

	// <fstream> is included under the Writer.h file.
	ifstream infile;

	infile.open(infile_name);

	vector<string> lines;
	string line;

	// Before sending our files to the parser, let's get rid of comments and whitespaces.
	while(getline(infile, line)) {

		line.erase(std::remove_if(line.begin(), line.end(), ::isspace), line.end());

        if(line.find("#") != string::npos) {
            int index = line.find("#");
            line.replace(index, (int)line.size(), "");
        }

        lines.push_back(line);
 
	}

	// Create a parser object
	Parser parser(argv[1]);
	// Send the lines to the parser
	parser.read(lines);



    infile.close();
    return 0;
}