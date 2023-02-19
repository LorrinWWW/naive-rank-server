from flask import Flask
from flask import request
import threading
import time
import json
import random

sem = threading.Semaphore()

rank_store = {}

app = Flask(__name__)

@app.route('/')
def index():
    return 'The rank server is running!'

@app.route("/rank/<job_id>",methods=['POST'])
def rank(job_id):
    sem.acquire()
    
    data = request.json
    
    if job_id in rank_store:
        rank = rank_store[job_id]['count']
        rank_store[job_id]['count'] += 1
    else:
        rank = 0
        rank_store[job_id] = {
            'prime_ip': data.get('ip', '127.0.0.1'),
            'nccl_port': data.get('port', random.randint(10000, 20000)),
            'count': 1,
        }
        
    return_data = {
        'prime_ip': rank_store[job_id].get('prime_ip', '127.0.0.1'),
        'nccl_port': rank_store[job_id].get('nccl_port', '8181'),
        'rank': rank,
    }
        
    return_data = json.dumps(return_data)

    sem.release()
    return return_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)