#include "filereader.h"


FileReader::FileReader(string fn)//Constructor
{
        fileName = fn;

}
FileReader::~FileReader()//destructor
{

}

void FileReader::setFileName(string fn)//mutator
{
        fileName = fn;
}

RBTree FileReader::getContents()
{
    return contents;
}
string FileReader::getFileName()//accessor
{
        return fileName;
}

void FileReader::readToTree()
{
        ifstream fin(fileName.c_str());
        while(!fin.eof()) //loop until end of file is reached
        {
                string iWord = "";//initial word
                string fWord = "";//final word
                fin >> iWord;
                if(iWord != "")
                {
                        fWord = parse(iWord);
                        if(fWord != "")
                        contents.insert(fWord);
                }
        }
}
void FileReader::printTree()
{
        contents.print();
}

string FileReader::parse(string input)
{
        string out = "";//will be return value


        int loopFor = input.size();//checking how many times to loop
        for(int i = 0; i < loopFor; i++)
        {
                if(isalnum(input[0]) )//only alnum chars will be added to out
                {
                        out += tolower(input[0]);//calling tolower +  addinchar to out                       
                        input.erase(input.begin());//removing char from input
                }
                else
                {
                        input.erase(input.begin());//erasing non alnum
                }

        }


        return out;//returning string parsed to lab1 specific format

}

