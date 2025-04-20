

class CategoriesRoutes:
    def __init__(self, app):
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/categories', methods=['GET'])
        def get_categories():
            return {"message": "List of categories"}

        @self.app.route('/categories/<int:category_id>', methods=['GET'])
        def get_category(category_id):
            return {"message": f"Category {category_id}"}

        @self.app.route('/categories', methods=['POST'])
        def create_category():
            return {"message": "Category created"}, 201

        @self.app.route('/categories/<int:category_id>', methods=['PUT'])
        def update_category(category_id):
            return {"message": f"Category {category_id} updated"}

        @self.app.route('/categories/<int:category_id>', methods=['DELETE'])
        def delete_category(category_id):
            return {"message": f"Category {category_id} deleted"}