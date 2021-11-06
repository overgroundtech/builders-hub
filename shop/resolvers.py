from ariadne import QueryType, convert_kwargs_to_snake_case, MutationType, upload_scalar
from .models import Product, Category, ProductImage
from django.conf import settings
from cart.cart import Cart


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
        "name": category.name
    }


@query.field('categoryProducts')
def resolve_cat_prods(_, info):
    return [
        {
            "category": {
                "id": cat.id,
                "name": cat.name,
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
                    "images": [
                        f'{settings.SITE_URL}{obj.image.url}' for obj in ProductImage.objects.filter(product_id=prod.id)
                    ]
                } for prod in Product.objects.filter(category_id=cat.id)
            ]
        } for cat in Category.objects.all()
    ]


@query.field('cart')
def resolve_cart(_, info):
    request = info.context["request"]
    cart = Cart(request)
    return {
        "items": [
            {
                "order": item.order,
                "product": item.product,
                "unitPrice": item.unit_price,
                "quantity": item.quantity,
                "total": item.total_price
            }for item in cart
        ],
        "summary": cart.summary(),
        "count": cart.count(),
    }


@mutation.field('createCategory')
def resolve_create_category(_, info, name):
    try:
        category = Category.objects.create(name=name)
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
def resolve_create_product(_, info, name, category_id, price, offer, discount, in_stock):
    try:
        prod = Product.objects.create(
            name=name,
            category_id=category_id,
            price=price,
            offer=offer,
            discount=discount,
            in_stock=in_stock
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
def resolve_add_item(_, info, product_id, quantity):
    try:
        request = info.context["request"]
        cart = Cart(request)
        product = Product.objects.get(pk=product_id)
        cart.add(product, unit_price=product.price, quantity=quantity)
        return {
            "success": True
        }
    except:
        return {
            "success": False
        }


@mutation.field('removeItem')
@convert_kwargs_to_snake_case
def resolve_remove_item(_, info, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        request = info.context["request"]
        cart = Cart(request)
        cart.remove(product)
        return {
            "success": True
        }
    except:
        return{
            "success": False
        }

@mutation.field("updateItem")
@convert_kwargs_to_snake_case
def resolve_update_item(_, info, product_id, quantity):
    try:
        request = info.context["request"]
        cart = Cart(request)
        product = Product.objects.get(pk=product_id)
        cart.update(product=product, quantity=quantity)
        return {
            "success": True
        }
    except:
        return{
            "success": False
        }


resolvers = [query, mutation, upload_scalar]
