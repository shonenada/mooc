from flask import current_app as app

from mooc.course.model import LearnRecord, Clip


def get_learn_records():
    app.jinja_env.globals['learn_records'] = LearnRecord.query.limit(10).all()


def get_last_clip():
    app.jinja_env.globals['last_clip'] = \
        Clip.query.order_by(Clip.upload_time.desc()).limit(10).all()