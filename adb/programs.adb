package body programs is

   --------------------
   -- create_program --
   --------------------

    function create_program (blk: in block) return program is
        prog: program;
    begin
        prog.blk := blk;
        return prog;
   end create_program;

   -------------
   -- execute --
   -------------

   procedure execute (prog: in program) is
    begin
        execute (prog.blk);
   end execute;

end programs;
