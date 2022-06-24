import json

from flask import Flask
from flask import request
from .classes import CreateOptimizerRequest
from .classes import DeleteOptimizerRequest
from .classes import InputOptimizerRequest
from .bo_optimizer import *

app = Flask(__name__)


@app.route('/optimizer/create', methods=['POST'])
def create_optimizer():
    if request.method == 'POST':
        json_dict = request.json
        create_opt = CreateOptimizerRequest(json_dict['nodeId'], json_dict['maxConcurrency'],
                                            json_dict['maxParallelism'], json_dict['maxPipelining'],
                                            json_dict['maxChunkSize'])
        print(create_opt.__str__())
        bo_optimizer.create_optimizer(create_opt)
        return ('', 204)


@app.route('/optimizer/input', methods=['POST'])
def input_to_optimizer():
    if request.method == 'POST':
        jd = request.json
        input_operation = InputOptimizerRequest(jd['nodeId'], jd['throughput'], jd['rtt'], jd['concurrency'],
                                                jd['parallelism'], jd['pipelining'], jd['chunkSize'])
        print(input_operation.__str__())
        try:
            return bo_optimizer.input_optimizer(input_operation), 200
        except KeyError:
            print("Failed to insert point as we have already tried this point: ")
    return '', 500


@app.route('/optimizer/delete', methods=['POST'])
def delete_optimizer():
    if request.method == 'POST':
        jd = request.json
        delete_op = DeleteOptimizerRequest(jd['nodeId'])
        print(delete_op.__str__())
        bo_optimizer.delete_optimizer(delete_op)
    return '', 204
