import datetime
import json

from flask import jsonify, abort, request, make_response
from flask import url_for
from model.model import *
from utils.ResToOrder import OrderToDict, OrderToDict_withP
from utils.ResponseStat import *
from utils.timestampFix import *

# WX_APPID = 'wx933173854a5a9ba2'
# WX_SECRET = 'ebf07d30198d42d3322fcbc82c996f9e'


# 具体导入配
# 根据需求导入仅供参考


@app.route('/api/server_time', methods=['GET'])
def server_time():
    return jsonify({'server_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})


# 注册
# http方式：POST
# 成功：返回userid,状态码201
# 失败: 返回400 'existing user'/'missing arguments'
# 接口需要的 data:{userid,phonenumber,password,user_name,major,grade}
# 备注：user_status默认为'OK'
@app.route('/api/users', methods=['POST'])
def new_user():
    print(request.json)
    rqjson = request.json
    userid = rqjson.get('userid')
    phonenumber = rqjson.get('phonenumber')
    password = rqjson.get('password')
    user_name = rqjson.get('user_name')
    major = rqjson.get('major')
    grade = rqjson.get('grade')
    if userid is None or password is None or phonenumber is None:
        resp = response_err('missing arguments', "400 status")
        # resp = make_response(json.dumps({'err_type':'missing arguments'}))
        # resp.status = "400 status"
        abort(resp)  # missing arguments
    if User.query.filter_by(userid=userid).first() is not None or User.query.filter_by(
            phonenumber=phonenumber).first() is not None:
        # resp = make_response(json.dumps({'err_type':'existing user'}))
        # resp.status = "400 status"
        resp = response_err('existing user', "400 status")
        abort(resp)  # existing user
    user = User(userid=userid, phonenumber=phonenumber, user_name=user_name, major=major, grade=grade)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'userid': user.userid}), 201,
            {'Location': url_for('get_user', id=user.userid, _external=True)})


# 修改用户信息
# http方式：POST
# 成功：返回userid,状态码201
# 失败: 返回400
# 接口需要的 data:{user_name,major,grade}
# 备注：user_status默认为'OK'
@app.route('/api/modify_user', methods=['POST'])
def modify_user():
    print(request.json)
    rqjson = request.json
    userid = g.user.userid

    user_name = rqjson.get('user_name')
    major = rqjson.get('major')
    grade = rqjson.get('grade')
    if userid is None or grade is None or user_name is None:  # missing arguments
        resp = response_err('missing arguments', "400 status")
        abort(resp)  # no existing user
    pre_fix = db.session.query(User).filter(User.userid == userid).first()
    if pre_fix is None:
        resp = response_err('no existing user', "400 status")
        abort(resp)  # no existing user

    pre_fix.update(
        {'user_name': user_name, 'major': major, 'grade': grade})

    db.session.commit()
    return (jsonify({'userid': g.user.userid}), 201,
            {'Location': url_for('get_user', id=g.user.userid, _external=True)})


# 获得 公共可见 账户信息
# http方式：GET
# 成功：返回userid,user_name,状态码201
# 失败: 返回400
# 接口需要的 data:{}
# 备注：user_status默认为'OK'
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        resp = response_err('no existing user', "400 status")
        abort(resp)  # no existing user
    return jsonify({'userid': user.userid, 'user_name': user.user_name})


# 获得 当前用户 账户信息
# http方式：GET
# 成功：返回userid,user_name,状态码201
# 失败: 返回400
# 接口需要的 data:{}
# 备注：需要验证
@app.route('/api/my_user_info')
@auth.login_required
def get_my_user():
    user = db.session.query(User).filter(User.userid == g.user.userid).first()
    if not user:
        resp = response_err('no existing user', "400 status")
        abort(resp)  # no existing user
    return jsonify(
        {'userid': user.userid, 'phonenumber': user.phonenumber, 'user_name': user.user_name, 'major': user.major,
         'grade': user.grade, 'user_status': user.user_status,
         'sync_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})


# 获得令牌or登陆
# http方式：GET
# 成功：返回userid,状态码201
# 失败: 返回验证失败
# 接口需要的 data:{}
# 备注：需要验证
@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token, 'duration': 600, 'user_name': g.user.user_name})


# 验证是否成功登陆
# http方式：GET
# 成功：返回userid
# 失败: 返回验证失败
# 接口需要的 data:{}
# 备注：需要验证
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.userid})


# 待接单列表
# http方式：GET
# 成功：返回 全部 未接受的订单
# 失败: 返回验证失败
# 接口需要的 data:{}
# 备注：需要验证
@app.route('/api/all_undo_order')
@auth.login_required
def all_undo_order():
    pre_res = db.session.query(Order).filter(Order.order_stat == '未接受').all()
    res = OrderToDict(pre_res)
    return jsonify(res), 201


# 我发布的订单列表
# http方式：GET
# 成功：返回 全部 当前用户 发布 的订单
# 失败: 返回验证失败
# 接口需要的 data:{}
# 备注：需要验证
@app.route('/api/my_order_pub')
@auth.login_required
def my_order_pub():
    # res = Order.query.filter_by(pub_id=g.user.userid).all()
    res = db.session.query(User, Order).outerjoin(Order, Order.pub_id == User.userid).filter(
        Order.pub_id == g.user.userid)
    res = OrderToDict_withP(res)
    return jsonify(res), 201


# 我接受的订单列表
# http方式：GET
# 成功：返回 全部 当前用户 接受 的订单
# 失败: 返回验证失败
# 接口需要的 data:{}
# 备注：需要验证
@app.route('/api/my_order_recv')
@auth.login_required
def my_order_recv():
    res = db.session.query(User, Order).outerjoin(Order, Order.pub_id == User.userid).filter(
        Order.rec_id == g.user.userid)
    # res = Order.query.join(User,Order.pub_id==User.userid).filter(User.userid==g.user.userid).all()
    # res = Order.query.filter_by(rec_id=g.user.userid)
    res = OrderToDict_withP(res)
    return jsonify(res), 201


# 发布新订单
# http方式：POST
# 成功：返回 data:{order_id,order_title}
# 失败: 返回验证失败
# 接口需要的 data:{order_title, pub_id, start_time, end_time,order_payment, order_info}
# 备注：需要验证
@app.route('/api/publish_order', methods=['POST'])
@auth.login_required
def publish_order():
    rqjson = request.json
    print(rqjson)
    order_title = rqjson.get('order_title')
    pub_id = g.user.userid
    # rec_id=rqjson.get('rec_id')
    # start_time = datetime.datetime.strptime(rqjson.get('start_time'), '%Y-%m-%d %H:%M')
    # end_time = datetime.datetime.strptime(rqjson.get('end_time'), '%Y-%m-%d %H:%M')
    start_time = StrtoStamp(rqjson.get('start_time'))
    end_time = StrtoStamp(rqjson.get('end_time'))
    order_payment = rqjson.get('order_payment')
    order_info = rqjson.get('order_info')
    print(start_time, end_time)
    if order_title is None or pub_id is None or order_payment is None:
        resp = response_err('missing arguments', "400 status")
        abort(resp)  # missing arguments
    if User.query.filter_by(userid=pub_id, user_status='OK').first() is None:
        resp = response_err('no existing user', "400 status")
        abort(resp)  # no existing user
    order = Order(order_title=order_title, pub_id=pub_id, start_time=start_time, end_time=end_time,
                  order_payment=order_payment, order_info=order_info)
    db.session.add(order)
    db.session.commit()
    return (jsonify({'order_id': order.order_id, 'order_name': order.order_title}), 201)


# 接受新订单
# http方式：POST
# 成功：返回 data:{order_id,order_stat}
# 失败: 返回验证失败
# 接口需要的 data:{order_id}
# 备注：需要验证
@app.route('/api/get_order', methods=['POST'])
@auth.login_required
def get_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    if order_id is None:
        resp = response_err('missing arguments', "400 status")
        abort(resp)  # missing arguments
    if db.session.query(Order).filter(Order.order_id == order_id, Order.order_stat == '未接受',
                                      Order.pub_id != g.user.userid).first() is None:
        # if Order.query.filter_by(order_id=order_id, order_stat='未接受', pub_id=g.user.userid).first() is None:
        resp = response_err('no existing order', "400 status")
        abort(resp)  # no existing user
    db.session.query(Order).filter(Order.order_id == order_id). \
        update({"order_stat": '正在进行', "rec_id": g.user.userid})
    return jsonify({'order_id': order_id, "order_stat": '正在进行'}), 201


# 完成订单
# 成功：返回 data:{order_id,order_stat}
# 失败: 返回验证失败
# 接口需要的 data:{order_id}
# 备注：需要验证
@app.route('/api/finish_order', methods=['POST'])
@auth.login_required
def finish_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    if order_id is None:
        resp = response_err('missing arguments', "400 status")
        abort(resp)  # missing arguments
    if Order.query.filter_by(order_id=order_id, pub_id=g.user.userid, order_stat='正在进行').first() is None:
        resp = response_err('no existing order', "400 status")
        abort(resp)  # no existing user
    db.session.query(Order).filter(Order.order_id == order_id). \
        update({"order_stat": '已完成'})
    return jsonify({'order_id': order_id, "order_stat": '已完成'}), 201


# 删除订单
# 成功：返回 data:{order_id,order_stat}
# 失败: 返回验证失败
# 接口需要的 data:{order_id}
# 备注：需要验证
@app.route('/api/del_order', methods=['POST'])
@auth.login_required
def del_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    if order_id is None:
        resp = response_err('missing arguments', "400 status")
        abort(resp)  # missing arguments
    pre_del = db.session.query(Order).filter(Order.order_id == order_id, Order.order_stat == '未接受').first()
    if pre_del is None:
        resp = response_err('no existing order', "400 status")
        abort(resp)  # no existing order
    db.session.query(Order).filter(Order.order_id == order_id). \
        update({"order_stat": '已删除'})
    db.session.commit()
    return jsonify({'order_id': order_id, "order_stat": '已删除'}), 201


# 放弃 已接受 订单
# 成功：返回 data:{order_id,order_stat}
# 失败: 返回验证失败
# 接口需要的 data:{order_id}
# 备注：需要验证
@app.route('/api/cancel_rec_order', methods=['POST'])
@auth.login_required
def cancel_rec_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    if order_id is None:
        resp = response_err('missing arguments', "400 status")
        abort(resp)  # missing arguments
    pre_del = db.session.query(Order).filter(Order.order_id == order_id, Order.order_stat == '正在进行',
                                             Order.rec_id == g.user.userid).first()
    if pre_del is None:
        resp = response_err('no existing order', "400 status")
        abort(resp)  # no existing order
    db.session.query(Order).filter(Order.order_id == order_id). \
        update({"order_stat": '未接受',"rec_id":-1})
    db.session.commit()
    return jsonify({'order_id': order_id, "order_stat": '未接受'}), 201


# 修改订单信息
# 成功：返回 data:{order_id}
# 失败: 返回验证失败/400
# 接口需要的 data:{order_title, pub_id, start_time, end_time,order_payment, order_info}
# 备注：需要验证
@app.route('/api/modify_order', methods=['POST'])
@auth.login_required
def modify_order():
    rqjson = request.json
    print(rqjson)
    order_id = rqjson.get('order_id')
    order_title = rqjson.get('order_title')
    pub_id = g.user.userid
    # rec_id=rqjson.get('rec_id')
    start_time = datetime.datetime.strptime(rqjson.get('start_time'), '%Y-%m-%d')
    end_time = datetime.datetime.strptime(rqjson.get('end_time'), '%Y-%m-%d')
    order_payment = rqjson.get('order_payment')
    order_info = rqjson.get('order_info')

    if order_title is None or pub_id is None or order_payment is None:
        resp = response_err('missing arguments', "400 status")
        abort(resp)  # missing arguments
    pre_fix = db.session.query(Order).filter(Order.pub_id == pub_id, Order.order_id == order_id,
                                             Order.order_stat != '已完成' and Order.order_stat != '已删除').first()
    if pre_fix is None:
        resp = response_err('no existing order', "400 status")
        abort(resp)  # no existing order
    pre_fix.update(
        {'order_title': order_title, 'start_time': start_time, 'end_time': end_time, 'order_payment': order_payment,
         'order_info': order_info})
    db.session.commit()
    return (jsonify({'order_id': order_id}), 201,
            {'Location': url_for('my_order_pub', id=g.user.userid, _external=True)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# curl -H "Content-Type:application/json" -H "Data_Type:msg" -X POST --data "{\"username\":\"xxx\",password:\"1233423\"}" http://127.0.0.1:5000/api/users
