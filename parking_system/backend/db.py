from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from models import Admin

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        engine = db.get_engine()
        if not database_exists(engine.url):
            create_database(engine.url)
        db.create_all()

        # 检查是否存在管理员账号
        if not Admin.query.filter_by(username='admin123').first():
            default_admin = Admin(username='admin123', password='admin123')
            db.session.add(default_admin)
            db.session.commit()
            print("✅ 已自动创建默认管理员账号：admin123 / admin123")