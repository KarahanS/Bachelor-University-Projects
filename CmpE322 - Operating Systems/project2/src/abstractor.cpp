#include <iostream> // cout
#include <fstream> // input - output
#include <vector>
#include <sstream>  // for stringstream objects
#include <string> 
#include <unordered_set> // for Jaccard Similarity metric
#include <iomanip>  // setprecision
#include <pthread.h>  // threads
#include <algorithm>  // sort
#include <unistd.h>

/* 
@author = Karahan

Main idea of the project is to process the given abstracts by equally sharing the amount work 
to be done among the threads.
Each thread runs a while loop which terminates until all of the abstract files are processed. 
When a thread completes processing, it looks for an available abstract file to process, therefore
this approach leads to the equal share of the work naturally.

Run the code using relative paths of the input/output files (since they are stored in the src folder).
*/

// A struct to keep record of each result
struct result {
    std::string file;
    float score;
    std::string summary;
};
bool custom_sort(result const& lhs, result const& rhs) {
    return lhs.score > rhs.score;
}


/*
Print out the fields of the result easily by overloading the operator << 
*/
std::ostream& operator<<(std::ostream& stream, const result& result) {
    return stream << "File: " << result.file << std::endl
              << "Score: " << result.score << std::endl
              << "Summary: " << result.summary;
}


// GLOBAL VARIABLES
std::vector<result> results;
std::vector<std::string> abstractFiles;
std::string keywords;
int idx = 0;
int idy = 0;
// create a mutex to avoid race conditions
pthread_mutex_t mutex;
std::ofstream outfile;


/*
Jaccard tokenizes the given strings and constructs union-intersection sets.
Then returns the Jaccard similarity by dividing the length of intersection set
to the length of union set.
*/
void* Jaccard(void* arg) {
    std::stringstream tokenizer(keywords);
    std::unordered_set<std::string> set1;
    // tokenize
    std::string token;
    while(tokenizer >> token) set1.insert(token);

    std::string text = keywords;
    char letter = -1;
    while(true) {
        /* Lock the mutex and read from the shared variable, then modify the shared counter */
        pthread_mutex_lock(&mutex);
        if(letter == -1) {
            letter = 'A' + idx;
            idx++;
        }
        bool cond = (idy < abstractFiles.size());
        std::string file;
        if(cond) {
            file = abstractFiles[idy];
            idy++;
            outfile << "Thread " << letter << " is calculating " << file << "\n";
        }
        pthread_mutex_unlock(&mutex);

        if(!cond) break;

        // put the tokens (words) into sets
        std::unordered_set<std::string> set2;
        std::unordered_set<std::string> Intersection;
        std::unordered_set<std::string> Union;

        for(auto& st: set1) Union.insert(st);

        std::ifstream infile;
        infile.open("../abstracts/" + file);  // path = ../abstracts/file
        /*
        Keep the record of words for similarity analysis and sentences for summarization.
        */
        std::vector<std::string> sentences;

        std::string word;
        std::string sentence;
        /*
        Read all the strings from the file, construct sentences when encountered with dot and add all words to the vector.
        */

        bool inSentence = false;
        while(infile >> word) {
            if(word == ".") 
            {
                set2.insert(word);
                Union.insert(word);
                sentence += word + " ";
                if(inSentence) sentences.push_back(sentence);
                sentence.clear();  // O(1)
                inSentence = false;
            }
            else if(word == "\n") {}
            else 
            {
                /* Check if one of the keywords matches with the found word */
                if(!inSentence) // No need to check if we have already found a match in the sentence.
                {
                std::unordered_set<std::string>::const_iterator found = set1.find(word);  // O(1) - unordered set
                if(found != set1.end()) inSentence = true;
                }

                set2.insert(word);
                Union.insert(word);
                word += " ";
                sentence += word;  // append word to the sentence - O(1) mutable strings
            }
        }

        /* TO DO 
        First calculate the Jaccard similarity between abstractWords and given text.
        Then find the sentences with at least one word from the given query to summarize the abstract.
        */
        // construct the intersection set
        for(auto& st: set1) {
            std::unordered_set<std::string>::const_iterator found = set2.find(st);
            if(found != set2.end()) Intersection.insert(st);
        }
    
        /*
        for(auto& c: set1) std::cout << c << std::endl;
        for(auto& c: set2) std::cout << c << std::endl;
        std::cout << " ---- " << std::endl;
        for(auto& c: Intersection) std::cout << c << std::endl;
        std::cout << " ---- " << std::endl;
        for(auto& c: Union) std::cout << c << std::endl;
        */

        float score = (float)Intersection.size() / (float)Union.size();

        /*
        Create a result struct and record the results of the scan. 
        */
    
        result Result;
        Result.file = file;
        Result.score = score;
    
        std::string summ;
        for(auto& c: sentences) {
            summ += c;
        }
        Result.summary = summ;

    
        // Writing to a shared variable requires using a mutex
        pthread_mutex_lock(&mutex);
        results.push_back(Result);
        pthread_mutex_unlock(&mutex);

        infile.close();
    
        }

    return NULL;
}



int main(int argc, char const *argv[]) {
    /* Input file and output file must be provided as command line arguments. */
	if (argc < 3) {
		printf ("usage: %s input_file_name.txt output_file_name.txt\n", argv[0]);
		exit (1);
	}
    std::string inputFile = argv[1];
	std::string outputFile = argv[2];

    std::ifstream infile;
    infile.open(inputFile);
    outfile.open(outputFile);

    outfile<< std::fixed << std::setprecision(4);

    /* For the consistency, input file will be read line by line */
    std::string line;
    int T, A, N;
    std::getline(infile, line);
    
    /* Parse the first line into integers to get T, A and N. */
    std::stringstream stream(line);
    std::string st;
    stream >> st;
    T = std::stoi(st); // number of threads (other than the main thread)
    stream >> st; 
    A = std::stoi(st);  // number of abstract files to be scanned
    stream >> st;
    N = std::stoi(st);  // number of abstracts that will be summarized

    // Each thread will inspect T/A number of abstract files.
    
    keywords;
    std::getline(infile, keywords);         // words
    //std::vector<std::string> abstractFiles; // abstract files

    for(int i=1; i<=A; i++) {
        std::getline(infile, line);
        abstractFiles.push_back(line);
    }
    
    
    std::vector<pthread_t> threads;
    pthread_mutex_init(&mutex, NULL);


    // create threads
    for(int i=0; i<T; i++) {
        pthread_t threadID;
        // error check
        if(pthread_create(&threadID, NULL, &Jaccard, NULL) != 0) {
            perror("Error occurred while creating the threads.");
            exit(1);          
        }
        threads.push_back(threadID);
    }

    // wait for threads to complete their work
    for(int i=0; i<T; i++) {
        // error check
        if(pthread_join(threads[i], NULL) != 0) {
            perror("Error occurred while waiting for threads to join.");
            exit(1);
        }
    }

    /*
    Sort the results using the custom_sort function and std::sort.
    */
    std::sort(results.begin(), results.end(), &(custom_sort));
    
    outfile << "###" << "\n";
    for(int i=0; i<N; i++) {
       outfile << "Result " << i+1 << ":" << "\n";
       outfile << results[i] << "\n";
       outfile << "###" << "\n";
    }
    // destroy the mutex
    pthread_mutex_destroy(&mutex);

    infile.close();
    return 0;
}