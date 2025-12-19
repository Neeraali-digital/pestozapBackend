#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestozap_backend.settings')
django.setup()

from django.test import Client
from enquiries.models import Enquiry

# Test data for enquiry form
enquiry_data = {
    "type": "enquiry",
    "subject": "Service Enquiry from John Doe",
    "customer_name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "service_type": "residential",
    "message": "Test enquiry message",
    "address": "123 Test Street",
    "property_type": "Apartment",
    "area": 1000.0,
    "building_age": "5-10 years",
    "pests": ["cockroach", "termite"],
    "severity": "moderate",
    "urgency": "urgent",
    "preferred_time": "morning",
    "additional_info": "Additional test info",
    "status": "new",
    "priority": "medium"
}

# Test data for contact form
contact_data = {
    "type": "contact",
    "customer_name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "0987654321",
    "service_type": "commercial",
    "message": "Test contact message",
    "subject": "Contact Message from Jane Smith",
    "status": "new",
    "priority": "medium"
}

client = Client()

print("Testing Enquiry Form Submission...")
response = client.post('/api/v1/enquiries/', data=json.dumps(enquiry_data), content_type='application/json')
print(f"Enquiry Status Code: {response.status_code}")
if response.status_code == 201:
    print("✓ Enquiry form submission successful")
    enquiry_response = response.json()
    print(f"✓ Enquiry saved with ID: {enquiry_response.get('id')}")
else:
    print(f"✗ Enquiry form submission failed: {response.content.decode()}")

print("\nTesting Contact Form Submission...")
response = client.post('/api/v1/enquiries/', data=json.dumps(contact_data), content_type='application/json')
print(f"Contact Status Code: {response.status_code}")
if response.status_code == 201:
    print("✓ Contact form submission successful")
    contact_response = response.json()
    print(f"✓ Contact saved with ID: {contact_response.get('id')}")
else:
    print(f"✗ Contact form submission failed: {response.content.decode()}")

print("\nTesting Admin Enquiries List...")
from django.contrib.auth import get_user_model
User = get_user_model()
admin_user = User.objects.filter(is_staff=True).first()
if admin_user:
    client.force_login(admin_user)
    response = client.get('/api/v1/admin/enquiries/?page=1&type=enquiry')
    print(f"Admin Enquiries Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        enquiries = data.get('results', [])
        print(f"✓ Found {len(enquiries)} enquiries")
        if enquiries:
            print("✓ Sample enquiry data:")
            print(json.dumps(enquiries[0], indent=2))
    else:
        print(f"✗ Admin enquiries failed: {response.content.decode()}")

    response = client.get('/api/v1/admin/enquiries/?page=1&type=contact')
    print(f"Admin Contacts Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        contacts = data.get('results', [])
        print(f"✓ Found {len(contacts)} contacts")
        if contacts:
            print("✓ Sample contact data:")
            print(json.dumps(contacts[0], indent=2))
    else:
        print(f"✗ Admin contacts failed: {response.content.decode()}")
else:
    print("✗ No admin user found for testing admin endpoints")
