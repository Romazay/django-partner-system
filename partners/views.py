from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Partner, PromoCode
from .forms import PartnerRegistrationForm, PromoCodeForm


def home(request):
    return render(request, 'partners/home.html')


def register(request):
    if request.method == 'POST':
        form = PartnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 'Реєстрація успішна! Очікуйте підтвердження від адміністратора.')
            return redirect('partner_dashboard')
    else:
        form = PartnerRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def partner_dashboard(request):
    try:
        partner = request.user.partner
        promo_codes = partner.promo_codes.all()
        return render(request, 'partners/partner_dashboard.html', {
            'partner': partner,
            'promo_codes': promo_codes
        })
    except Partner.DoesNotExist:
        messages.error(request, 'Партнерський профіль не знайдено.')
        return redirect('home')


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    partners = Partner.objects.all().order_by('-created_at')
    all_promo_codes = PromoCode.objects.all().order_by('-created_at')
    return render(request, 'partners/admin_dashboard.html', {
        'partners': partners,
        'all_promo_codes': all_promo_codes
    })


@login_required
@user_passes_test(is_admin)
def approve_partner(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)
    partner.is_approved = True
    partner.save()
    messages.success(request, f'Партнер {partner.company_name} схвалений.')
    return redirect('admin_dashboard')


@login_required
@user_passes_test(is_admin)
def create_promo_code(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)

    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            promo_code = form.save(commit=False)
            promo_code.partner = partner
            promo_code.created_by = request.user
            promo_code.save()
            messages.success(
                request, f'Промокод {promo_code.code} створено для {partner.company_name}.')
            return redirect('admin_dashboard')
    else:
        form = PromoCodeForm()

    return render(request, 'partners/create_promo_code.html', {
        'form': form,
        'partner': partner
    })


@login_required
@user_passes_test(is_admin)
def toggle_promo_code(request, code_id):
    if request.method == 'POST':
        promo_code = get_object_or_404(PromoCode, id=code_id)
        promo_code.is_active = not promo_code.is_active
        promo_code.save()
        return JsonResponse({
            'success': True,
            'is_active': promo_code.is_active
        })
    return JsonResponse({'success': False})


@login_required
@user_passes_test(is_admin)
def delete_promo_code(request, code_id):
    if request.method == 'POST':
        promo_code = get_object_or_404(PromoCode, id=code_id)
        code_text = promo_code.code
        partner_name = promo_code.partner.company_name
        promo_code.delete()
        messages.success(
            request, f'Промокод {code_text} для {partner_name} видалено.')
    return redirect('admin_dashboard')
