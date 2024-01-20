# $$ def some_inlined_computation(times, acc):
for macro_var_i in range('$$ insert(times) $$'):
    '$$ insert(acc) $$' = 1
# $$ :end
j = k = 0
# $$ some_inlined_computation(3, "j")
if True:
    # $$ some_inlined_computation(2, "k")
