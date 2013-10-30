#include "filereader.h"
#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
    string file_name = "";
    if(argc >1)
        file_name = argv[1];
    else
        file_name = "tests/input1.txt";
    FileReader fReader(file_name);
    fReader.readToTree();
    fReader.printTree();
    return 0;
}
