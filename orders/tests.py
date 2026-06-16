from django.test import TestCase

from boxes.models import Box
from products.models import Product
from services.box_selecter import recommend_box_for_product


class BoxRecommendationTests(TestCase):
    def test_returns_cheapest_box_that_fits_product(self):
        product = Product.objects.create(
            name='Laptop Box',
            length=20,
            width=15,
            height=10,
            weight=5,
        )

        Box.objects.create(name='Small Box', length=20, width=15, height=10, max_weight=10, cost=50)
        Box.objects.create(name='Large Box', length=30, width=25, height=20, max_weight=20, cost=120)

        recommended = recommend_box_for_product(product)

        self.assertIsNotNone(recommended)
        self.assertEqual(recommended.name, 'Small Box')

    def test_returns_none_when_no_box_can_fit(self):
        product = Product.objects.create(
            name='Heavy Item',
            length=100,
            width=100,
            height=100,
            weight=100,
        )

        Box.objects.create(name='Tiny Box', length=10, width=10, height=10, max_weight=1, cost=10)

        recommended = recommend_box_for_product(product)

        self.assertIsNone(recommended)

    def test_dashboard_recommends_from_multiple_products(self):
        Box.objects.create(name='Too Small', length=10, width=10, height=10, max_weight=4, cost=10)
        Box.objects.create(name='Combined Fit', length=20, width=20, height=20, max_weight=10, cost=20)

        response = self.client.post('/', {
            'name': ['Stackable Item', 'Wide Item'],
            'length': ['10', '5'],
            'width': ['10', '5'],
            'height': ['1', '2'],
            'weight': ['1', '1'],
            'quantity': ['2', '3'],
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['last_items']), 2)
        self.assertEqual(response.context['last_quantity'], 5)
        self.assertEqual(response.context['last_box'].name, 'Combined Fit')
