#include "rbtree.h"

using namespace std;

//Start of RBNode Implementation  
RBNode::RBNode()
{
        left = NULL;
        right = NULL;
        //data = NULL;
        parent = NULL;
        color = 'r';
}

RBNode::RBNode(pair<string, int> d)
{
        left = NULL;
        right = NULL;
        parent = NULL;
        data = d;
        color = 'r';
}

RBNode::~RBNode()
{
        left = NULL;
        right = NULL;
        parent = NULL;
}

void  RBNode::setColor(char c)
{
        if(c == 'r' || c == 'b')
                color = c;
        else
                cerr << "ERROR NODE CAN BE BLACK(b) OR RED(r)" << endl;
}

char  RBNode::getColor()
{
        return color;
}

void RBNode::setData(pair<string, int> d)
{
        data = d;
}

void RBNode::setLeft(RBNode* target)
{
        left = target;
}

void RBNode::setRight(RBNode* target)
{
        right = target;
}

void RBNode::setParent(RBNode* target)
{
        parent = target;
}

pair<string, int> RBNode::getData() const
{
        return data;
}

pair<string, int>& RBNode::getData()
{
        return data;
}

RBNode*& RBNode::getRight()
{
        return right;
}

RBNode* RBNode::getRight() const
{
        return right;
}

RBNode*& RBNode::getLeft() 
{
        return left;
}

RBNode* RBNode::getLeft() const
{
        return left;
}

RBNode*& RBNode::getParent()
{
        return parent;
}

RBNode* RBNode::getParent() const
{
        return parent;
}
//End of RBNode implementation

//Start of RBTree Implementation

RBTree::RBTree()
{
        NIL = new RBNode();
        NIL->setColor('b');
        root = NIL;
}
void RBTree::insert(string d)
{
        pair<string, int> z(d, 1);
        RBNode* parent =  NIL; //y
        RBNode* iter = root; //x

        while(iter != NIL)
        {
                parent = iter;
                if(parent->getData().first > z.first)
                        iter = iter->getLeft();
                else if(parent->getData().first < z.first) 
                        iter = iter->getRight();
                else
                {
                        parent->getData().second++;
                        return;
                }
        }

        if(parent == NIL)
        {
                root = new RBNode(z);
                root->setParent(NIL);
                root->setLeft(NIL);
                root->setRight(NIL);
                iter = root;
        }
        else if(parent->getData().first > z.first)
        {
                parent->setLeft(new RBNode(z));
                iter = parent->getLeft();
                iter->setParent(parent);
                iter->setLeft(NIL);
                iter->setRight(NIL);
        }
        else
        {
                parent->setRight(new RBNode(z));
                iter =  parent->getRight();
                iter->setParent(parent);
                iter->setLeft(NIL);
                iter->setRight(NIL);
        }
        insertionFixUp(iter);
}

void RBTree::insertionFixUp(RBNode*& newNode)
{
        RBNode* uncle = NIL;
        while(newNode->getParent()->getColor() == 'r')
        {
                if(newNode->getParent() == newNode->getParent()->getParent()->getLeft())
                {
                        uncle = newNode->getParent()->getParent()->getRight();
                        if(uncle->getColor() == 'r')
                        {
                                newNode->getParent()->setColor('b');
                                uncle->setColor('b');
                                newNode->getParent()->getParent()->setColor('r');
                                newNode = newNode->getParent()->getParent();
                        }
                        else
                        {
                                if(newNode == newNode->getParent()->getRight())
                                {
                                        newNode = newNode->getParent();
                                        leftRotate(newNode);
                                }
                                newNode->getParent()->setColor('b');
                                newNode->getParent()->getParent()->setColor('r');
                                rightRotate(newNode->getParent()->getParent());
                        }

                }
                else
                {
                        uncle = newNode->getParent()->getParent()->getLeft();
                        if(uncle->getColor() == 'r')
                        {
                                newNode->getParent()->setColor('b');
                                uncle->setColor('b');
                                newNode->getParent()->getParent()->setColor('r');
                                newNode = newNode->getParent()->getParent();
                        }
                        else
                        {
                                if(newNode == newNode->getParent()->getLeft())
                                {
                                        newNode = newNode->getParent();
                                        rightRotate(newNode);
                                }
                                newNode->getParent()->setColor('b');
                                newNode->getParent()->getParent()->setColor('r');
                                leftRotate(newNode->getParent()->getParent());
                        }
                }
                // root->setColor('b');
        }
        root->setColor('b');		
}

RBNode*& RBTree::getRoot()
{
        return root;
}

RBNode* RBTree::getRoot() const
{
        return root;
}

void RBTree::print()
{
        if(root == NIL)
                cout << "Tree is empty." << endl;
        else
        {
                print(root->getLeft());
                cout << root->getData().first << " "
                        << root->getData().second << endl;
                print(root->getRight());
        }
}

void RBTree::print(RBNode* treeRoot)
{
        if(treeRoot != NIL)
        {
                print(treeRoot->getLeft());
                cout << treeRoot->getData().first << " "
                        << treeRoot->getData().second << endl;
                print(treeRoot->getRight());
        }
}
RBNode* RBTree::find(string target)
{
        RBNode* iter = root;
        if(root == NIL)
        {
                cout << "the tree is empty" << endl;
                return NIL;
        }
        else
        {
                while(iter != NIL && iter->getData().first != target)
                {
                        if(iter->getData().first > target)
                                iter = iter->getLeft();
                        else
                                iter = iter->getRight();
                }
                return iter;
        }
}

void RBTree::leftRotate(RBNode* target)
{

        RBNode* y = target->getRight();
        target->setRight(y->getLeft());
        if(y->getRight() != NIL)
                y->getLeft()->setParent(target);
        y->setParent(target->getParent());
        if(target->getParent() == NIL)
                root = y;
        else if(target == target->getParent()->getLeft())
                target->getParent()->setLeft(y);
        else
                target->getParent()->setRight(y);
        y->setLeft(target);
        target->setParent(y);
}

void RBTree::rightRotate(RBNode* target)
{

        RBNode* y = target->getLeft();
        target->setLeft(y->getRight());
        if(y->getRight()!= NIL)
                y->getRight()->setParent(target);
        y->setParent(target->getParent());
        if(target->getParent()== NIL)
                root = y;
        else if(target == target->getParent()->getRight())
                target->getParent()->setRight(y);
        else
                target->getParent()->setLeft(y);
        y->setRight(target);
        target->setParent(y);
}

int RBTree::treeHeight()
{
        if(root != NIL)
                return  treeHeight(root, 1);
        else
                return -1;
}

int RBTree::treeHeight(RBNode* treeRoot, int blackCount)
{
        if(treeRoot->getLeft() != NIL)
        {
                if(treeRoot->getColor() == 'r')
                        return treeHeight(treeRoot->getLeft(), blackCount);
                else
                        return treeHeight(treeRoot->getLeft(), ++blackCount);
        }
        else
                return blackCount;

}

/*int RBTree::checkTree()
  {
  if(root != NIL)
  return checkTree(root, 0);
  else
  return -1;
  }

  int RBTree::checkTree(RBNode* treeRoot, int blackCount)
  {
  int left = 0;
  int right = 0;

  if(treeRoot->getColor() == 'r')
  {
  if(treeRoot->getLeft() == NIL)
  left = blackCount;
  else
  left = checkTree(treeRoot->getLeft(), blackCount);
  if(treeRoot->getRight() == NIL)
  right = blackCount;
  else
  right = checkTree(treeRoot->getRight(), blackCount);
  }
  else
  {
  if(treeRoot->getLeft() == NIL)
  left = ++blackCount;
  else
  left = checkTree(treeRoot->getLeft(),++blackCount);

  if(treeRoot->getRight() == NIL)
  right = ++blackCount;
  else
  right = checkTree(treeRoot->getRight(), ++blackCount);
  }

  if( left == right)
  return left;
  else
  return -1;
  }*/
