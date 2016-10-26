
class Scope:

    def __init__(self, parent=None):
        self.parent = parent
        self.dic = {}

    def __getitem__(self, name):
        if self.dic.get(name):
            return self.dic[name]
        else:
            return self.parent[name]

    def __setitem__(self, name, val):
        self.dic[name] = val


class Number:

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self

    def accept(self, visitor):
        return visitor.visit_number(self)


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        if not self.body:
            return Number(0)
        for stmt in self.body:
            res = stmt.evaluate(scope)
        return res

    def accept(self, visitor):
        return visitor.visit_function(self)


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visit_f_def(self)


class Conditional:

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if self.condition.evaluate(scope).value == 0:
            if not self.if_false:
                return Number(0)
            else:
                for stmt in self.if_false:
                    res = stmt.evaluate(scope)
                return res
        else:
            if not self.if_true:
                return Number(0)
            else:
                for stmt in self.if_true:
                    res = stmt.evaluate(scope)
                return res

    def accept(self, visitor):
        return visitor.visit_conditional(self)


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print_number = self.expr.evaluate(scope)
        print(print_number.value)
        return print_number

    def accept(self, visitor):
        return visitor.visit_print(self)


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        read_val = int(input())
        scope[self.name] = Number(read_val)
        return Number(read_val)

    def accept(self, visitor):
        return visitor.visit_read(self)


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for arg_name, arg_value in zip(function.args, self.args):
            call_scope[arg_name] = arg_value.evaluate(scope)
        return function.evaluate(call_scope)

    def accept(self, visitor):
        return visitor.visit_f_call(self)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit_ref(self)


class BinaryOperation:

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        lhs = self.lhs.evaluate(scope).value
        rhs = self.rhs.evaluate(scope).value
        if self.op == '-':
            return Number(lhs - rhs)
        if self.op == '+':
            return Number(lhs + rhs)
        if self.op == '%':
            return Number(lhs % rhs)
        if self.op == '*':
            return Number(lhs * rhs)
        if self.op == '/':
            return Number(lhs // rhs)
        if self.op == '&&':
            return Number(int(lhs and rhs))
        if self.op == '||':
            return Number(int(rhs or lhs))
        if self.op == '>':
            return Number(int(lhs > rhs))
        if self.op == '<':
            return Number(int(lhs < rhs))
        if self.op == '>=':
            return Number(int(lhs >= rhs))
        if self.op == '<=':
            return Number(int(lhs <= rhs))
        if self.op == '==':
            return Number(int(lhs == rhs))
        if self.op == '!=':
            return Number(int(not lhs == rhs))

    def accept(self, visitor):
        return visitor.visit_bin_op(self)


class UnaryOperation:

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        cur_val = self.expr.evaluate(scope).value
        if self.op == '-':
            return Number(-cur_val)
        if self.op == '!':
            return Number(int(not cur_val))

    def accept(self, visitor):
        return visitor.visit_un_op(self)


class PrettyPrinter:

    def visit(self, tree):
        tree.accept(self)

    def visit_number(self, tree):
        print(tree.value, end=';\n')

    def visit_ref(self, tree):
        print(tree.name, end=';\n')

    def visit_conditional(self, tree):
        u_p = Ugly_Printer()
        print('if (', end='')
        u_p.visit(tree.condition)
        print(') {', sep='', end='\n')
        for i in tree.if_true:
            self.visit(i)
        print('}', 'else', '{', end='\n')
        for i in tree.if_false:
            self.visit(i)
        print(end='};\n')

    def visit_read(self, tree):
        print('read', tree.name, end='')
        print(end=';\n')

    def visit_f_def(self, tree):
        print('def', tree.name, sep=' ', end='')
        print('(', *tree.function.args, ')', '{', sep='', end='\n')
        for i in tree.function.body:
            self.visit(i)
        print(end='};\n')

    def visit_bin_op(self, tree):
        u_p = Ugly_Printer()
        u_p.visit(tree)
        print(end=';\n')

    def visit_print(self, tree):
        print('print', end=' ')
        u_p = Ugly_Printer()
        u_p.visit(tree.expr)
        print(end=';\n')

    def visit_un_op(self, tree):
        u_p = Ugly_Printer()
        u_p.visit(tree)
        print(')', end=';\n')

    def visit_f_call(self, tree):
        u_p = Ugly_Printer()
        u_p.visit(tree)        
        print(end=';\n')


class Ugly_Printer:

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


class ConstantFolder:

    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, tree):
        return tree

    def visit_read(self,tree):
        return tree
  
    def visit_ref(self, tree):
        return tree

    def visit_conditional(self, tree):
        tree.condition = self.visit(tree.condition)
        for i in tree.if_true:
            i = self.visit(i)
        for i in tree.if_false:
            i = self.visit(i)
        return tree


    def visit_f_def(self, tree):
        for i in tree.function.body:
            i = self.visit(i)
        return tree

    def visit_bin_op(self, tree):
        if isinstance(tree.lhs, Number):
            if tree.lhs.value == 0 and tree.op == '*':
                return Number(0)
            if isinstance(tree.rhs, Number):
                return tree.evaluate(0)
        if isinstance(tree.rhs, Number) and tree.rhs.value == 0 and tree.op == '*':
            return Number(0)
        if isinstance(tree.lhs, Reference) and isinstance(tree.rhs, Reference):
            if tree.lhs.name == tree.rhs.name and tree.op('-'):
                return Number(0)
        tree.lhs = self.visit(tree.lhs)
        tree.rhs = self.visit(tree.rhs)
        return tree
       
        
    def visit_print(self, tree):
        tree.expr = self.visit(tree.expr)
        return tree
    def visit_un_op(self, tree):
        if isinstance(tree.expr, Number):
            return tree.evaluate(0)
    

    def visit_f_call(self, tree):
        fun_expr = self.visit(tree.fun_expr)
        for i in tree.args:
            i = self.visit(i)
        return tree
        

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

