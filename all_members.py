import pandas as pd
from datetime import datetime

# Load CSV
df = pd.read_csv("IT-Club-All-Member.csv")

sql_statements = []
for index, row in df.iterrows():
    digital_id = f"BITC-{str(index+1).zfill(6)}"
    
    # Format birthdate (nullable)
    birthdate = "NULL"
    if pd.notna(row.get('Date of Birth', None)):
        try:
            birthdate = f"'{datetime.strptime(str(row['Date of Birth']), '%m/%d/%Y').strftime('%Y-%m-%d')}'"
        except:
            birthdate = "NULL"
    
    # Format timestamp for created_at/updated_at
    try:
        timestamp = datetime.strptime(str(row['Timestamp']), '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # joined_at = only date part
    joined_at = timestamp.split(" ")[0]
    
    # Clean phone number
    phone = str(row.get('Mobile', '')).strip()
    phone = ''.join(filter(lambda x: x.isdigit() or x == '+', phone)) if phone else ''
    
    # Clean student_id
    student_id = str(row.get('StudentID', '')).split('.')[0]
    
    # Intake
    intake = str(row.get('Intake', '')).split('(')[0].strip()
    
    # Department
    department = str(row.get('Department', '')).strip()
    
    # Gender (nullable, lowercase)
    gender = str(row.get('Gender', '')).lower()
    gender = gender if gender in ['male', 'female', 'other'] else 'NULL'
    if gender != 'NULL':
        gender = f"'{gender}'"
    
    # Escape single quotes in strings
    name = str(row.get('Name', '')).replace("'", "''")
    email = str(row.get('Email', '')).replace("'", "''")
    
    # Member SQL
    member_sql = f"""
    INSERT INTO members 
    (digital_id, email, student_id, name, phone, birthdate, password, department, intake, gender, position, executive_committee_id, bio, photo_url, social_links, favorite_categories, joined_at, membership_expires_at, created_at, updated_at) 
    VALUES 
    ('{digital_id}', '{email}', '{student_id}', '{name}', '{phone}', {birthdate}, MD5('{digital_id}'), '{department}', '{intake}', {gender}, 'General Member', NULL, NULL, NULL, NULL, NULL, '{joined_at}', NULL, '{timestamp}', '{timestamp}');
    """
    
    # Payment SQL (always hand_cash)
    payment_sql = f"""
    INSERT INTO membership_payments 
    (member_id, amount, status, payment_method, transaction_id, created_at, updated_at)
    VALUES 
    (LAST_INSERT_ID(), 150, 'pending', 'hand_cash', 'hand_cash', '{timestamp}', '{timestamp}');
    """
    
    sql_statements.append(member_sql.strip() + "\n" + payment_sql.strip())

with open("all_members_data.sql", "w", encoding="utf-8") as f:
    f.write("\n\n".join(sql_statements))

print("SQL file generated successfully!")

