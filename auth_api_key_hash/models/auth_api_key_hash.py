# Copyright 2023 Solvti Sp. z o.o.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from hashlib import md5

from odoo import _, api, fields, models, tools
from odoo.exceptions import AccessError, ValidationError
from odoo.tools import consteq


class AuthApiKeyHash(models.Model):
    _name = "auth.api.key.hash"
    _description = "API Key (Hash)"

    name = fields.Char(required=True)
    key = fields.Char(required=True, copy=False, help="""The API key.""",)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        required=True,
        help="""The user used to process the requests authenticated by
        the api key""",
    )

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Api Key name must be unique."),
        ("key_uniq", "unique(key)", "Api Key must be unique."),
    ]

    @api.model
    def _retrieve_api_key(self, key):
        return self.browse(self._retrieve_api_key_id(key))

    @api.model
    @tools.ormcache("key")
    def _retrieve_api_key_id(self, key):
        if not self.env.user.has_group("base.group_system"):
            raise AccessError(_("User is not allowed"))
        hash_key = md5(key.encode("utf-8")).hexdigest()
        for api_key in self.search([]):
            if consteq(hash_key, api_key.key):
                return api_key.id
        raise ValidationError(_("The key %s is not allowed") % key)

    @api.model
    @tools.ormcache("key")
    def _retrieve_uid_from_api_key(self, key):
        return self._retrieve_api_key(key).user_id.id

    def _clear_key_cache(self):
        self._retrieve_api_key_id.clear_cache(self.env[self._name])
        self._retrieve_uid_from_api_key.clear_cache(self.env[self._name])

    @api.model
    def create(self, vals):
        if new_key := vals.get("key", ""):
            vals["key"] = md5(new_key.encode("utf-8")).hexdigest()
        record = super(AuthApiKeyHash, self).create(vals)
        if "key" in vals or "user_id" in vals:
            self._clear_key_cache()
        return record

    def write(self, vals):
        if vals.get("key", False):
            raise ValidationError(_("You can't change api-key! Please add new one."))
        super(AuthApiKeyHash, self).write(vals)
        if "key" in vals or "user_id" in vals:
            self._clear_key_cache()
        return True
