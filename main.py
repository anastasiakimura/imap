import sys

from imap import Imap


def parse_args(args: list) -> dict:
    params = dict()

    if '-h' in args or '--help' in args:
        params['is_help_msg'] = True
        params['help_text'] = '-h/--help - справка\n' \
                              '--ssl - разрешить использование ssl, если сервер поддерживает ' \
                              '(по умолчанию не использовать).\n' \
                              '-s/--server - адрес (или доменное имя) ' \
                              'IMAP-сервера в формате адрес[:порт] (порт по умолчанию 143).\n' \
                              '-n N1 [N2] - диапазон писем, по умолчанию все.\n' \
                              '-u/--user - имя пользователя, ' \
                              'пароль спросить после запуска и не отображать на экране.\n'
        return params

    params['is_help_msg'] = False
    params['ssl'] = False

    if '--ssl' in args:
        params['ssl'] = True

    if '-n' not in args:
        print('Введите диапозон значений')
        return dict()

    try:
        params['n1'] = int(args[args.index('-n') + 1])
    except ValueError:
        print('Введите значение n1')
        return dict()

    try:
        params['n2'] = int(args[args.index('-n') + 2])
    except ValueError:
        params['n2'] = 'all'

    if params['n2'] != 'all' and params['n1'] > params['n2']:
        print('Вы ввели некорректный диапозон значений')
        return dict()

    if '-u' not in args and '--user' not in args:
        print('Вы не ввели имя пользователя')
        return dict()

    user_key = '-u'

    if '--user' in args:
        user_key = '--user'

    params['user'] = args[args.index(user_key) + 1]

    if '-s' not in args and '--server' not in args:
        print('Вы не ввели адрес IMAP-сервера')
        return dict()

    server_key = '-s'

    if '--server' in args:
        server_key = '--server'

    server = args[args.index(server_key) + 1]

    double_dot_index = server.find(':')

    if double_dot_index == -1:
        params['addr'] = server
        params['port'] = 143
    else:
        params['addr'] = server[0:server.find(':')]
        params['port'] = int(server[(server.find(':') + 1):len(server)])

    return params


def main():
    params = parse_args(sys.argv)

    if params.get('is_help_msg'):
        print(params.get('help_text'))
        return

    for message in Imap().get_messages(params):
        print(message)


if __name__ == '__main__':
    main()
