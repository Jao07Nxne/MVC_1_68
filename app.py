from flask import Flask
from extensions import db, login_manager
from config import Config

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'กรุณาเข้าสู่ระบบก่อนใช้งาน'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.controllers.main_controller import main_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.job_controller import job_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(job_bp, url_prefix='/jobs')
    
    return app

def create_database(app):
    """Create database tables"""
    with app.app_context():
        # Import models to create tables
        from app.models import company, job, candidate, user, application
        db.create_all()
        print("✅ Database tables created successfully!")

def seed_database(app):
    """Seed database with sample data"""
    from app.models.seed_data import seed_all_data
    with app.app_context():
        seed_all_data()

if __name__ == '__main__':
    app = create_app()
    
    print("🚀 Starting Flask Job Recruitment System...")
    print("📊 Setting up database...")
    create_database(app)
    print("🌱 Seeding sample data...")
    seed_database(app)
    print("🎯 System ready! Visit http://127.0.0.1:5000")
    
    app.run(debug=True, host='127.0.0.1', port=5000)