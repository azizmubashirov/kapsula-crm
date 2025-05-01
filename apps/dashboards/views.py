from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.order.models import Order
from django.db.models import Sum, F, DecimalField, Count
from apps.product.models import QuantityChange
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.http import JsonResponse

today = timezone.now().date()
one_month_ago = today - timedelta(days=30)

class DashboardsView(TemplateView):
    def get_context_data(self, **kwargs):
        date = self.request.GET.get("date", f"{today.year}-{today.month:02d}").split('-')
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['sales_by_region'] = (
                QuantityChange.objects.filter(
                    change_type='subtract',
                    type='amount',
                    created_at__year=date[0],
                    created_at__month=date[1]
                )
                .values('region__name_uz', 'region_id')
                .annotate(total_sold=Sum('quantity_changed'))
                .order_by('-total_sold')
            )
        
        context['most_sold_products'] = QuantityChange.objects.filter(
                change_type='subtract',
                type='amount',
                created_at__year=date[0],
                created_at__month=date[1]
            ).values(
                'product__name',
                'color__code' 
            ).annotate(
                total_sold=Sum('quantity_changed')
            ).order_by('-total_sold')
        
        context['top_clients'] = Order.objects.values(
                'client__id',
                'client__name'
            ).annotate(
                total_sales=Sum('count'),
                total_price=Sum(F('count') * F('price'))
            ).order_by('-total_price')
        
        context['date'] = date

        return context


def get_chart_data(request):
    current_year = datetime.now().year
    months = [f"{current_year}-{str(month).zfill(2)}" for month in range(1, 13)]

    monthly_data = (
        Order.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total_count=Count('id'),
            total_sales=Sum(F('count') * F('price'), output_field=DecimalField())
        )
        .order_by('month')
    )

    data_dict = {data['month'].strftime('%Y-%m'): data for data in monthly_data}
    counts = [data_dict.get(month, {}).get('total_count', 0) for month in months]
    sales = [
        float(data_dict.get(month, {}).get('total_sales', 0))
        for month in months
    ]

    result = {
        "data": [
            {
                "id": 1,
                "chart_data": counts,
                "active_option": 2
            },
            {
                "id": 2,
                "chart_data": sales,
                "active_option": 6
            }
        ]
    }

    return JsonResponse(result)