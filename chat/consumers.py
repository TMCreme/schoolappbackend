from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from django.contrib.auth.models import UserManager
# from django.core.checks import messages
from home.models import BaseUser
from .models import Message




class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        # response to client, that we are connected.
        self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.my_name,
            self.channel_name
        )

    # Receive message from client WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json['type']

        if eventType == 'login':
            name = text_data_json['data']['name']

            # we will use this as room name as well
            self.my_name = name

            # Join room
            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )
        
        if eventType == 'call':
            name = text_data_json['data']['name']
            print(self.my_name, "is calling", name);
            # print(text_data_json)


            # to notify the callee we sent an event to the group name
            # and their's groun name is the name
            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'answer_call':
            # has received call from someone now notify the calling user
            # we can notify to the group with the caller name
            
            caller = text_data_json['data']['caller']
            # print(self.my_name, "is answering", caller, "calls.")

            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'ICEcandidate':

            user = text_data_json['data']['user']

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

    def call_received(self, event):

        # print(event)
        print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))


    def call_answered(self, event):

        # print(event)
        print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data']
        }))


    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({
            'type': 'ICEcandidate',
            'data': event['data']
        }))

    # def init_chat(self, data):
    #     username = data["username"]
    #     user, created = BaseUser.objects.get_or_create(username=username)
    #     content = {
    #         'command': 'init_chat'
    #     }

    #     if not user:
    #         content['error']  = "Unable to get or create User with Username: " + username
    #         self.send_message(content)

    #     content['sucesss'] = "Chatting in with success with username: "+ username
    #     self.send_message(content)

    # def fetch_message(self, data):
    #     messages = Message.last_50_messages()
    #     content = {
    #         'command': 'messages',
    #         'messages': self.messages_to_json(messages)
    #     }
    #     self.send_message(content)

    
    # def new_message(self, data):
    #     author = data["from"]
    #     text = data["text"]
    #     author_user, created = BaseUser.objects.get_or_create(username=author)
    #     message = Message.objects.create(author=author_user, content=text)
    #     content = {
    #         'command': 'new_message',
    #         'message':self.message_to_json(message)
    #     }
    #     self.send_chat_message(content)

    # def messages_to_json(self, messages):
    #     result = []
    #     for message in messages:
    #         result.append(self.message_to_json(message))
    #     return result

    # def message_to_json(self, message):
    #     return {
    #         "id" : str(message.id),
    #         "author" : message.author.username,
    #         "content": message.content,
    #         "created_at": str(message.created_at)
    #     }

    # commands = {
    #     "init_chat":init_chat,
    #     "fetch_messages":fetch_message,
    #     "new_message": new_message
    # }


    # def connect(self):
    #     self.room_name = "room"
    #     self.room_group_name = "chat_%s" % self.room_name

    #     async_to_sync(self.channel_layer.group_add)(
    #         self.room_group_name, 
    #         self.channel_name
    #     )
    #     self.accept()

    # def disconnect(self, close_code):
    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.room_group_name, 
    #         self.channel_name
    #     )

    # def receive(self, text_data):
    #     data = json.loads(text_data)
    #     self.commands[data['command']](self, data)



    
    # def send_message(self, message):
    #     self.send(text_data=json.dumps(message))

    # def send_chat_message(self, message):
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name, 
    #         {
    #             "type":"chat_message",
    #             "message":message
    #         }
    #     )

    # def chat_message(self, event):
    #     message = event["message"]
    #     self.send(text_data=json.dumps(message))










