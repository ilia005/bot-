from user import User

u = User(0)

while True:
    msg = input('Введите запрос: ').lower()
    if msg == 'выход':
        break

    print(u.handle_request(msg))
