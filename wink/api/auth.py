from wink.api.base import api, login_manager
from wink.common.resp import Success, LoginError, TokenError
from wink.models.user import WinkUser
from wink.common.utils import generate_token, validate_token

from flask_login import current_user, login_required
from flask import request


@api.post('/user/login')
def login():
    form = request.get_json()
    login_id = form['login_id']
    login_pwd = form['login_pwd']
    user = WinkUser.query.filter_by(login_id=login_id).first()
    print(user)
    if not user or not user.check_login_pwd(login_pwd):
        print('error???')
        return LoginError()
    token = generate_token({'user_id': user.id})
    return Success({'token': token})


@api.post('/user/logout')
def logout():
    return Success()


@api.get('/user/info')
@login_required
def info():
    # return Success({
    #     'roles': ['admin'],
    #     'introduction': 'I am a super administrator',
    #     'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    #     'name': 'Super Admin'
    # })
    return Success(current_user)


@login_manager.request_loader
def load_user(request):
    headers = request.headers
    token = headers.get('X-Token')
    if not token:
        raise TokenError()
    data = validate_token(token)
    if not data:
        raise TokenError()
    return WinkUser.query.filter_by(id=data['user_id']).first()
