from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.auth import login_required

class MachineDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Allow only Managers and Supervisors to connect
        if self.scope['user'].role in ['manager', 'supervisor']:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def send_machine_data(self, data):
        await self.send(text_data=json.dumps(data))

