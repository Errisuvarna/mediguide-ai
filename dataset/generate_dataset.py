"""
Generates the full synthetic hospital dataset (CSV + JSON + SQL seed)
required by the spec: departments, doctors, services, procedures,
required documents, buildings, floors, rooms, FAQs, and hospital map
coordinates. Total records across all tables exceeds 500.

Run:
    python generate_dataset.py

Outputs land in this same dataset/ directory, and are what
backend/app/seed/seed_db.py loads into the database on first run.

Data collection / cleaning / synthetic-generation notes are in
docs/data_handling.md.
"""
import csv
import json
import random
from pathlib import Path

random.seed(42)
OUT_DIR = Path(__file__).parent

DEPARTMENTS = [
    ("General Medicine", "Everyday illness, fever, general checkups", 1, "Main Building",
     "General,Fever,Cold,Cough,Checkup,OPD"),
    ("Cardiology", "Heart disease and cardiovascular care", 3, "Main Building",
     "Heart,Chest Pain,Cardiac,ECG,Blood Pressure"),
    ("Orthopedics", "Bone, joint, and spine care", 2, "Main Building",
     "Bone,Fracture,Joint,Spine,Back Pain"),
    ("Neurology", "Brain and nervous system disorders", 4, "Main Building",
     "Brain,Nerve,Headache,Migraine,Stroke,Seizure"),
    ("Gastroenterology", "Digestive system care", 2, "Main Building",
     "Stomach,Digestion,Liver,Ulcer,Acidity"),
    ("Pulmonology", "Breathing and respiratory disorders", 3, "Main Building",
     "Lungs,Breathing,Asthma,Cough,Respiratory"),
    ("Oncology", "Cancer diagnosis and treatment", 5, "Cancer Care Building",
     "Cancer,Tumor,Chemotherapy,Oncology"),
    ("Pediatrics", "Child healthcare", 1, "Main Building",
     "Child,Baby,Infant,Vaccination,Pediatric"),
    ("Gynecology", "Women's health and maternity", 2, "Main Building",
     "Pregnancy,Women,Maternity,Gynecology"),
    ("Dermatology", "Skin, hair, and nail care", 1, "Main Building",
     "Skin,Rash,Allergy,Hair,Dermatology"),
    ("ENT", "Ear, nose, and throat care", 1, "Main Building",
     "Ear,Nose,Throat,Hearing,Sinus"),
    ("Ophthalmology", "Eye care", 1, "Main Building",
     "Eye,Vision,Cataract,Ophthalmology"),
    ("Dentistry", "Dental and oral care", 0, "Main Building",
     "Teeth,Dental,Tooth,Oral"),
    ("Psychiatry", "Mental health care", 4, "Main Building",
     "Mental Health,Anxiety,Depression,Psychiatry"),
    ("Nephrology", "Kidney care", 3, "Main Building",
     "Kidney,Dialysis,Nephrology"),
    ("Urology", "Urinary system care", 3, "Main Building",
     "Urinary,Bladder,Prostate,Urology"),
    ("Emergency", "24x7 emergency and trauma care", 0, "Main Building",
     "Emergency,Trauma,Accident,Urgent,Casualty"),
    ("Radiology & Imaging", "X-ray, CT, MRI, ultrasound", 0, "Diagnostics Building",
     "X-ray,Scan,MRI,CT,Ultrasound,Imaging"),
    ("Laboratory", "Blood tests and diagnostics", 0, "Diagnostics Building",
     "Blood Test,Lab,Sample,Diagnostics,Pathology"),
    ("Pharmacy", "Medicine dispensing", 0, "Main Building",
     "Medicine,Pharmacy,Drugs,Prescription"),
]

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Ishaan", "Krishna",
    "Ananya", "Diya", "Priya", "Sneha", "Kavya", "Meera", "Rohan", "Karthik",
    "Sanjay", "Deepak", "Anjali", "Neha", "Rahul", "Suresh", "Ramesh", "Lakshmi",
    "Padma", "Geeta", "Anita", "Vijay", "Manoj", "Sunil", "Kiran", "Pooja",
]
LAST_NAMES = [
    "Sharma", "Verma", "Rao", "Reddy", "Nair", "Iyer", "Gupta", "Menon",
    "Naidu", "Pillai", "Kapoor", "Chatterjee", "Mukherjee", "Das", "Joshi",
    "Kumar", "Singh", "Patel", "Krishnan", "Bhat",
]
DESIGNATIONS = ["Consultant", "Senior Consultant", "Assistant Professor",
                "Associate Professor", "Head of Department", "Resident Doctor"]
QUALIFICATIONS = ["MBBS, MD", "MBBS, MS", "MBBS, DM", "MBBS, MCh", "MBBS, DNB", "MBBS"]
DAY_PATTERNS = ["Mon,Wed,Fri", "Tue,Thu,Sat", "Mon-Fri", "Mon,Tue,Wed,Thu,Fri", "Tue,Thu"]
TIME_SLOTS = ["09:00-13:00", "10:00-14:00", "14:00-18:00", "16:00-20:00", "09:00-17:00"]


def gen_departments():
    rows = []
    for i, (name, desc, floor, building, keywords) in enumerate(DEPARTMENTS, start=1):
        rows.append({
            "id": i, "name": name, "description": desc, "floor_number": floor,
            "building_name": building, "contact_number": f"+91-40-4000-{1000+i:04d}",
            "office_hours": "Mon-Sat 09:00-17:00" if name != "Emergency" else "24x7",
            "avg_waiting_time_minutes": random.choice([10, 15, 20, 25, 30]),
            "keywords": keywords,
        })
    return rows


def gen_doctors(departments, count=140):
    rows = []
    for i in range(1, count + 1):
        dept = random.choice(departments)
        rows.append({
            "id": i,
            "full_name": f"Dr. {random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "department_id": dept["id"],
            "designation": random.choice(DESIGNATIONS),
            "qualification": random.choice(QUALIFICATIONS),
            "consultation_fee": random.choice([300, 500, 600, 800, 1000, 1200, 1500]),
            "room_number": f"{dept['floor_number']}{random.randint(1, 30):02d}",
            "available_days": random.choice(DAY_PATTERNS),
            "available_time": random.choice(TIME_SLOTS),
            "experience_years": random.randint(2, 30),
        })
    return rows


SERVICE_TEMPLATES = [
    ("OPD Consultation", 500), ("General Checkup", 400), ("Follow-up Consultation", 300),
    ("Blood Test - CBC", 350), ("Blood Test - Lipid Profile", 600), ("X-Ray", 500),
    ("CT Scan", 4500), ("MRI Scan", 7500), ("Ultrasound", 1200), ("ECG", 400),
    ("Echocardiogram", 2000), ("Physiotherapy Session", 700), ("Minor Procedure", 2500),
    ("Vaccination", 800), ("Health Package - Basic", 2500), ("Health Package - Executive", 6000),
    ("Dialysis Session", 3000), ("Endoscopy", 3500), ("Biopsy", 5000), ("Dental Cleaning", 1000),
    ("Eye Test", 300), ("Hearing Test", 500), ("Pregnancy Ultrasound", 1500),
    ("Chemotherapy Session", 15000), ("Emergency Consultation", 1000),
]


def gen_services(departments, count=120):
    rows = []
    for i in range(1, count + 1):
        template = SERVICE_TEMPLATES[(i - 1) % len(SERVICE_TEMPLATES)]
        dept = random.choice(departments)
        rows.append({
            "id": i, "name": template[0], "department_id": dept["id"],
            "description": f"{template[0]} provided by the {dept['name']} department.",
            "fee": template[1] + random.choice([-50, 0, 0, 50, 100]),
            "location": f"{dept['building_name']}, Floor {dept['floor_number']}",
        })
    return rows


PROCEDURE_TEMPLATES = [
    ("Appendectomy", "Surgery", 45000, "8 hours fasting required before surgery."),
    ("Angioplasty", "Cardiology", 250000, "Blood tests and consent form required."),
    ("Knee Replacement", "Orthopedics", 350000, "Pre-op assessment 1 week prior."),
    ("Cataract Surgery", "Ophthalmology", 30000, "Avoid eye makeup on the day of surgery."),
    ("Gallbladder Removal", "Surgery", 60000, "12 hours fasting required."),
    ("Root Canal Treatment", "Dentistry", 6000, "Avoid hot/cold food before procedure."),
    ("Hernia Repair", "Surgery", 40000, "Fasting for 8 hours before surgery."),
    ("Cesarean Delivery", "Gynecology", 55000, "Admission 1 day prior recommended."),
    ("Colonoscopy", "Gastroenterology", 8000, "Special diet 1 day before procedure."),
    ("Hip Replacement", "Orthopedics", 380000, "Pre-op physiotherapy assessment required."),
]


def gen_procedures(count=40):
    rows = []
    for i in range(1, count + 1):
        template = PROCEDURE_TEMPLATES[(i - 1) % len(PROCEDURE_TEMPLATES)]
        rows.append({
            "id": i, "name": template[0], "category": template[1],
            "description": f"{template[0]} - performed by our {template[1]} specialists.",
            "estimated_cost": template[2] + random.choice([-2000, 0, 0, 2000, 5000]),
            "prep_instructions": template[3],
        })
    return rows


DOCUMENT_TEMPLATES = {
    "Registration": ["Government ID Proof", "Address Proof", "Passport-size Photo", "Referral Letter (if any)"],
    "Admission": ["ID Proof", "Insurance Card / Policy Document", "Admission Deposit Receipt",
                  "Previous Medical Records", "Emergency Contact Details Form"],
    "Billing": ["Admission ID", "Insurance Approval Letter (if applicable)", "Itemized Bill Request Form"],
    "Insurance": ["Insurance Policy Card", "Government ID Proof", "Pre-authorization Form",
                  "Claim Form", "Hospital Empanelment Letter"],
    "Discharge": ["Discharge Summary Acknowledgement", "Final Bill Payment Receipt",
                  "Follow-up Appointment Slip"],
    "Laboratory": ["Doctor's Test Prescription", "Patient ID Card"],
    "Pharmacy": ["Doctor's Prescription", "Patient ID Card"],
}


def gen_documents():
    rows = []
    idx = 1
    for process, docs in DOCUMENT_TEMPLATES.items():
        for doc in docs:
            rows.append({
                "id": idx, "process_name": process, "document_name": doc,
                "is_mandatory": "yes" if idx % 4 != 0 else "no",
                "notes": f"Required for the {process.lower()} process.",
            })
            idx += 1
    return rows


BUILDINGS = [
    ("Main Building", "OPD, wards, and administrative offices"),
    ("Diagnostics Building", "Laboratory, radiology, and imaging"),
    ("Cancer Care Building", "Oncology and chemotherapy day-care"),
    ("Emergency Block", "24x7 emergency and trauma care"),
]


def gen_buildings():
    return [{"id": i, "name": n, "description": d} for i, (n, d) in enumerate(BUILDINGS, start=1)]


def gen_floors(buildings, per_building=5):
    rows = []
    idx = 1
    for b in buildings:
        for fl in range(0, per_building):
            rows.append({
                "id": idx, "building_id": b["id"], "floor_number": fl,
                "label": "Ground Floor - Reception & Emergency" if fl == 0 else f"Floor {fl}",
            })
            idx += 1
    return rows


ROOM_TYPES = ["OPD", "Ward", "ICU", "Lab", "Pharmacy", "Consultation", "Procedure Room"]


def gen_rooms(floors, departments, per_floor=8):
    rows = []
    idx = 1
    for floor in floors:
        for r in range(per_floor):
            dept = random.choice(departments)
            rows.append({
                "id": idx, "floor_id": floor["id"],
                "room_number": f"{floor['floor_number']}{r+1:02d}",
                "room_type": random.choice(ROOM_TYPES),
                "department_name": dept["name"],
            })
            idx += 1
    return rows


FAQ_TEMPLATES = [
    ("Registration", "How do I register as a new patient?",
     "Visit the Registration counter on the Ground Floor with a valid ID proof and address proof. "
     "A staff member will create your patient file and issue a Patient ID card."),
    ("Billing", "How can I get an itemized bill?",
     "Submit an itemized bill request at the Billing counter (Ground Floor, Main Building) with "
     "your admission ID. Itemized bills are typically ready within 24 hours."),
    ("Insurance", "Which insurance providers are accepted?",
     "Most major insurance providers are accepted through cashless and reimbursement claims. "
     "Please check with the Insurance Desk with your policy card for specific coverage."),
    ("Admission", "What is required for hospital admission?",
     "Bring your ID proof, insurance card (if applicable), and pay the admission deposit at the "
     "Admission counter. A bed will be allotted based on availability and doctor's advice."),
    ("Laboratory", "Where is the laboratory located?",
     "The Laboratory is on the Ground Floor of the Diagnostics Building. Bring your doctor's "
     "test prescription and Patient ID card."),
    ("Pharmacy", "Where can I collect my medicines?",
     "The Pharmacy is located on the Ground Floor of the Main Building, next to the OPD waiting "
     "area. Submit your doctor's prescription at the counter."),
    ("Emergency", "What should I do in a medical emergency?",
     "Go directly to the Emergency Department (Ground Floor, Emergency Block, red signage) or "
     "alert any staff member immediately. Emergency care is available 24x7."),
    ("General", "What are the hospital's visiting hours?",
     "General visiting hours are 11:00-13:00 and 17:00-19:00 daily. ICU visiting is restricted "
     "to immediate family with staff permission."),
    ("General", "Is parking available?",
     "Yes, multi-level parking is available near the Main Building entrance, with a dedicated "
     "drop-off zone for Emergency and elderly patients."),
    ("Discharge", "How does the discharge process work?",
     "Your doctor issues a discharge summary, the Billing counter settles the final bill, and "
     "the nursing station completes discharge formalities before you leave the ward."),
]


def gen_faqs(count=60):
    rows = []
    for i in range(1, count + 1):
        template = FAQ_TEMPLATES[(i - 1) % len(FAQ_TEMPLATES)]
        rows.append({
            "id": i, "category": template[0], "question": template[1], "answer": template[2],
            "keywords": template[0].lower(),
        })
    return rows


MAP_CATEGORIES = ["Entrance", "Reception", "Department", "Lab", "Pharmacy", "Emergency",
                   "Parking", "Cafeteria", "ATM", "Billing Counter"]


def gen_map_points(departments, buildings, count=60):
    rows = []
    for i in range(1, count + 1):
        building = random.choice(buildings)
        category = random.choice(MAP_CATEGORIES)
        name = (random.choice(departments)["name"] if category == "Department"
                else f"{category} - {building['name']}")
        rows.append({
            "id": i, "name": name, "category": category, "building_name": building["name"],
            "floor_number": random.randint(0, 4),
            "x_coordinate": round(random.uniform(0, 100), 2),
            "y_coordinate": round(random.uniform(0, 100), 2),
            "description": f"{name} located in {building['name']}.",
        })
    return rows


def write_csv_json(name, rows):
    if not rows:
        return
    csv_path = OUT_DIR / f"{name}.csv"
    json_path = OUT_DIR / f"{name}.json"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)


def sql_escape(value):
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def write_sql(all_tables):
    """all_tables: dict[table_name] -> (rows, column_map_to_sql_column)"""
    lines = ["-- MediGuide AI seed data (auto-generated by dataset/generate_dataset.py)", ""]
    for table, rows in all_tables.items():
        if not rows:
            continue
        cols = list(rows[0].keys())
        lines.append(f"-- {table}: {len(rows)} rows")
        for row in rows:
            values = ", ".join(sql_escape(row[c]) for c in cols)
            lines.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({values});")
        lines.append("")
    (OUT_DIR / "seed_data.sql").write_text("\n".join(lines), encoding="utf-8")


def main():
    departments = gen_departments()
    doctors = gen_doctors(departments)
    services = gen_services(departments)
    procedures = gen_procedures()
    documents = gen_documents()
    buildings = gen_buildings()
    floors = gen_floors(buildings)
    rooms = gen_rooms(floors, departments)
    faqs = gen_faqs()
    map_points = gen_map_points(departments, buildings)

    tables = {
        "departments": departments, "doctors": doctors, "services": services,
        "procedures": procedures, "required_documents": documents, "buildings": buildings,
        "floors": floors, "rooms": rooms, "faqs": faqs, "hospital_map_points": map_points,
    }
    for name, rows in tables.items():
        write_csv_json(name, rows)
    write_sql(tables)

    total = sum(len(rows) for rows in tables.values())
    print(f"Generated {len(tables)} tables, {total} total records.")
    for name, rows in tables.items():
        print(f"  {name}: {len(rows)} rows")


if __name__ == "__main__":
    main()
