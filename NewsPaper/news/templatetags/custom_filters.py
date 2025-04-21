from django import template

register = template.Library()

DELETE_WORDS = {1:'редиска', 2:'огурец'
                }

def _search(list, item):
    if list.get(item):
        return list.get(item)
    return False


@register.filter()
def censor(content):
    content = content.lower()
    for i in range(1, len(DELETE_WORDS) + 1):
        if _search(DELETE_WORDS, i) in content:
            word = _search(DELETE_WORDS, i)
            edit_word = _search(DELETE_WORDS, i)[0] + (len(word) - 1) * '*'
            content = content.replace(word, edit_word)

    return content



