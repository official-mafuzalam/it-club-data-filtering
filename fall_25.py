import pandas as pd
from datetime import datetime

# Load CSV
df = pd.read_csv("Members.csv")

sql_statements = []
for index, row in df.iterrows():
    digital_id = f"BITC-{str(index+1).zfill(6)}"
    
    # Format birthdate for MySQL (YYYY-MM-DD)
    try:
        birthdate = datetime.strptime(row['Date of Birth'], '%m/%d/%Y').strftime('%Y-%m-%d')
    except:
        birthdate = 'NULL'  # Handle invalid dates
    
    # Format timestamp for MySQL (convert from MM/DD/YYYY HH:MM:SS to YYYY-MM-DD HH:MM:SS)
    try:
        timestamp = datetime.strptime(row['Timestamp'], '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fallback to current time
    
    # Clean phone number (remove non-numeric characters except +)
    phone = str(row['Phone Number:'])
    phone = ''.join(filter(lambda x: x.isdigit() or x == '+', phone))
    
    # Clean student_id (remove any special characters)
    student_id = str(row['ID']).split('.')[0]  # Remove .0 if present
    
    # Clean intake (remove any special characters)
    intake = str(row['Intake']).split('(')[0]  # Remove (DH) if present
    
    # Clean department (remove trailing spaces)
    department = str(row['Department']).strip()
    
    member_sql = f"""
    INSERT INTO members (name, email, password, birthdate, student_id, department, intake, phone, gender, photo_url, joined_at, created_at, updated_at, digital_id)
    VALUES ('{row['Name'].replace("'", "''")}', '{row['Email Address']}', MD5('{digital_id}'), '{birthdate}', '{student_id}', '{department}', '{intake}', '{phone}', '{row['Gender'].lower()}', NULL, '{timestamp}', '{timestamp}', '{timestamp}', '{digital_id}');
    """
    
    payment_sql = f"""
    INSERT INTO membership_payments (member_id, amount, status, payment_method, transaction_id, created_at, updated_at)
    VALUES (LAST_INSERT_ID(), 150, 'pending', '{row['Payment Method'].lower()}', '{str(row['Transaction Id']).replace("'", "''")}', '{timestamp}', '{timestamp}');
    """
    
    sql_statements.append(member_sql + "\n" + payment_sql)

with open("fall_2025.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_statements))

print("SQL file generated successfully!")