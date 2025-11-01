# 🚗 停车场管理系统（Flask + MySQL + HTML/JS）

一个基于 **Flask + MySQL** 的停车场管理系统，包含 **前后端分离架构**、**图形化管理页面**、**管理员登录系统** 以及 **车辆入库 / 出库 / 状态统计** 等核心功能。  
适用于教学演示、系统设计实验或小型停车场信息化项目。

---

## 🧭 功能概览

| 模块 | 功能描述 |
|------|-----------|
| 🚘 车辆管理 | 车辆入库、出库、自动计算停车费用 |
| 🧮 状态统计 | 实时显示总车位、已占用车位、空闲车位 |
| 👤 管理员系统 | 管理员登录、退出、权限验证 |
| 🧱 车位管理 | 管理员可增删车位 |
| 🖼️ 图形化界面 | 可视化展示停车场车位状态 |
| 🔒 默认演示账号 | 系统自带 `admin123 / admin123` 管理员账号 |

---

## 🧩 技术栈

### 后端：
- **Flask** — Python Web 框架  
- **Flask-SQLAlchemy** — ORM 数据库操作  
- **Flask-CORS** — 跨域支持  
- **MySQL** — 数据存储  
- **Gunicorn** — Heroku 生产服务器  

### 前端：
- **HTML + CSS + JavaScript**
- **原生 AJAX** 与 Flask API 通信  
- **纯静态文件部署**（无需 Node.js）  

---

## 📁 项目结构
parking-system/ 
│ ├── backend/ 
│   ├── init.py              # 标识 Python 包 │   
├── app.py                   # Flask 主程序（路由与 API） │  
├── db.py                    # 数据库连接与初始化 │   
├── models.py                # ORM 模型（Car、Admin、ParkingSpace） 
│ ├── frontend/ │   
├── index.html               # 用户页面（入库 / 出库） │   
├── login.html               # 管理员登录页 │   
├── admin.html               # 管理员图形化管理界面 │   
├── css/ 
│   │   └── style.css            # 页面样式 
│   └── js/ │       
├── app.js               # 入/出库逻辑 │       
├── admin.js             # 图形化管理逻辑 │       
└── login.js             # 登录逻辑 
│ ├── requirements.txt             # Python 依赖 
├── Procfile                     # Heroku 启动命令 
├── runtime.txt                  # Python 版本（可选） 
├── .gitignore                   # Git 忽略规则 
└── README.md                    # 项目说明（本文件）
---

## ⚙️ 环境与依赖

### 1️⃣ 安装依赖
```bash
pip install -r requirements.txt