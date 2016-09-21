import json
import requests
import threading
from flask import Flask, jsonify

AUTOREGISTER_MODE = 'AUTOREGISTER_MODE'
NORMAL_MODE = 'NORMAL_MODE'

def autoregister(app, name, info, swagger, mode, ct_url=False, url=False, active=True):
  payload = {'name': name, 'url': url, 'active': active}
  r = requests.post(ct_url+'/api/v1/microservice', json=payload)
  if r.status_code != 200:
    raise ValueError('microservice has not been registered')

def register(app, name, info, swagger, mode, ct_url=False, url=False, active=True):
  """"""
  if mode == AUTOREGISTER_MODE:
    t = threading.Timer(5.0, autoregister, [app, name, info, swagger, mode, ct_url, url, active])
    t.start()

  @app.route('/info')
  def get_info():
    info['swagger'] = swagger
    return jsonify(info) #@TODO: JSONAPI format

  @app.route('/ping')
  def get_ping():
    return "pong"
