

class WishlistRoutes:
    def __init__(self, app, wishlist_controller):
        self.app = app
        self.wishlist_controller = wishlist_controller
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/api/wishlist', view_func=self.wishlist_controller.get_wishlist, methods=['GET'])
        self.app.add_url_rule('/api/wishlist', view_func=self.wishlist_controller.add_to_wishlist, methods=['POST'])
        self.app.add_url_rule('/api/wishlist/<int:item_id>', view_func=self.wishlist_controller.remove_from_wishlist, methods=['DELETE'])