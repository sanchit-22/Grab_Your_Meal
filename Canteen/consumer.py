import json
from channels.generic.websocket import WebsocketConsumer
from random import randint
from time import sleep
from User.models import currentorder

class WSConsumer(WebsocketConsumer):

    def connect (self):
        self.accept()
        all_orders=currentorder.objects.all()
        for i in range(10000):
            self.send(json.dumps({'message': randint(1,1000)}))
            sleep(1)