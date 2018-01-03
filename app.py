import sys
import urllib3
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = ''
WEBHOOK_URL = ''

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'help',
        'usr',
		'state1',
		'state2',
    ],
    transitions=[
		{
			'trigger': 'init',
			'source': [
			    'help',
				'state1',
				'state2',
			],
			'dest': 'usr',
			'conditions': 'is_going_to_usr'
		},
		{
		    'trigger': 'go',
            'source': 'usr',
            'dest': 'help',
            'conditions': 'is_going_to_help'
		},
        {
            'trigger': 'go',
            'source': 'usr',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'go',
            'source': 'usr',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'go',
            'source': 'state1',
            'dest': 'state2',
            'conditions': 'state1_is_going_to_state2'  
        }
    ],
    initial='usr',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.go(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
