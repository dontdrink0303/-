import sys
import os
from tkinter.tix import Tree

from sklearn import tree
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
if rootPath not in sys.path:
    sys.path.append(rootPath)

from automation.function import *
from typing import Union

'''全局定义变量'''
# 规则简称和函数名的对应字典
formula={
    "Ref":"refParse",
    "∈":"refParse",
    "→+":"exportAdd",
    "∧-":"andDelete",
    "∨+":"perhapsAdd",
    "¬-":"notDelete",
    "¬+":"notAdd",
    "→-":"exportDelete",
    "∧+":"andAdd",
    "∨-":"perhapsDelete",
    "↔-":"sameDelete",
    "↔+":"sameAdd",
    "∀-":"universalDelete",
    "∀+":"universalAdd",
    "∃-":"existDelete",
    "∃+":"existAdd",
    "≡-":"equalDelete",
    "≡+":"equalAdd",
    "+":"addParse",  #必须放在后面遍历
    # 命题逻辑
    "假言推理":"modusPonens",
    "附加前提引入":"additionalPremise",
    "附加":"add",
    "化简":"simplify",
    "拒取式":"modusTollendoPonens",
    "假言三段论":"hypotheticalSyllogism",
    "析取三段论":"disjunctiveSyllogism",
    "构造性二难推理":"constructiveDilemma",
    "破坏性二难推理":"destructiveDilemma",
    "合取引入":"disjunctionIntroduction",
    "前提引入":"refParse",
}


'''定义通用函数'''
def conjunction(subconditions: list) -> bool:
    """只有所有子条件成立，该条件才能成立

    Args:
        subconditions (list): 子条件列表

    Returns:
        bool: 子条件列表是否满足特定条件
    """    
    if False not in subconditions:
        return True
    else:
        return False


def disjunction(subconditions: list) -> bool:
    """只有所有子条件都不成立，该条件才不成立

    Args:
        subconditions (list): 子条件列表

    Returns:
        bool: 子条件列表是否满足特定条件
    """    
    if True not in subconditions:
        return False
    else:
        return True


def include(element, obj) -> bool:
    """如果element包含在obj中,则该子条件成立

    Args:
        element (_type_): 待检验的被包含的对象
        obj (_type_): 待检验的包含element的对象
        element-obj对:符号-结论, 结论-前提, 前提-前提
    
    Type:
        一对一(One-to-One)
        一对多(One-to-Many)
        多对多(Many-to-Many)


    Returns:
        bool: 包含的结果
    """    
    traversal = []    # 遍历列表
    list_in = []  # 存放遍历结果的列表

    # 如果element不是列表（即一对X类型），则将类型转化为多对多
    for t in [element]:
        if isinstance(t, list) != True:
            if isinstance(t, TreeNode):
                traversal.append(inOrderTraverse(t))
            else:
                traversal.append(t)
        # 如果t是二叉树,则转化为str
        elif isinstance(t, TreeNode):
            traversal = inOrderTraverse(t)
        else:
            traversal = t
    
    if list(set([type(x) for x in obj]))[0] is TreeNode:
        obj[:] = list(map(lambda x:inOrderTraverse(x), obj)) 

    # 遍历element列表，逐个分析element元素是否包含在obj中
    for tra in traversal:
            if tra in obj:
                list_in.append(True)
            else:
                list_in.append(False)
    # 如果element列表全为True，则包含关系成立
    return conjunction(list_in)


def compare(obj1, obj2, obj3=None, mod='str', type=None) -> bool:
    """
    obj:比较对象，可以是str,list
    mod: 'set'指列表间的比较('str'指两个字符串的比较，可以转化为'list'型), 'len'指两个列表的长度的比较,'tree'指两个二叉树的比较
    return: 'set':布尔值； 'len'“:两个列表长度的差值
    type:(只有mod="len"才需要)">"前者大于后者则成立；"="两者相等则成立；"<"前者小于后者则成立
    """
    
    # 如果输入是"tree"的话，将"tree"转化为str,再将"list"转化为"set"进行比较
    if mod == 'tree':
        if obj3 != None:
            list1, list2, list3 = [], [], [] #初始化列表
            str1, str2, str3 = inOrderTraverse(obj1), inOrderTraverse(obj2), inOrderTraverse(obj3)
            list1.append(str1), list2.append(str2), list3.append(str3)  #将字符串导入列表  
            set1, set2, set3 = set(list1), set(list2), set(list3)   #将列表转化为集合(set)
            if set1 == set2 == set3:
                return True
            else:
                return False
        else:
            list1, list2 = [], [] #初始化列表
            str1, str2 = inOrderTraverse(obj1), inOrderTraverse(obj2)
            list1.append(str1), list2.append(str2)  #将字符串导入列表  
            set1, set2 = set(list1), set(list2)   #将列表转化为集合(set)
            if set1 == set2:
                return True
            else:
                return False


    # 如果输入是"str"的话，将"str"转化为"list",再将"list"转为"set"进行比较
    elif mod == 'str':
        if obj3 != None:
            # 三个列表间的比较
            list1, list2, list3 = [], [], [] #初始化列表
            list1.append(obj1), list2.append(obj2), list3.append(obj3)  #将字符串导入列表  
            set1, set2, set3 = set(list1), set(list2), set(list3)   #将列表转化为集合(set)
            if set1 == set2 == set3:
                return True
            else:
                return False

        else:
            # 两个列表间的比较
            list1, list2 = [], [] #初始化列表
            list1.append(obj1), list2.append(obj2)  #将字符串导入列表  
            set1, set2 = set(list1), set(list2)   #将列表转化为集合(set)
            if set1 == set2:
                return True
            else:
                return False

    # 集合间的比较
    elif mod == 'set':
        if obj3 != None:
            # 说明是三个列表间的比较
            if set(obj1) == set(obj2) == set(obj3):
                return True
            else:
                return False
        else:
            # 说明是两个列表间的比较
            if set(obj1) == set(obj2):
                return True
            else:
                return False

    # 列表长度的比较
    elif mod == 'len':
        difference = len(obj1)-len(obj2)
        if (type == ">" and difference > 0) or (type == '=' and difference == 0) or (type == "<" and difference < 0):
            return True
        else:
            return False


def inv(formula: str) -> str:
    """取反"""
    tree = to_tree(formula) 
    if compare("¬", tree.elem, mod="str"):
        return inOrderTraverse(to_tree(formula.strip("¬"))) #双重否定即肯定
    else:
        return inOrderTraverse(to_tree("¬(" + formula + ")"))



def feature_extract(formula: str) -> tuple:
    """特征提取"""
    formula = formula.replace("(", "").replace(")", "") #删去所有的括号
    for char in operations:
        '''遍历离散数学相关的符号'''
        if char in formula:
            '''如果符号在公式中，则去掉符号'''
            formula.replace(char, "")
    x, F = [], []
    for letter in formula:
        '''遍历公式中的字母'''
        if letter.islower():
            x.append(letter)    #小写字母代表个体变项符号
        elif letter.isupper():
            F.append(letter)    #大写字母代表谓词符号
    x = list(set(x))    #去重复后的个体变项符号列表
    F = list(set(F))    #去重复后的谓词符号列表
    if len(x) == 1 and len(F) == 1:
        '''例: A(x)'''
        return x[0], F[0]
    elif len(x) == 1 and len(F) != 1:
        '''例: A(x)→B(x)'''
        return x[0], F
    else:
        '''例: A(x)→B(y)'''
        return x, F


def get_rrchild(node: str) -> str:
    """返回右结点的右子树"""
    tree = BTree(change_To_PE(node))    #根节点
    rnode = tree.rchild #右结点
    rrchild = rnode.rchild  #右结点的右子树
    return inOrderTraverse(rrchild) #中序遍历的右结点的右子树

def translocation(node: str) -> str:
    '''假言易位'''
    tree = to_tree(node)    #根节点
    rchild_inv = inv(inOrderTraverse(tree.rchild))   #取反后的中序遍历的右子树
    lchild_inv = inv(inOrderTraverse(tree.lchild))   #取反后的中序遍历的左子树
    tree = inOrderTraverse(to_tree((rchild_inv + tree.elem + lchild_inv)))   #左右子树对调
    return tree

def idempotence(node: str, type: str = None, root:str = None) -> str:
    """幂等律

    Args:
        node (str): 待置换的式子
        type (_type_, optional): 置换的方向：从左到右(to_right)，从右到左(to_left). Defaults to None:str.
        root (_type_, optional): 从左到右置换所需的根节点. Defaults to None:str.

    Returns:
        str: 置换后的式子
    """    
    tree = to_tree(node)
    if type == "to_right":
        print(inOrderTraverse(tree.lchild))
        result = inOrderTraverse(tree.lchild)
    elif type == "to_left":
        result = inOrderTraverse(TreeNode(root, tree, tree))
    return result
    

def to_tree(function: Union[str, list[str]]) -> Union[TreeNode, list[TreeNode]]:
    """将公式转化为二叉树"""
    if isinstance(function, list):
        return list(map(lambda x: BTree(change_To_PE(x)), function))
    else:
        return BTree(change_To_PE(function))