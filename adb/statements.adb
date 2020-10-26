with memory, Ada.Text_IO;
use memory, Ada.Text_IO;

package body statements is

   ---------------------------------
   -- create_assignment_statement --
   ---------------------------------

   function create_assignment_statement (var: in id; expr: in arithmetic_expression_access)
                                         return statement_access is
        stmt: statement_access;
    begin
        stmt := new statement (ASSN_STMT);
        stmt.assn_var := var;
        stmt.assn_expr := expr;
        return stmt;
   end create_assignment_statement;

   ----------------------------
   -- create_while_statement --
   ----------------------------

   function create_while_statement  (expr: in boolean_expression; blk: in block)
                                     return statement_access is
        stmt: statement_access;
    begin
        stmt := new statement (WHILE_STMT);
        stmt.while_expr := expr;
        stmt.while_blk := blk;
        return stmt;
   end create_while_statement;

   ----------------------------
   -- create_print_statement --
   ----------------------------

   function create_print_statement (expr: in arithmetic_expression_access)
                                    return statement_access is
        stmt: statement_access;
    begin
        stmt := new statement (PRINT_STMT);
        stmt.print_expr := expr;
        return stmt;
   end create_print_statement;

   -----------------------------
   -- create_repeat_statement --
   -----------------------------

   function create_repeat_statement (blk: in block;  expr: in boolean_expression)
                                     return statement_access is
        stmt: statement_access;
    begin
        stmt := new statement (REPEAT_STMT);
        stmt.repeat_blk := blk;
        stmt.repeat_expr := expr;
        return stmt;
   end create_repeat_statement;

   -------------------------
   -- create_if_statement --
   -------------------------

   function create_if_statement (expr: in boolean_expression; blk1, blk2: in block)
                                 return statement_access is
        stmt: statement_access;
    begin
        stmt := new statement (IF_STMT);
        stmt.if_expr := expr;
        stmt.if_blk1 := blk1;
        stmt.if_blk2 := blk2;
        return stmt;
   end create_if_statement;

   ---------
   -- add --
   ---------

   procedure add (blk: in out block; stmt: in statement_access) is
    begin
        statement_list.Append(blk.l, stmt);
   end add;

   -------------
   -- execute --
   -------------

    procedure execute (blk: in block) is
        current: statement_list.cursor;
   begin
        if statement_list.is_empty (blk.l) then
            raise empty_block_exception with "executing empty block";
        end if;
        current := statement_list.first (blk.l);
        while statement_list.has_element (current) loop
            execute (statement_list.element (current));
            statement_list.next(current);
        end loop;
   end execute;

   -------------
   -- execute --
   -------------

   procedure execute (stmt: in statement_access) is
    begin
        case stmt.stmt_type is
            when ASSN_STMT =>
                store (get_char(stmt.assn_var), evaluate(stmt.assn_expr));
            when WHILE_STMT =>
                while evaluate (stmt.while_expr) loop
                    execute (stmt.while_blk);
                end loop;
            when REPEAT_STMT =>
                loop
                    execute (stmt.repeat_blk);
                    exit when evaluate (stmt.repeat_expr);
                end loop;
            when PRINT_STMT =>
                put (integer'image (evaluate(stmt.print_expr)));
            when IF_STMT =>
                if evaluate(stmt.if_expr) then
                    execute (stmt.if_blk1);
                else
                    execute (stmt.if_blk2);
                end if;
        end case;
   end execute;

end statements;
