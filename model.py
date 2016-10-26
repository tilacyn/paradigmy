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
