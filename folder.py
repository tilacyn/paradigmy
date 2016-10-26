from yat.model import *

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
        
