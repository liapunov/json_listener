# -*- coding: utf-8 -*-
"""
Created on Sat May 16 13:31:02 2020.

@author: frina
"""

from json import dumps
from datetime import timedelta
from datetime import datetime
from requests import request
# import logging as log
from jose import jwt
from utils.translator import translate_to


with open("./keys/zoom.json") as zoom_json_key:
    zoom_keys = loads(zoom_json_key)

# the base URL required to connect to the auth server on zoom.
API_AUTH_URL = "https://api.zoom.us/v2/users"


API_REG_TEMPLATE = ["https://api.zoom.us/v2/webinars/", "/registrants"]


#log.basicConfig(filename="webhook.log",
#                level=log.DEBUG,
#                format='%(asctime)s - %(levelname)s - %(message)s')
#logger = log.getLogger("Zoom JSON utils")


class ZoomWebinar():
    """
    Request of update to a zoom webinar.

    Attributes:
        common_form (dict): the form encoded in the common schema.
        zoom_form (dict): the form encoded as a dictionary in the zoom schema.
        webinar_id (str): the zoom webinar unique identifier.
        jwt_token (str): the token required to authenticate to zoom.

    """

    def __init__(self, meta, form):
        """
        Initialize the class and send the data to zoom immediately.

        Args:
            form (dict): the form in common schema.
            webinar_id (str): the zoom webinar unique identifier.

        Returns:
            An instance of ZoomWebinar.

        """
        self.common_form = form
        self.webinar_id, self.name = self._get_meta(meta)
        self.jwt_token = self._create_jwt_token(0.5)
        self.zoom_form = self._compose_zoom_form()
        # send the data immediately.
        self.response = self._send_data()
        print(self.response.__dict__)

    def _get_meta(self, meta):
        """Extract Webinar ID and name from the meta."""
        return meta["ZoomID"], meta["FormName"]

    def _create_jwt_token(self, hours_validity=0.5):
        """Create the JWT token based on the keys."""
        # retrieve the parameters from zoom_keys
        claims = zoom_keys["claims"]
        claims["exp"] = datetime.now() + timedelta(hours=hours_validity)
        header = zoom_keys["header"]
        key = zoom_keys["access_token"]
        # package the ingredients and get the jwt token
        token = jwt.encode(claims, key, headers=header)
        return token

    def _get_auth_headers(self):
        """Return the headers required to authenticate with zoom."""
        token = self.jwt_token
        return {
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "status": "active",
            "page_size": 30,
            "page_number": 1
            }

    def _zoom_authenticate(self):
        """Authenticate to the zoom API server in order to communicate."""
        r = request("GET", url=API_AUTH_URL,
                    headers=self._get_auth_headers())
        if r.status_code != 200:
            reason = "Zoom authentication server responded with " +\
                f"status {r.status_code}"
            raise Exception(reason)

    def _compose_zoom_form(self):
        """Take the fields and put them into the zoom form."""
        form = translate_to(self.common_form, "zoom")
        return form

    def _get_reg_url(self):
        """Compose the post URL to register the participant."""
        return (self.webinar_id).join(API_REG_TEMPLATE)

    def _get_send_headers(self):
        """Compose the header used to register the participant."""
        token = self.jwt_token
        return {
            "authorization": f"Bearer {token}",
            "content-type": "application/json"
            }

    def _send_data(self, service="web_reg_add"):
        """Send the relevant json package to zoom."""
        url = self._get_reg_url()
        headers = self._get_send_headers()
        data = dumps(self.zoom_form)
        r = request("POST", url, headers=headers, data=data)
        return r

    def dispatch(self, form_fields):
        """Take the relevant fields and pack them into a json for zoom."""
        self._zoom_authenticate()
        data = self.zoom_form
        self._send_data(data, "web_reg_add")
