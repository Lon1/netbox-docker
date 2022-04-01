import sys

from startup_script_utils import load_yaml, pop_custom_fields, set_custom_fields_values
from tenancy.models import Contact, ContactGroup

contacts = load_yaml("/opt/netbox/initializers/contacts.yml")

if contacts is None:
    sys.exit()

optional_assocs = {
    "group": (ContactGroup, "name")
}

for params in contacts:
    custom_field_data = pop_custom_fields(params)

    for assoc, details in optional_assocs.items():
        if assoc in params:
            model, field = details
            query = {field: params.pop(assoc)}

            params[assoc] = model.objects.get(**query)

    contact, created = Contact.objects.get_or_create(**params)

    if created:
        set_custom_fields_values(contact, custom_field_data)

        print("👩‍💻 Created Contact", contact.name)