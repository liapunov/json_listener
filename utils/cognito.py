# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:14:35 2020

@author: frina
"""


import json
#import logging as log
from utils.translator import translate_from

#log.basicConfig(filename="webhook.log",
#                level=log.DEBUG,
#                format='%(asctime)s - %(levelname)s - %(message)s')
#logger = log.getLogger("cognito JSON utils")


# a dictionary containing all the relevant fields
# to be passed between cognito forms and zoom.
_relevant_dict = {
    "Form": {
        "Name": None},
    "Entry": {
        "DateSubmitted": None,
        "DateUpdated": None,
        "Origin": {
            "Address": None,
            "UserAgent": None
            },
        "Status": None,
        "Timestamp": None,
        "Version": None,
        "ViewLink": None,
        "Document1": None,
        "Document2": None,
        },
    "Name": {
        "First": None,
        "Last": None,
        },
    "Email": None,
    "Phone": None,
    "Company": None,
    "AreYouAICCJMember": None,
    "ConditionsAccept": None,
    "Number_Value": None,
    "AddressReceipt": {
        "City": None,
        "Country": None,
        "FullAddress": None,
        "PostalCode": None,
        "State": None,
        "StreetAddress": None,
        "Type": None
        },
    "GuestsName": None,
    "ZoomID": None
  }


class CognitoParser():
    """Utilities to extract information from the CognitoForms Json."""

    def __init__(self, json_req):
        """Initialize the parser by loading the json form from Cognito."""
        self.original = json.loads(json_req)

    def _traverse_and_select_fields(self):
        """
        Traverse the json dict and return only the relevant fields.

        The structure will be flattened, so there will not be groups
        of fields.

        Returns:
            a flattened dictionary of selected fields, according to
            ``relevant_dict``.

        """
        selected = {}
        for key in _relevant_dict.keys():
            if isinstance(_relevant_dict[key], dict):
                for key_2 in _relevant_dict[key].keys():
                    # flattening the structure
                    if key_2 in self.original[key].keys():
                        selected[key_2] = self.original[key][key_2]
            else:
                if key in self.original.keys():
                    selected[key] = self.original[key]
        return selected

    def _get_meta(self, flat_form):
        """Retrieve the data used to identify the form."""
        return {"ZoomID": flat_form["ZoomID"],
                "FormName": flat_form["Name"]
                }

    def get_data(self):
        """Return the meta data and the content of the cognito form."""
        relevant_fields = self._traverse_and_select_fields()
        meta = self._get_meta(relevant_fields)
        translated_fields = translate_from(relevant_fields, "cognito")
        return meta, translated_fields
