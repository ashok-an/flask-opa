import json
import logging
import os

from flask import Flask, jsonify, request, Response, abort
from flask_restx import Api, Resource
import requests


################################################
## initializations
################################################
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

app = Flask(__name__)
api = Api(version='1.0', title='Simple List, Read, Delete',
  description='Simple CRUD API based on The Office character list', authorizations=authorizations)
api.init_app(app)
app.logger.setLevel(logging.DEBUG)


opaUrl = os.environ.get("OPA_URL", "http://localhost:8181/v1/data/example/allow")


################################################
## load data
################################################
with open('data.json', 'r') as fd:
  data = json.load(fd)


################################################
## CRUD operations
################################################
def add_employee(inputJson):
  global data
  if emp in data:
    return False
  else:
    data.update(inputJson)
    return True

def get_employee(emp):
  global data
  return data.get(emp, {})

def set_employee(emp, inputJson):
  global data
  if emp in data:
    data[emp] = inputJson
    return True
  else:
    return False

def del_employee(key):
  global data
  try:
    del data[key]
  except KeyError:
    return False
  else:
    return True


################################################
## OPA
################################################
@app.before_request
def check_authorization():
    method = request.method 
    path = request.path.strip().split("/")[1:] # last part
    user = request.headers.get("Authorization", "")

    try:
        opaInput = json.dumps({'input': {'method': method, 'path': path, 'user': user}})
        app.logger.info("OPA query:{} Body:{}".format(opaUrl, opaInput))

        response = requests.post(opaUrl, data=opaInput)
    except Exception as e:
        app.logger.exception("Unexpected error querying OPA.")
        abort(500)

    app.logger.warn("OPA status code:{} Body:{} Text:{}".format(response.status_code, response.json(), response.text))
    if response.status_code != 200:
        abort(500)

    allowed = response.json()
    app.logger.info("OPA result: {}".format(allowed))

    if allowed.get('result', ''):
      return

    abort(403)


################################################
## routes
################################################
@api.route('/office', methods=['GET', 'POST'])
class GetAll(Resource):
  def get(self):
    names = sorted(data.keys())
    return jsonify({'employees': names})

  @api.doc(security='apikey')
  def post(self):
    return {'message': str(add_employee(request.json))}
    


@api.route('/office/<string:employee>', methods=['GET', 'PUT', 'DELETE'])
class Employee(Resource):
  @api.doc(security='apikey')
  def get(self, employee):
    output = get_employee(employee)
    return output if output else {'message': 'lookup failed'}

  @api.doc(security='apikey')
  def put(self, employee):
    return {'message': str(set_employee(employee, request.json))}
    
  @api.doc(security='apikey')
  def delete(self, employee):
    return {'message': str(del_employee(employee))}


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=12345)
