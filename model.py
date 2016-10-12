class Scope:

    def __init__(self, parent=None):
        self.parent = parent
        dic = {}
        self.dic = dic

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


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        for smth in self.body:
            t = smth.evaluate(scope)
        return t


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if self.condition.evaluate(scope).value == 0:
            if self.if_false is None:
                return Number(0)
            else:
                return self.if_false[- 1].evaluate(scope)
        else:
            if self.if_true is None:
                return Number(0)
            else:
                return self.if_true[- 1].evaluate(scope)


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)
        return self.expr


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        read_val = int(input())
        scope[self.name] = Number(read_val)
        return Number(read_val)


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for i in zip(function.args, self.args):
            call_scope[i[0]] = i[1].evaluate(scope)
        return function.evaluate(call_scope)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


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
            if lhs == 0 or rhs == 0:
                return Number(0)
            else:
                return Number(1)
        if self.op == '||':
            if lhs == 0 and rhs == 0:
                return Number(0)
            else:
                return Number(1)
        if self.op == '>':
            if(lhs > rhs):
                return Number(lhs - rhs)
            else:
                return Number(0)
        if self.op == '<':
            if(lhs < rhs):
                return Number(rhs - lhs)
            else:
                return Number(0)
        if self.op == '>=':
            if(lhs >= rhs):
                return Number(lhs - rhs + 1)
            else:
                return Number(0)
        if self.op == '<=':
            if(lhs <= rhs):
                return Number(rhs - lhs + 1)
            else:
                return Number(0)
        if self.op == '==':
            if(lhs == rhs):
                return Number(1)
            else:
                return Number(0)
        if self.op == '!=':
            if(lhs != rhs):
                return Number(1)
            else:
                return Number(0)


class UnaryOperation:

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        self.expr = self.expr.evaluate(scope).value
        if self.op == '-':
            return Number(-self.expr)
        if self.op == '!':
            if self.expr == 0:
                return Number(1)
            else:
                return Number(0)


def example():
    parent = Scope()
    parent['foo'] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent['bar'] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope['bar'] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def example1():
    print('It should read arg1')
    print('It should print (int)(arg1 == 200):')
    parent = Scope()
    Read('arg1').evaluate(parent)
    Print(Conditional(BinaryOperation(Reference('arg1'), '==', Number(200)),
                      [Print(Number(1))], [Print(Number(0))]).evaluate(parent))


def example2():
    print('It should read arg1, arg2')
    print('It should print (arg1//arg2)*(arg1%arg2):')
    parent = Scope()
    d = BinaryOperation(Reference('arg1'), '/', Reference('arg2'))
    t = BinaryOperation(Reference('arg1'), '%', Reference('arg2'))
    parent['/%'] = Function(('arg1', 'arg2'),
                            [Print(d),  Print(t),
                            Print(BinaryOperation(d, '*', t))])
    Read('1').evaluate(parent)
    Read('2').evaluate(parent)
    FunctionCall(Reference('/%'), [parent['1'], parent['2']]).evaluate(parent)


if __name__ == '__main__':
    example()
    example1()
    example2()
