
import json
import time

from flask import Flask, request
from flask import Response
from flask import render_template

app = Flask(__name__)


def get_message():
    """this could be any function that blocks until data is ready"""
    time.sleep(1)
    s = time.ctime(time.time())
    return json.dumps(['目前時間：' + s , 'a'], ensure_ascii=False)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/stream', methods=['POST'])
def stream():
    data = request.json
    print(json.dumps(data))
    
    def eventStream():
        for c in 'Hello world!':
            data = {
                "id":"chatcmpl-98mr8zE8BKcX4vNFlGXauESQ4mwyH",
                "object":"chat.completion.chunk",
                "created":1711881454,
                "model":"gpt-3.5-turbo-0125",
                "system_fingerprint":"fp_3bc1b5746c",
                "choices":[
                    {
                        "index":0,
                        "delta":{"content":c},
                        "logprobs":None,
                        "finish_reason":None
                    }
                ]
            }
            response = "data: {}\n\n".format(json.dumps(data))
            yield response
            time.sleep(0.5)
        yield "data: [DONE]\n\n"
    return Response(eventStream(), mimetype="text/event-stream")

@app.route("/stream1")
def stream1():
    def eventStream():
        for c in 'hello-world':
            # Poll data from the database
            # and see if there's a new message
            yield "data: {}\n\n".format(c)
    return Response(eventStream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run()   
