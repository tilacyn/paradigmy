import model
from model import *
import sys
from io import StringIO
import pytest

BinOp = BinaryOperation
Num = Number

def val(num, monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    Print(num).evaluate(scope)
    return int(sys.stdout.getvalue())

class Test_Scope:
    def test_setitem(self):
        parent = Scope()
        NumObj = Number(1)
        parent["foo"] = NumObj
        assert parent["foo"] == NumObj

    def test_setitem_par(self):
        parent = Scope()
        scope = Scope(parent)
        NumObj = Number(1)
        parent["foo"] = NumObj
        assert scope["foo"] == NumObj


class Test_Number:
    def test_eval(self):
        parent = Scope()
        NumObj = Number(1)
        assert NumObj.evaluate(parent) is NumObj

    def test_value(self, monkeypatch):
        parent = Scope()
        NumObj = Number(1)
        assert val(NumObj, monkeypatch) == 1

class Test_Function:
    def test_eval_simple(self, monkeypatch):
        scope = Scope()
        scope['hullo'] = Number(99)
        scope['goodbye'] = Number(55)
        f = Function([Reference('hullo'), Reference('goodbye')],
                     [BinOp(Reference('hullo'), '-', Reference('goodbye'))])
        assert val(f.evaluate(scope), monkeypatch) == 44

    def test_empty_args(self, monkeypatch):
        scope = Scope()
        f = Function([], [BinOp(Number(5), '-', Number(17)),
                          BinOp(Number(5), '+', Number(17))])
        assert val(f.evaluate(scope), monkeypatch) == 22

    def test_empty_body(self, monkeypatch):
        scope = Scope()
        scope['arg1'] = Number(22)
        scope['arg2'] = Number(33)
        f = Function([Reference('arg1'), Reference('arg2')], [])
        assert val(f.evaluate(scope), monkeypatch) == 0


class Test_FunDef:
    def test_definition(self):
        scope = Scope()
        scope['hullo'] = Number(99)
        scope['goodbye'] = Number(55)
        f = Function([Reference('hullo'), Reference('goodbye')],
                     [BinOp(Reference('hullo'), '-', Reference('goodbye'))])
        fdef = FunctionDefinition('f', f).evaluate(scope)
        assert fdef is f


class Test_UnaryOp:
    def test_minus(self, monkeypatch):
        scope = Scope()
        scope['hullo'] = Number(99)
        scope['goodbye'] = Number(-53)
        un_op = UnaryOperation('-', Reference('hullo'))
        assert val(un_op.evaluate(scope), monkeypatch) == -99
        un_op = UnaryOperation('-', Reference('goodbye'))
        assert val(un_op.evaluate(scope), monkeypatch) == 53

    def test_not(self, monkeypatch):
        scope = Scope()
        scope['hullo'] = Number(34)
        scope['goodbye'] = Number(0)
        un_op = UnaryOperation('!', Reference('hullo'))
        assert val(un_op.evaluate(scope), monkeypatch) == 0
        un_op = UnaryOperation('!', Reference('goodbye'))
        assert val(un_op.evaluate(scope), monkeypatch) != 0
    def test_complicated(self, monkeypatch):
        scope = Scope()
        fifteen = UnaryOperation('-', Num(-15))
        assert val(UnaryOperation('-', fifteen).evaluate(scope), monkeypatch) == -15

class Test_BinOp:
    def test_all(self, monkeypatch):
        parent = Scope()
        parent['a1'] = Number(4)
        parent['a2'] = Number(3)
        assert val(BinaryOperation(Reference('a1'), '+',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 7
        assert val(BinaryOperation(Reference('a1'), '-',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 1
        assert val(BinaryOperation(Reference('a1'), '*',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 12
        assert val(BinaryOperation(Reference('a1'), '/',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 1
        assert val(BinaryOperation(Reference('a1'), '>',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 1
        assert val(BinaryOperation(Reference('a1'), '<',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 0
        assert val(BinaryOperation(Reference('a1'), '>=',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 1
        assert val(BinaryOperation(Reference('a1'), '<=',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 0
        assert val(BinaryOperation(Reference('a1'), '&&',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 3
        assert val(BinaryOperation(Reference('a1'), '||',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 3
        assert val(BinaryOperation(Reference('a1'), '!=',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 1
        assert val(BinaryOperation(Reference('a1'), '==',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 0
        assert val(BinaryOperation(Reference('a1'), '%',
                                     Reference('a2')).evaluate(parent), monkeypatch) == 1
    def test_complicated(self, monkeypatch):
        scope = Scope()
        fifteen = BinOp(Num(5), '+', Num(10))
        assert val(BinOp(fifteen, '*', fifteen).evaluate(scope), monkeypatch) == 225

class Test_FunctionCall:
    def test_simple(self, monkeypatch):
        parent = Scope()
        parent['foo'] = Function(('hello', 'world'),
                                 [BinaryOperation(Reference('hello'),
                                                        '+',
                                                        Reference('world'))])
        scope = Scope(parent)
        assert val(FunctionCall(FunctionDefinition('foo', parent['foo']),
                   [Number(5),
                    UnaryOperation('-', Number(3))]).evaluate(scope), monkeypatch) == 2
    def test_empty_args(self, monkeypatch):
        parent = Scope()
        parent['foo'] = Function([],
                                 [BinaryOperation(Number(9),
                                                        '+',
                                                        Number(8))])
        scope = Scope(parent)
        assert val(FunctionCall(FunctionDefinition('foo', parent['foo']),
                   []).evaluate(scope), monkeypatch) == 17

class Test_Reference:
    def test_simple(self):
        scope = Scope()
        #Not sure about is (whether it has to be exactly that object)
        NumObj = Number(123)
        scope['hullo'] = NumObj
        assert Reference('hullo').evaluate(scope) is scope['hullo']
        assert Reference('hullo').evaluate(scope) is NumObj
    def test_function(self):
        parent = Scope()
        f = Function(('hello', 'world'),
                                 [BinaryOperation(Reference('hello'),
                                                        '+',
                                                        Reference('world'))])
        parent['foo'] = f
        assert Reference('foo').evaluate(parent) is f
        #What is this test for?


class Test_Conditional:
    def test_simple(self, monkeypatch):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [BinOp(Num(0), '%', Num(2)),
                            BinOp(Num(3), '/', Num(-3)),
                            BinOp(Num(-2), '*', Num(99))],
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))])
        assert val(cond.evaluate(scope), monkeypatch) == -198
        scope['key'] = Num(1)
        assert val(cond.evaluate(scope), monkeypatch) == 3
    
    def test_if_true_none(self, monkeypatch):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')), None,
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))])
        assert val(cond.evaluate(scope), monkeypatch) == 0
        scope['key'] = Num(1)
        assert val(cond.evaluate(scope), monkeypatch) == 3
        
    def test_if_true_empty(self, monkeypatch):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')), [],
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))])
        assert val(cond.evaluate(scope), monkeypatch) == 0
        scope['key'] = Num(1)
        assert val(cond.evaluate(scope), monkeypatch) == 3

    def test_if_false_none(self, monkeypatch):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))], None)
        assert val(cond.evaluate(scope), monkeypatch) == 3
        scope['key'] = Num(1)
        assert val(cond.evaluate(scope), monkeypatch) == 0

    def test_if_false_empty(self, monkeypatch):
        scope = Scope()
        scope['key'] = Num(0)
        cond = Conditional(UnaryOperation('!', Reference('key')),
                           [BinOp(Num(5), '+', Num(4)),
                            BinOp(Num(2), '+', Num(1))], [])
        assert val(cond.evaluate(scope), monkeypatch) == 3
        scope['key'] = Num(1)
        assert val(cond.evaluate(scope), monkeypatch) == 0


class Test_Read:
    def test_read_simple(self, monkeypatch):
        monkeypatch.setattr(sys, 'stdin', StringIO('2\n'))
        scope = Scope()
        read = Read('a').evaluate(scope)
        assert val(read, monkeypatch) == 2
        

class Test_Print:
    def test_simple(self, monkeypatch):
        NumObj = Number(22)
        assert val(NumObj, monkeypatch) == 22

    def test_complicated(self, monkeypatch):
        scope = Scope()
        PrintObj = Print(BinOp(Num(6), '/', Num(3))).evaluate(scope)
        assert val(PrintObj, monkeypatch) == 2

class Test_Multi:
    def test_multi_test(self, monkeypatch):
        pass
        




