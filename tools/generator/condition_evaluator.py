from __future__ import annotations

import ast
from typing import Any, Dict


class ConditionEvaluator:
    """Evaluate blueprint condition expressions safely."""

    SAFE_NODES = {
        ast.Expression,
        ast.BoolOp,
        ast.UnaryOp,
        ast.BinOp,
        ast.Compare,
        ast.Name,
        ast.Constant,
        ast.Subscript,
        ast.Index,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Load,
        ast.And,
        ast.Or,
        ast.Not,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.In,
        ast.NotIn,
        ast.Is,
        ast.IsNot,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
    }

    def evaluate(self, expression: str, context: Dict[str, Any]) -> bool:
        tree = ast.parse(expression, mode="eval")
        self._validate_ast(tree)
        return bool(self._eval(tree.body, context))

    def _validate_ast(self, node: ast.AST) -> None:
        if not isinstance(node, tuple(self.SAFE_NODES)):
            raise ValueError(f"Unsupported condition syntax: {type(node).__name__}")
        for child in ast.iter_child_nodes(node):
            self._validate_ast(child)

    def _eval(self, node: ast.AST, context: Dict[str, Any]) -> Any:
        if isinstance(node, ast.Expression):
            return self._eval(node.body, context)
        if isinstance(node, ast.BoolOp):
            values = [self._eval(value, context) for value in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not self._eval(node.operand, context)
        if isinstance(node, ast.BinOp):
            left = self._eval(node.left, context)
            right = self._eval(node.right, context)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Mod):
                return left % right
        if isinstance(node, ast.Compare):
            left = self._eval(node.left, context)
            for operator, comparator in zip(node.ops, node.comparators):
                right = self._eval(comparator, context)
                if isinstance(operator, ast.Eq) and left != right:
                    return False
                if isinstance(operator, ast.NotEq) and left == right:
                    return False
                if isinstance(operator, ast.Lt) and left >= right:
                    return False
                if isinstance(operator, ast.LtE) and left > right:
                    return False
                if isinstance(operator, ast.Gt) and left <= right:
                    return False
                if isinstance(operator, ast.GtE) and left < right:
                    return False
                if isinstance(operator, ast.In) and left not in right:
                    return False
                if isinstance(operator, ast.NotIn) and left in right:
                    return False
                if isinstance(operator, ast.Is) and left is not right:
                    return False
                if isinstance(operator, ast.IsNot) and left is right:
                    return False
                left = right
            return True
        if isinstance(node, ast.Name):
            return context.get(node.id)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Subscript):
            value = self._eval(node.value, context)
            key = self._eval(node.slice, context)
            return value[key]
        if isinstance(node, ast.Index):
            return self._eval(node.value, context)
        if isinstance(node, ast.List):
            return [self._eval(element, context) for element in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(self._eval(element, context) for element in node.elts)
        if isinstance(node, ast.Dict):
            return {self._eval(k, context): self._eval(v, context) for k, v in zip(node.keys, node.values)}
        raise ValueError(f"Unsupported condition node: {type(node).__name__}")
