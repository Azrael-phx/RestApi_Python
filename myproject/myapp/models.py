from django.db import models
from cryptography.fernet import Fernet

class Party(models.Model):
    party_id = models.CharField(max_length=255)
    pseudo_id = models.CharField(max_length=255)
    party_type_enum_id = models.CharField(max_length=255)
    owner_party_id = models.CharField(max_length=255)
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, default='Unknown', null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    marital_status_enum_id = models.CharField(max_length=255, null=True, blank=True)
    role_type_id = models.CharField(max_length=255)

class Product(models.Model):
    product_id = models.CharField(max_length=255)
    product_type_enum_id = models.CharField(max_length=255)
    asset_type_enum_id = models.CharField(max_length=255)
    asset_class_Enum_Id = models.CharField(max_length=255)
    charge_shipping = models.CharField(max_length=1)
    returnable = models.CharField(max_length=1)
    product_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    owner_party_id = models.CharField(max_length=255)

class Order(models.Model):
    order_id = models.CharField(primary_key = True, max_length=100, unique=True)
    order_name = models.CharField(max_length=255)
    currency_uom_id = models.CharField(max_length=3, default='USD')
    sales_channel_enum_id = models.CharField(max_length=10, default='ScWeb')
    status_id = models.CharField(max_length=20, default='OrderPlaced')
    product_store_id = models.CharField(max_length=20, default='OMS_DEFAULT_STORE')
    placed_date = models.DateField()
    approved_date = models.DateField(null=True, blank=True)

    CREDIT_CARD_KEY = Fernet.generate_key()
    cipher_suite = Fernet(CREDIT_CARD_KEY)

    credit_card = models.TextField(null=True, blank=True)

    def set_credit_card(self, credit_card_number):
        encrypted_credit_card = self.cipher_suite.encrypt(credit_card_number.encode())
        self.credit_card = encrypted_credit_card.decode()

    def get_credit_card(self):
        if self.credit_card:
            decrypted_credit_card = self.cipher_suite.decrypt(self.credit_card.encode())
            return decrypted_credit_card.decode()
        return None

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product_id = models.CharField(max_length=100)
    item_description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_amount = models.DecimalField(max_digits=10, decimal_places=2)

class Person(models.Model):
    party_id = models.CharField(max_length=40, primary_key=True)
    party_type_enum_id = models.CharField(max_length=40, default=None, null=True)
