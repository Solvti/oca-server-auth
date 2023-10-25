# Copyright 2023 Solvti Sp. z o.o.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import SavepointCase


class TestAuthApiKeyHash(SavepointCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        cls.AuthApiKeyHash = cls.env["auth.api.key.hash"]
        cls.demo_user = cls.env.ref("base.user_demo")
        cls.api_key_good = cls.AuthApiKeyHash.create(
            {"name": "good", "user_id": cls.demo_user.id, "key": "api_key"}
        )

    def test_lookup_key_from_db(self):
        demo_user = self.env.ref("base.user_demo")
        self.assertEqual(
            self.env["auth.api.key.hash"]._retrieve_uid_from_api_key("api_key"),
            demo_user.id,
        )

    def test_wrong_key(self):
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            self.env["auth.api.key.hash"]._retrieve_uid_from_api_key("api_wrong_key")

    def test_user_not_allowed(self):
        # only system users can check for key
        with self.assertRaises(AccessError), self.env.cr.savepoint():
            self.env["auth.api.key.hash"].with_user(
                user=self.demo_user
            )._retrieve_uid_from_api_key("api_wrong_key")

    def test_no_edit_key(self):
        self.assertEqual(
            self.env["auth.api.key.hash"]._retrieve_uid_from_api_key("api_key"),
            self.demo_user.id,
        )
        with self.assertRaises(ValidationError):
            self.api_key_good.write({"key": "updated_key"})
