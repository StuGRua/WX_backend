import json

from flask import make_response, abort


def response_err(err_type, stat="400 status"):
    resp = make_response(json.dumps({'err_type': err_type}))
    resp.status = stat
    return resp
