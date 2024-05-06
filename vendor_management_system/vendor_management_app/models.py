from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

def rating_validator(value):
    if value<0.0 or value>5.0:
        raise ValidationError(_('Rating value must be between 0.0 and 5.0'))

class Vendor(models.Model):
    name = models.CharField(max_length=30,verbose_name=_("Name"))
    contact_details = models.TextField(max_length=150,verbose_name=_("Contact Details"))
    address = models.TextField(max_length=200,verbose_name=_("Address"))
    vendor_code = models.CharField(max_length=6,verbose_name=_("Vendor Code"),unique=True,blank=True,null=False)
    on_time_delivery_rate = models.FloatField(verbose_name=_("On-Time Delivery Rate"),default=0)
    quality_rating_avg = models.FloatField(verbose_name=_("Quality rating Average"),default=0,validators=[rating_validator])
    average_response_time = models.FloatField(verbose_name=_("Average Response Time"),default=0)
    fulfillment_rate = models.FloatField(verbose_name=_("Fulfillment Rate"),default=0)
    
    def __str__(self):
        return f'Vendor {self.name}'

class Purchase_Order(models.Model):
    po_number = models.CharField(max_length=6,verbose_name=_("PO_Number"),unique=True,blank=True,null=False)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,verbose_name=_("Vendor"))
    order_date = models.DateTimeField(verbose_name=_("Order Date"))
    items = models.JSONField(verbose_name=_("Items"))
    quantity = models.IntegerField(verbose_name=_("Quantity"))
    choices = (
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Canceled','Canceled'),
    )
    status = models.CharField(verbose_name=_("Status"),max_length=10,choices=choices)
    expected_delivery_date = models.DateTimeField(verbose_name=_("Expected Delivery Date"))
    quality_rating = models.FloatField(verbose_name=_("Quality Rating"),null=True,validators=[rating_validator])
    issue_date = models.DateTimeField(verbose_name=_("Issue Date"),auto_now_add=True)
    acknowledgment_date = models.DateTimeField(verbose_name=_("Acknowledgment Date"),null=True)
    
    def __str__(self):
        return f'Order {self.po_number}'

class Historical_Performance(models.Model):
    vendor = models.OneToOneField(Vendor,on_delete=models.CASCADE,verbose_name=_("Vendor"))
    date = models.DateTimeField(verbose_name=_("Performance Record Date"),auto_now_add=True)
    on_time_delivery_rate = models.FloatField(verbose_name=_("On-Time Delivery Rate"),default=0)
    quality_rating_avg = models.FloatField(verbose_name=_("Quality rating Average"),validators=[rating_validator],default=0)
    average_response_time = models.FloatField(verbose_name=_("Average Response Time"),default=0)
    fulfillment_rate = models.FloatField(verbose_name=_("Fulfillment Rate"),default=0)
    
    def __str__(self):
        return f'{self.vendor} Performance'
    
    
    
