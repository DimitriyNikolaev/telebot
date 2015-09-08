__author__ = 'dimitriy'

import asyncio
import predefined_answers


def response_fn(response_count):
    def response_fn_decorator(fn):
        def wrapped(self, *args):
            if response_count == 1:
                one = self.get_response_obj()
                self.response.append(fn(self, one, *args))
            else:
                many = [self.get_response_obj() for x in range(response_count)]
                self.response = fn(self, many, *args)
            return self.response
        return wrapped
    return response_fn_decorator


class TeleBot(object):

    COMMANDS = {
        'start': 'start_response',
        'help': 'help_response',
        'помощь': 'help_response'
    }

    def __init__(self, loop, **kwargs):
        self.message = TMessage(**kwargs.get('message'))
        self.update_id = kwargs.get('update_id')
        self.response = []
        self.eloop = loop

    @asyncio.coroutine
    def get_response(self):
        command, *arguments = self.message.text.split(" ", 1)
        method_name = self.COMMANDS.get(command.lower())
        if hasattr(self, method_name):
            response = yield from getattr(self, method_name)(*arguments)
            return response
        return None

    def get_response_obj(self):
        return {'msg': {'chat_id': self.message.chat.chat_id}}  # , 'reply_to_message_id': self.message.message_id}}

    @staticmethod
    def set_text(resp, text):
        resp['msg']['text'] = text
        resp['method'] = 'sendMessage'

    @staticmethod
    def set_location(resp, x, y):
        resp['msg']['longitude'] = y
        resp['msg']['latitude'] = x
        resp['method'] = 'sendLocation'

    @asyncio.coroutine
    @response_fn(2)
    def start_response(self, resp, *args):
        TeleBot.set_text(resp[0], """Самое популярное сегодня
        http://www.blog-fiesta.com/spb/news/v-gorode-poyavilsya-besplatnyy-prokat-samokatov/""")
        #TeleBot.set_response_text(resp[1], """Бесплатно кататься на самокате Oxelo Town 9 можно аж 3 часа. Щедрое предложение от BGL (наб. Фонтанки, 96 и Московский пр., 159) и спортивного гипермаркета Decathlon будет действовать до конца сентября. """)
        TeleBot.set_location(resp[1], 59.87696, 30.35932)
        return resp

    @asyncio.coroutine
    @response_fn(1)
    def help_response(self, resp,  *args):
        TeleBot.set_text(resp, predefined_answers.HELP_MESSAGE)
        return resp

    @asyncio.coroutine
    @response_fn(1)
    def undefined_command_response(self, resp, *args):
        TeleBot.set_text(resp, predefined_answers.UNDEFINED_COMMAND_MESSAGE)
        return self.response


class TMessage(object):
    def __init__(self, **kwargs):
        if kwargs:
            self.chat = TChat(**kwargs.get('chat'))
            self.user_from = TUser(**kwargs.get('from'))
            self.date = kwargs.get('date')
            self.message_id = kwargs.get('message_id')
            self.text = kwargs.get('text')
            if self.text.startswith('/'):
                self.text = self.text[1:]


class TUser(object):
    def __init__(self, **kwargs):
        if kwargs:
            self.chat_id = kwargs.get('id')
            self.first_name = kwargs.get('first_name')
            self.last_name = kwargs.get('last_name')
            self.username = kwargs.get('username')


class TChat(TUser):
    def __init__(self, ** kwargs):
        super(TChat, self).__init__(**kwargs)
        self.title = kwargs.get('title')
