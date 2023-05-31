import email
import getpass
from email.header import decode_header
from imaplib import IMAP4_SSL, IMAP4


class Imap:
    @staticmethod
    def decode(list_data: list) -> str:
        result = []

        for data_tuple in list_data:
            data, charset = data_tuple

            if charset is not None:
                result.append(data.decode(charset))
                continue

            if isinstance(data, bytes):
                result.append(data.decode())
                continue

            result.append(data)

        return ', '.join(result)

    def get_messages(self, params: dict) -> list:
        server = None

        try:
            server = IMAP4_SSL(params['addr'], params['port']) \
                      if params.get('ssl') else IMAP4(params['addr'], params['port'])
        except ConnectionRefusedError as e:
            return [f'Error: {e}']

        params['password'] = getpass.getpass('Введите пароль: ')

        status = None
        msg = None

        try:
            status, msg = server.login(params.get('user'), params.get('password'))
        except IMAP4.error as e:
            return [f'Error: {e}']
        except UnicodeEncodeError:
            return ['Error: вводите пароль на русском']

        try:
            server.starttls()
        except IMAP4.abort as e:
            pass

        server.select('INBOX')
        status, message_ids = server.search(None, 'ALL')

        message_ids = message_ids[0].split()

        msgs = list()

        for ind in message_ids:
            id_value = int(ind.decode())

            if id_value < params.get('n1'):
                break

            if params.get('n2') != 'all' and params.get('n2') < id_value:
                break

            status, messages = server.fetch(ind, '(RFC822)')
            data = messages[0][1]

            msg = email.message_from_bytes(data)

            sender = self.decode(decode_header(msg['From']))
            subject = self.decode(decode_header(msg['Subject']))

            to = msg['To']
            date = msg['Date']

            message_size = len(data)

            msgs.append(
                f'\n'
                f'Message, '
                f'from: {sender}, to: {to}, '
                f'subject: {subject}, date: {date}, '
                f'message size: {message_size}\n'
            )

        server.close()
        server.logout()

        return msgs
