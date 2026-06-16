from boxes.models import Box


def recommend_box_for_product(product, quantity=1):
    return recommend_box_for_product_items([{
        'product': product,
        'quantity': quantity,
    }])


def recommend_box_for_product_items(items):
    total_weight = 0
    total_volume = 0

    for item in items:
        product = item['product']
        quantity = item['quantity']

        total_weight += product.weight * quantity
        total_volume += (
            product.length
            * product.width
            * product.height
            * quantity
        )

    suitable_boxes = []

    for box in Box.objects.all():
        box_volume = box.length * box.width * box.height

        if box.max_weight >= total_weight and box_volume >= total_volume:
            suitable_boxes.append(box)

    if not suitable_boxes:
        return None

    suitable_boxes.sort(key=lambda x: x.cost)
    return suitable_boxes[0]


def recommend_box(order):

    total_weight = 0
    total_volume = 0

    for item in order.items.all():

        product = item.product
        qty = item.quantity

        total_weight += product.weight * qty

        total_volume += (
            product.length
            * product.width
            * product.height
            * qty
        )

    suitable_boxes = []

    for box in Box.objects.all():

        box_volume = (
            box.length
            * box.width
            * box.height
        )

        if (
            box.max_weight >= total_weight
            and box_volume >= total_volume
        ):
            suitable_boxes.append(box)

    if not suitable_boxes:
        return None

    suitable_boxes.sort(key=lambda x: x.cost)

    return suitable_boxes[0]
