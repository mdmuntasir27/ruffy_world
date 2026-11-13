from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum

from pets.models import Pet
from adoptions.models import AdoptionRequest
from store.models import Product, Order, OrderItem
from vets.models import Vet
from community.models import AdoptionPost, AdoptionInquiry
from accounts.models import UserProfile

from .decorators import admin_panel_required
from .forms import (
    AdminLoginForm, PetAdminForm, ProductAdminForm,
    OrderAdminForm, VetAdminForm, AdoptionRequestStatusForm,
    CommunityPostStatusForm, CommunityInquiryStatusForm, UserAdminEditForm
)


# ==========================================
# AUTHENTICATION
# ==========================================

def admin_login_view(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('custom_admin:dashboard')

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    messages.success(request, f'Welcome back to Ruffy World Admin Panel, {user.username}!')
                    next_url = request.GET.get('next') or 'custom_admin:dashboard'
                    return redirect(next_url)
                else:
                    messages.error(request, 'Access denied. You do not have administrator permissions.')
            else:
                messages.error(request, 'Invalid admin username or password.')
    else:
        form = AdminLoginForm()

    return render(request, 'custom_admin/login.html', {'form': form})


def admin_logout_view(request):
    logout(request)
    messages.info(request, 'You have been safely logged out of the Admin Panel.')
    return redirect('custom_admin:login')


# ==========================================
# DASHBOARD
# ==========================================

@admin_panel_required
def dashboard_view(request):
    total_pets = Pet.objects.count()
    available_pets = Pet.objects.filter(status='Available').count()
    pending_adoptions = AdoptionRequest.objects.filter(status='Pending').count()
    total_products = Product.objects.count()
    out_of_stock_products = Product.objects.filter(quantity=0).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
    total_vets = Vet.objects.count()
    total_users = User.objects.count()
    total_posts = AdoptionPost.objects.count()

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:6]
    recent_requests = AdoptionRequest.objects.select_related('user', 'pet').order_by('-created_at')[:6]
    recent_pets = Pet.objects.order_by('-created_at')[:6]

    context = {
        'total_pets': total_pets,
        'available_pets': available_pets,
        'pending_adoptions': pending_adoptions,
        'total_products': total_products,
        'out_of_stock_products': out_of_stock_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'total_vets': total_vets,
        'total_users': total_users,
        'total_posts': total_posts,
        'recent_orders': recent_orders,
        'recent_requests': recent_requests,
        'recent_pets': recent_pets,
    }
    return render(request, 'custom_admin/dashboard.html', context)


# ==========================================
# PETS MANAGEMENT
# ==========================================

@admin_panel_required
def pet_list_view(request):
    query = request.GET.get('q', '').strip()
    animal_type = request.GET.get('type', '').strip()
    status = request.GET.get('status', '').strip()

    pets = Pet.objects.all().order_by('-created_at')

    if query:
        pets = pets.filter(Q(name__icontains=query) | Q(breed__icontains=query) | Q(location__icontains=query))
    if animal_type:
        pets = pets.filter(animal_type=animal_type)
    if status:
        pets = pets.filter(status=status)

    paginator = Paginator(pets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'custom_admin/pets/pet_list.html', {
        'page_obj': page_obj,
        'query': query,
        'animal_type': animal_type,
        'status': status,
        'animal_types': Pet.ANIMAL_TYPE_CHOICES,
        'status_choices': Pet.STATUS_CHOICES,
    })


@admin_panel_required
def pet_add_view(request):
    if request.method == 'POST':
        form = PetAdminForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f'Pet "{pet.name}" has been successfully added.')
            return redirect('custom_admin:pet_list')
    else:
        form = PetAdminForm()

    return render(request, 'custom_admin/pets/pet_form.html', {'form': form, 'title': 'Add New Pet'})


@admin_panel_required
def pet_edit_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetAdminForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f'Pet "{pet.name}" updated successfully.')
            return redirect('custom_admin:pet_list')
    else:
        form = PetAdminForm(instance=pet)

    return render(request, 'custom_admin/pets/pet_form.html', {'form': form, 'title': f'Edit Pet: {pet.name}', 'pet': pet})


@admin_panel_required
def pet_delete_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        name = pet.name
        pet.delete()
        messages.success(request, f'Pet "{name}" was successfully deleted.')
        return redirect('custom_admin:pet_list')

    return render(request, 'custom_admin/pets/pet_confirm_delete.html', {'pet': pet})


# ==========================================
# ADOPTIONS MANAGEMENT
# ==========================================

@admin_panel_required
def adoption_list_view(request):
    status = request.GET.get('status', '').strip()
    query = request.GET.get('q', '').strip()

    requests_qs = AdoptionRequest.objects.select_related('user', 'pet').order_by('-created_at')

    if status:
        requests_qs = requests_qs.filter(status=status)
    if query:
        requests_qs = requests_qs.filter(
            Q(user__username__icontains=query) |
            Q(pet__name__icontains=query) |
            Q(phone__icontains=query)
        )

    paginator = Paginator(requests_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'custom_admin/adoptions/adoption_list.html', {
        'page_obj': page_obj,
        'status': status,
        'query': query,
    })


@admin_panel_required
def adoption_detail_view(request, pk):
    adoption_req = get_object_or_404(AdoptionRequest.objects.select_related('user', 'pet'), pk=pk)

    if request.method == 'POST':
        form = AdoptionRequestStatusForm(request.POST, instance=adoption_req)
        if form.is_valid():
            form.save()
            # If approved, update pet status if requested
            if adoption_req.status == 'Approved' and 'mark_pet_adopted' in request.POST:
                adoption_req.pet.status = 'Adopted'
                adoption_req.pet.save()
                messages.info(request, f'Pet "{adoption_req.pet.name}" has been marked as Adopted.')
            messages.success(request, f'Adoption request #{adoption_req.pk} status updated to {adoption_req.status}.')
            return redirect('custom_admin:adoption_detail', pk=adoption_req.pk)
    else:
        form = AdoptionRequestStatusForm(instance=adoption_req)

    return render(request, 'custom_admin/adoptions/adoption_detail.html', {
        'adoption_req': adoption_req,
        'form': form,
    })


@admin_panel_required
def adoption_delete_view(request, pk):
    adoption_req = get_object_or_404(AdoptionRequest, pk=pk)
    if request.method == 'POST':
        adoption_req.delete()
        messages.success(request, f'Adoption request #{pk} deleted.')
        return redirect('custom_admin:adoption_list')

    return render(request, 'custom_admin/adoptions/adoption_confirm_delete.html', {'adoption_req': adoption_req})


# ==========================================
# STORE PRODUCTS MANAGEMENT
# ==========================================

@admin_panel_required
def product_list_view(request):
    category = request.GET.get('category', '').strip()
    query = request.GET.get('q', '').strip()
    stock = request.GET.get('stock', '').strip()

    products = Product.objects.all().order_by('category', 'name')

    if category:
        products = products.filter(category=category)
    if query:
        products = products.filter(name__icontains=query)
    if stock == 'out':
        products = products.filter(quantity=0)
    elif stock == 'in':
        products = products.filter(quantity__gt=0)

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'custom_admin/store/product_list.html', {
        'page_obj': page_obj,
        'category': category,
        'query': query,
        'stock': stock,
        'categories': Product.CATEGORY_CHOICES,
    })


@admin_panel_required
def product_add_view(request):
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save()
            messages.success(request, f'Product "{prod.name}" created successfully.')
            return redirect('custom_admin:product_list')
    else:
        form = ProductAdminForm()

    return render(request, 'custom_admin/store/product_form.html', {'form': form, 'title': 'Add Store Accessory'})


@admin_panel_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('custom_admin:product_list')
    else:
        form = ProductAdminForm(instance=product)

    return render(request, 'custom_admin/store/product_form.html', {'form': form, 'title': f'Edit: {product.name}', 'product': product})


@admin_panel_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted successfully.')
        return redirect('custom_admin:product_list')

    return render(request, 'custom_admin/store/product_confirm_delete.html', {'product': product})


# ==========================================
# STORE ORDERS MANAGEMENT
# ==========================================

@admin_panel_required
def order_list_view(request):
    status = request.GET.get('status', '').strip()
    payment_status = request.GET.get('payment', '').strip()
    query = request.GET.get('q', '').strip()

    orders = Order.objects.select_related('user').order_by('-created_at')

    if status:
        orders = orders.filter(status=status)
    if payment_status:
        orders = orders.filter(payment_status=payment_status)
    if query:
        orders = orders.filter(
            Q(pk__icontains=query) |
            Q(user__username__icontains=query) |
            Q(full_name__icontains=query) |
            Q(phone__icontains=query)
        )

    paginator = Paginator(orders, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'custom_admin/store/order_list.html', {
        'page_obj': page_obj,
        'status': status,
        'payment_status': payment_status,
        'query': query,
        'order_statuses': Order.ORDER_STATUS_CHOICES,
        'payment_statuses': Order.PAYMENT_STATUS_CHOICES,
    })


@admin_panel_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order.objects.select_related('user').prefetch_related('items__product'), pk=pk)

    if request.method == 'POST':
        form = OrderAdminForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Order #{order.pk} updated successfully.')
            return redirect('custom_admin:order_detail', pk=order.pk)
    else:
        form = OrderAdminForm(instance=order)

    return render(request, 'custom_admin/store/order_detail.html', {
        'order': order,
        'form': form,
    })


@admin_panel_required
def order_delete_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, f'Order #{pk} was deleted.')
        return redirect('custom_admin:order_list')

    return render(request, 'custom_admin/store/order_confirm_delete.html', {'order': order})


# ==========================================
# VETS MANAGEMENT
# ==========================================

@admin_panel_required
def vet_list_view(request):
    shift = request.GET.get('shift', '').strip()
    query = request.GET.get('q', '').strip()

    vets = Vet.objects.all().order_by('shift', 'name')

    if shift:
        vets = vets.filter(shift=shift)
    if query:
        vets = vets.filter(Q(name__icontains=query) | Q(specialization__icontains=query) | Q(clinic_address__icontains=query))

    return render(request, 'custom_admin/vets/vet_list.html', {
        'vets': vets,
        'shift': shift,
        'query': query,
        'shifts': Vet.SHIFT_CHOICES,
    })


@admin_panel_required
def vet_add_view(request):
    if request.method == 'POST':
        form = VetAdminForm(request.POST, request.FILES)
        if form.is_valid():
            vet = form.save()
            messages.success(request, f'Dr. {vet.name} added to Vet Directory.')
            return redirect('custom_admin:vet_list')
    else:
        form = VetAdminForm()

    return render(request, 'custom_admin/vets/vet_form.html', {'form': form, 'title': 'Add Veterinarian'})


@admin_panel_required
def vet_edit_view(request, pk):
    vet = get_object_or_404(Vet, pk=pk)
    if request.method == 'POST':
        form = VetAdminForm(request.POST, request.FILES, instance=vet)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dr. {vet.name} details updated.')
            return redirect('custom_admin:vet_list')
    else:
        form = VetAdminForm(instance=vet)

    return render(request, 'custom_admin/vets/vet_form.html', {'form': form, 'title': f'Edit Dr. {vet.name}', 'vet': vet})


@admin_panel_required
def vet_delete_view(request, pk):
    vet = get_object_or_404(Vet, pk=pk)
    if request.method == 'POST':
        name = vet.name
        vet.delete()
        messages.success(request, f'Dr. {name} removed from Directory.')
        return redirect('custom_admin:vet_list')

    return render(request, 'custom_admin/vets/vet_confirm_delete.html', {'vet': vet})


# ==========================================
# COMMUNITY MANAGEMENT
# ==========================================

@admin_panel_required
def community_post_list_view(request):
    status = request.GET.get('status', '').strip()
    query = request.GET.get('q', '').strip()

    posts = AdoptionPost.objects.select_related('author').annotate(inquiry_count=Count('adoption_inquiries')).order_by('-created_at')

    if status:
        posts = posts.filter(status=status)
    if query:
        posts = posts.filter(Q(pet_name__icontains=query) | Q(author__username__icontains=query))

    paginator = Paginator(posts, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'custom_admin/community/post_list.html', {
        'page_obj': page_obj,
        'status': status,
        'query': query,
    })


@admin_panel_required
def community_post_delete_view(request, pk):
    post = get_object_or_404(AdoptionPost, pk=pk)
    if request.method == 'POST':
        title = post.pet_name
        post.delete()
        messages.success(request, f'Community post for "{title}" deleted.')
        return redirect('custom_admin:community_post_list')

    return render(request, 'custom_admin/community/post_confirm_delete.html', {'post': post})


@admin_panel_required
def community_inquiry_list_view(request):
    status = request.GET.get('status', '').strip()
    inquiries = AdoptionInquiry.objects.select_related('post', 'requester').order_by('-created_at')

    if status:
        inquiries = inquiries.filter(status=status)

    paginator = Paginator(inquiries, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'custom_admin/community/inquiry_list.html', {
        'page_obj': page_obj,
        'status': status,
    })


@admin_panel_required
def community_inquiry_detail_view(request, pk):
    inquiry = get_object_or_404(AdoptionInquiry.objects.select_related('post', 'requester'), pk=pk)
    if request.method == 'POST':
        form = CommunityInquiryStatusForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, f'Inquiry #{inquiry.pk} status updated to {inquiry.status}.')
            return redirect('custom_admin:community_inquiry_detail', pk=inquiry.pk)
    else:
        form = CommunityInquiryStatusForm(instance=inquiry)

    return render(request, 'custom_admin/community/inquiry_detail.html', {
        'inquiry': inquiry,
        'form': form,
    })


@admin_panel_required
def community_inquiry_delete_view(request, pk):
    inquiry = get_object_or_404(AdoptionInquiry, pk=pk)
    if request.method == 'POST':
        inquiry.delete()
        messages.success(request, f'Inquiry #{pk} deleted.')
        return redirect('custom_admin:community_inquiry_list')

    return render(request, 'custom_admin/community/inquiry_confirm_delete.html', {'inquiry': inquiry})


# ==========================================
# USERS MANAGEMENT
# ==========================================

@admin_panel_required
def user_list_view(request):
    query = request.GET.get('q', '').strip()
    role = request.GET.get('role', '').strip()

    users = User.objects.all().order_by('-date_joined')

    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    if role == 'staff':
        users = users.filter(is_staff=True)
    elif role == 'member':
        users = users.filter(is_staff=False)

    paginator = Paginator(users, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'custom_admin/users/user_list.html', {
        'page_obj': page_obj,
        'query': query,
        'role': role,
    })


@admin_panel_required
def user_edit_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserAdminEditForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {target_user.username} updated successfully.')
            return redirect('custom_admin:user_list')
    else:
        form = UserAdminEditForm(instance=target_user)

    return render(request, 'custom_admin/users/user_form.html', {
        'form': form,
        'target_user': target_user,
    })


@admin_panel_required
def user_delete_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    if target_user == request.user:
        messages.error(request, 'You cannot delete your own logged-in admin account!')
        return redirect('custom_admin:user_list')

    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        messages.success(request, f'User {username} was deleted.')
        return redirect('custom_admin:user_list')

    return render(request, 'custom_admin/users/user_confirm_delete.html', {'target_user': target_user})
