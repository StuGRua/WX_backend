import base64
import datetime

import requests, json


class TestPart1:
    def __init__(self, acc='201873030', pas='value22', url='http://127.0.0.1:5000'):
        self.token = testlogin(acc, pas)
        self.url = url

    def test_pub(self):
        url_json = self.url + '/api/publish_order'
        serect = self.token
        serect = str(base64.b64encode(serect.encode("utf-8")), "utf-8")
        headers = {'Content-Type': "application/json", "Authorization": "Basic {}".format(serect)}
        data_json = json.dumps(
            {'order_title': '测试2', 'start_time': '2021-04-13', 'end_time': '2021-04-14', 'order_payment': 'test2',
             'order_info': 'test2'})  # dumps：将python对象解码为json数据
        r_json = requests.post(url_json, headers=headers, data=data_json)
        print(data_json)
        print(r_json.json())
        res = dict(r_json.json())
        print('order:',res['order_id'])
        return res['order_id']

    def test_del(self):
        url_json = self.url + '/api/publish_order'
        print(url_json)
        serect = self.token
        serect = str(base64.b64encode(serect.encode("utf-8")), "utf-8")
        headers = {'Content-Type': "application/json", "Authorization": "Basic {}".format(serect)}
        ord=self.test_pub()
        data_json = json.dumps(
            {'order_id': ord})  # dumps：将python对象解码为json数据
        r_json = requests.post(url_json, headers=headers, data=data_json)
        print(data_json)
        print(r_json.json())


def testsignin():
    url_json = 'http://127.0.0.1:5000/api/users'
    headers = {'Content-Type': 'application/json'}
    data_json = json.dumps(
        {'userid': 201873030, 'password': 'value22', 'phonenumber': 13888071504})  # dumps：将python对象解码为json数据
    r_json = requests.post(url_json, headers=headers, data=data_json)
    print(data_json)
    print(r_json.headers)
    print(r_json.raw)


def testrequest(userid):
    url_json = 'http://127.0.0.1:5000/api/users/' + userid
    r_json = requests.get(url_json)
    print(r_json.headers)
    print(r_json.content)


def testlogin(acc, pas):
    url = 'http://127.0.0.1:5000/api/token'
    serect = acc + ":" + pas
    serect = str(base64.b64encode(serect.encode("utf-8")), "utf-8")
    print(serect)
    headers = {"Authorization": "Basic {}".format(serect)}
    r_json = requests.get(url, headers=headers, data='')
    res = dict(r_json.json())
    print(res['token'])
    return res['token']


def test_publish(token):
    url_json = 'http://127.0.0.1:5000/api/publish_order'
    serect = token + ":" + ''
    serect = str(base64.b64encode(serect.encode("utf-8")), "utf-8")
    headers = {'Content-Type': "application/json", "Authorization": "Basic {}".format(serect)}
    data_json = json.dumps(
        {'order_title': '测试1', 'start_time': '2021-04-10 02:00', 'end_time': '2021-04-11 03:00', 'order_payment': 'test1',
         'order_info': 'test1'})  # dumps：将python对象解码为json数据
    print(headers)
    r_json = requests.post(url_json, headers=headers, data=data_json).json()
    #print(data_json)
    # print(r_json.json())
    res_=dict(r_json)['order_id']
    print(res_)
    return res_,serect

def test_del(token):
    url_json = 'http://127.0.0.1:5000/api/del_order'
    print(url_json)
    # serect = token
    # serect = str(base64.b64encode(serect.encode("utf-8")), "utf-8")
    order,token_ = test_publish(token)
    headers = {'Content-Type': "application/json", "Authorization": "Basic {}".format(token_)}

    print('del:',1)
    data_json = json.dumps({'order_id': 1})  # dumps：将python对象解码为json数据
    r_json = requests.post(url_json, headers=headers, data=data_json)
    print(headers)
    print(r_json)



def testres(token):
    url = 'http://127.0.0.1:5000/api/resource'
    serect = token + ":" + ''
    serect = str(base64.b64encode(serect.encode("utf-8")), "utf-8")
    headers = {"Authorization": "Basic {}".format(serect)}
    print(headers)
    r_json = requests.get(url, headers=headers, data='')
    print(r_json.json())
    s = ''
    s.split()


def test_all_undo_order(token):
    url_json = 'http://127.0.0.1:5000/api/all_undo_order'
    serect = token + ":" + ''
    serect = str(base64.b64encode(serect.encode("utf-8")), "utf-8")
    headers = {'Content-Type': "application/json", "Authorization": "Basic {}".format(serect)}
    data_json = json.dumps({})  # dumps：将python对象解码为json数据
    r_json = requests.get(url_json, headers=headers, data=data_json)
    print(data_json)
    print(r_json.json())


if __name__ == '__main__':
    # testsignin()
    # testrequest('201873030')
    token = testlogin('201873030', 'value22')
    # testres(token)
    #test_publish(token)
    test_del(token)
    # test_all_undo_order(token)
    # test_1=TestPart1()
    # test_1.test_del()