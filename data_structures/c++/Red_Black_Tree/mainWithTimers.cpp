#include "wordcounts.h"
#include "filereader.h"
#include <iostream>
#include <time.h>
#include <stdlib.h>

using namespace std;
timespec diff(timespec start, timespec end);

int main(int argc, char** argv)
{
    srand(time(NULL));
    timespec time1, time2;
	clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &time1);
    string file_name = argv[1];
    FileReader fReader(file_name);
    fReader.readToTree();
    fReader.printTree();
    	clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &time2);

   	cout << diff(time1, time2).tv_sec << ":" << diff(time1, time2).tv_nsec;
   	cout << endl;

    //cout << endl << "Height of tree: " << fReader.getContents().checkTree() << endl;
    return 0;
}

timespec diff(timespec start, timespec end)
{
    timespec temp;
    if((end.tv_nsec-start.tv_nsec)<0)
    {
        temp.tv_sec = end.tv_sec-start.tv_sec-1;
        temp.tv_nsec = 1000000000+end.tv_nsec-start.tv_nsec;
    }
    else
    {
        temp.tv_sec = end.tv_sec-start.tv_sec;
        temp.tv_nsec = end.tv_nsec-start.tv_nsec;
    }
    return temp;
}
