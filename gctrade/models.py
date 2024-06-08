from django.db import models
from django.contrib.auth.models import User
import secrets
from .paystack import PayStack
# Create your models here.



STATUS =(
    ('Processing', 'Processing'),
    ('Declined', 'Declined'),
    ('Approved', 'Approved'),
)

CARD_BTN =(
    ('Dollars', 'USD'),
    ('Canada', 'CAD'),
    ('United State', 'UK'),
    ('Australia', 'AUD'),
    ('Euro', 'EUR'),
    ('China', 'CHF'),
    ('New Zeland', 'NZD'),
)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="profile_images", default="blank.webp")
    country = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
            


    class Meta:
        
        verbose_name_plural = 'Profile'
        


class GiftCard(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gift_card_images')
    description = models.TextField()
    rate = models.CharField(max_length=20)
    rate_for_range = models.CharField(max_length=10)
    rate_for_single = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    card_dif = models.CharField(choices=CARD_BTN, blank=True, max_length=12, null=True)
    

    def __str__(self):
        return self.name



class UserSellorBuy(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    gift_card_name = models.CharField(max_length=100)
    ecode = models.TextField()
    amount = models.PositiveBigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=100 , null=True, blank=True)
    momo_provider = models.CharField(max_length=100 , null=True, blank=True)
    momo_number = models.CharField(max_length=100 , null=True, blank=True)
    trans_type = models.CharField(max_length=100 , null=True, blank=True)
    status = models.CharField(choices=STATUS, blank=True, max_length=12, null=True)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    giftCardType = models.CharField(max_length=200)
    otherGiftCardType = models.CharField(max_length=200)
    giftCardAmount = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)
        
    class Meta:
        ordering = ('-date',)
     
    if trans_type == "Bought":
        def __str__(self):
            return f" {self.user} paid {self.amount}"
    else:
        def __str__(self):
            return f" {self.user} Sold {self.giftCardType} for GHS {self.amount}"
    
    

class UserSellImage(models.Model):
    user = models.ForeignKey(UserSellorBuy, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sell_gift_card_images')
    def __str__(self):
        return f" {self.user.user.user} sold {self.user.gift_card_name} image {self.image}"






# class Payments(models.Model):
#     user = models.ForeignKey(Profile, related_name='image', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='payment_images')
#     momo_provider = models.CharField(max_length=100 , null=True, blank=True)
#     def __str__(self):
#         return f"{self.user} payment through {self.momo_provider}"
    



class UserBuy(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    giftCardType = models.CharField(max_length=200)
    otherGiftCardType = models.CharField(max_length=200)
    giftCardAmount = models.PositiveBigIntegerField()
    
    
    class Meta:
        ordering = ('-date',)
        
    def __str__(self):
        return f"Payment: {self.amount}"
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = UserBuy.objects.filter(ref=ref)
            
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)
        
    def amount_value(self) -> int:
        # Just return the amount directly
        return self.amount
    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] == self.amount:
                self.verified = True
            
            self.save()
            if self.verified:
                return True
        return False
