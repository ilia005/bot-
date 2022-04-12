import os


def filter_not_printable(text):
    return ''.join(x for x in text if x.isprintable() or x.isspace())


for filename in os.listdir():
    if filename.startswith('vuz'):
        with open(filename) as file:
            text = file.read()
        text = filter_not_printable(text)
        with open(filename, 'w') as file:
            file.write(text)
