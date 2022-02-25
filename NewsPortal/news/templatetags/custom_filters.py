from django import template

register = template.Library()


@register.filter(name='censor')
def censor(text):
    cens_list = ['word1', 'word2', 'wo3']
    for word in cens_list:
        text = text.replace(word, '*' * len(word))
    return text
