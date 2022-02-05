from ariadne import QueryType, convert_kwargs_to_snake_case, MutationType, upload_scalar
from .models import Product, Category, ProductImage, Order
from django.conf import settings
from cart.cart import Cart
from ariadne_jwt.decorators import login_required

query = QueryType()
mutation = MutationType()


@query.field('product')
@convert_kwargs_to_snake_case
def resolve_product(_, info, product_id):
    prod = Product.objects.get(pk=product_id)
    return {
        "id": prod.id,
        "name": prod.name,
        "categoryId": prod.category_id,
        "price": prod.price,
        "offer": prod.offer,
        "discount": prod.discount,
        "inStock": prod.in_stock,
        "createdAt": prod.created_at,
        "description": prod.description,
        "images": [
            f'{settings.SITE_URL}{obj.image.url}' for obj in ProductImage.objects.filter(product_id=prod.id)
        ]
    }


@query.field('products')
def resolve_products(_, info):
    return [{
        "id": prod.id,
        "name": prod.name,
        "categoryId": prod.category_id,
        "price": prod.price,
        "offer": prod.offer,
        "discount": prod.discount,
        "inStock": prod.in_stock,
        "createdAt": prod.created_at,
        "description": prod.description,
        "images": [
            f'{settings.SITE_URL}{obj.image.url}' for obj in ProductImage.objects.filter(product_id=prod.id)
        ]
    } for prod in Product.objects.all()]


@query.field('category')
@convert_kwargs_to_snake_case
def resolve_category(_, info, category_id):
    category = Category.objects.get(pk=category_id)
    return {
        "id": category.id,
        "name": category.name,
        "image": f'{settings.SITE_URL}{category.image.url}'
    }


@query.field('categoryProducts')
def resolve_cat_prods(_, info):
    return [
        {
            "category": {
                "id": cat.id,
                "name": cat.name,
                "image": f'{settings.SITE_URL}{cat.image.url}'
            },
            "products": [
                {
                    "id": prod.id,
                    "name": prod.name,
                    "categoryId": prod.category_id,
                    "price": prod.price,
                    "offer": prod.offer,
                    "discount": prod.discount,
                    "inStock": prod.in_stock,
                    "createdAt": prod.created_at,
                    "description": prod.description,
                    "images": [
                        f'{settings.SITE_URL}{obj.image.url}' for obj in ProductImage.objects.filter(product_id=prod.id)
                    ]
                } for prod in Product.objects.filter(category_id=cat.id)
            ]
        } for cat in Category.objects.all()
    ]


def get_prod(prod_id):
    prod = Product.objects.get(pk=prod_id)
    return {
            "id": prod.id,
            "name": prod.name,
            "categoryId": prod.category_id,
            "price": prod.price,
            "offer": prod.offer,
            "discount": prod.discount,
            "inStock": prod.in_stock,
            "createdAt": prod.created_at,
            "description": prod.description,
            "images": [
                f'{settings.SITE_URL}{obj.image.url}' for obj in ProductImage.objects.filter(product_id=prod.id)
            ]
    }


@query.field('similarProducts')
@convert_kwargs_to_snake_case
def resolve_similar_products(_, info, product_id):
    product = Product.objects.get(pk=product_id)
    category_id = product.category_id
    return [
        get_prod(prod.id) for prod in Product.objects.filter(category_id=category_id)
    ]


@query.field('cart')
@convert_kwargs_to_snake_case
def resolve_cart(_, info, cart_id):
    request = info.context["request"]
    cart = Cart(cart_id)
    return {
        "items": [
            {
                "product": get_prod(item.product.id),
                "unitPrice": item.unit_price,
                "quantity": item.quantity,
                "total": item.total_price
            }for item in cart
        ],
        "summary": cart.summary(),
        "count": cart.count()
    }


@query.field('orders')
def resolve_orders(_, info):
    return Order.objects.all()


@query.field("order")
@convert_kwargs_to_snake_case
def resolve_order(_, info, product_id):
    return Order.objects.get(pk=product_id)

@query.field("userOrders")
@convert_kwargs_to_snake_case
def resolve_user_orders(_, info, user_id):
    return Order.objects.filter(customer_id=user_id)



@mutation.field('createCategory')
@login_required
def resolve_create_category(_, info, name, image):
    try:
        category = Category.objects.create(name=name, image=image)
        category.save()
        return {
            "success": True
        }
    except:
        return {
            "success": False
        }


@mutation.field('createProduct')
@convert_kwargs_to_snake_case
@login_required
def resolve_create_product(_, info, name, category_id, price, offer, discount, in_stock, description):
    try:
        prod = Product.objects.create(
            name=name,
            category_id=category_id,
            price=price,
            offer=offer,
            discount=discount,
            in_stock=in_stock,
            description=description
        )
        return{
            "success": True
        }
    except:
        return {
            "success": False
        }


@mutation.field('uploadProductImage')
@convert_kwargs_to_snake_case
@login_required
def resolve_upload_prod_image(_, info, product_id, image):
    try:
        image = ProductImage.objects.create(product_id=product_id, image=image)
        image.save()
        return {
            "success": True
        }
    except:
        return {
            "success": False
        }


@mutation.field('addItem')
@convert_kwargs_to_snake_case
def resolve_add_item(_, info, cart_id, product_id, quantity):
    try:
        cart = Cart(cart_id)
        product = Product.objects.get(pk=product_id)
        cart.add(product, unit_price=product.price, quantity=quantity)
        return {
            "success": True,
            "cart": {
                "items": [
                    {
                        "order": item.order,
                        "product": get_prod(item.product.id),
                        "unitPrice": item.unit_price,
                        "quantity": item.quantity,
                        "total": item.total_price
                    } for item in cart
                ],
                "summary": cart.summary(),
                "count": cart.count()
            }
        }
    except:
        return {
            "success": False,
            "cart": {
                "items": [
                    {
                        "order": item.order,
                        "product": get_prod(item.product.id),
                        "unitPrice": item.unit_price,
                        "quantity": item.quantity,
                        "total": item.total_price
                    } for item in cart
                ],
                "summary": cart.summary(),
                "count": cart.count()
            }
        }


@mutation.field('removeItem')
@convert_kwargs_to_snake_case
def resolve_remove_item(_, info, cart_id, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        cart = Cart(cart_id)
        cart.remove(product)
        return {
            "success": True,
            "cart": {
                "items": [
                    {
                        "order": item.order,
                        "product": get_prod(item.product.id),
                        "unitPrice": item.unit_price,
                        "quantity": item.quantity,
                        "total": item.total_price
                    } for item in cart
                ],
                "summary": cart.summary(),
                "count": cart.count()
            }
        }
    except:
        return{
            "success": False,
            "cart": {
                "items": [
                    {
                        "order": item.order,
                        "product": get_prod(item.product.id),
                        "unitPrice": item.unit_price,
                        "quantity": item.quantity,
                        "total": item.total_price
                    } for item in cart
                ],
                "summary": cart.summary(),
                "count": cart.count()
            }
        }

@mutation.field("updateItem")
@convert_kwargs_to_snake_case
def resolve_update_item(_, info, cart_id, product_id, quantity):
    try:
        cart = Cart(cart_id)
        product = Product.objects.get(pk=product_id)
        cart.update(product=product, quantity=quantity, unit_price=product.price)
        return {
            "success": True,
            "cart": {
                "items": [
                    {
                        "order": item.order,
                        "product": get_prod(item.product.id),
                        "unitPrice": item.unit_price,
                        "quantity": item.quantity,
                        "total": item.total_price
                    } for item in cart
                ],
                "summary": cart.summary(),
                "count": cart.count()
            }
        }
    except:
        return{
            "success": False,
            "cart": {
                "items": [
                    {
                        "order": item.order,
                        "product": get_prod(item.product.id),
                        "unitPrice": item.unit_price,
                        "quantity": item.quantity,
                        "total": item.total_price
                    } for item in cart
                ],
                "summary": cart.summary(),
                "count": cart.count()
            }
        }

@mutation.field('search')
def resolve_search(_, info, key):
    results = []

    for product in Product.objects.filter(name__contains=key):
        results.append(get_prod(product.id))

    for product in Product.objects.filter(category__name__contains=key):
        results.append(get_prod(product.id))

    return {
        "results": results
        }


@mutation.field("createOrder")
@convert_kwargs_to_snake_case
@login_required
def resolve_create_order(_, info, customer_id, cart_id):
    try:
        order = Order.objects.create(customer_id=customer_id, cart_id=cart_id)
        order.save()
        return {
            "success": True
        }
    except:
        return {
            "success": False
        }


@mutation.field("updateOrder")
@convert_kwargs_to_snake_case
@login_required
def resolve_update_order(_, info,order_id, paid, payment, status):
    try:
        order = Order.objects.get(pk=order_id)
        order.paid = paid
        order.payment = payment
        order.status = status
        order.save()
        return {
           "success": True
        }
    except:
        return {
            "success": False
        }


resolvers = [query, mutation, upload_scalar]
