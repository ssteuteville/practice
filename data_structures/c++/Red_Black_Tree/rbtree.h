#pragma once
#include <iostream>
using namespace std;
/** RBNode :: Data wrapper class for RBTree class
    This class is used as the nodes in a red black tree I implemented.
    The class was designed specifically for my RBTree class.
    It uses a pair as its data type so it resembles an STL map.
    red nodes are represented by the char 'r'
    black nodes are represtented by the char 'b'
**/
class RBNode
{
        public:
/** RBNode() :: Default Constructor for RBNode class.
Initial color = red
left, right and right pointers point to NIL.
**/
                RBNode();
/** RBNode(pair<string, int> d) :: Overloaded Constructor for RBNode class.
same as default construct except:
data = d.
**/
                RBNode(pair<string, int> d);
/** ~RBNode() :: Destructor for RBNode class
This functions cleans up all dynamic memory associated with RBNodes.
**/
                ~RBNode();
/** setData(pair<string, int d) :: Mutator for private member variable data.
This sets data = d.
**/
                void setData(pair<string, int> d);
/** setLeft(RBNode* target) :: Mutator for private member variable left.
Sets left = target.
**/
                void setLeft(RBNode* target);
/**setRight(RBNode* target) :: Mutator for private member variable right.
Sets right = target.
**/
                void setRight(RBNode* target);
/**setParent(RbNode* target) :: Mutator for private member variable parent.
Sets parent = target.
**/
                void setParent(RBNode* target);
/** getData() const :: Accessor for private member variable data.
@return a constant version of data. (for when data doesnt need to be changed)
**/
                pair<string, int> getData() const;
/** getData() :: Accessor for private member variable data.
@return a referense to the memory location pointed to by data.
(can be manipulated)
**/
                pair<string, int>& getData();
/** getRight() and getRight() const :: Accessors for private member variable right. **/
                RBNode*& getRight();
                RBNode* getRight() const;
/** getLeft() and getLeft() const :: Accessors for private member variable left. **/                
                RBNode*& getLeft();
                RBNode* getLeft() const;
/** getParent() and getParent() const :: Accessors for private member variable right. **/                
                RBNode*& getParent();
                RBNode* getParent() const;
/** getColor() :: Accesor for private member variable color **/
                char getColor();
/** setColor(char c) :: Mutator for private member variable color
Sets color = c.
Makes sure only 'b' or 'r' can be set.
outputs an error other wise.
**/
                void setColor(char c);
        private:
                RBNode* left;
                RBNode* right;
                RBNode* parent;
                char color;
                pair<string, int> data;
};

class RBTree
{
        public:
/** print() :: Function prints the tree in order. Formated for Adam's 311 class.
**/
                void print();
/** insert(strind d) :: insertion function for RBTree class.
This function inserts a new piece of data into the tree. 
It also calls the function insertionFixUp to maintain RBT properties.
Specially designed to increment a nodes second piece of data rather than
insert duplicates.

@param d the string being inserted into the tree.
**/
                void insert(string d);
/** getRoot() and getRoot() const :: Accessor functions for private member variable root **/
                RBNode*& getRoot();
                RBNode* getRoot() const;
/** RBTree() :: default constructor for RBTree
Instantiates NIL pointer and root pointer.
**/
                RBTree();
/** find(string target) :: Function queries the tree for a specific string (target). **/
                RBNode* find(string target);
/** leftRotate(RBNode* target) :: Tree left rotation function.
Rotates a sub tree of the RBTree about the node target.
**/
                void leftRotate(RBNode* target);
/** rightRotate(RBNode* target) :: Tree right rotation function.
Rotates a sub tree of the RBTtree about the node target.
**/
                void rightRotate(RBNode* target);
/** treeHeight() :: Find the height of the tree
This function recurses down the left side of the tree while counting black nodes.
@return the black height of the RBTree
used for testing.
Their is a private version of this function that requires extra parametes. (for recursion)
**/
                int treeHeight();
                // int checkTree();
        private:
/**
All private functions are helper functions that are
described in the function they are called from's documentations.**/
                RBNode* root;
                RBNode* NIL;
                int treeHeight(RBNode* treeRoot, int blackCount);
                void insertionFixUp(RBNode*& newNode);
                int count;
                void print(RBNode* treeRoot);
                // int checkTree(RBNode* treeRoot, int blackCount);
};
