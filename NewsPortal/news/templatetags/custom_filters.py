from django import template

register = template.Library()


class TypeException(Exception):
    pass


@register.filter(name='censor')
def censor(text):
    if type(text) != str:
        raise TypeException(f'Объект <{text}> не является строкой! Нельзя применить фильтр "Цензор"!')

    cens_list = ['word1', 'word2', 'wo3']
    text_lower = text.lower()
    for word in cens_list:
        begin_index = 0
        replace_id = True
        while replace_id:
            replace_index = text_lower[begin_index:].find(word) + begin_index
            if (replace_index - begin_index) == -1:
                replace_id = False
            else:
                begin_index = replace_index + len(word)
                text = text[:replace_index + 1] + '*' * (len(word) - 1) + text[begin_index:]
                text_lower = text_lower[:replace_index + 1] + '*' * (len(word) - 1) + text_lower[begin_index:]
    return text
