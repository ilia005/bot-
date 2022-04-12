def format_declension(number, singular, dual, plural):
    '''
    >>> format_declension(91, 'балл', 'балла', 'баллов')
    '91 балл'

    >>> format_declension(92, 'балл', 'балла', 'баллов')
    '92 балла'

    >>> format_declension(97, 'балл', 'балла', 'баллов')
    '97 баллов'
    '''
    if number % 100 in (11, 12, 13, 14):
        return f'{number} {plural}'

    d = number % 10
    if d == 1:
        return f'{number} {singular}'
    if d in (2, 3, 4):
        return f'{number} {dual}'

    return f'{number} {plural}'


def parse_request(message_text: str) -> dict[str, int]:
    words = message_text.split()
    try:
        subs = dict(zip(words[::2], map(int, words[1::2])))
        if not subs:
            raise ValueError('no subjects provided')
    except ValueError:
        return 'Некорректный ввод. Образец ввода: математика 80 русский 70 информатика 99'
    return subs
