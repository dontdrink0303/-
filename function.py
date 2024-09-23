import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
if rootPath not in sys.path:
    sys.path.append(rootPath)

# 创建所有一员运算符列表
unary_operator = ['∀', '∃', '¬']

# 创建所有二元运算符列表
binary_operator = ['→', '∨', '∧', '↔', '≡']

# 创建优先级的运算符列表，规定左边的大于右边的
operations = ['∀', '∃', '¬', '∧', '∨', '→', '↔', '≡']


class Queue(object):
    '''python模拟队列'''
    __slots__ = '__items'

    # 初始化队列
    def __init__(self):
        self.__items = []

    # 入队
    def push(self, item):
        self.__items.append(item)

    # 出队
    def put(self):
        return self.__items.pop(0)

    # 判断队列是否为空
    def is_empty(self):
        return self.__items == []

    # 获取队列长度
    def size(self):
        return len(self.__items)


class Stack(object):
    '''列表模拟栈'''
    __slots__ = '__items'

    # 初始化栈为空列表
    def __init__(self):
        self.__items = []

    # 判断栈是否为空，返回布尔类型
    def is_empty(self):
        return self.__items == []

    # 返回栈顶元素，仍保留在栈顶
    def peek(self):
        return self.__items[-1]

    # 把新元素压入栈
    def push(self, item):
        self.__items.append(item)

    # 取出栈顶元素并在栈顶删除
    def pop(self):
        return self.__items.pop()

    # 返回栈的大小
    def size(self):
        return len(self.__items)


def division(furmula):
    '''将字符串公式切割为单位符号列表'''
    # 创建一个列表用来存储切割后的单位符号
    list1 = []
    str1 = ''
    label = 0

    # 依次遍历字符串公式
    for character in furmula:
        # 如果当前字符为操作符则直接append操作
        if character in operations and label != 1:
            list1.append(character)
            label = 0
        else:
            # 如果当前字符为大写字母，则改变标签并将当前字符加入字符串str1中
            if str.isupper(character) and label == 0:
                if len(str1) == 1:
                    list1.append(str1)
                    str1 = ''
                label = 1
                str1 += character
            # 如果当前字符为运算符且标签为1时，将当前字符串和当前字符先后加入列表，lebel置0，str1置空
            elif character in operations and label == 1:
                list1.append(str1)
                str1 = ''
                list1.append(character)
                label = 0
            # 如果标签为1且当前字符为‘）’时，将当前字符加入字符串str1后再将改变标签
            elif label == 1 and character == ')':
                list1.append(str1)
                str1 = ''
                label = 0
                list1.append(character)
            # 如果标签大于1且当前字符为’）’，当前字符加入str1中再入列表，label变为0，str1置空
            elif label > 1 and character == ')':
                str1 += character
                list1.append(str1)
                label = 0
                str1 = ''
            # 如果标签不为0，则将当前字符加入str1中
            elif label != 0:
                str1 += character
                label += 1
            # 如果当前标签为0，则将当前字符直接append操作
            elif label == 0:
                list1.append(character)
    if str1:
        list1.append(str1)
    # 返回列表
    return list1


def is_verb(furmula: str):
    '''判断是否与谓词有关'''
    for i in division(furmula):
        if len(i) > 1:
            return True
    return False


def change_To_PE(furmula):
    '''传进来的公式包括一阶逻辑推理公式和一阶谓语逻辑推理公式'''
    '''将公式转成后缀表达式'''
    posExpression = Queue()
    operators = Stack()
    # 将公式符号分离成列表
    furmula = division(furmula)
    # 依次遍历符号列表
    for character in furmula:
        ##print(character)
        # 当前字符为大写字母 或者长度大于1（A(X)）时直接入队
        if str.isupper(character) or len(character) > 1:
            posExpression.push(character)
        else:
            # 当前运算符栈为空时，当前字符直接入栈
            if operators.is_empty():
                operators.push(character)
            # 当前字符为小写字母，直接入栈
            elif str.islower(character):
                operators.push(character)
            elif character == '(':
                operators.push(character)
            elif character == ')':
                while True:
                    top = operators.pop()
                    if top == '(':
                        break
                    else:
                        posExpression.push(top)
            else:
                # 如果当前运算符栈栈顶为左括号，当前字符直接入栈
                if operators.peek() == '(':
                    operators.push(character)
                else:
                    if not operators.is_empty():
                        if str.islower(operators.peek()):
                            pass
                        # 如果当前字符优先级小于运算符栈栈顶字符的优先级，运算符栈顶字符出栈入队，当前字符入栈
                        else:
                            while True:
                                if operators.is_empty() or operators.peek() == '(':
                                    break
                                elif operations.index(operators.peek()) < operations.index(character):
                                    top = operators.pop()
                                    posExpression.push(top)
                                elif operations.index(operators.peek()) >= operations.index(character):
                                    break
                            operators.push(character)
    # 将运算符栈的剩余的字符依次取出入队
    while operators.is_empty() == False:
        top = operators.pop()
        posExpression.push(top)

    return posExpression


class TreeNode():
    '''树节点'''

    def __init__(self, item, lchild=None, rchild=None):
        self.elem = item
        self.lchild = None
        self.rchild = None

    def __init__(self, item, lchild=None, rchild=None):
        self.elem = item
        self.lchild = lchild
        self.rchild = rchild


def BTree(Queue1: Queue):
    '''实现将公式转为二叉树存储'''
    stack1 = Stack()
    while Queue1.is_empty() == False:
        # 取出队头并创建节点
        element = Queue1.put()
        pnode = TreeNode(element)
        # 如果当前元素不是运算符和小写字母，则直接入栈
        if len(element) > 1 or str.isupper(element):
            stack1.push(pnode)
        # 如果当前元素是一元运算符，则从stack1中取出一个元素，当前元素转成树节点形式，且出栈元素为当前元素的右子树，最后将节点重新入栈
        elif element in unary_operator or str.islower(element):
            top = stack1.pop()
            pnode.rchild = top
            stack1.push(pnode)
        # 如果当前元素是二元运算符，则从stack2中取出两个元素，元素转成树节点形式，且第一个出栈元素为当前元素的右子树，第二个出栈的元素为当前元素的左子树，最后将节点重新入栈
        elif element in binary_operator:
            top1 = stack1.pop()
            top2 = stack1.pop()
            pnode.rchild = top1
            pnode.lchild = top2
            stack1.push(pnode)
    res = stack1.pop()
    return res


def inOrderTraverse(root: TreeNode):
    '''中序遍历'''
    res = ''

    def helper(root):
        nonlocal res
        if not root:
            return None
        # 递归遍历左子树，根，右子树
        helper(root.lchild)
        res += root.elem
        helper(root.rchild)

    helper(root)
    return res


def maxDepth(root: TreeNode) -> int:
    '''返回树的高度'''
    if not root:
        return 0
    else:
        l = 1 + maxDepth(root.lchild)
        r = 1 + maxDepth(root.rchild)
        return max(l, r)


def root(str1: str) -> str:
    '''返回二叉树根节点元素'''
    tree = BTree(change_To_PE(str1))
    return tree.elem
