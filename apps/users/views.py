from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from web_project import TemplateLayout
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Client, Contact, UserCategory
from apps.product.models import Product
from apps.geo.models import Region, District
from .forms import UserForm, ContactForm
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from config.context_processors import is_ajax
from django.template.response import TemplateResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from apps.order.models import Order
import pandas as pd
from django.http import HttpResponse
import pandas as pd
from django.db import transaction
from django.http import JsonResponse

class UsersView(TemplateView):
    permission_required = ("user.view_user", "user.delete_user", "user.change_user", "user.add_user")
    form_class = UserForm
    success_url = reverse_lazy('app-user-list')

    def get_context_data(self, **kwargs):
        search_query = self.request.GET.get('q', '')
        page_number = int(self.request.GET.get('page', 1))
        entries = int(self.request.GET.get("entries", 100))
        district = int(self.request.GET.get("district", 0))
        region = int(self.request.GET.get("region", 0))
        category = int(self.request.GET.get("category", 0))
        product = int(self.request.GET.get("product", 0))
        
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        clients = Client.objects.order_by('name')
        
        context['form'] = self.form_class()
        ContactFormSet = inlineformset_factory(
            Client, Contact, form=ContactForm, extra=5
        )
        context['contact_formset'] = ContactFormSet(instance=Client()) 
        
        if search_query:
            clients = clients.filter(Q(name__icontains=search_query)|
                                     Q(region__name_uz__icontains=search_query)|
                                     Q(district__name_uz__icontains=search_query)|
                                     Q(product__name__icontains=search_query)|
                                     Q(client_contacts__name__icontains=search_query) |
                                    Q(client_contacts__phone_number__icontains=search_query)
                                ).distinct()
        if region:
            clients = clients.filter(region_id=region)
            context['districts'] = District.objects.filter(region_id=region).order_by('name_uz')
        else:
            context['districts'] = []
            district = 0
        if district:
            clients = clients.filter(district_id=district)
        if category:
            clients = clients.filter(category__id=category)
        if product:
            clients = clients.filter(product__id=product)
            
        paginator = Paginator(clients, entries)
        context['clients'] = paginator.page(page_number)
        
        
        context['regions'] = Region.objects.order_by('name_uz')
        context['categories'] = UserCategory.objects.order_by('name')
        context['products'] = Product.objects.order_by('ordering')
        
        context['dis'] = district
        context['reg'] = region
        context['pro'] = product
        context['cat'] = category
        context['search_query'] = search_query
        context['entries'] = entries
        context['entries_list'] = [5,25,50,100,200]
        return context
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if is_ajax(request):
            form = self.form_class(request.POST or None, instance=Client(region_id=request.GET.get("region_id", 0)))
            context = {"form": form}
            return TemplateResponse(request, "district.html", context)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        ContactFormSet = inlineformset_factory(
            Client, Contact, form=ContactForm, extra=5
        )
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()
            
            contact_formset = ContactFormSet(request.POST, instance=user)
            if contact_formset.is_valid():
                contact_formset.save()
            return redirect(self.success_url)
        else:
            print("Main Form Errors:", form.errors)
        context = self.get_context_data()
        context['form'] = form
        
        context['contact_formset'] = ContactFormSet(request.POST)
        return self.render_to_response(context)
    

class CLientUpdateDetailView(UpdateView, DetailView):
    model = Client
    form_class = UserForm
    success_url = reverse_lazy('app-user-list')

    def form_valid(self, form):
        page_number = self.request.GET.get('page', 1)
        context = self.get_context_data()
        contact_formset = context['contact_formset']
        model = form.save()
        
        if contact_formset.is_valid():
            contact_formset.instance = self.object
            
            self.object.client_contacts.all().delete()

            for contact_form in contact_formset:
                if contact_form.cleaned_data:
                    if not contact_form.cleaned_data.get("DELETE"):
                        contact = contact_form.save(commit=False)
                        contact.client = self.object
                        contact.save()
                        contact_form.save_m2m()

            return redirect(reverse_lazy('app-user-list')+ f"?page={page_number}" + f"#section{model.id}")
        else:
            print("Main Form Errors:", form.errors)
            print("Contact Formset Errors:", contact_formset.errors)
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    

    def get_context_data(self, **kwargs):
        
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['object'] = self.get_object()
        context['form'] = self.form_class(instance=self.object)
        ContactFormSet = inlineformset_factory(
            Client, Contact, form=ContactForm, extra=5, can_delete=True
        )
        if self.request.POST:
            contact_formset = ContactFormSet(self.request.POST, instance=self.object)
        else:
            contact_formset = ContactFormSet(instance=self.object)
        
        for form in contact_formset:
            if 'id' in form.fields:
                form.fields['id'].required = False 

        context['contact_formset'] = contact_formset
        return context
    
def delete_user(request, pk):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return JsonResponse({"success": True, "message": "Foydalanuvchi o‘chirildi!"})
    return JsonResponse({"success": False, "message": "Noto‘g‘ri so‘rov turi!"}, status=400)


def export_clients_to_excel(request):
    clients = Client.objects.order_by('name')

    data = []
    
    for client in clients:
        data.append({
            'Имя': client.name,
            'Область': client.region.name_uz if client.region else '',
            'Туман': client.district.name_uz if client.district else '',
            'Категория': client.category,
            'Продукты': ", ".join([product.name for product in client.product.all()]),
            'Контакт': ", ".join([f"{contact.name} - {contact.phone_number} - {contact.position}" for contact in client.client_contacts.all()]),
            'Комментарий': client.comment,
        })
    
    df = pd.DataFrame(data)

    file_path = "media/analytics.xlsx"
    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, sheet_name='Mijozlar', index=False)

    with open(file_path, "rb") as excel_file:
        response = HttpResponse(excel_file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename=clients.xlsx"
        return response

def import_clients_from_excel(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        df = pd.read_excel(myfile, engine="openpyxl")
        
        df = df.dropna(how='all')
        with transaction.atomic():
            for _, row in df.iterrows():
                name = row.iloc[1]
                if pd.notna(name): 
                    model = Client.objects.create(
                        name=row.iloc[1],
                        comment=row.iloc[6]
                    )
                    Contact.objects.create(
                        client= model,
                        name = row.iloc[3]
                    )
                    Contact.objects.create(
                        client= model,
                        name = row.iloc[4]
                    )            
        return redirect(reverse_lazy('app-user-list'))