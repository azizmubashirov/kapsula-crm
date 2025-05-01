from django.utils.safestring import mark_safe
from django import template
from web_project.template_helpers.theme import TemplateHelper
from django.contrib.auth.decorators import user_passes_test
import re
from apps.product.models import Product, QuantityChange, Color
from django.db.models import Sum, F, DecimalField
from decimal import Decimal
from apps.order.models import Order, OrderPayment
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def get_theme_variables(scope):
    return mark_safe(TemplateHelper.get_theme_variables(scope))


@register.simple_tag
def get_theme_config(scope):
    return mark_safe(TemplateHelper.get_theme_config(scope))


@register.filter
def filter_by_url(submenu, url):
    if submenu:
        for subitem in submenu:
            subitem_url = subitem.get("url")
            if subitem_url == url.path or subitem_url == url.resolver_match.url_name:
                return True

            # Recursively check for submenus
            elif subitem.get("submenu"):
                if filter_by_url(subitem["submenu"], url):
                    return True

    return False


# Check if the user has the group
@register.filter
def has_group(user, group):
    if user.groups.filter(name=group).exists():
        return True

# Check if the user has the permission
@register.filter
def has_permission(user, permission):
    if user.has_perm(permission):
        return True


# For checking if the user group is admin
@register.filter(name="is_admin")
def is_admin(user):
    return user.groups.filter(name="admin").exists()

@register.filter(name="admin_required")
def admin_required(view_func):
    return user_passes_test(is_admin, login_url='login')(view_func)


# For checking if the user group is client
@register.filter(name="is_client")
def is_client(user):
    return user.groups.filter(name="client").exists()

@register.filter(name="client_required")
def client_required(view_func):
    return user_passes_test(is_client, login_url='login')(view_func)


# For checking if is_superuser
@register.filter(name="is_superuser")
def is_superuser(user):
    return user.is_superuser

@register.filter(name="superuser_required")
def superuser_required(view_func):
    return user_passes_test(is_superuser, login_url='login')(view_func)


# For checking if is_staff
@register.filter(name="is_staff")
def is_staff(user):
    return user.is_staff

@register.filter(name="staff_required")
def staff_required(view_func):
    return user_passes_test(is_staff, login_url='login')(view_func)

@register.simple_tag
def current_url(request):
    return request.build_absolute_uri()

@register.simple_tag
def amount_and_weight_count(products):
    weight, amount, pack = 0, 0, 0
    for item in products.product_color_quantity.all():
        amount += item.quantity
        
        name = item.product.product.name
        number_part = re.match(r'^\d+', name)
        if number_part:
            number_part = number_part.group()
        try:
            result = int(number_part) / 1000 if number_part else 0.01
        except ValueError:
            result = 0.01
        weight1 = result
        weight += weight1 * item.quantity
        pack += item.quantity / item.product.product.pack if item.product.product.pack else 0
    return mark_safe("""<td style='color: black;'class='text-center'><b>%s</b></td>
                     <td style='color: black;' class="text-center">
                     <div class="d-flex justify-content-between align-items-center">
                        <b class="mx-auto">%s</b>
                    </td>
          <td style='color: black;'class='text-center'><b>%s</b></td>
          <td></td>
          """% (p_format(amount), simplify_number(pack),  simplify_number(weight)))

@register.simple_tag
def weight_calculation(quantity, item):
    name = item.product.name
    number_part = re.match(r'^\d+', name)
    if number_part:
        number_part = number_part.group()
    try:
        result = int(number_part) / 1000 if number_part else 0.01
    except ValueError:
        result = 0.01 
        
    weight = result
    total_weight = quantity * weight
    return round(total_weight, 2)

@register.simple_tag
def pack_calculation(quantity, item):
    pack = item.product.pack
    total_weight = quantity / pack if pack else 0
    return simplify_number(total_weight)

@register.simple_tag
def total_calculation(products):
    weight, amount = 0, 0
    for product in products:
        name = product.product.name
        number_part = re.match(r'^\d+', name)
        if number_part:
            number_part = number_part.group()
        try:
            result = int(number_part) / 1000 if number_part else 0.01
        except ValueError:
            result = 0.01 
        weight1 = result
        for item in product.product_color_quantity.all():
            amount += item.quantity
            weight += weight1 * item.quantity
    return p_format(amount)

@register.simple_tag
def total_weight_calculation(products):
    weight, amount = 0, 0
    for product in products:
        name = product.product.name
        number_part = re.match(r'^\d+', name)
        if number_part:
            number_part = number_part.group()
        try:
            result = int(number_part) / 1000 if number_part else 0.01
        except ValueError:
            result = 0.01 
        weight1 = result
        for item in product.product_color_quantity.all():
            weight += weight1 * item.quantity
    return p_format(weight)

@register.simple_tag
def order_payment_calculation(order, current_year):
    html_parser = ""
    
    count = 1
    total_paid = order.order_payments.aggregate(total=Sum('paid_price'))['total'] or 0.0
    previous_orders = order.__class__.objects.filter(id__lt=order.id, client=order.client)
    total_remainder = sum(previous_orders.values_list('remainder', flat=True)) + order.remainder + Decimal(total_paid)
    for obj in order.order_payments.all().order_by('id'):
        if count == 2:
            html_parser += "<tr>"
        if count >= 2:
            html_parser += f"<td></td><td></td><td></td><td></td><td></td><td>{simplify_number(obj.paid_price_sum)}</td><td>{simplify_number(obj.paid_price)}</td><td>{obj.created_at.strftime('%d.%m.%Y')}</td><td>{simplify_number(total_remainder - obj.paid_price)}</td><td>{obj.comment or ''}</td></tr>"
        else:
            html_parser += f"""<td>{simplify_number(obj.paid_price_sum)}</td><td>{simplify_number(obj.paid_price)}</td><td></td><td>{simplify_number(total_remainder - obj.paid_price)}</td><td>{obj.comment or ''}
            <div class="d-inline-block">
                <a href="" class="btn btn-sm btn-text-secondary rounded-pill btn-icon dropdown-toggle hide-arrow"
                  data-bs-toggle="dropdown"><i class="ti ti-dots-vertical ti-md"></i>
                </a>
                <ul class="dropdown-menu dropdown-menu-end m-0">
                  <li><button class="dropdown-item" data-bs-toggle="modal" data-bs-target="#PaidAmount" data-objId="{order.id}">Оплата</button></li>
                  <div class="dropdown-divider"></div>
                  <li><button class="dropdown-item" data-bs-toggle="modal" data-bs-target="#EditOrder-{order.id}">Редактировать</button></li>
                  <li><a class="dropdown-item text-danger delete-record" href='/app/order-delete/{order.id}?client={order.client_id}&year={current_year}'>Удалить</a></li>
                </ul>
              </div>
            </td>
            """
        if count == 1:
            html_parser += "</tr>"
        count += 1
        total_remainder -= obj.paid_price
    if count != 2:
        html_parser += "</tr>"
    return mark_safe(html_parser)

@register.simple_tag
def perv_item_payment(order):
    previous_orders = order.__class__.objects.filter(id__lt=order.id, client=order.client)
    total_remainder = sum(previous_orders.values_list('remainder', flat=True)) + order.remainder
    return simplify_number(total_remainder)

@register.simple_tag
def calculation_remainder(orders):
    total = 0
    for obj in orders:
        total += obj.remainder
    return simplify_number(total)

@register.simple_tag
def calculation_stocks(item):
    total = 0
    for obj in item.stocks_list.all():
        total += obj.amount
    return p_format(total)

@register.simple_tag
def parce_html(item, date):

    products = Product.objects.filter(is_active=True).order_by('ordering')
    html = ""
    for product in products:
        html += f"""<td style='background-color:#2fff00'>{product.name.split()[0]}</td>"""
        for obj in product.color.all():
            stock = QuantityChange.objects.filter(
                color=obj, product=product,
                change_type='subtract',
                created_at__date=item['created_at__date'],
                user = item['user'],
                region=item['region']
            ).aggregate(total_quantity=Sum('quantity_changed'))['total_quantity'] or 0
            if stock:
                html += f"""
                    <td class='border-1' style="background-color: {obj.code}; 
                                    border: 1px solid black;
                                    {'color: #fff;' if obj.code == '#000000' else 'color: #000;'}">
                        <b>{stock}</b>
                    </td>
                    """
            else:
                html += f"""<td class='border-1' style="background-color: {obj.code}; 
                            border: 1px solid black;
                            {'color: #fff;' if obj.code == '#000000' else 'color: #000;'}"></td>"""
    return mark_safe(html)

@register.simple_tag
def edit_otgruska(item):
    stocks = QuantityChange.objects.filter(
        change_type='subtract',
        created_at__date=item['created_at__date'],
        user=item['user'],
        region=item['region']
    )

    context = {
        'stocks': stocks,
        'products': Product.objects.filter(is_active=True).order_by('ordering'),
        'colors': Color.objects.all(),
    }

    return render_to_string('edit_otgruska.html', context)

@register.simple_tag
def edit_order(obj):
    objs = OrderPayment.objects.filter(order_id=obj.id)
    return objs

@register.simple_tag
def total_quantity_changes(date, pro): 
    products = Product.objects.filter(is_active=True).order_by('ordering')
    html = ""
    for product in products:
        html += f"<td></td>"
        for obj in product.color.all():
            count = QuantityChange.objects.filter(color=obj, product=product,
                change_type='subtract',
                created_at__range=date,
            ).aggregate(
                    total=Sum('quantity_changed')
                )['total'] or 0 
            html += f"<td><b>{count}</b></td>"
    return mark_safe(html)

@register.simple_tag
def total_kg_changes(date, pro):
    products = Product.objects.filter(is_active=True).order_by('ordering')
    html = ""
    for product in products:
        html += f"<td></td>"
        for obj in product.color.all():
            count = QuantityChange.objects.filter(color=obj, product=product,
                change_type='subtract',
                created_at__range=date,
            ).aggregate(
                    total=Sum('quantity_changed')
                )['total'] or 0 
            number_part = re.match(r'^\d+', product.name)
            if number_part:
                number_part = number_part.group()
            try:
                result = int(number_part) / 1000 if number_part else 0.01
            except ValueError:
                result = 0.01 
            weight = result
            total_weight = count * weight
            html += f"<td><b>{round(total_weight, 2)}</b></td>"
    return mark_safe(html)

@register.simple_tag
def total_product_quantity_changes(date, pro):
    products = Product.objects.filter(is_active=True).order_by('ordering')
    html = ""
    for product in products:
        html += f"<td></td>"
        count = QuantityChange.objects.filter(product=product,
                                              change_type='subtract',
                                        created_at__range=date,
                ).aggregate(
                total=Sum('quantity_changed')
            )['total'] or 0 
        html += f"<td class='text-center' colspan='{product.color.count()}'><b>{count} шт </b></td>"
    return mark_safe(html)

@register.simple_tag
def total_product_kg_changes(date, pro):
    products = Product.objects.filter(is_active=True).order_by('ordering')
    html = ""
    for product in products:
        html += f"<td></td>"
        count = QuantityChange.objects.filter(product=product,
                                              change_type='subtract',
                                        created_at__range=date,
                ).aggregate(
                total=Sum('quantity_changed')
            )['total'] or 0 
        number_part = re.match(r'^\d+', product.name)
        if number_part:
            number_part = number_part.group()
        try:
            result = int(number_part) / 1000 if number_part else 0.01
        except ValueError:
            result = 0.01 
        weight = result
        total_weight = count * weight
        html += f"<td class='text-center' colspan='{product.color.count()}'><b>{round(total_weight, 2)} кг</b></td>"
    return mark_safe(html)

@register.simple_tag
def total_product_kg(date):
    products = Product.objects.filter(is_active=True).order_by('ordering')
    total_weight = float()
    for product in products:
        for obj in product.color.all():
            count = QuantityChange.objects.filter(color=obj, product=product,
                change_type='subtract',
                created_at__range=date
            ).aggregate(
                    total=Sum('quantity_changed')
                )['total'] or 0 
            number_part = re.match(r'^\d+', product.name)
            if number_part:
                number_part = number_part.group()
            try:
                result = int(number_part) / 1000 if number_part else 0.01
            except ValueError:
                result = 0.01 
            weight = result
            total_weight += count * weight
    return round(total_weight, 2)


@register.simple_tag
def get_price_region(pk, date):
    orders = Order.objects.filter(
                    client__region_id=pk,
                    created_at__year=date[0],
                    created_at__month=date[1]
                    )
    total_sales = orders.aggregate(
        total_amount=Sum(F('count') * F('price'))
    )['total_amount']
    total_sales = total_sales or 0
    return round(total_sales, 2)

# @register.simple_tag
# def edit_shipment(item):

def p_format(inp):
    price = int(inp)
    res = "{:,}".format(price)
    formated = re.sub(",", " ", res)
    return formated

@register.filter
def simplify_number(value):
    try:
        return f"{value:.10f}".rstrip("0").rstrip(".")
    except:
        return value

@register.simple_tag
def get_prev_item(items, i):
    try:
        return items[i-1] 
    except IndexError:
        return None