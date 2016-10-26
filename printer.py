from yat.model import *
from yat.folder import *

cur_tab = 0

def ntab(n):
    for i in range(0, n):
        print('\t', end='')

class PrettyPrinter:

    def visit(self, tree):
        tree.accept(self)

    def visit_number(self, tree):
        print(tree.value, end=';\n')

    def visit_ref(self, tree):
        a_printer = ArythmPrinter()
        a_printer.visit(tree)

    def visit_conditional(self, tree):
        global cur_tab
        a_printer = ArythmPrinter()
        ntab(cur_tab)
        print('if (', end='')
        a_printer.visit(tree.condition)   
        print(') {', sep='', end='\n')
        cur_tab += 1
        for i in tree.if_true:
            ntab(cur_tab)
            self.visit(i)
        ntab(cur_tab - 1)
        print('}', 'else', '{', end='\n')
        for i in tree.if_false:
            ntab(cur_tab)
            self.visit(i)
        cur_tab -= 1
        print(end='};\n')

    def visit_read(self, tree):
        print('read', tree.name, end='')
        print(end=';\n')

    def visit_f_def(self, tree):
        global cur_tab
        print('def', tree.name, sep=' ', end='')
        print('(', end='')
        for i in tree.function.args:
            self.visit(i)
            if count < len(tree.args) - 1:
                print(', ', end='')
            count = count + 1
        print(') {', end='\n')
        cur_tab += 1
        for i in tree.function.body:
            ntab(cur_tab)
            self.visit(i)
        cur_tab -= 1
        print(end='};\n')

    def visit_bin_op(self, tree):
        a_printer = ArythmPrinter()
        a_printer.visit(tree)   
        print(end=';\n')

    def visit_print(self, tree):
        print('print', end=' ')
        a_printer = ArythmPrinter()
        a_printer.visit(tree.expr)   
        print(end=';\n')

    def visit_un_op(self, tree):
        print('(', end='')
        a_printer = ArythmPrinter()
        a_printer.visit(tree)   
        print(')', end=';\n')

    def visit_f_call(self, tree):
        a_printer = ArythmPrinter()
        a_printer.visit(tree)   
        print(end=';\n')


class ArythmPrinter:

    def visit(self, tree):
        tree.accept(self)

    def visit_number(self, tree):
        print(tree.value, end='')

    def visit_ref(self, tree):
        print(tree.name, end='')

    def visit_bin_op(self, tree):
        print('(', end='')
        self.visit(tree.lhs)
        print('', tree.op, end=' ')
        self.visit(tree.rhs)
        print(')', end='')

    def visit_un_op(self, tree):
        print('(', end='')
        print(tree.op, end='')
        self.visit(tree.expr)
        print(')', end='')

    def visit_f_call(self, tree):
        self.visit(tree.fun_expr)
        print('(', end='')
        count = 0
        for i in tree.args:
            self.visit(i)
            if count < len(tree.args) - 1:
                print(', ', end='')
            count = count + 1
        print(')', end='')



"""tests"""

ten = Number(2332536)
printer = PrettyPrinter()
printer.visit(ten)
five = Number(5)
six = Number(6)
con = Conditional(BinaryOperation(five, '<', six),
                  [Print(Number(222)),
                   Print(Number(333))], [Print(Number(444)),
                                         Print(Number(555))])
printer.visit(con)

read = Read('x')
printer = PrettyPrinter()
printer.visit(read)

number = Number(42)
unary = UnaryOperation('-', number)
printer = PrettyPrinter()
printer.visit(unary)

n0 = Number(0)
n00 = Number(1)
mul1 = BinaryOperation(n0, '*', n00)
printer = PrettyPrinter()
printer.visit(mul1)


n0, n1, n2 = Number(1), Number(2), Number(3)
add = BinaryOperation(n1, '+', n2)
mul = BinaryOperation(n0, '*', add)
printer = PrettyPrinter()
printer.visit(mul)

number = Number(42)
print1 = Print(number)
printer = PrettyPrinter()
printer.visit(print1)


function = Function([], [Print(Number(222)), Print(Number(333)),
                         Print(Number(444)), Print(Number(555))])
definition = FunctionDefinition('foo', function)
printer = PrettyPrinter()
printer.visit(definition)

reference = Reference('foo')
call = FunctionCall(reference, [Number(1), Number(2), Number(3)])
printer = PrettyPrinter()
printer.visit(call)


print('\n')
folder = ConstantFolder()
mul1 = folder.visit(mul1)
printer.visit(mul1)

p1 = Number(9)
p2 = Number(10)

con = Conditional(BinaryOperation(p1, '>', p2), [Print(BinaryOperation(p1, '*', p2)), Print(BinaryOperation(p2, '/', p1))],
                                                [Print(BinaryOperation(p1, '+', p2)), Print(BinaryOperation(p2, '+', p1))])
con1 = Conditional(BinaryOperation(p1, '>', p2), [], [])
printer.visit(folder.visit(con1))
