from wink.api.base import api
from wink.models.button import WinkButton
from wink.models.mapping import WinkMapping
from wink.common.resp import Success, NotFoundError, List
from wink.models.base import db
from wink.api.views.menu import WinkMenuView
from wink.common import db_utils

from flask import request
from flask_login import current_user, login_required


@api.get('/wink/button/query')
@login_required
def wink_button_query():
    # 获取菜单的按钮列表
    args = request.args
    # TODO 表单验证
    menu_code = args.get('menu_code')
    if not menu_code:
        return NotFoundError('menu_code 不能为空')
    # 通过 menu_code 查找按钮
    buttons = WinkButton.query.filter_by(menu_code=menu_code).all()
    return Success(data=buttons)
