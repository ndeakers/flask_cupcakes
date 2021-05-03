from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        #like spread!
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake
        #self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_update_cupcake(self):
        """
        test update flavor
        return updated JSON
        {cupcake: {id, flavor, size, rating, image}}
        && doesnt add a new cupcake to database
        """
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json={'cupcake':  {
                    "flavor": "vanilla",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg",
                    "id" : self.cupcake.id
                }
            })

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "vanilla",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg",
                    "id" : self.cupcake.id
                }
            })

            self.assertEqual(Cupcake.query.count(), 1)



    def test_delete_cupcake(self):
        """
        test delete cupcake
        returns JSON { "message": "Deleted" }
        and 0 cupcakes in database
        """
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"

            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(data, {
                "message": "Deleted"
            })

            self.assertEqual(Cupcake.query.count(), 0)

