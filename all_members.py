import pandas as pd
import random
from datetime import datetime

# Load CSV
df = pd.read_csv("All-Member-Filter.csv")

sql_statements = []
for index, row in df.iterrows():
    digital_id = f"BITC-{random.randint(100000, 999999)}"
    
    # Birthdate (nullable)
    birthdate = "NULL"
    if pd.notna(row.get('Birthday', None)) and row['Birthday'] != '':
        try:
            birthdate = f"'{datetime.strptime(str(row['Birthday']), '%m/%d/%Y').strftime('%Y-%m-%d')}'"
        except:
            birthdate = "NULL"
    
    # Timestamps (created_at, updated_at)
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
    
    # Determine PaymentMethod and TransactionId (nullable)
    payment_method = row.get('PaymentMethod', 'hand_cash') or 'hand_cash'
    transaction_id = row.get('TransactionId', 'hand_cash') or 'hand_cash'
    
    # Member SQL
    member_sql = f"""
    INSERT INTO members 
    (digital_id, email, student_id, name, phone, birthdate, password, department, intake, gender, position, executive_committee_id, bio, photo_url, social_links, favorite_categories, joined_at, membership_expires_at, created_at, updated_at) 
    VALUES 
    ('{digital_id}', '{email}', '{student_id}', '{name}', '{phone}', {birthdate}, MD5('{digital_id}'), '{department}', '{intake}', {gender}, 'General Member', NULL, NULL, NULL, NULL, NULL, '{joined_at}', NULL, '{timestamp}', '{timestamp}');
    """
    
    # Payment SQL
    payment_sql = f"""
    INSERT INTO membership_payments 
    (member_id, amount, status, payment_method, transaction_id, created_at, updated_at)
    VALUES 
    (LAST_INSERT_ID(), 150, 'pending', '{payment_method}', '{transaction_id}', '{timestamp}', '{timestamp}');
    """
    
    sql_statements.append(member_sql.strip() + "\n" + payment_sql.strip())

with open("all_members_data.sql", "w", encoding="utf-8") as f:
    f.write("\n\n".join(sql_statements))

print("SQL file generated successfully!")
