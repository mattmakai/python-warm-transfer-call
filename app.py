import os
from flask import Flask, Response, request
from twilio import twiml
from twilio.rest import TwilioRestClient


app = Flask(__name__)
client = TwilioRestClient()

# this should be your Twilio number, format: +14155551234
CUSTOMER_SERVICE_NUMBER = os.environ.get('CUSTOMER_SERVICE_NUMBER', '')
# your cell phone number (agent's number), format: +14155551234
AGENT1_NUMBER = os.environ.get('AGENT1_NUMBER', '')
# second person's phone or Twilio number if testing, format: +14155551234
AGENT2_NUMBER = os.environ.get('AGENT2_NUMBER', '')
# ngrok URL, such as "https://17224f9e.ngrok.io", no trailing slash
BASE_URL = os.environ.get('BASE_URL', 'https://143e6ab2.ngrok.io')


@app.route('/call', methods=['POST'])
def inbound_call():
    call_sid = request.form['CallSid']
    response = twiml.Response()
    response.dial().conference(call_sid)
    call = client.calls.create(to=AGENT1_NUMBER,
                               from_=CUSTOMER_SERVICE_NUMBER,
                               url=BASE_URL + '/conference/' + call_sid)
    return Response(str(response), 200, mimetype="application/xml")


@app.route('/conference/<conference_name>', methods=['GET', 'POST'])
def conference_line(conference_name):
    response = twiml.Response()
    response.dial(hangupOnStar=True).conference(conference_name)
    response.gather(action=BASE_URL + '/add-agent/' + conference_name,
                    numDigits=1)
    return Response(str(response), 200, mimetype="application/xml")


@app.route('/add-agent/<conference_name>', methods=['POST'])
def add_second_agent(conference_name):
    client.calls.create(to=AGENT2_NUMBER, from_=CUSTOMER_SERVICE_NUMBER,
                        url=BASE_URL + '/conference/' + conference_name)
    response = twiml.Response()
    response.dial(hangupOnStar=True).conference(conference_name)
    return Response(str(response), 200, mimetype="application/xml")


# this function is optional - for testing purposes if you don't have
# a third phone to call
@app.route('/agent-johnson-test', methods=['POST'])
def agent_johnson_test():
    response = twiml.Response()
    response.say("Hello, this is Agent Johnson.", loop=10)
    return Response(str(response), 200, mimetype="application/xml")


if __name__ == '__main__':
    app.run(debug=True)

