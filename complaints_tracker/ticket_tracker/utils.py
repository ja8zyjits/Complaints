from websocket import create_connection
import json


def broadcast(user_id, location, function):
    try:
        ws = create_connection('ws://localhost:8000/chat', timeout=0.5)
        message = {'user_id': user_id, 'location': location, 'function': function}
        ws.send(json.dumps(message))
        ws.close()
    except Exception, e:
        pass