from flask import Flask, Response
from twilio import twiml

app = Flask(__name__)


@app.route('/call')
def inbound_call():
    response = twiml.Response()
    response.dial().conference('handoff')
    return Response(str(response), 200, mimetype="application/xml")


if __name__ == '__main__':
    app.run(debug=True)
