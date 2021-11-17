from . import models


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class Cart:
    def __init__(self, cart_id):
        self.cart_id = cart_id
        try:
            cart = models.Cart.objects.get(cart_id=self.cart_id, checked_out=False)
        except models.Cart.DoesNotExist:
            cart = self.new()
        self.cart = cart

    def __iter__(self):
        for item in models.Item.objects.filter(cart_id=self.cart.id):
            yield item

    def new(self):
        cart = models.Cart.objects.create(cart_id=self.cart_id)
        cart.save()

        return cart

    def add(self, product, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                cart_id=self.cart.id,
                product=product,
            )
            item.unit_price = unit_price
            item.quantity = item.quantity + int(quantity)
            item.save()
        except models.Item.DoesNotExist:
            item = models.Item.objects.create(cart_id=self.cart.id, product=product, unit_price=unit_price, quantity=quantity)
            item.save()


    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            item.delete()
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist


    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart_id=self.cart.id,
                product=product,
            )
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = int(quantity)
                item.save()
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist



    def count(self):
        result = 0
        for item in models.Item.objects.filter(cart_id=self.cart.id):
            result += 1 * item.quantity
        return result
        
    def summary(self):
        result = 0
        for item in models.Item.objects.filter(cart_id=self.cart.id):
            result += item.total_price
        return result

    def clear(self):
        for item in models.Item.objects.filter(cart_id=self.cart.id):
            item.delete()

