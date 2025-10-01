import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def create_user_with_role(email: str, password: str, role: str):
    try:
        auth_response = supabase.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True
        })

        user_id = auth_response.user.id
        print(f"Created user {email} with ID: {user_id}")

        role_response = supabase.table("user_roles").insert({
            "user_id": user_id,
            "role": role
        }).execute()

        print(f"Assigned role '{role}' to user {email}")
        return True

    except Exception as e:
        if "already registered" in str(e).lower() or "duplicate" in str(e).lower():
            print(f"User {email} already exists, skipping...")
            return False
        else:
            print(f"Error creating user {email}: {e}")
            return False

def seed_initial_data():
    print("Starting database seed...")
    print("-" * 50)

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    employee_email = os.getenv("EMPLOYEE_EMAIL")
    employee_password = os.getenv("EMPLOYEE_PASSWORD")

    create_user_with_role(admin_email, admin_password, "admin")

    create_user_with_role(employee_email, employee_password, "employee")

    print("-" * 50)
    print("Seed completed!")

if __name__ == "__main__":
    seed_initial_data()
