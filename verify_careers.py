
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestozap_backend.settings')
django.setup()

from apps.careers.models import Job, JobApplication
from django.db import connection

def verify_tables():
    tables = connection.introspection.table_names()
    print(f"Existing tables: {tables}")
    if 'careers_job' in tables and 'careers_jobapplication' in tables:
        print("SUCCESS: Careers tables exist.")
    else:
        print("FAILURE: Careers tables MISSING.")

def test_job_crud():
    print("\nTesting Job CRUD...")
    # Create
    try:
        job = Job.objects.create(
            title="Test Job",
            location="Remote",
            description="Test Description",
            requirements=["Req 1"],
            status="active"
        )
        print(f"Created Job: {job.id}")
        
        # Read
        jobs = Job.objects.all()
        print(f"Jobs count: {jobs.count()}")
        
        # Update
        job.title = "Updated Job"
        job.save()
        print(f"Updated Job: {job.title}")

        # Delete
        job.delete()
        print("Deleted Job")
        
    except Exception as e:
        print(f"CRUD ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify_tables()
    test_job_crud()
