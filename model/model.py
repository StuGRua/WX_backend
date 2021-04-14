import os
import time
from typing import AbstractSet

from flask import Flask, jsonify, abort, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
#/www/wwwroot/wxapp/templates/views
app = Flask('test',template_folder='F:\\Project\\PY\\WX_backend\\templates')
# # 配置数据库连接
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////www/wwwroot/wxapp/model/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:\\Project\\PY\\WX_backend\\model\\test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'user_info'
    userid = db.Column(db.BIGINT, primary_key=True)
    phonenumber = db.Column(db.BIGINT, unique=True)
    user_name = db.Column(db.String(32), default='NotSet')
    password_hash = db.Column(db.String(128), default='000000')
    major = db.Column(db.String(32), default='NotSet')
    grade = db.Column(db.String(32), default='NotSet')
    user_status = db.Column(db.String(32), default='OK')
    print('Building Done', type(userid), type(password_hash))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        print(self.password_hash)

    def verify_password(self, password):
        res = check_password_hash(self.password_hash, password)
        print(res)
        return res

    def generate_auth_token(self, expires_in=600):
        res = jwt.encode(payload={'id': self.userid, 'exp': time.time() + expires_in}, key=app.config['SECRET_KEY'],
                         algorithm='HS256')
        print(res, 'generated')
        return res

    @staticmethod
    def verify_auth_token(token):
        print('token?')
        try:
            print('token in:', token)
            data = jwt.decode(jwt=token, key=app.config['SECRET_KEY'], algorithms='HS256')
            print(data)
        except Exception as e:
            print(e)
            print('no token1')
            return
        return User.query.get(data['id'])


# 验证密码/token模块
@auth.verify_password
def verify_password(userid_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(userid_or_token)
    if not user:
        print('not token')
        # try to authenticate with username/password
        user = User.query.filter_by(userid=userid_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class Order(db.Model):
    __tablename__ = 'order_list'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_title = db.Column(db.String(32), nullable=False)
    pub_id = db.Column(db.BIGINT)
    rec_id = db.Column(db.String(32), default=-1)
    start_time = db.Column(db.BIGINT)
    end_time = db.Column(db.BIGINT)
    order_stat = db.Column(db.String(32), default='未接受')
    order_payment = db.Column(db.String(32), default='面议~')
    order_info = db.Column(db.String(255), default='没有详细说明了哦')


class Feedback(db.Model):
    __tablename__ = 'user_feedback'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.BIGINT, nullable=False)
    post_time = db.Column(db.BIGINT,nullable=False)
    info = db.Column(db.String(255), default='没有详细说明了哦')
