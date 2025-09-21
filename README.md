# 🚀 CS Job Fair (Job Recruitment System)

## 📋 รายละเอียดโปรเจกต์

ระบบรับสมัครงานออนไลน์ที่พัฒนาด้วย Python Flask ตามแนวทาง MVC Architecture รองรับการจัดการตำแหน่งงานและสหกิจศึกษาสำหรับบริษัทและผู้สมัครงาน

**เวอร์ชัน:** 1.0.0  
**สถานะ:** Development (🔄 อยู่ในขั้นตอนพัฒนาต่อเนื่อง)

## ✨ ฟีเจอร์หลัก

### 👥 ระบบผู้ใช้งาน (Multi-Role Authentication)
- **Admin** - จัดการระบบทั้งหมด
- **Company** - โพสต์งาน จัดการใบสมัคร
- **User/Candidate** - สมัครงาน ติดตามสถานะ

### 💼 การจัดการตำแหน่งงาน
- โพสต์ตำแหน่งงานปกติและสหกิจศึกษา
- กรองและค้นหาตำแหน่งงาน
- การแสดงวันคงเหลือแบบ Real-time
- ระบบสถานะการเปิด/ปิดรับสมัคร

### 📝 ระบบสมัครงาน
- สมัครงานออนไลน์
- ติดตามสถานะใบสมัคร
- ประวัติการสมัครงาน
- ระบบแจ้งเตือน

### 🎨 Modern UI/UX
- ออกแบบด้วย Bootstrap 5
- Color Scheme: Orange (#E35205) เป็นสีหลัก
- Responsive Design
- Thai Typography (Kanit + Sarabun fonts)
- Modern Card-based Layout

## 🏗️ สถาปัตยกรรม (MVC Architecture)

```
📦 MVC_1_68/
├── 📂 app/
│   ├── 📂 models/           # MODEL: ข้อมูลและ Business Logic
│   │   ├── company.py       # โมเดลบริษัท
│   │   ├── job.py          # โมเดลตำแหน่งงาน
│   │   ├── candidate.py    # โมเดลผู้สมัคร
│   │   ├── user.py         # โมเดลผู้ใช้
│   │   └── application.py  # โมเดลใบสมัคร
│   │
│   ├── 📂 controllers/      # CONTROLLER: จัดการ Request/Response
│   │   ├── main_controller.py    # หน้าหลัก
│   │   ├── auth_controller.py    # ล็อกอิน/ลงทะเบียน
│   │   └── job_controller.py     # จัดการงาน
│   │
│   ├── 📂 templates/        # VIEW: HTML Templates
│   │   ├── base.html        # Template หลัก
│   │   ├── index.html       # หน้าแรก
│   │   ├── auth/           # หน้า Login/Register
│   │   └── jobs/           # หน้าเกี่ยวกับงาน
│   │
│   ├── 📂 static/          # CSS, JS, Images
│   └── 📂 views/           # View Helpers
│
├── app.py                  # Main Application
├── config.py              # Configuration
├── extensions.py          # Flask Extensions
└── requirements.txt       # Dependencies
```

## 🛠️ เทคโนโลยีที่ใช้

- **Backend:** Python 3.8+ / Flask 2.3.3
- **Database:** SQLite + SQLAlchemy ORM
- **Authentication:** Flask-Login
- **Frontend:** Bootstrap 5 + Font Awesome
- **Typography:** Google Fonts (Kanit, Sarabun)
- **Architecture:** MVC Pattern

## 📦 การติดตั้ง

### 1. Clone Repository
```bash
git clone https://github.com/Jao07Nxne/MVC_1_68.git
cd MVC_1_68
```

### 2. สร้าง Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 4. รันแอปพลิเคชัน
```bash
python app.py
```

เปิดเบราว์เซอร์ไปที่ `http://127.0.0.1:5000`

## 👤 ข้อมูลล็อกอินทดสอบ

### Admin
- **Username:** admin
- **Password:** admin123

### บริษัท (Tech Company)
- **Username:** tech_hr
- **Password:** tech123

### ผู้สมัครงาน
- **Username:** somchai
- **Password:** pass123

*หรือสมัครสมาชิกใหม่ได้ที่หน้า Register*

## 📄 License

โปรเจกต์นี้อยู่ภายใต้ MIT License - ดู [LICENSE](LICENSE) สำหรับรายละเอียด

## 👨‍💻 ผู้พัฒนา

- **Developer:** Jao07Nxne
- **GitHub:** [@Jao07Nxne](https://github.com/Jao07Nxne)

หากมีคำถามหรือข้อเสนอแนะ สามารถติดต่อได้ผ่าน GitHub Issues

---
