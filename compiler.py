# 导入正则表达式模块
import re

# 定义token类型
class Token:
    def __init__(self,type,value):
        self.type=type
        self.value=value
        # Token的类型，如数字number，加号+，减号-，plus，multiply等
        # Token的值，如数字的具体值，符号的具体字符，1，+，-等

    def __repr__(self):
        return f'Token({self.type},{self.value})'
        # repr 返回的字符串通常是该对象的代码表示形式
        # 返回一个字符串，格式为 Token(type, value)
        # self.type 是 Token 对象的类型（例如 number、plus 等）。
        # self.value 是 Token 对象的值（例如 1、+ 等）。

# 定义词法分析器
class Lexer:
    def __init__(self,text):
        self.text=text # 输入文本
        self.pos=0     # 输入当前处理等位置POS
        self.current_char = self.text[self.pos] # 当前文本【当前位置】=当前字符

    # 抛出错误，作用是提示遇到无效的字符的报警 
    # raise 抛出，exception异常，Invald character无效字符
    def error(self):
        raise Exception('Invald character')

    # 前进到下一个字符,如果位置 < 文本长度，则更新当前字符，位置 = 文本长度则结束。
     def advance(self):
        self.pos+=1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    # 跳过空白字符，因为空白字符通常不需要被解析为 Token。
    # self.current_char 是当前正在处理的字符。
    # is not None 检查当前字符是否为空（即是否已经处理完所有字符）。
    # isspace() 是 Python 的字符串方法，用于检查当前字符是否为空白字符（如空格、制表符、换行符等）。
    # 如果当前字符存在且是空白字符，则进入循环
    # 每次循环都会调用 advance()，从而跳过当前空白字符，继续处理下一个字符。
     def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance() # 移动到下一个字符

    # 提取一个数字
    # 初始化一个空字符串，用于存储数字字符
    # isdigit() 是 Python 的字符串方法，用于检查当前字符是否为数字。
     def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result +=self.current_char # 当当前字符不为空且是数字时，执行循环
            self.advance() # 移动到下一个字符
        return int(result) # 将结果字符串转换为整数并返回

    # 获取下一个Token
     def get_next_token(self):
        while self.current_char is not None: # 当当前字符不为空时，继续处理
            if self.current_char.isspace():  # 如果当前字符是空白字符（如空格、换行等）
                self.skip_whitespace() # 调用skip_whitespace方法跳过空白字符
                continue # 跳过当前循环，继续处理下一个字符

            if self.current_char.isdigit(): # 如果当前字符是数字
                return Tonken('NUMBER',self.number())  # 调用number方法提取数字，并返回一个类型为'NUMBER'的Token

            if self.current_char == '+': # 如果当前字符是加号
                self.advance() # 移动到下一个字符
                return Token('PLUS','+') # 返回一个类型为'PLUS'的Token，值为'+'

            if self.current_chat == '*': # 如果当前字符是乘号
                self.advance() # 移动到下一个字符
                return Token('MULTIPLY','*') # 返回一个类型为'MULTIPLY'的Token，值为'*'

            self.error() # 如果当前字符不是上述任何一种情况，抛出异常，表示遇到无效字符

        return Token('EOF',None)  # 如果所有字符处理完毕，返回一个类型为'EOF'的Token，表示输入结束
 
# 定义抽象语法树🌲节点
# ASTNode 的基类，用于表示抽象语法树（Abstract Syntax Tree, AST）的节点
# ASTNode 类本身没有实现任何功能，它只是一个占位符，用于继承和扩展
class ASTNode:
    pass

class BinOp(ASTNode): #BinOp 类继承自 ASTNode，表示一个二元操作符节点。它有三个属性：
    def __init__(self,left,op,right):
        self.left = left # 左子树
        self.op =op # 运算符
        self.right = right # 右子树

class Number(ASTNode): # Number 类也继承自 ASTNode，表示一个数字节点。它有一个属性：value
    def __init__(self,value):
        self.value =value # 数字值

# 定义语法分析器
class Parser:
    def __init__(self,lexer):
        self.lexer = lexer # 词法分析器
        self.current_token = self.lexer.get_next_token() # 当前Token

 # 抛出错误
    def error(self):
        raise Exception('Invalid syntax')

    # 匹配当前Token并获取下一个Token
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    # 解析因子（数字）
    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(token.value)
        else:
            self.error()

    # 解析表达式
    def expr(self):
        node = self.factor()

        while self.current_token.type in ('PLUS', 'MULTIPLY'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
                node = BinOp(left=node, op=token, right=self.factor())
            elif token.type == 'MULTIPLY':
                self.eat('MULTIPLY')
                node = BinOp(left=node, op=token, right=self.factor())

        return node

# 定义解释器
class Interpreter:
    def __init__(self, parser):
        self.parser = parser  # 语法分析器

    # 解释抽象语法树
    def visit(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, BinOp):
            if node.op.type == 'PLUS':
                return self.visit(node.left) + self.visit(node.right)
            elif node.op.type == 'MULTIPLY':
                return self.visit(node.left) * self.visit(node.right)
        else:
            raise Exception('Unknown node type')

    # 解释表达式
    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

# 主函数
def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()