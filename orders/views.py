from django.shortcuts import render

from products.models import Product
from boxes.models import Box
from orders.models import Order
from services.box_selecter import recommend_box, recommend_box_for_product_items


def dashboard(request):
    recent_orders = list(Order.objects.all().order_by('-id')[:5])
    recommendation_count = 0
    order_recommendations = []

    for order in recent_orders:
        recommended_box = recommend_box(order)
        if recommended_box:
            recommendation_count += 1
        order_recommendations.append({
            'order': order,
            'recommended_box': recommended_box,
        })

    last_products = []
    last_box = None
    last_quantity = 1
    last_items = []

    if request.method == 'POST':
        names = request.POST.getlist('name')
        lengths = request.POST.getlist('length')
        widths = request.POST.getlist('width')
        heights = request.POST.getlist('height')
        weights = request.POST.getlist('weight')
        quantity_values = request.POST.getlist('quantity')

        try:
            product_items = []

            for name, length, width, height, weight, quantity in zip(
                names,
                lengths,
                widths,
                heights,
                weights,
                quantity_values,
            ):
                name = (name or '').strip()

                if not all([name, length, width, height, weight]):
                    continue

                product = Product.objects.create(
                    name=name,
                    length=float(length),
                    width=float(width),
                    height=float(height),
                    weight=float(weight),
                )
                product_items.append({
                    'product': product,
                    'quantity': max(1, int(quantity or 1)),
                })

            if product_items:
                last_products = [item['product'] for item in product_items]
                last_items = product_items
                last_quantity = sum(item['quantity'] for item in product_items)
                last_box = recommend_box_for_product_items(product_items)
        except (TypeError, ValueError):
            last_box = None

    context = {
        "total_products": Product.objects.count(),
        "total_boxes": Box.objects.count(),
        "total_orders": Order.objects.count(),
        "recommendations": recommendation_count,
        "orders": order_recommendations,
        "last_products": last_products,
        "last_items": last_items,
        "last_box": last_box,
        "last_quantity": last_quantity,
    }
    return render(request, "dashboard.html", context)


def products_view(request):
    products = Product.objects.all().order_by('name')
    return render(request, "products.html", {"products": products})


def boxes_view(request):
    notice = None

    if request.method == 'POST':
        action = request.POST.get('action')

        try:
            box_data = {
                'name': (request.POST.get('name') or '').strip(),
                'length': float(request.POST.get('length')),
                'width': float(request.POST.get('width')),
                'height': float(request.POST.get('height')),
                'max_weight': float(request.POST.get('max_weight')),
                'cost': float(request.POST.get('cost')),
            }

            if not box_data['name']:
                raise ValueError

            if action == 'add':
                Box.objects.create(**box_data)
                notice = 'Box added successfully.'
            elif action == 'update':
                box = Box.objects.get(id=request.POST.get('box_id'))
                for field, value in box_data.items():
                    setattr(box, field, value)
                box.save()
                notice = 'Box updated successfully.'
        except (Box.DoesNotExist, TypeError, ValueError):
            notice = 'Please enter valid box details before saving.'

    boxes = Box.objects.all().order_by('name')
    return render(request, "boxes.html", {"boxes": boxes, "notice": notice})


def orders_view(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, "orders.html", {"orders": orders})
