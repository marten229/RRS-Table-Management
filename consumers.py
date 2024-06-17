import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TableConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("table_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("table_updates", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "table_updates",
            {
                'type': 'table_update',
                'message': data['message']
            }
        )

    async def table_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
