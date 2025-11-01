from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from db import db, init_db
from models import Car, ParkingSpace, Admin
from datetime import datetime
import os, random

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
app.secret_key = "secret-key"
CORS(app)

# ---------------- 数据库配置 ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://root:zjy666@localhost/parking_system"
).replace("mysql://", "mysql+mysqlconnector://")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    init_db(app)

# ---------------- 静态页面 ----------------
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def serve_login():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(app.static_folder, 'admin.html')


# ---------------- 车辆入/出库 ----------------
@app.route('/api/parking/in', methods=['POST'])
def park_in():
    data = request.json
    plate = data.get('plate_number')
    if not plate:
        return jsonify({'error': '缺少车牌号'}), 400

    level = random.randint(1, 3)
    area = random.choice(['A', 'B', 'C'])
    space = random.randint(1, 20)

    car = Car(plate_number=plate, time_in=datetime.now(), level=level, area=area, space=space)

    slot = ParkingSpace.query.filter_by(level=level, area=area, space=space).first()
    if slot and slot.is_occupied:
        return jsonify({'error': '该车位已被占用'}), 409
    if not slot:
        slot = ParkingSpace(level=level, area=area, space=space)
        db.session.add(slot)

    slot.is_occupied = True
    slot.plate_number = plate
    db.session.add(car)
    db.session.commit()
    return jsonify({'message': '入库成功', 'location': f'{level}层 {area}区 {space}号'})


@app.route('/api/parking/out', methods=['POST'])
def park_out():
    data = request.json
    plate = data.get('plate_number')
    car = Car.query.filter_by(plate_number=plate, time_out=None).first()
    if not car:
        return jsonify({'error': '未找到该车辆'}), 404

    car.time_out = datetime.now()
    stay = (car.time_out - car.time_in).total_seconds() / 60
    car.cost = round(max(1, stay / 5), 2)

    slot = ParkingSpace.query.filter_by(level=car.level, area=car.area, space=car.space).first()
    if slot:
        slot.is_occupied = False
        slot.plate_number = None

    db.session.commit()
    return jsonify({'message': '出库成功', 'cost': car.cost})


@app.route('/api/parking/status', methods=['GET'])
def get_status():
    total = ParkingSpace.query.count()
    occupied = ParkingSpace.query.filter_by(is_occupied=True).count()
    return jsonify({'total': total, 'occupied': occupied, 'free': total - occupied})


# ---------------- 管理员功能 ----------------
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.password == password:
        session['admin'] = username
        return jsonify({'message': '登录成功'})
    return jsonify({'error': '用户名或密码错误'}), 401


@app.route('/api/parking/add_space', methods=['POST'])
def add_space():
    data = request.json
    level, area, space = data.get('level'), data.get('area'), data.get('space')
    if not level or not area or not space:
        return jsonify({'error': '缺少参数'}), 400
    if ParkingSpace.query.filter_by(level=level, area=area, space=space).first():
        return jsonify({'error': '该车位已存在'}), 409
    new_space = ParkingSpace(level=level, area=area, space=space)
    db.session.add(new_space)
    db.session.commit()
    return jsonify({'message': '添加成功'})


@app.route('/api/parking/delete_space', methods=['DELETE'])
def delete_space():
    data = request.json
    level, area, space = data.get('level'), data.get('area'), data.get('space')
    target = ParkingSpace.query.filter_by(level=level, area=area, space=space).first()
    if not target:
        return jsonify({'error': '未找到该车位'}), 404
    db.session.delete(target)
    db.session.commit()
    return jsonify({'message': '删除成功'})


# ---------------- 启动服务 ----------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)