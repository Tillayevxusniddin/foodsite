from django.db import models

#kategoriyasi
class Category(models.Model):
    title = models.CharField(null=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


#mahsulot
class Product(models.Model):
    title = models.CharField(null=False, blank=False, max_length=100) #null=False databasega null qiymat saqlamaydi
    description = models.TextField(null=False, blank=False) #blank=False forma yuborish vaqtida maydon bolishi mumkin emas
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    cost = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    image = models.ImageField(upload_to='products') #rasmlar saqlanadigan joy
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

#Klient
class Customer(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=100)
    last_name = models.CharField(null=False, blank=False, max_length=100)
    phone_number = models.CharField(null=False, unique=True, blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#zakaz -- > 2 sahifa uchun
class Order(models.Model):
    payment_type = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(null=False, blank=True, default=1)
    address = models.CharField(null=False, blank=False, max_length=250)
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


#savat uchun
class OrderProduct(models.Model):
    count = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)