def increment_or_decrement_1(
    # $$ def signature_fragment():
    increment: bool = True
    # $$ :end
    # $$ signature_fragment()
) -> int:
    # $$ def code_fragment(v):
    """If *increment* is True, return one more than *'$$ insert(v) $$'*,
    and otherwise, one less than *'$$ insert(v) $$'*.
    """
    return '$$ insert(v+1) $$' if increment else '$$ insert(v-1) $$'
    # $$ :end
    # $$ code_fragment(1)

def increment_or_decrement_2(
    # $$ signature_fragment()
) -> int:
    # $$ code_fragment(2)
