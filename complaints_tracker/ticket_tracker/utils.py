import json
import sys

from websocket import create_connection


def broadcast(**kwargs):
    try:
        ws = create_connection('ws://localhost:8000/chat', timeout=0.5)
        message = {k: v for k, v in kwargs.items()}
        ws.send(json.dumps(message))
        ws.close()
    except Exception, e:
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        print e.args