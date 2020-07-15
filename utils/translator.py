# -*- coding: utf-8 -*-
"""
Created on Sat May 16 16:38:31 2020

@author: frina
"""

#import logging as log

# a subset of the zoom registrant schema.
zoom_dict = {
  "email": "email",
  "name": "first_name",
  "surname": "last_name",
  "address": "address",
  "city": "city",
  "country": "country",
  "zip": "zip",
  "state": "state",
  "phone": "phone",
  "company": "org"
}

# a flattened version of the cognito form schema.
cognito_dict = {
  "email": "Email",
  "name": "First",
  "surname": "Last",
  "address": "StreetAddress",
  "city": "City",
  "country": "Country",
  "zip": "PostalCode",
  "state": "State",
  "phone": "Phone",
  "company": "Company"
}


#log.basicConfig(filename="webhook.log",
#                level=log.DEBUG,
#                format='%(asctime)s - %(levelname)s - %(message)s')
#logger = log.getLogger("JSON translator")


def get_dict(key):
    """Select the right translation dictionary based on the app keyword."""
    name = f"{key}_dict"
    return eval(name)


def translate_to(common_form, target):
    """Transform a form in common schema to a format compatible with target."""
    # retrieve the correct translation dictionary
    target_dict = get_dict(target)
    # recreate the form with the translated keys
    target_form = {target_dict[key]: common_form[key]
                   for key in target_dict.keys()}
    return target_form


def translate_from(original_form, source):
    """Take a flattened form and translate into common schema."""
    # retrieve the correct translation dictionary
    source_dict = get_dict(source)
    # recreate the form with the translated values
    common_form = {}
    for key in source_dict.keys():
        if source_dict[key] in original_form.keys():
            common_form[key] = original_form[source_dict[key]]
        else:
            common_form[key] = ""
    return common_form
