from tortoise import fields
from tortoise.models import Model


class DiscountModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=45, unique=True)
    percentage = fields.DecimalField(max_digits=30, decimal_places=5)
    is_visible = fields.BooleanField(default=True)

    class Meta:
        table = "crm_discounts"

    def __repr__(self):
        return f"<Discount(name={self.name}, percentage={self.percentage}%, is_visible={self.is_visible})>"
