from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="amount_and_price_count")
def amount_and_weight_count(products):
    weight, amount = 0
    for item in products.product_color_quantity.all():
        amount += item.cost
    return mark_safe("<td>%s</td><td><td>"% (amount, ))