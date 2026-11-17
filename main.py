import os
import json
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, Request, Depends, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc

from database import (
    get_db, init_db, Showroom, Car, RentalCar, RentalBooking, 
    InspectionRequest, FinanceLead
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="لقطة - Loqta Cars Egypt")

# Mount static files & templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Format currency helper for Jinja2
def format_egp(value):
    if value is None:
        return "0 ج.م"
    try:
        return f"{int(value):,} ج.م"
    except:
        return f"{value} ج.م"

def format_number(value):
    if value is None:
        return "0"
    try:
        return f"{int(value):,}"
    except:
        return str(value)

def parse_json(value):
    if not value:
        return []
    try:
        return json.loads(value)
    except:
        return []

templates.env.filters["format_egp"] = format_egp
templates.env.filters["format_number"] = format_number
templates.env.filters["parse_json"] = parse_json

# --- Routes ---

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    featured_cars = db.query(Car).filter(Car.is_featured == True, Car.status == "نشط").order_by(desc(Car.created_at)).limit(6).all()
    latest_cars = db.query(Car).filter(Car.status == "نشط").order_by(desc(Car.created_at)).limit(8).all()
    rentals = db.query(RentalCar).filter(RentalCar.status == "متاح").limit(4).all()
    showrooms = db.query(Showroom).limit(3).all()
    
    # Quick statistics
    cars_count = db.query(Car).count()
    showrooms_count = db.query(Showroom).count()
    rentals_count = db.query(RentalCar).count()
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "featured_cars": featured_cars,
            "latest_cars": latest_cars,
            "rentals": rentals,
            "showrooms": showrooms,
            "stats": {
                "cars": cars_count,
                "showrooms": showrooms_count,
                "rentals": rentals_count
            }
        }
    )

@app.get("/cars", response_class=HTMLResponse)
async def list_cars(
    request: Request,
    make: Optional[str] = None,
    model: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    price_min: Optional[int] = None,
    price_max: Optional[int] = None,
    governorate: Optional[str] = None,
    condition: Optional[str] = None,
    transmission: Optional[str] = None,
    sort: Optional[str] = "newest",
    only_featured: Optional[bool] = False,
    db: Session = Depends(get_db)
):
    query = db.query(Car).filter(Car.status == "نشط")
    
    if make and make != "الكل":
        query = query.filter(Car.make == make)
    if model and model.strip():
        query = query.filter(Car.model.ilike(f"%{model}%"))
    if year_min:
        query = query.filter(Car.year >= year_min)
    if year_max:
        query = query.filter(Car.year <= year_max)
    if price_min:
        query = query.filter(Car.price >= price_min)
    if price_max:
        query = query.filter(Car.price <= price_max)
    if governorate and governorate != "الكل":
        query = query.filter(Car.governorate == governorate)
    if condition and condition != "الكل":
        query = query.filter(Car.condition == condition)
    if transmission and transmission != "الكل":
        query = query.filter(Car.transmission == transmission)
    if only_featured:
        query = query.filter(Car.is_featured == True)

    # Sorting
    if sort == "price_asc":
        query = query.order_by(Car.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Car.price.desc())
    elif sort == "year_desc":
        query = query.order_by(Car.year.desc())
    else: # newest
        query = query.order_by(desc(Car.is_featured), desc(Car.created_at))

    cars = query.all()
    
    # Available makes for filter dropdown
    all_makes = [m[0] for m in db.query(Car.make).distinct().all()]
    all_govs = ["القاهرة", "الجيزة", "الإسكندرية", "الشرقية", "الدقهلية", "الغربية", "القليوبية", "البحيرة"]

    return templates.TemplateResponse(
        request=request,
        name="cars.html",
        context={
            "cars": cars,
            "total_count": len(cars),
            "makes": all_makes,
            "govs": all_govs,
            "filters": {
                "make": make,
                "model": model,
                "year_min": year_min,
                "year_max": year_max,
                "price_min": price_min,
                "price_max": price_max,
                "governorate": governorate,
                "condition": condition,
                "transmission": transmission,
                "sort": sort,
                "only_featured": only_featured
            }
        }
    )

@app.get("/cars/{car_id}", response_class=HTMLResponse)
async def car_detail(request: Request, car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="السيارة غير موجودة")
    
    # Increment views
    car.views_count += 1
    db.commit()

    # Similar cars
    similar_cars = db.query(Car).filter(
        Car.id != car.id,
        or_(Car.make == car.make, Car.body_type == car.body_type),
        Car.status == "نشط"
    ).limit(3).all()

    return templates.TemplateResponse(
        request=request,
        name="car_detail.html",
        context={
            "car": car,
            "similar_cars": similar_cars
        }
    )

@app.get("/rentals", response_class=HTMLResponse)
async def list_rentals(request: Request, governorate: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(RentalCar).filter(RentalCar.status == "متاح")
    if governorate and governorate != "الكل":
        query = query.filter(RentalCar.governorate == governorate)
    rentals = query.order_by(RentalCar.daily_price.asc()).all()

    return templates.TemplateResponse(
        request=request,
        name="rentals.html",
        context={
            "rentals": rentals,
            "selected_gov": governorate
        }
    )

@app.get("/rentals/{rental_id}", response_class=HTMLResponse)
async def rental_detail(request: Request, rental_id: int, db: Session = Depends(get_db)):
    rental = db.query(RentalCar).filter(RentalCar.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="سيارة الإيجار غير موجودة")
    
    return templates.TemplateResponse(
        request=request,
        name="rental_detail.html",
        context={
            "rental": rental
        }
    )

@app.post("/api/book-rental")
async def book_rental(
    rental_id: int = Form(...),
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    total_days: int = Form(1),
    db: Session = Depends(get_db)
):
    rental = db.query(RentalCar).filter(RentalCar.id == rental_id).first()
    if not rental:
        return JSONResponse({"status": "error", "message": "السيارة غير موجودة"}, status_code=400)
    
    total_amount = rental.daily_price * max(1, total_days)
    commission = rental.deposit_commission # عمولة الموقع المباشرة من الحجز
    
    booking = RentalBooking(
        rental_car_id=rental.id,
        customer_name=customer_name,
        customer_phone=customer_phone,
        start_date=start_date,
        end_date=end_date,
        total_days=total_days,
        total_amount=total_amount,
        commission_earned=commission,
        payment_status="تم دفع العربون (عمولة لقطة)"
    )
    db.add(booking)
    db.commit()

    return JSONResponse({
        "status": "success",
        "booking_id": booking.id,
        "commission": commission,
        "total_amount": total_amount,
        "message": f"تم تسجيل الحجز بنجاح! تم استحقاق عمولة لقطة بقيمة {commission} ج.م وسيتم التواصل معك لتأكيد الاستلام."
    })

@app.post("/api/request-inspection")
async def request_inspection(
    car_id: Optional[int] = Form(None),
    car_title: str = Form(...),
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    center_location: str = Form("مركز فحص لقطة المعتمد - مدينة نصر"),
    db: Session = Depends(get_db)
):
    inspection = InspectionRequest(
        car_id=car_id,
        car_title=car_title,
        customer_name=customer_name,
        customer_phone=customer_phone,
        center_location=center_location,
        inspection_fee=1500, # ربح المنصة من خدمة الفحص المعتمد
        status="طلب فحص جديد"
    )
    db.add(inspection)
    db.commit()

    return JSONResponse({
        "status": "success",
        "message": "تم استلام طلب الفحص بنجاح! سيتصل بك فريق فحص لقطة لتحديد الموعد."
    })

@app.post("/api/finance-lead")
async def finance_lead(
    car_title: str = Form(...),
    car_price: int = Form(...),
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    monthly_income: str = Form(...),
    job_type: str = Form(...),
    down_payment: int = Form(0),
    installments_years: int = Form(3),
    db: Session = Depends(get_db)
):
    lead = FinanceLead(
        car_title=car_title,
        car_price=car_price,
        customer_name=customer_name,
        customer_phone=customer_phone,
        monthly_income=monthly_income,
        job_type=job_type,
        down_payment=down_payment,
        installments_years=installments_years,
        estimated_commission=3500, # عمولة بنكية متوقعة للمنصة
        status="جديد"
    )
    db.add(lead)
    db.commit()

    return JSONResponse({
        "status": "success",
        "message": "تم تقديم طلب التقسيط بنجاح! سيقوم مستشار التمويل بمراجعة الشروط والتواصل معك فوراً."
    })

@app.get("/add-listing", response_class=HTMLResponse)
async def add_listing_page(request: Request, db: Session = Depends(get_db)):
    showrooms = db.query(Showroom).all()
    return templates.TemplateResponse(
        request=request,
        name="add_listing.html",
        context={"showrooms": showrooms}
    )

@app.post("/add-listing")
async def submit_listing(
    request: Request,
    title: str = Form(...),
    make: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    price: int = Form(...),
    payment_type: str = Form("كاش"),
    down_payment: int = Form(0),
    condition: str = Form("مستعمل"),
    paint_condition: str = Form("فابريكا بالكامل"),
    mileage: int = Form(0),
    transmission: str = Form("أوتوماتيك"),
    fuel_type: str = Form("بنزين"),
    body_type: str = Form("سيدان"),
    color: str = Form("أبيض"),
    governorate: str = Form("القاهرة"),
    city: str = Form("مدينة نصر"),
    description: str = Form(""),
    seller_name: str = Form(...),
    seller_phone: str = Form(...),
    seller_whatsapp: str = Form(...),
    seller_type: str = Form("فرد"),
    listing_tier: str = Form("مجاني"), # مجاني, مميز لقطة (199 ج), سوبر VIP (399 ج)
    main_image: str = Form("https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&auto=format&fit=crop&q=80"),
    db: Session = Depends(get_db)
):
    is_featured = (listing_tier in ["مميز لقطة", "سوبر VIP"])
    
    new_car = Car(
        title=title,
        make=make,
        model=model,
        year=year,
        price=price,
        payment_type=payment_type,
        down_payment=down_payment,
        condition=condition,
        paint_condition=paint_condition,
        mileage=mileage,
        transmission=transmission,
        fuel_type=fuel_type,
        body_type=body_type,
        color=color,
        governorate=governorate,
        city=city,
        description=description,
        seller_name=seller_name,
        seller_phone=seller_phone,
        seller_whatsapp=seller_whatsapp,
        seller_type=seller_type,
        listing_tier=listing_tier,
        is_featured=is_featured,
        main_image=main_image,
        gallery=json.dumps([main_image]),
        features=json.dumps(["تكييف", "باور ستيرنج", "سنتر لوك", "وسائد هوائية"]),
        status="نشط"
    )
    db.add(new_car)
    db.commit()

    return RedirectResponse(url=f"/cars/{new_car.id}?created=1", status_code=303)

@app.get("/showrooms", response_class=HTMLResponse)
async def showrooms_list(request: Request, db: Session = Depends(get_db)):
    showrooms = db.query(Showroom).all()
    return templates.TemplateResponse(
        request=request,
        name="showrooms.html",
        context={"showrooms": showrooms}
    )

@app.get("/showrooms/{slug}", response_class=HTMLResponse)
async def showroom_detail(request: Request, slug: str, db: Session = Depends(get_db)):
    showroom = db.query(Showroom).filter(Showroom.slug == slug).first()
    if not showroom:
        raise HTTPException(status_code=404, detail="المعرض غير موجود")
    
    cars = db.query(Car).filter(Car.showroom_id == showroom.id, Car.status == "نشط").all()
    
    return templates.TemplateResponse(
        request=request,
        name="showroom_detail.html",
        context={
            "showroom": showroom,
            "cars": cars
        }
    )

@app.get("/finance", response_class=HTMLResponse)
async def finance_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="finance.html",
        context={}
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    cars = db.query(Car).order_by(desc(Car.created_at)).all()
    rentals = db.query(RentalCar).all()
    bookings = db.query(RentalBooking).order_by(desc(RentalBooking.created_at)).all()
    inspections = db.query(InspectionRequest).order_by(desc(InspectionRequest.created_at)).all()
    finance_leads = db.query(FinanceLead).order_by(desc(FinanceLead.created_at)).all()
    showrooms = db.query(Showroom).all()

    # Calculate Revenue and Commissions
    rental_commissions = sum([b.commission_earned for b in bookings])
    
    # Listing fees (199 EGP for مميز لقطة, 399 EGP for سوبر VIP)
    listing_fees = sum([
        399 if c.listing_tier == "سوبر VIP" else (199 if c.listing_tier == "مميز لقطة" else 0)
        for c in cars
    ])
    
    inspection_revenue = sum([i.inspection_fee for i in inspections])
    finance_commissions = sum([f.estimated_commission for f in finance_leads])
    
    total_platform_revenue = rental_commissions + listing_fees + inspection_revenue + finance_commissions

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "cars": cars,
            "rentals": rentals,
            "bookings": bookings,
            "inspections": inspections,
            "finance_leads": finance_leads,
            "showrooms": showrooms,
            "stats": {
                "total_revenue": total_platform_revenue,
                "rental_commissions": rental_commissions,
                "listing_fees": listing_fees,
                "inspection_revenue": inspection_revenue,
                "finance_commissions": finance_commissions,
                "active_cars_count": len(cars),
                "bookings_count": len(bookings),
                "inspections_count": len(inspections)
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
