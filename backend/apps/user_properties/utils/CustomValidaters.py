from django.core.exceptions import ValidationError
import re

# id username に登録できない文字
# - 特殊文字やメンション用に @ は不可にする場合
def validate_bad_id_username_words(value:str) -> bool:

    # 許可しない文字
    bad_words = ['@', '＠']
    # 1 文字目に許可する文字
    first_letter_sucsess_words_unicode = (
        '[\u3040-\u309f\u30a0-\u30ff\uff61-\uff9f' # ひらがな・カタカナ（全角/半角）
        '\u4e00-\u9fff\u3005-\u3007'               # 漢字・々など
        '\u0041-\u005a\u0061-\u007a'               # A-Z, a-z
        '\u0030-\u0039'                            # 0-9
        '\uff21-\uff3a\uff41-\uff5a\uff10-\uff19]' # 全角英数
    )

    for word in bad_words:
        if word in value:
            raise ValidationError(f'{bad_words} は登録できません', params={'value': value},)

    first_letter_value    = value[0]
    sucsess_words_compile = re.compile(first_letter_sucsess_words_unicode)
    hit                   = sucsess_words_compile.match(first_letter_value)
    if hit is None:
        raise ValidationError(f'1 文字目に登録できない文字が含まれています', params={'value': value},)
    return True