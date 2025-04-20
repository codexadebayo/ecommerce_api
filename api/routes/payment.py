

class PaymentRoutes:
    def __init__(self, app):
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/payment', methods=['POST'])
        def process_payment():
            # Logic to process payment
            return "Payment processed", 200

        @self.app.route('/payment/status', methods=['GET'])
        def payment_status():
            # Logic to check payment status
            return "Payment status", 200