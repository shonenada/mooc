from time import time

from mooc.extensions import db
from mooc.extensions import login_manager
from mooc.models.account import User, SzuAccount


def update_user_state(user_id, state):
    if not state in User.USER_STATE_VALUES:
        raise ValueError('State is invalid.')
    user = User.query.get(user_id)
    if not user:
        raise RuntimeError('User is not found')
    if state == 'frozen':
        user.freeze()
    elif state == 'active':
        user.active()
    user.save()


def change_user_password(user_id, new_password):
    user = User.query.get(user_id)
    if not user:
        raise RuntimeError('User is not found')
    user.change_password(new_password)
    user.save()


def create_user(data):
    college = data.get('college', None)
    user = User(
        username=data['username'],
        passwd=data['raw_passwd'],
        nickname=data['nickname'],
        is_male=data['is_male'] is 'True',
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        qq=data['qq'],
        state=data['state'],
    )
    szu_account = SzuAccount(
        user=user,
        card_num=data['card_num'],
        stu_number=data['stu_number'],
        college=college,
        szu_account_type=data['szu_account_type'],
        short_phone=data['short_phone'],
    )
    user.save(commit=False)
    szu_account.save(commit=False)
    db.session.commit()


def get_user_recommends(user):
    recommends = set()
    if not user or user.is_anonymous():
        return None

    tags = [r.tag for r in user.recommends]
    for tag in tags:
        for course in tag.courses:
            recommends.add(course)

    return recommends
