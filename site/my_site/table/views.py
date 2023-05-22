from django.shortcuts import render, get_object_or_404, redirect
from .models import Asset, Maintenance, Repair
from .forms import AssetForm, MaintenanceForm, RepairForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.http import FileResponse
from django.template.loader import render_to_string
import csv
from django.views import View
from django.http import HttpResponse



def home(request):
    return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')
def asset_list(request):
    assets = Asset.objects.all()
    return render(request, 'asset_list.html', {'assets': assets})

def create_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm()
    return render(request, 'create_asset.html', {'form': form})

def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    maintenance_form = MaintenanceForm()
    repair_form = RepairForm()
    return render(request, 'asset_detail.html', {'asset': asset, 'maintenance_form': maintenance_form, 'repair_form': repair_form})


def asset_delete(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        asset.delete()
        return redirect('asset_list')
    return render(request, 'asset_delete.html', {'asset': asset})

def edit_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'edit_asset.html', {'form': form, 'asset': asset})

def maintenance_list(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    maintenance_list = asset.maintenance_set.all()
    context = {'asset': asset, 'maintenance_list': maintenance_list}
    return render(request, 'maintenance_list.html', context)
def add_maintenance(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.asset = asset
            maintenance.save()
            return redirect('asset_detail', asset_id=asset_id)
    else:
        form = MaintenanceForm()
    return render(request, 'add_maintenance.html', {'form': form, 'asset': asset})

def repair_list(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    repair_list = asset.repair_set.all()
    context = {'asset': asset, 'repair_list': repair_list}
    return render(request, 'repair_list.html', context)

def add_repair(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair = form.save(commit=False)
            repair.asset = asset
            repair.save()
            return redirect('asset_detail', asset_id=asset_id)
    else:
        form = RepairForm()
    return render(request, 'add_repair.html', {'form': form, 'asset': asset})

def get_queryset(request):
    q = request.GET.get('q')
    assets = Asset.objects.filter(asset_name__icontains=q)
    context = {'assets': assets}
    return render(request, 'search_result.html', context=context)

def asset_statistics(request):
    # Получите нужные данные для статистики
    total_assets = Asset.objects.count()
    total_cost = Asset.objects.aggregate(total_cost=Sum('cost')).get('total_cost')
    avg_cost = Asset.objects.aggregate(avg_cost=Avg('cost')).get('avg_cost')
    # Добавьте другие вычисления статистики, если необходимо

    context = {
        'total_assets': total_assets,
        'total_cost': total_cost,
        'avg_cost': avg_cost,
        # Добавьте другие переменные статистики в контекст
    }

    return render(request, 'asset_statistics.html', context)

def generate_word_report(total_assets, total_cost, avg_cost):
    # Создаем новый документ Word
    doc = Document()

    # Добавляем заголовок
    doc.add_heading('Статистика активов', level=1)

    # Добавляем информацию о статистике
    doc.add_paragraph(f'Общее количество активов: {total_assets}')
    doc.add_paragraph(f'Общая стоимость активов: {total_cost}')
    doc.add_paragraph(f'Средняя стоимость активов: {avg_cost}')

    # Сохраняем документ
    doc.save('statistics_report.docx')

    # Возвращаем путь к созданному документу
    return 'statistics_report.docx'

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = '/'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def profile(request):
    return render(request, 'profile.html')