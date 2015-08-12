import os
from flask import Flask, Response, request, url_for
from twilio import twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)
client = TwilioRestClient()

# this should be your Twilio number
CUSTOMER_SERVICE_NUMBER = os.environ.get('CUSTOMER_SERVICE_NUMBER', '')
AGENT1_NUMBER = os.environ.get('AGENT1_NUMBER', '')
AGENT2_NUMBER = os.environ.get('AGENT2_NUMBER', '')
# ngrok URL, such as "https://17224f9e.ngrok.com"
BASE_URL = os.environ.get('BASE_URL', '')

# does not need to be changed, it's just the name of the conference call
CONFERENCE_NAME = 'Warm Call Transfer Example'


@app.route('/call', methods=['POST'])
def inbound_call():
    response = twiml.Response()
    response.dial().conference(CONFERENCE_NAME)
    client.calls.create(to=AGENT1_NUMBER, from_=CUSTOMER_SERVICE_NUMBER,
                        url=BASE_URL + '/conference')
    return Response(str(response), 200, mimetype="application/xml")


@app.route('/conference', methods=['POST'])
def conference_line():
    response = twiml.Response()
    response.dial(hangupOnStar=True).conference(CONFERENCE_NAME)
    response.gather(action=BASE_URL + '/add-agent', numDigits=1)
    return Response(str(response), 200, mimetype="application/xml")


@app.route('/add-agent', methods=['POST'])
def add_second_agent():
    client.calls.create(to=AGENT2_NUMBER, from_=CUSTOMER_SERVICE_NUMBER,
                        url=BASE_URL + '/conference')
    response = twiml.Response()
    response.dial(hangupOnStar=True).conference(CONFERENCE_NAME)
    return Response(str(response), 200, mimetype="application/xml")


if __name__ == '__main__':
    app.run(debug=True)
