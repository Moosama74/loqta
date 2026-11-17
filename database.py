import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'loqta.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Showroom(Base):
    __tablename__ = "showrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True)
    logo = Column(String(255), default="/static/images/default_showroom.png")
    banner = Column(String(255), default="/static/images/default_banner.jpg")
    governorate = Column(String(50), default="القاهرة")
    city = Column(String(50), default="مدينة نصر")
    address = Column(String(255))
    phone = Column(String(20))
    whatsapp = Column(String(20))
    subscription_tier = Column(String(20), default="Gold") # Gold, Platinum, Silver
    verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cars = relationship("Car", back_populates="showroom")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    make = Column(String(50), nullable=False, index=True) # e.g. هيونداي
    model = Column(String(50), nullable=False, index=True) # e.g. إلنترا
    year = Column(Integer, nullable=False, index=True) # e.g. 2022
    price = Column(Integer, nullable=False, index=True) # e.g. 1150000
    payment_type = Column(String(30), default="كاش") # كاش, قسط, كاش أو قسط
    down_payment = Column(Integer, default=0) # مقدم
    monthly_installment = Column(Integer, default=0) # قسط شهري
    
    condition = Column(String(20), default="مستعمل") # مستعمل, زيرو
    paint_condition = Column(String(50), default="فابريكا بالكامل") # فابريكا بالكامل, راشة خارجي نظافة, فابريكا دواخل
    mileage = Column(Integer, default=0) # كيلومترات
    transmission = Column(String(20), default="أوتوماتيك") # أوتوماتيك, مانيوال
    fuel_type = Column(String(20), default="بنزين") # بنزين, غاز طبيعي, كهرباء, هايبرد
    engine_capacity = Column(String(20), default="1600 CC")
    body_type = Column(String(30), default="سيدان") # سيدان, SUV / عائلية, هاتشباك, بيك أب
    color = Column(String(30), default="أبيض")
    
    governorate = Column(String(50), default="القاهرة", index=True)
    city = Column(String(50), default="مدينة نصر")
    
    description = Column(Text, default="")
    features = Column(Text, default="") # JSON list or comma separated (فتحة سقف, شاشة, مثبت سرعة, إلخ)
    
    seller_name = Column(String(100), default="صاحب السيارة")
    seller_phone = Column(String(20), default="01000000000")
    seller_whatsapp = Column(String(20), default="01000000000")
    seller_type = Column(String(20), default="فرد") # فرد, معرض
    
    showroom_id = Column(Integer, ForeignKey("showrooms.id"), nullable=True)
    showroom = relationship("Showroom", back_populates="cars")
    
    main_image = Column(String(255), default="/static/images/car_placeholder.jpg")
    gallery = Column(Text, default="[]") # JSON list of images
    
    is_featured = Column(Boolean, default=False) # إعلان لقطة سوبر مميز
    listing_tier = Column(String(20), default="مجاني") # مجاني, مميز لقطة (مدفوع 199 ج), سوبر VIP (مدفوع 399 ج)
    
    status = Column(String(20), default="نشط") # نشط, مباع, قيد المراجعة
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class RentalCar(Base):
    __tablename__ = "rental_cars"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, default=2024)
    transmission = Column(String(20), default="أوتوماتيك")
    daily_price = Column(Integer, nullable=False) # e.g. 1500 EGP
    monthly_price = Column(Integer, default=0)
    deposit_commission = Column(Integer, default=250) # عمولة المنصة تدفع أونلاين عند الحجز
    with_driver = Column(Boolean, default=False)
    governorate = Column(String(50), default="القاهرة")
    city = Column(String(50), default="مصر الجديدة")
    image = Column(String(255), default="/static/images/car_placeholder.jpg")
    company_name = Column(String(100), default="شركة لقطة ليموزين")
    phone = Column(String(20), default="01012345678")
    status = Column(String(20), default="متاح")
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("RentalBooking", back_populates="car")

class RentalBooking(Base):
    __tablename__ = "rental_bookings"

    id = Column(Integer, primary_key=True, index=True)
    rental_car_id = Column(Integer, ForeignKey("rental_cars.id"))
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20), nullable=False)
    total_days = Column(Integer, default=1)
    total_amount = Column(Integer, default=0)
    commission_earned = Column(Integer, default=0) # ربح الموقع من العملية
    payment_status = Column(String(20), default="تم دفع العربون")
    created_at = Column(DateTime, default=datetime.utcnow)

    car = relationship("RentalCar", back_populates="bookings")

class InspectionRequest(Base):
    __tablename__ = "inspection_requests"

    id = Column(Integer, primary_key=True, index=True)
    car_title = Column(String(200), nullable=False)
    car_id = Column(Integer, nullable=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    center_location = Column(String(100), default="مركز فحص لقطة المعتمد - مدينة نصر")
    inspection_fee = Column(Integer, default=1500) # رسوم الفحص وربح الموقع
    status = Column(String(20), default="قيد المراجعة")
    created_at = Column(DateTime, default=datetime.utcnow)

class FinanceLead(Base):
    __tablename__ = "finance_leads"

    id = Column(Integer, primary_key=True, index=True)
    car_title = Column(String(200), nullable=False)
    car_price = Column(Integer, default=0)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    monthly_income = Column(String(50), default="15,000 - 25,000 ج.م")
    job_type = Column(String(50), default="قطاع خاص")
    down_payment = Column(Integer, default=0)
    installments_years = Column(Integer, default=3)
    estimated_commission = Column(Integer, default=3500) # عمولة متوقعة من البنك أو شركة التمويل
    status = Column(String(20), default="جديد")
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
