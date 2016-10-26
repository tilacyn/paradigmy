from model import *
from folder import *


def write_indent(n):
    print('\t' * n, end='')


class PrettyPrinter:

    def __init__(self, cur_indent=0):
        self.cur_indent = cur_indent
        self.a_printer = ArithmPrinter()

    def visit(self, tree):
        tree.accept(self)

    def visit_number(self, tree):
        self.a_printer.visit(tree)
        print(end=';\n')

    def visit_ref(self, tree):
        self.a_printer.visit(tree)
        print(';')

    def visit_conditional(self, tree):
        write_indent(self.cur_indent - 1)
        print('if (', end='')
        self.a_printer.visit(tree.condition)
        print(') {', sep='', end='\n')
        self.cur_indent += 1
        if tree.if_true:
            for sentence in tree.if_true:
                write_indent(self.cur_indent)
                self.visit(sentence)
        write_indent(self.cur_indent - 1)
        print('}', 'else', '{', end='\n')
        if tree.if_false:
            for sentence in tree.if_false:
                write_indent(self.cur_indent)
                self.visit(sentence)
        write_indent(self.cur_indent - 1)
        print(end='};\n')
        self.cur_indent -= 1

    def visit_read(self, tree):
        print('read', tree.name, end='')
        print(end=';\n')

    def visit_f_def(self, tree):
        print('def ', tree.name, '(',
              ', '.join(tree.function.args), ') {', sep='')
        self.cur_indent += 1
        for sentence in tree.function.body:
            write_indent(self.cur_indent)
            self.visit(sentence)
        self.cur_indent -= 1
        write_indent(self.cur_indent)
        print(end='};\n')

    def visit_bin_op(self, tree):
        self.a_printer.visit(tree)
        print(end=';\n')

    def visit_print(self, tree):
        print('print', end=' ')
        self.a_printer.visit(tree.expr)
        print(end=';\n')

    def visit_un_op(self, tree):
        print('(', end='')
        self.a_printer.visit(tree)
        print(')', end=';\n')

    def visit_f_call(self, tree):
        self.a_printer.visit(tree)
        print(end=';\n')


class ArithmPrinter:

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
        for i, sentence in enumerate(tree.args):
            self.visit(sentence)
            if i < len(tree.args) - 1:
                print(', ', end='')
        print(')', end='')
