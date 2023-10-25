# Copyright 2023 Solvti Sp. z o.o.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import models
from odoo.exceptions import AccessDenied
from odoo.http import request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_api_key_hash(cls):
        headers = request.httprequest.environ
        api_key = headers.get("HTTP_API_KEY")
        if api_key:
            request.uid = 1
            auth_api_key_hash = request.env["auth.api.key.hash"]._retrieve_api_key(
                api_key
            )
            if auth_api_key_hash:
                metadata = f"IP: {headers.get('REMOTE_ADDR')} USER_AGENT: {headers.get('HTTP_USER_AGENT')}, REFERER: {headers.get('HTTP_REFERER')}, ORIGIN: {headers.get('HTTP_ORIGIN')}"
                _logger.info("api_key_hash called: Metadata -> {}".format(metadata))
                # reset _env on the request since we change the uid...
                # the next call to env will instantiate an new
                # odoo.api.Environment with the user defined on the
                # auth.api_key
                request._env = None
                request.uid = auth_api_key_hash.user_id.id
                request.auth_api_key_hash = api_key
                request.auth_api_key_hash_id = auth_api_key_hash.id
                return True
        _logger.error("Wrong HTTP_API_KEY, access denied")
        raise AccessDenied()
