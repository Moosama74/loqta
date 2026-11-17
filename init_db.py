import os
import json
from database import engine, Base, SessionLocal, Showroom, Car, RentalCar, RentalBooking, InspectionRequest, FinanceLead

def seed_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1. Add Showrooms (معارض سيارات كبرى)
    showrooms_data = [
        Showroom(
            name="معرض أوتو كينج موتورز",
            slug="auto-king-motors",
            logo="https://images.unsplash.com/photo-1563720223185-11003d516935?w=150&auto=format&fit=crop&q=80",
            banner="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=1200&auto=format&fit=crop&q=80",
            governorate="القاهرة",
            city="التجمع الخامس - شارع التسعين",
            address="قطعة 42، شارع التسعين الشمالي، بجوار ووتر واي",
            phone="01011223344",
            whatsapp="201011223344",
            subscription_tier="Platinum",
            verified=True
        ),
        Showroom(
            name="معرض الأهرام كارز",
            slug="ahram-cars",
            logo="https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=150&auto=format&fit=crop&q=80",
            banner="https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1200&auto=format&fit=crop&q=80",
            governorate="الجيزة",
            city="الدقي - شارع التحرير",
            address="15 شارع التحرير، أمام محطة مترو البحوث",
            phone="01122334455",
            whatsapp="201122334455",
            subscription_tier="Gold",
            verified=True
        ),
        Showroom(
            name="معرض الإسكندرية الدولي للسيارات",
            slug="alex-auto",
            logo="https://images.unsplash.com/photo-1617788138017-80ad40651399?w=150&auto=format&fit=crop&q=80",
            banner="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1200&auto=format&fit=crop&q=80",
            governorate="الإسكندرية",
            city="سموحة",
            address="طريق 14 مايو، أمام جرين بلازا",
            phone="01233445566",
            whatsapp="201233445566",
            subscription_tier="Gold",
            verified=True
        )
    ]
    for s in showrooms_data:
        db.add(s)
    db.commit()

    # 2. Add Realistic Egyptian Market Cars (مستعمل وزيرو وصفقات لقطة)
    cars_data = [
        Car(
            title="هيونداي إلنترا CN7 فئة رابعة أعلى فئة 2022 فابريكا بالكامل",
            make="هيونداي",
            model="إلنترا CN7",
            year=2022,
            price=1250000,
            payment_type="كاش أو قسط",
            down_payment=350000,
            monthly_installment=26500,
            condition="مستعمل",
            paint_condition="فابريكا بالكامل",
            mileage=38000,
            transmission="أوتوماتيك",
            fuel_type="بنزين",
            engine_capacity="1600 CC",
            body_type="سيدان",
            color="رمادي فيراني",
            governorate="القاهرة",
            city="مدينة نصر",
            description="السيارة بحالة الزيرو تماماً صيانات دورية بالتوكيل بالفواتير، لا يوجد أي خرابيش أو دهانات نهائياً، رخصة سنة باسم المالك الأول بدون توكيلات. فحص لقطة معتمد متاح فوراً.",
            features=json.dumps(["فتحة سقف كهربائية", "شاشة ملاحة تاتش 10.25 بوصة", "كاميرا خلفية وحساسات 360", "مثبت سرعة ذكي", "بصمة تشغيل ودخول ذكي", "فرش جلد طبيعي", "جنوط رياضية 17"]),
            seller_name="المهندس طارق العوضي",
            seller_phone="01098765432",
            seller_whatsapp="201098765432",
            seller_type="فرد",
            showroom_id=None,
            main_image="https://images.unsplash.com/photo-1617469767053-d3b523a0b982?w=800&auto=format&fit=crop&q=80",
            gallery=json.dumps([
                "https://images.unsplash.com/photo-1617469767053-d3b523a0b982?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&auto=format&fit=crop&q=80"
            ]),
            is_featured=True,
            listing_tier="سوبر VIP",
            status="نشط",
            views_count=342
        ),
        Car(
            title="كيا سبورتاج 2023 توب لاين بلس GT Line زيرو لم ترخص",
            make="كيا",
            model="سبورتاج",
            year=2023,
            price=1980000,
            payment_type="كاش أو قسط",
            down_payment=500000,
            monthly_installment=42000,
            condition="زيرو",
            paint_condition="فابريكا بالكامل",
            mileage=1200,
            transmission="أوتوماتيك",
            fuel_type="بنزين",
            engine_capacity="1600 CC Turbo",
            body_type="SUV / كروس أوفر",
            color="أبيض لؤلؤي",
            governorate="القاهرة",
            city="التجمع الخامس",
            description="كيا سبورتاج الجيل الجديد أعلى مواصفة جي تي لاين، فتحة بانوراما كاملة، شاشات منحنية توأم، رادار وتحديد مسار، إضاءة ليد كاملة، سيارة زيرو لم ترخص استلام فوري.",
            features=json.dumps(["بانوراما كاملة", "شاشة عدادات وشاشة ترفيه ديجيتال", "رادار ونقط عمياء", "دفع كلي مستمر", "كراسي كهرباء مع تبريد وتدفئة", "شنطة كهربائية"]),
            seller_name="أوتو كينج موتورز",
            seller_phone="01011223344",
            seller_whatsapp="201011223344",
            seller_type="معرض",
            showroom_id=1,
            main_image="https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800&auto=format&fit=crop&q=80",
            gallery=json.dumps([
                "https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800&auto=format&fit=crop&q=80"
            ]),
            is_featured=True,
            listing_tier="مميز لقطة",
            status="نشط",
            views_count=520
        ),
        Car(
            title="تويوتا كورولا الفئة الثانية 2021 عداد قليل بحالة ممتازة",
            make="تويوتا",
            model="كورولا",
            year=2021,
            price=1050000,
            payment_type="كاش",
            down_payment=0,
            monthly_installment=0,
            condition="مستعمل",
            paint_condition="راشة إكصدامين نظافة فابريكا دواخل وسقف وكبوت",
            mileage=52000,
            transmission="أوتوماتيك",
            fuel_type="بنزين",
            engine_capacity="1600 CC",
            body_type="سيدان",
            color="فضي ميتاليك",
            governorate="الجيزة",
            city="الشيخ زايد",
            description="كورولا ياباني أصلية مريحة وموفرة للبنزين جداً، تم عمل صيانة الـ 50 ألف وتغيير الزيوت والسيور، تكييف ثلاجة وبطاريه جديدة بالضمان، رخصة سنتين الشيخ زايد.",
            features=json.dumps(["تكييف ديجيتال مزدوج", "فرامل ABS و EBD", "حساسات ركن خلفية", "بلوتوث و USB", "مرايات ضم كهرباء"]),
            seller_name="دكتور حسام الدالي",
            seller_phone="01155667788",
            seller_whatsapp="201155667788",
            seller_type="فرد",
            showroom_id=None,
            main_image="https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&auto=format&fit=crop&q=80",
            gallery=json.dumps([
                "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&auto=format&fit=crop&q=80"
            ]),
            is_featured=False,
            listing_tier="مجاني",
            status="نشط",
            views_count=215
        ),
        Car(
            title="نيسان صني سوبر صالون 2020 أعلى فئة بصمة وجنوط",
            make="نيسان",
            model="صني",
            year=2020,
            price=560000,
            payment_type="كاش أو قسط",
            down_payment=160000,
            monthly_installment=11200,
            condition="مستعمل",
            paint_condition="فابريكا بالكامل ما عدا رفرف يمين",
            mileage=74000,
            transmission="أوتوماتيك",
            fuel_type="بنزين",
            engine_capacity="1500 CC",
            body_type="سيدان",
            color="ذهبي برونزي",
            governorate="الإسكندرية",
            city="سموحة",
            description="نيسان صني سوبر صالون، بصمة، سبويلر خلفي أصلي، صالون الفابريكا بحالة الجديد تماماً، لا تحتاج جنيه مصروف والمعاينة خير دليل.",
            features=json.dumps(["بصمة تشغيل", "تكييف خلفي صالون", "شاشة تاتش مع كاميرا", "طارة مالتي فانكشن", "جنوط رياضية 15"]),
            seller_name="الأهرام كارز",
            seller_phone="01122334455",
            seller_whatsapp="201122334455",
            seller_type="معرض",
            showroom_id=2,
            main_image="https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&auto=format&fit=crop&q=80",
            gallery=json.dumps([]),
            is_featured=False,
            listing_tier="مجاني",
            status="نشط",
            views_count=180
        ),
        Car(
            title="مرسيدس بنز C180 موديل 2021 AMG نايت باكج فابريكا",
            make="مرسيدس",
            model="C180",
            year=2021,
            price=2850000,
            payment_type="كاش",
            down_payment=0,
            monthly_installment=0,
            condition="مستعمل",
            paint_condition="فابريكا بالكامل",
            mileage=32000,
            transmission="أوتوماتيك",
            fuel_type="بنزين",
            engine_capacity="1500 CC Turbo",
            body_type="سيدان",
            color="أسود ملوكي",
            governorate="القاهرة",
            city="المعادي",
            description="مرسيدس C180 AMG Night Package أصلي، السيارة حالة شاذة ونادرة، صيانات بالكامل توكيل جيرمانيا، طبقة نانو سيراميك أصلية، رخصة سارية.",
            features=json.dumps(["AMG Body Kit", "سقف بانوراما", "شاشة عريضة ديجيتال", "نظام صوتي Burmester", "إضاءة محيطية 64 لون", "كراسي ميموري وجلد الكانتارا"]),
            seller_name="أوتو كينج موتورز",
            seller_phone="01011223344",
            seller_whatsapp="201011223344",
            seller_type="معرض",
            showroom_id=1,
            main_image="https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&auto=format&fit=crop&q=80",
            gallery=json.dumps([]),
            is_featured=True,
            listing_tier="سوبر VIP",
            status="نشط",
            views_count=690
        ),
        Car(
            title="شيري تيجو 7 برو 2023 فئة ثانية أعلى مواصفة لقطة بالسعر",
            make="شيري",
            model="تيجو 7 برو",
            year=2023,
            price=1180000,
            payment_type="كاش أو قسط",
            down_payment=320000,
            monthly_installment=24000,
            condition="مستعمل",
            paint_condition="فابريكا بالكامل",
            mileage=24000,
            transmission="أوتوماتيك",
            fuel_type="بنزين",
            engine_capacity="1500 CC Turbo",
            body_type="SUV / كروس أوفر",
            color="كحلي ميتاليك",
            governorate="الشرقية",
            city="الزقازيق",
            description="تيجو 7 برو سيارة عائلية فخمة جداً وثابتة على الطريق، رخصة 3 سنوات باسم المالك الأول، صيانات توكيل غبور بالفواتير، كاوتش وبطارية بحالة الزيرو.",
            features=json.dumps(["سقف بانوراما", "كاميرات 360 درجة", "شاحن لاسلكي سريع", "شاشة 10 بوصة مع أبل كاربلاي", "مثبت سرعة وفرامل يد كهربائية"]),
            seller_name="الأستاذ محمد إبراهيم",
            seller_phone="01229988776",
            seller_whatsapp="201229988776",
            seller_type="فرد",
            showroom_id=None,
            main_image="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&auto=format&fit=crop&q=80",
            gallery=json.dumps([]),
            is_featured=True,
            listing_tier="مميز لقطة",
            status="نشط",
            views_count=298
        )
    ]
    for c in cars_data:
        db.add(c)
    db.commit()

    # 3. Add Rental Cars (إيجار يومي وشهري مع حجز مباشر وعمولة موقع)
    rental_cars_data = [
        RentalCar(
            title="تويوتا كورولا 2024 زيرو للإيجار السياحي ورجال الأعمال",
            make="تويوتا",
            model="كورولا",
            year=2024,
            transmission="أوتوماتيك",
            daily_price=1200,
            monthly_price=24000,
            deposit_commission=250, # عمولة الموقع المحصلة أونلاين
            with_driver=False,
            governorate="القاهرة",
            city="مطار القاهرة الدولي / مصر الجديدة",
            image="https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&auto=format&fit=crop&q=80",
            company_name="شركة لقطة إكسبريس ليموزين",
            phone="01099887766",
            status="متاح"
        ),
        RentalCar(
            title="مرسيدس E200 موديل 2023 لحفلات الزفاف والوفود والليموزين الفاخر",
            make="مرسيدس",
            model="E200",
            year=2023,
            transmission="أوتوماتيك",
            daily_price=4500,
            monthly_price=85000,
            deposit_commission=800, # عمولة الموقع
            with_driver=True,
            governorate="القاهرة",
            city="التجمع الخامس / وسط البلد",
            image="https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&auto=format&fit=crop&q=80",
            company_name="رويال كارز إيجيبت",
            phone="01155443322",
            status="متاح"
        ),
        RentalCar(
            title="كيا سبورتاج 2024 SUV عائلية للسفر والساحل وشرم الشيخ",
            make="كيا",
            model="سبورتاج",
            year=2024,
            transmission="أوتوماتيك",
            daily_price=1900,
            monthly_price=38000,
            deposit_commission=350, # عمولة الموقع
            with_driver=False,
            governorate="الإسكندرية",
            city="سموحة / الساحل الشمالي",
            image="https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800&auto=format&fit=crop&q=80",
            company_name="الأهرام رنت إيجيبت",
            phone="01224466880",
            status="متاح"
        ),
        RentalCar(
            title="نيسان صني 2023 اقتصادية وعملية بأوفر سعر إيجار يومي",
            make="نيسان",
            model="صني",
            year=2023,
            transmission="أوتوماتيك",
            daily_price=750,
            monthly_price=16000,
            deposit_commission=150, # عمولة الموقع
            with_driver=False,
            governorate="الجيزة",
            city="المهندسين / الهرم",
            image="https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&auto=format&fit=crop&q=80",
            company_name="الأهرام رنت إيجيبت",
            phone="01224466880",
            status="متاح"
        )
    ]
    for r in rental_cars_data:
        db.add(r)
    db.commit()

    # 4. Add Sample Commission & Activity Data (لتوضيح لوحة الأرباح لصاحب الموقع)
    bookings_sample = [
        RentalBooking(
            rental_car_id=1,
            customer_name="كريم الشناوي",
            customer_phone="01023456789",
            start_date="2026-11-20",
            end_date="2026-11-25",
            total_days=5,
            total_amount=6000,
            commission_earned=250,
            payment_status="تم دفع العربون"
        ),
        RentalBooking(
            rental_car_id=2,
            customer_name="أحمد فهمي (زفاف)",
            customer_phone="01187654321",
            start_date="2026-11-22",
            end_date="2026-11-23",
            total_days=1,
            total_amount=4500,
            commission_earned=800,
            payment_status="تم دفع العربون"
        )
    ]
    for b in bookings_sample:
        db.add(b)

    # 5. Add Sample Inspection Requests
    inspections_sample = [
        InspectionRequest(
            car_title="هيونداي إلنترا CN7 2022",
            car_id=1,
            customer_name="محمود صبري",
            customer_phone="01298712345",
            center_location="مركز فحص لقطة المعتمد - مدينة نصر",
            inspection_fee=1500,
            status="تم الفحص والتحصيل"
        ),
        InspectionRequest(
            car_title="تويوتا كورولا 2021",
            car_id=3,
            customer_name="سامح الجوهري",
            customer_phone="01011228899",
            center_location="فحص متنقل عند البائع - الشيخ زايد",
            inspection_fee=2000,
            status="مجدول غداً"
        )
    ]
    for ins in inspections_sample:
        db.add(ins)

    # 6. Add Sample Finance Leads
    finance_leads = [
        FinanceLead(
            car_title="كيا سبورتاج 2023 GT Line",
            car_price=1980000,
            customer_name="مروان عبد الرحمن",
            customer_phone="01065432109",
            monthly_income="45,000 ج.م",
            job_type="صاحب شركة خاصة",
            down_payment=500000,
            installments_years=4,
            estimated_commission=4500,
            status="تمت الموافقة البنكية"
        )
    ]
    for fl in finance_leads:
        db.add(fl)

    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
