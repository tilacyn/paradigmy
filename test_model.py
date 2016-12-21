import model
from model import *
import sys
from io import StringIO
import pytest

BinOp = BinaryOperation
Num = Number


def val(num):
    scope = Scope()
    cur_stdout = sys.stdout
    sys.stdout = StringIO()
    Print(num).evaluate(scope)
    return int(sys.stdout.getvalue())
    sys.stdout = cur_stdout


class TestScope:
    def test_setitem(self):
        parent = Scope()
        NumObj = Num(1)
        parent["foo"] = NumObj
        assert parent["foo"] == NumObj

    def test_setitem_par(self):
        parent = Scope()
        scope = Scope(parent)
        NumObj = Num(1)
        parent["foo"] = NumObj
        assert scope["foo"] == NumObj


class TestNum:
    def test_eval(self):
        parent = Scope()
        NumObj = Num(1)
        assert NumObj.evaluate(parent) is NumObj

    def test_value(self):
        parent = Scope()
        NumObj = Num(1)
        assert val(NumObj) == 1


class TestFunction:
    def test_eval_simple(self):
        scope = Scope()
        scope['hullo'] = Num(99)
        scope['goodbye'] = Num(55)
        f = Function([Reference('hullo'), Reference('goodbye')],
                     [BinOp(Reference('hullo'), '-', Reference('goodbye'))])
        assert val(f.evaluate(scope)) == 44

    def test_empty_args(self):
        scope = Scope()
        f = Function([], [BinOp(Num(5), '-', Num(17)),
                          BinOp(Num(5), '+', Num(17))])
        assert val(f.evaluate(scope)) == 22

    def test_empty_body(self):
        scope = Scope()
        scope['arg1'] = Num(22)
        scope['arg2'] = Num(33)
        f = Function([Reference('arg1'), Reference('arg2')], [])
        assert f.evaluate(scope)

    def test_eval_all_body(self, monkeypatch):
        scope = Scope()
        monkeypatch.setattr(sys, "stdout", StringIO())
        f = Function([], [Print(Num(9)), Print(Num(1)), Print(Num(22))])
        f.evaluate(scope)
        assert sys.stdout.getvalue() == '9\n1\n22\n'


class TestFunDef:
    def test_definition(self):
        scope = Scope()
        scope['hullo'] = Num(99)
        scope['goodbye'] = Num(55)
        f = Function([Reference('hullo'), Reference('goodbye')],
                     [BinOp(Reference('hullo'), '-', Reference('goodbye'))])
        fdef = FunctionDefinition('f', f).evaluate(scope)
        assert fdef is f


class TestUnaryOp:
    def test_minus(self):
        scope = Scope()
        scope['hullo'] = Num(99)
        scope['goodbye'] = Num(-53)
        un_op = UnaryOperation('-', Reference('hullo'))
        assert val(un_op.evaluate(scope)) == -99
        un_op = UnaryOperation('-', Reference('goodbye'))
        assert val(un_op.evaluate(scope)) == 53

    def test_not(self):
        scope = Scope()
        scope['hullo'] = Num(34)
        scope['goodbye'] = Num(0)
        un_op = UnaryOperation('!', Reference('hullo'))
        assert val(un_op.evaluate(scope)) == 0
        un_op = UnaryOperation('!', Reference('goodbye'))
        assert val(un_op.evaluate(scope)) != 0

    def test_complicated(self):
        scope = Scope()
        fifteen = UnaryOperation('-', Num(-15))
        assert val(UnaryOperation('-', fifteen).evaluate(scope)) == -15


class TestBinOp:
    def test_all(self):
        parent = Scope()
        parent['a1'] = Num(4)
        parent['a2'] = Num(3)
        assert val(BinOp(Reference('a1'), '+',
                         Reference('a2')).evaluate(parent)) == 7
        assert val(BinOp(Reference('a1'), '-',
                         Reference('a2')).evaluate(parent)) == 1
        assert val(BinOp(Reference('a1'), '*',
                         Reference('a2')).evaluate(parent)) == 12
        assert val(BinOp(Reference('a1'), '/',
                         Reference('a2')).evaluate(parent)) == 1
        assert val(BinOp(Reference('a1'), '>',
                         Reference('a2')).evaluate(parent)) != 0
        assert val(BinOp(Reference('a1'), '<',
                         Reference('a2')).evaluate(parent)) == 0
        assert val(BinOp(Reference('a1'), '>=',
                         Reference('a2')).evaluate(parent)) != 0
        assert val(BinOp(Reference('a1'), '<=',
                         Reference('a2')).evaluate(parent)) == 0
        assert val(BinOp(Reference('a1'), '&&',
                         Reference('a2')).evaluate(parent)) != 0
        assert val(BinOp(Reference('a1'), '||',
                         Reference('a2')).evaluate(parent)) != 0
        assert val(BinOp(Reference('a1'), '!=',
                         Reference('a2')).evaluate(parent)) != 0
        assert val(BinOp(Reference('a1'), '==',
                         Reference('a2')).evaluate(parent)) == 0
        assert val(BinOp(Reference('a1'), '%',
                         Reference('a2')).evaluate(parent)) == 1

    def test_complicated(self):
        scope = Scope()
        fifteen = BinOp(Num(5), '+', Num(10))
        assert val(BinOp(fifteen, '*', fifteen).evaluate(scope)) == 225


class TestFunctionCall:
    def test_simple(self):
        parent = Scope()
        parent['foo'] = Function(('hello', 'world'),
                                 [BinOp(Reference('hello'),
                                        '+',
                                        Reference('world'))])
        scope = Scope(parent)
        assert val(FunctionCall(FunctionDefinition('foo', parent['foo']),
                   [Num(5),
                    UnaryOperation('-', Num(3))]).evaluate(scope)) == 2

    def test_empty_args(self):
        parent = Scope()
        parent['foo'] = Function([],
                                 [BinOp(Num(9),
                                        '+',
                                        Num(8))])
        scope = Scope(parent)
        assert val(FunctionCall(FunctionDefinition('foo', parent['foo']),
                   []).evaluate(scope)) == 17

    def test_fcall_in_fcall(self):
        parent = Scope()
        parent['foo'] = Function(('hello', 'world'),
                                 [BinOp(Reference('hello'),
                                        '+',
                                        Reference('world'))])

        parent['bar'] = Function(('hello', 'world'),
                                 [BinOp(Reference('hello'),
                                        '-',
                                        Reference('world'))])

        scope = Scope(parent)
        assert val(FunctionCall(FunctionDefinition('foo', parent['foo']),
                   [FunctionCall(FunctionDefinition('bar', parent['bar']),
                    [Num(5), Num(-3)]),
                    UnaryOperation('-', Num(3))]).evaluate(scope)) == 5


class TestReference:
    def test_simple(self):
        scope = Scope()
        NumObj = Num(123)
        scope['hullo'] = NumObj
        assert Reference('hullo').evaluate(scope) is scope['hullo']
        assert Reference('hullo').evaluate(scope) is NumObj

    def test_function(self):
        parent = Scope()
        f = Function(('hello', 'world'),
                     [BinOp(Reference('hello'),
                            '+',
                            Reference('world'))])
        parent['foo'] = f
        assert Reference('foo').evaluate(parent) is f


class TestConditional:
    def test_simple(self):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [BinOp(Num(0), '%', Num(2)),
                            BinOp(Num(3), '/', Num(-3)),
                            BinOp(Num(-2), '*', Num(99))],
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))])
        assert val(cond.evaluate(scope)) == -198
        scope['key'] = Num(1)
        assert val(cond.evaluate(scope)) == 3

    def test_if_true_none(self):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')), None,
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))])
        assert cond.evaluate(scope)
        scope['key'] = Num(1)
        assert val(cond.evaluate(scope)) == 3

    def test_if_true_empty(self):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')), [],
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))])
        assert cond.evaluate(scope)
        scope['key'] = Num(1)
        assert val(cond.evaluate(scope)) == 3

    def test_if_false_none(self):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))], None)
        assert val(cond.evaluate(scope)) == 3
        scope['key'] = Num(1)
        assert cond.evaluate(scope)

    def test_if_false_no(self):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))])
        assert val(cond.evaluate(scope)) == 3
        scope['key'] = Num(1)
        assert cond.evaluate(scope)

    def test_if_false_empty(self):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))], [])
        assert val(cond.evaluate(scope)) == 3
        scope['key'] = Num(1)
        assert cond.evaluate(scope)

    def test_all_body(self, monkeypatch):
        scope = Scope()
        monkeypatch.setattr(sys, 'stdout', StringIO())
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [Print(Num(22)),
                            Print(Num(99))], [])
        cond.evaluate(scope)
        assert sys.stdout.getvalue() == '22\n99\n'
        scope['key'] = Num(1)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [], [Print(Num(22)),
                           Print(Num(99))])
        cond.evaluate(scope)
        assert sys.stdout.getvalue() == '22\n99\n22\n99\n'


class TestRead:
    def test_read_simple(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdin', StringIO('2\n'))
        scope = Scope()
        read = Read('a').evaluate(scope)
        assert val(read) == 2


class TestPrint:
    def test_simple(self):
        NumObj = Num(22)
        assert val(NumObj) == 22

    def test_complicated(self):
        scope = Scope()
        PrintObj = Print(BinOp(Num(6), '/', Num(3))).evaluate(scope)
        assert val(PrintObj) == 2


class TestMulti:
    def test_multi_test(self, monkeypatch):
        parent = Scope()
        monkeypatch.setattr(sys, 'stdout', StringIO())
        parent['arg1'] = Num(10)
        Conditional(BinOp(Reference('arg1'), '>', Num(5)),
                    [Print(UnaryOperation('-', BinOp(Reference('arg1'),
                                                     '-', Num(1)))),
                     Print(UnaryOperation('-', BinOp(Reference('arg1'),
                                                     '-', Num(2)))),
                     Print(UnaryOperation('-', BinOp(Reference('arg1'),
                                                     '-', Num(3))))],
                    [Print(BinOp(Reference('arg1'), '-', Num(1))),
                     Print(BinOp(Reference('arg1'), '-', Num(2))),
                     Print(BinOp(Reference('arg1'),
                           '-', Num(3)))]).evaluate(parent)
        assert sys.stdout.getvalue() == '-9\n-8\n-7\n'
