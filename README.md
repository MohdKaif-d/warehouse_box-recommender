# Warehouse Box Recommendation System

## Overview

The Warehouse Box Recommendation System is a Django-based application designed to help warehouse teams choose the most suitable shipping box for customer orders.

In many e-commerce operations, selecting the right packaging is important for reducing shipping costs and ensuring products are packed safely. This project automates that process by analyzing product dimensions, weight, and quantity, then recommending the most appropriate box from the available inventory.

The system also provides a simple box management interface where warehouse administrators can add, view, and update box specifications such as dimensions, weight capacity, and cost.

---

## Key Features

* Dashboard for managing box recommendations
* Support for single or multiple products in an order
* Quantity-based calculations for products
* Automatic box recommendation based on weight and volume
* Box management interface for adding and updating box information
* Product, box, and order listings
* Unit tests covering core business logic

---

## Technology Stack

* Python
* Django
* SQLite
* HTML & CSS
* Django Templates

---

## Project Structure

```text
warehouse_project/
├── boxes/                 # Box management and related tests
├── orders/                # Order models, views, and dashboard logic
├── products/              # Product models and product management
├── services/              # Box recommendation service
├── templates/             # HTML templates
├── warehouse_project/     # Django settings and URL configuration
├── db.sqlite3
├── manage.py
└── README.md
```

---

## How the Recommendation Engine Works

The recommendation logic is implemented in:

```text
services/box_selector.py
```

For each product, the system calculates:

```python
product_volume = length * width * height * quantity
product_weight = weight * quantity
```

When multiple products are included in an order, their volumes and weights are aggregated to determine the overall shipping requirements.

The system then evaluates all available boxes and filters those that satisfy both of the following conditions:

```python
box.max_weight >= total_weight
box_volume >= total_volume
```

If multiple boxes meet the requirements, the system recommends the box with the lowest cost.

### Current Scope

The recommendation is based on total volume and weight calculations. Advanced packing techniques such as 3D bin packing, product orientation, or exact placement optimization are outside the scope of this implementation.

---

## Installation and Setup

### Clone the Repository

```bash
git clone <repository-url>
cd warehouse_project
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install django
```

### Apply Database Migrations

```bash
python manage.py migrate
```

### Start the Development Server

```bash
python manage.py runserver
```

Once the server is running, open:

```text
http://127.0.0.1:8000/
```

---

## Application Pages

| URL          | Description                                 |
| ------------ | ------------------------------------------- |
| `/`          | Main dashboard and recommendation interface |
| `/products/` | Product listing page                        |
| `/boxes/`    | Box management dashboard                    |
| `/orders/`   | Order management page                       |
| `/admin/`    | Django administration panel                 |

---

## Using the Recommendation System

1. Open the dashboard.
2. Enter product details including dimensions, weight, and quantity.
3. Add additional products if the order contains multiple items.
4. Submit the order for evaluation.
5. The system calculates the combined volume and weight of all products.
6. A suitable shipping box is recommended based on the available box inventory.

---

## Managing Shipping Boxes

The box management section allows administrators to maintain available packaging options.

Users can:

* Add new boxes
* Update box dimensions
* Modify weight capacities
* Adjust box costs
* View all available box configurations

Any updates made to box data are immediately considered in future recommendations.

---

## Running Tests

To execute all tests:

```bash
python manage.py test
```

To run tests for specific applications:

```bash
python manage.py test boxes orders
```

### Test Coverage

The test suite validates:

* Correct selection of the lowest-cost suitable box
* Handling of orders that do not fit any available box
* Recommendations involving multiple products
* Box creation functionality
* Box update operations

---

## Data Models

### Product

Stores product-related information:

* Name
* Length
* Width
* Height
* Weight

### Box

Stores shipping box specifications:

* Name
* Length
* Width
* Height
* Maximum Weight Capacity
* Cost

### Order & OrderItem

These models represent customer orders and the products associated with each order, including quantities.

---

## Future Improvements

Potential enhancements for future versions include:

* Advanced 3D packing algorithms
* Multiple-box recommendations for large orders
* Shipping carrier integration
* Cost optimization based on shipping rates
* User authentication and role-based access control
* REST API support for external integrations

---

## Conclusion

This project demonstrates the core concepts behind an automated warehouse box recommendation system using Django. It provides a practical solution for selecting appropriate packaging based on product dimensions and weight while maintaining a simple and maintainable architecture.

While the current implementation focuses on fundamental recommendation logic, it provides a strong foundation for future enhancements and real-world warehouse applications.
