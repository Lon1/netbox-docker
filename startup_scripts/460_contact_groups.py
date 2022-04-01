import sys

from startup_script_utils import load_yaml, pop_custom_fields, set_custom_fields_values
from tenancy.models import ContactGroup

contact_groups = load_yaml("/opt/netbox/initializers/contact_groups.yml")

if contact_groups is None:
    sys.exit()

optional_assocs = {
    "parent": (ContactGroup, "name")
}

for params in contact_groups:
    custom_field_data = pop_custom_fields(params)

    for assoc, details in optional_assocs.items():
        if assoc in params:
            model, field = details
            query = {field: params.pop(assoc)}

            params[assoc] = model.objects.get(**query)

    contact_group, created = ContactGroup.objects.get_or_create(**params)

    if created:
        set_custom_fields_values(contact_group, custom_field_data)

        print("🔳 Created Contact Group", contact_group.name)