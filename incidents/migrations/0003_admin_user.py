"""
    This migrations adds a new admin user and group.
"""
import os
from django.db import migrations


def create_admin_user(apps, schema_editor):
    from django.contrib.auth.models import User
    from django.contrib.auth.models import Group
    from django.contrib.auth.models import Permission
    
    # Create a new user
    user = User.objects.create_user(
        username='admin',
        email=os.environ["ADMIN_EMAIL"],
        password=os.environ["ADMIN_PASSWORD"]
    )
    user.save()

class Migration(migrations.Migration):
        dependencies = [
            ('incidents', '0002_remove_incident_created_by_and_more'),
        ]
        operations = [
            migrations.RunPython(
                code=create_admin_user,
            ),
        ]