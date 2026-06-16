from django.test import TestCase

from boxes.models import Box


class BoxAdminDashboardTests(TestCase):
    def test_adds_box_from_boxes_page(self):
        response = self.client.post('/boxes/', {
            'action': 'add',
            'name': 'Medium Box',
            'length': '20',
            'width': '15',
            'height': '10',
            'max_weight': '25',
            'cost': '80',
        })

        self.assertEqual(response.status_code, 200)
        box = Box.objects.get(name='Medium Box')
        self.assertEqual(box.length, 20)
        self.assertEqual(box.width, 15)
        self.assertEqual(box.height, 10)
        self.assertEqual(box.max_weight, 25)
        self.assertEqual(box.cost, 80)

    def test_updates_existing_box_from_boxes_page(self):
        box = Box.objects.create(
            name='Old Box',
            length=10,
            width=10,
            height=10,
            max_weight=5,
            cost=20,
        )

        response = self.client.post('/boxes/', {
            'action': 'update',
            'box_id': str(box.id),
            'name': 'Updated Box',
            'length': '30',
            'width': '20',
            'height': '15',
            'max_weight': '40',
            'cost': '120',
        })

        self.assertEqual(response.status_code, 200)
        box.refresh_from_db()
        self.assertEqual(box.name, 'Updated Box')
        self.assertEqual(box.length, 30)
        self.assertEqual(box.width, 20)
        self.assertEqual(box.height, 15)
        self.assertEqual(box.max_weight, 40)
        self.assertEqual(box.cost, 120)
