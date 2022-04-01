import sys

from startup_script_utils import load_yaml, pop_custom_fields, set_custom_fields_values
from tenancy.models import ContactRole

contact_roles = load_yaml("/opt/netbox/initializers/contact_roles.yml")

if contact_roles is None:
    sys.exit()

for params in contact_roles:
    custom_field_data = pop_custom_fields(params)
    contact_role, created = ContactRole.objects.get_or_create(**params)

    if created:
        set_custom_fields_values(contact_role, custom_field_data)

        print("🔳 Created Contact Role", contact_role.name)