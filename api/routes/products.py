

class Products:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.get_all_products()

    def get_by_id(self, product_id):
        return self.db.get_product_by_id(product_id)

    def create(self, product_data):
        return self.db.create_product(product_data)

    def update(self, product_id, product_data):
        return self.db.update_product(product_id, product_data)

    def delete(self, product_id):
        return self.db.delete_product(product_id)