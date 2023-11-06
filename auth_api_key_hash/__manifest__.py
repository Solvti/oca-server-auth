# Copyright 2023 Solvti Sp. z o.o.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Auth Api Key (Hash)",
    "summary": """
        Authenticate http requests from an API key (hash)""",
    "version": "13.0.1.0.0",
    "license": "LGPL-3",
    "author": "Solvti Sp. z o.o.,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-auth",
    "depends": ["base", "base_sparse_field"],
    "data": ["security/ir.model.access.csv", "views/auth_api_key_hash.xml"],
    "demo": [],
}
