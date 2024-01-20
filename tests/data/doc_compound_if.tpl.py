# $$ import datetime
# $$ d = datetime.date.today()
# $$ if d > datetime.date(2024, 1, 1):
# $$ code_block = 1
# This comes from the first macro code block, number '$$ insert(code_block) $$'
print('January 1st, 2024, or later')
# $$ else:
# This comes from the second macro code block, number '$$ insert(code_block) $$'
print('Earlier than January 1st, 2024')
# $$ :end
