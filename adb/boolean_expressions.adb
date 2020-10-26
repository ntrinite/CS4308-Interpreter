package body boolean_expressions is

   -------------------------------
   -- create_boolean_expression --
   -------------------------------

    function create_boolean_expression (op: in relational_operator;
                                        exp1: in arithmetic_expression_access;
                                        exp2: in arithmetic_expression_access)
                                        return boolean_expression is
        expr: boolean_expression;
    begin
        expr.op := op;
        expr.expr1 := exp1;
        expr.expr2 := exp2;
        return expr;
    end create_boolean_expression;

   --------------
   -- evaluate --
   --------------

   function evaluate (expr: in boolean_expression) return boolean is
        value: boolean;
    begin
        case expr.op is
            when EQ_OP =>
                value := evaluate(expr.expr1) = evaluate(expr.expr2);
            when NE_OP =>
                value := evaluate(expr.expr1) /= evaluate(expr.expr2);
            when LT_OP =>
                value := evaluate(expr.expr1) < evaluate(expr.expr2);
            when LE_OP =>
                value := evaluate(expr.expr1) <= evaluate(expr.expr2);
            when GT_OP =>
                value := evaluate(expr.expr1) > evaluate(expr.expr2);
            when GE_OP =>
                value := evaluate(expr.expr1) >= evaluate(expr.expr2);
        end case;
        return value;
    end evaluate;

end boolean_expressions;
