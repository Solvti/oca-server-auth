To apply this authentication system to your http request you must set 'api_key_hash'
as value for the 'auth' parameter of your route definition into your controller.

.. code-block:: python

    class MyController(Controller):

        @route('/my_service', auth='api_key_hash', ...)
        def my_service(self, *args, **kwargs):
            pass
