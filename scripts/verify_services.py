import os
import sys
import django
from django.conf import settings
from google.cloud import storage
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eduassist.settings")
django.setup()

def check_gcloud_auth():
    print("Checking Google Cloud Authentication...")
    try:
        # Just try to use a Google Cloud client directly
        # If this works, authentication is working
        from google.cloud import storage
        
        # Just creating the client is enough to test auth
        storage_client = storage.Client()
        
        # Getting project ID is a simple operation
        project = storage_client.project
        
        print(f"Google Cloud Authentication successful. Project: {project}")
        return True
    except Exception as e:
        print(f"Google Cloud Authentication failed: {str(e)}")
        return False

def check_database_connection():
    print("Checking PostgreSQL Database Connection...")
    try:
        # Django setup to access database
        import django
        django.setup()
        from django.db import connections
        connection = connections['default']
        connection.ensure_connection()
        
        # List tables in the database
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            """)
            tables = [row[0] for row in cursor.fetchall()]
        
        print(f"Database connection successful. Found tables: {', '.join(tables) if tables else 'No tables yet'}")
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return False
    return True

def check_storage_access():
    print("Checking Storage Access...")
    try:
        # Try to access the storage bucket
        bucket_name = os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET")
        if not bucket_name:
            print("GOOGLE_CLOUD_STORAGE_BUCKET not set in environment")
            return False
            
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = list(bucket.list_blobs(max_results=10))
        print(f"Storage access successful. Found {len(blobs)} files in bucket {bucket_name}.")
    except Exception as e:
        print(f"Storage access failed: {str(e)}")
        return False
    return True

def check_groq_api():
    print("Checking Groq API Connection...")
    try:
        # Test the Groq API with a simple request
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("GROQ_API_KEY not set in environment")
            return False
            
        model = os.environ.get("GROQ_MODEL")
        if not model:
            print("GROQ_MODEL not set in environment")
            return False
        
        print(f"  Testing with model: {model}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [{"role": "user", "content": "Hello, are you working?"}],
                "max_tokens": 10
            }
        )
        
        if response.status_code != 200:
            print(f"Groq API returned status code {response.status_code}: {response.text}")
            return False
            
        print("Groq API connection successful.")
    except Exception as e:
        print(f"Groq API connection failed: {str(e)}")
        return False
    return True

if __name__ == "__main__":
    print("Verifying services for EduAssist...\n")
    
    gcloud_ok = check_gcloud_auth()
    print()
    db_ok = check_database_connection()
    print()
    storage_ok = check_storage_access()
    print()
    groq_ok = check_groq_api()
    print()
    
    if all([gcloud_ok, db_ok, storage_ok, groq_ok]):
        print("All services verified successfully!")
        sys.exit(0)
    else:
        print("Some service verifications failed. Please check the errors above.")
        sys.exit(1)