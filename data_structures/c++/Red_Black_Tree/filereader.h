#pragma once

#include <fstream>
#include <map>
#include <iostream>
#include "rbtree.h"

using namespace std;

/** ....::::Class FileReader::::....
This class was implemnted to fill specific requirements of the lab1
project for my data structores/algorithms course.
FileReader has functionality to store, count, and output all of the
words contained in a txt document. The output is formatted specifically
for this lab.
**/
class FileReader
{
    public:
    /** FileReader(string fn) :: Constructor function
    This is the constructor for the FileReader class. 
    
    @param fn This parameter will be the file that FileReader will be loading
    into an ifstream.
    **/
        FileReader(string fn);
    /** ~FileReader() :: Destructor
    This is the destructor for the FileReader class. Since I didn't do any of
    the work dynamically its only function is to maintain good OO design
    **/
        ~FileReader();
    /** setFileName(string fn) :: Mutator Function
    This function was implimented to maintain good OO design.

    @param fn The file name that member varialbe fileName will be
    set to.
    **/
        void setFileName(string fn);
    /** getFileName() :: Accessor function
    This function was implemented to maintain good OO design.

    @return returns the string value of the private member
    variable fileName
    **/
        string getFileName();
    /** readToMap() :: Utility function of FileReader
    This function will read all the words stored in the file passed by
    constructor. After reading each word in it then stores it as the
    key to a map(private member variable contents) element of type string.
    If the element already exists  it will increment the integer value
    rather than insert a new element.
    This function makes use of the private member function parse()
    **/
    RBTree getContents();
        void readToTree();
    /** printTree() :: Utility function of FileReader
    This function will print all of the words stored in the map contents.
    It will first print the key name followed by a ' ' and the value stored
    at that element (the amount of time that word was found in the txt file.
    It will then output a newline character unless the final value was just
    printed.
    **/
        void printTree();

    private:
    /** fileName :: Private member variable of type string
    This is where the name of the file being read will be stored.
    **/
        string fileName;
    /** parse(string input) :: private member function
    This function will make sure all characters in the string passed in
    are alpha numeric. It also converts all of the character to lower case
    letters. This function relies on the isalphanum and tolower functions.
    
    @param input will be the string that is being parsed.
    @return the returned value is the parsed version of the paremter
    input.
    **/
        string parse(string input);
    /** contents :: private member variable of FileReader
    This is the map in which FileReader stores it's data.
    **/
        RBTree contents;
};

