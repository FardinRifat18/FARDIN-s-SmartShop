# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Q
# from django.http import JsonResponse
# from .models import *
# import json
# from decimal import Decimal
# from django.db.models import Count

# # ---------- HOME & PRODUCTS ----------
# def home(request):
#     products = Product.objects.filter(stock__gt=0)[:8]
#     categories = Category.objects.all()
#     return render(request, 'home.html', {
#         'products': products,
#         'categories': categories,
#         # 'cart_count': cart_count
#     })

# def product_list(request):
#     products = Product.objects.filter(stock__gt=0)
#     categories = Category.objects.all()
    
#     # Filter by category
#     category_slug = request.GET.get('category')
#     if category_slug:
#         products = products.filter(category__slug=category_slug)
    
#     # Search
#     query = request.GET.get('q')
#     if query:
#         products = products.filter(
#             Q(name__icontains=query) | 
#             Q(description__icontains=query)
#         )
    
#     return render(request, 'product_list.html', {
#         'products': products,
#         'categories': categories,
#         'selected_category': category_slug,
#         'query': query
#     })

# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
#     return render(request, 'product_detail.html', {
#         'product': product,
#         'related_products': related_products
#     })

# # ---------- AUTH ----------
# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm = request.POST['confirm_password']
        
#         if password != confirm:
#             messages.error(request, "Passwords don't match")
#             return redirect('register')
        
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect('register')
        
#         user = User.objects.create_user(username=username, email=email, password=password)
#         UserProfile.objects.create(user=user)
#         login(request, user)
#         messages.success(request, "Registration successful!")
#         return redirect('home')
    
#     return render(request, 'register.html')

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
        
#         if user:
#             login(request, user)
            
#             # Merge session cart with user cart
#             session_cart = request.session.get(CART_SESSION_ID, {})
#             if session_cart:
#                 cart, _ = Cart.objects.get_or_create(user=user)
#                 for product_id, item_data in session_cart.items():
#                     product = Product.objects.get(id=product_id)
#                     cart_item, created = CartItem.objects.get_or_create(
#                         cart=cart,
#                         product=product,
#                         defaults={'quantity': item_data['quantity']}
#                     )
#                     if not created:
#                         cart_item.quantity += item_data['quantity']
#                         cart_item.save()
#                 request.session[CART_SESSION_ID] = {}
            
#             messages.success(request, f"Welcome back, {username}!")
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid credentials")
    
#     return render(request, 'login.html')

# def user_logout(request):
#     logout(request)
#     messages.success(request, "Logged out successfully")
#     return redirect('home')

# @login_required
# def profile(request):
#     profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
#     if request.method == 'POST':
#         profile.phone = request.POST.get('phone', '')
#         profile.address = request.POST.get('address', '')
#         if request.FILES.get('profile_image'):
#             profile.profile_image = request.FILES['profile_image']
#         profile.save()
        
#         request.user.first_name = request.POST.get('first_name', '')
#         request.user.last_name = request.POST.get('last_name', '')
#         request.user.email = request.POST.get('email', '')
#         request.user.save()
        
#         messages.success(request, "Profile updated!")
#         return redirect('profile')
    
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'profile.html', {'profile': profile, 'orders': orders})

# # ---------- CART ----------
# CART_SESSION_ID = 'cart'

# def get_cart(request):
#     if request.user.is_authenticated:
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         return cart.items.all(), cart
#     else:
#         session_cart = request.session.get(CART_SESSION_ID, {})
#         cart_items = []
#         for product_id, item_data in session_cart.items():
#             product = Product.objects.get(id=product_id)
#             cart_items.append({
#                 'product': product,
#                 'quantity': item_data['quantity'],
#                 'total_price': product.final_price * item_data['quantity']
#             })
#         return cart_items, None

# def cart_view(request):
#     cart_items, cart_obj = get_cart(request)
#     total = sum(item.total_price if hasattr(item, 'total_price') else item['total_price'] for item in cart_items)
#     return render(request, 'cart.html', {
#         'cart_items': cart_items,
#         'total': total
#     })

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     quantity = int(request.POST.get('quantity', 1))
    
#     if request.user.is_authenticated:
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         cart_item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             product=product,
#             defaults={'quantity': quantity}
#         )
#         if not created:
#             cart_item.quantity += quantity
#             cart_item.save()
#     else:
#         cart = request.session.get(CART_SESSION_ID, {})
#         if str(product_id) in cart:
#             cart[str(product_id)]['quantity'] += quantity
#         else:
#             cart[str(product_id)] = {
#                 'quantity': quantity,
#                 'price': str(product.final_price)
#             }
#         request.session[CART_SESSION_ID] = cart
    
#     messages.success(request, f"{product.name} added to cart!")
#     return redirect('cart')

# def remove_from_cart(request, product_id):
#     if request.user.is_authenticated:
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         CartItem.objects.filter(cart=cart, product_id=product_id).delete()
#     else:
#         cart = request.session.get(CART_SESSION_ID, {})
#         if str(product_id) in cart:
#             del cart[str(product_id)]
#             request.session[CART_SESSION_ID] = cart
    
#     messages.success(request, "Item removed from cart")
#     return redirect('cart')

# def update_cart(request, product_id):
#     quantity = int(request.POST.get('quantity', 1))
    
#     if request.user.is_authenticated:
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         CartItem.objects.filter(cart=cart, product_id=product_id).update(quantity=quantity)
#     else:
#         cart = request.session.get(CART_SESSION_ID, {})
#         if str(product_id) in cart:
#             cart[str(product_id)]['quantity'] = quantity
#             request.session[CART_SESSION_ID] = cart
    
#     return redirect('cart')

# # ---------- CHECKOUT & ORDER ----------
# @login_required
# def checkout(request):
#     cart_items, cart_obj = get_cart(request)
#     if not cart_items:
#         messages.warning(request, "Your cart is empty!")
#         return redirect('cart')
    
#     total = sum(item.total_price if hasattr(item, 'total_price') else item['total_price'] for item in cart_items)
    
#     if request.method == 'POST':
#         payment_method = request.POST['payment_method']
#         transaction_id = request.POST.get('transaction_id', '')
        
#         # Create order
#         order = Order.objects.create(
#             user=request.user,
#             total_price=total,
#             payment_method=payment_method,
#             payment_status=(payment_method == 'cod'),
#             transaction_id=transaction_id
#         )
        
#         # Create order items
#         for item in cart_items:
#             if hasattr(item, 'product'):
#                 product = item.product
#                 quantity = item.quantity
#                 price = product.final_price
#             else:
#                 product = item['product']
#                 quantity = item['quantity']
#                 price = product.final_price
            
#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=quantity,
#                 price=price
#             )
            
#             # Reduce stock
#             product.stock -= quantity
#             product.save()
        
#         # Create payment record for bKash/Nagad/Rocket
#         if payment_method != 'cod':
#             Payment.objects.create(
#                 order=order,
#                 transaction_id=transaction_id,
#                 method=payment_method,
#                 amount=total
#             )
#             messages.info(request, "Payment submitted! Waiting for admin verification.")
#         else:
#             messages.success(request, "Order placed successfully! (Cash on Delivery)")
        
#         # Clear cart
#         if request.user.is_authenticated:
#             cart_obj.delete()
#         else:
#             request.session[CART_SESSION_ID] = {}
        
#         return redirect('order_detail', order_id=order.id)
    
#     # Get user profile for prefill
#     profile = UserProfile.objects.get(user=request.user)
    
#     return render(request, 'checkout.html', {
#         'cart_items': cart_items,
#         'total': total,
#         'profile': profile
#     })

# @login_required
# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     return render(request, 'order_detail.html', {'order': order})

# @login_required
# def order_history(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'order_history.html', {'orders': orders})

# # ---------- PAYMENT SUBMISSION ----------
# @login_required
# def submit_payment(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
    
#     if request.method == 'POST':
#         transaction_id = request.POST['transaction_id']
#         payment, created = Payment.objects.get_or_create(
#             order=order,
#             defaults={
#                 'transaction_id': transaction_id,
#                 'method': order.payment_method,
#                 'amount': order.total_price
#             }
#         )
#         if not created:
#             payment.transaction_id = transaction_id
#             payment.save()
        
#         order.transaction_id = transaction_id
#         order.save()
        
#         messages.success(request, "Payment information submitted. Admin will verify soon.")
#         return redirect('order_detail', order_id=order.id)
    
#     return render(request, 'submit_payment.html', {'order': order})

# # ---------- CONTEXT PROCESSOR ----------
# def cart_count(request):
#     if request.user.is_authenticated:
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         count = sum(item.quantity for item in cart.items.all())
#     else:
#         cart = request.session.get(CART_SESSION_ID, {})
#         count = sum(item['quantity'] for item in cart.values())
    
#     return {'cart_count': count}




#new code

# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.db.models.functions import TruncDate, TruncMonth
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
import json
import random

from .models import *
from django.contrib.auth.models import User

# ============================================================
# ============  ADMIN DASHBOARD VIEWS =======================
# ============================================================

def admin_dashboard_view(request):
    """
    Professional Admin Dashboard - No login required for demo
    Complete e-commerce control panel
    """
    # Get real data from database
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(payment_status=True).aggregate(total=Sum('total_price'))['total'] or 0
    total_products = Product.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()
    pending_orders = Order.objects.filter(order_status='pending').count()
    pending_payments = Payment.objects.filter(verified=False).count()
    low_stock_products = Product.objects.filter(stock__lt=10).count()
    
    # Recent orders with all details
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    # Pending payments
    pending_payments_list = Payment.objects.filter(verified=False).order_by('-created_at')[:6]
    
    # Sales analytics (last 7 days)
    last_7_days = []
    days_labels = []
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        days_labels.append(date.strftime('%a'))
        daily_total = Order.objects.filter(
            created_at__date=date,
            payment_status=True
        ).aggregate(total=Sum('total_price'))['total'] or 0
        last_7_days.append(float(daily_total))
    
    # Payment method distribution
    bkash_count = Order.objects.filter(payment_method='bkash', payment_status=True).count()
    nagad_count = Order.objects.filter(payment_method='nagad', payment_status=True).count()
    rocket_count = Order.objects.filter(payment_method='rocket', payment_status=True).count()
    cod_count = Order.objects.filter(payment_method='cod', payment_status=True).count()
    total_paid_orders = bkash_count + nagad_count + rocket_count + cod_count
    
    bkash_percent = round((bkash_count / total_paid_orders * 100) if total_paid_orders > 0 else 0)
    nagad_percent = round((nagad_count / total_paid_orders * 100) if total_paid_orders > 0 else 0)
    rocket_percent = round((rocket_count / total_paid_orders * 100) if total_paid_orders > 0 else 0)
    cod_percent = round((cod_count / total_paid_orders * 100) if total_paid_orders > 0 else 0)
    
    # Top selling products
    top_products = OrderItem.objects.values(
        'product__id', 'product__name', 'product__image'
    ).annotate(
        total_sold=Sum('quantity'),
        revenue=Sum(F('price') * F('quantity'))
    ).order_by('-total_sold')[:5]
    
    # Monthly revenue
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_revenue = Order.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year,
        payment_status=True
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Yesterday vs today comparison
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    today_sales = Order.objects.filter(
        created_at__date=today,
        payment_status=True
    ).aggregate(total=Sum('total_price'))['total'] or 0
    yesterday_sales = Order.objects.filter(
        created_at__date=yesterday,
        payment_status=True
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    sales_trend = 0
    if yesterday_sales > 0:
        sales_trend = round(((today_sales - yesterday_sales) / yesterday_sales) * 100, 1)
    
    context = {
        # Stats
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_customers': total_customers,
        'pending_orders': pending_orders,
        'pending_payments': pending_payments,
        'low_stock_products': low_stock_products,
        
        # Recent data
        'recent_orders': recent_orders,
        'pending_payments_list': pending_payments_list,
        
        # Charts
        'days_labels': days_labels,
        'sales_data': last_7_days,
        'bkash_percent': bkash_percent,
        'nagad_percent': nagad_percent,
        'rocket_percent': rocket_percent,
        'cod_percent': cod_percent,
        
        # Top products
        'top_products': top_products,
        
        # Monthly stats
        'monthly_revenue': monthly_revenue,
        'today_sales': today_sales,
        'sales_trend': sales_trend,
        
        # Current date
        'current_date': timezone.now().strftime('%B %d, %Y'),
    }
    
    return render(request, 'admin_dashboard.html', context)


# ============================================================
# ============  ORDER MANAGEMENT API ========================
# ============================================================

def admin_verify_payment(request, payment_id):
    """Verify pending payment"""
    if request.method == 'POST':
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.verified = True
            payment.verified_at = timezone.now()
            payment.save()
            
            # Update order payment status
            order = payment.order
            order.payment_status = True
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Payment verified for Order #{order.id}'
            })
        except Payment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Payment not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def admin_confirm_order(request, order_id):
    """Confirm pending order"""
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            order.order_status = 'confirmed'
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Order #{order.id} confirmed successfully'
            })
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def admin_update_order_status(request, order_id):
    """Update order status (packed, shipped, delivered)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            
            valid_statuses = ['packed', 'shipped', 'delivered', 'cancelled']
            if new_status not in valid_statuses:
                return JsonResponse({'success': False, 'message': 'Invalid status'})
            
            order = Order.objects.get(id=order_id)
            order.order_status = new_status
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Order #{order.id} status updated to {new_status}'
            })
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def admin_cancel_order(request, order_id):
    """Cancel order"""
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            order.order_status = 'cancelled'
            order.save()
            
            # Restore product stock
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                product = item.product
                product.stock += item.quantity
                product.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Order #{order.id} cancelled successfully'
            })
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def admin_get_order_details(request, order_id):
    """Get complete order details for view modal"""
    try:
        order = Order.objects.get(id=order_id)
        items = OrderItem.objects.filter(order=order).values(
            'product__name', 'quantity', 'price'
        )
        
        data = {
            'order_id': order.id,
            'customer': order.user.get_full_name() or order.user.username,
            'email': order.user.email,
            'date': order.created_at.strftime('%d %b %Y, %I:%M %p'),
            'total': float(order.total_price),
            'payment_method': dict(Order.PAYMENT_METHODS).get(order.payment_method, order.payment_method),
            'payment_status': 'Paid' if order.payment_status else 'Unpaid',
            'order_status': dict(Order.ORDER_STATUS).get(order.order_status, order.order_status),
            'transaction_id': order.transaction_id or 'N/A',
            'items': list(items),
        }
        
        # Get shipping address from user profile
        try:
            profile = UserProfile.objects.get(user=order.user)
            data['address'] = profile.address
            data['phone'] = profile.phone
        except UserProfile.DoesNotExist:
            data['address'] = 'Not provided'
            data['phone'] = 'Not provided'
        
        return JsonResponse({'success': True, 'data': data})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found'})


# ============================================================
# ============  PRODUCT MANAGEMENT API ======================
# ============================================================

def admin_get_products(request):
    """Get all products with optional filters"""
    products = Product.objects.all().select_related('category')
    
    # Search filter
    search = request.GET.get('search', '')
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(category__name__icontains=search)
        )
    
    # Category filter
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category__name__icontains=category)
    
    # Stock filter
    stock_status = request.GET.get('stock', '')
    if stock_status == 'low':
        products = products.filter(stock__lt=10)
    elif stock_status == 'out':
        products = products.filter(stock=0)
    
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'category': product.category.name if product.category else 'Uncategorized',
            'price': float(product.price),
            'discount_price': float(product.discount_price) if product.discount_price else None,
            'final_price': float(product.final_price),
            'stock': product.stock,
            'image': product.image.url if product.image else None,
            'status': 'Active' if product.stock > 0 else 'Out of Stock',
            'stock_level': 'high' if product.stock > 20 else 'medium' if product.stock > 5 else 'low'
        })
    
    return JsonResponse({'success': True, 'products': data})


def admin_add_product(request):
    """Add new product"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category_id = request.POST.get('category')
            price = request.POST.get('price')
            discount_price = request.POST.get('discount_price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            
            category = Category.objects.get(id=category_id)
            
            product = Product.objects.create(
                name=name,
                category=category,
                price=price,
                discount_price=discount_price if discount_price else None,
                stock=stock,
                description=description,
                image=image
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Product "{product.name}" added successfully',
                'product_id': product.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def admin_update_product(request, product_id):
    """Update existing product"""
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            
            product.name = request.POST.get('name', product.name)
            product.price = request.POST.get('price', product.price)
            product.discount_price = request.POST.get('discount_price') or None
            product.stock = request.POST.get('stock', product.stock)
            product.description = request.POST.get('description', product.description)
            
            if request.POST.get('category'):
                category = Category.objects.get(id=request.POST.get('category'))
                product.category = category
            
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            
            product.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Product "{product.name}" updated successfully'
            })
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def admin_delete_product(request, product_id):
    """Delete product"""
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            product_name = product.name
            product.delete()
            return JsonResponse({
                'success': True,
                'message': f'Product "{product_name}" deleted successfully'
            })
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# ============================================================
# ============  CATEGORY MANAGEMENT =========================
# ============================================================

def admin_get_categories(request):
    """Get all categories"""
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).order_by('name')
    
    data = []
    for cat in categories:
        data.append({
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'product_count': cat.product_count,
            'created_at': cat.created_at.strftime('%d %b %Y')
        })
    
    return JsonResponse({'success': True, 'categories': data})


def admin_add_category(request):
    """Add new category"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category = Category.objects.create(name=name)
            return JsonResponse({
                'success': True,
                'message': f'Category "{category.name}" added successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def admin_delete_category(request, category_id):
    """Delete category"""
    if request.method == 'POST':
        try:
            category = Category.objects.get(id=category_id)
            category_name = category.name
            category.delete()
            return JsonResponse({
                'success': True,
                'message': f'Category "{category_name}" deleted successfully'
            })
        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Category not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# ============================================================
# ============  FILTERED ORDERS API ========================
# ============================================================

def admin_get_orders_by_status(request, status):
    """Get orders filtered by status"""
    valid_statuses = ['pending', 'confirmed', 'packed', 'shipped', 'delivered', 'cancelled']
    
    if status not in valid_statuses and status != 'all':
        return JsonResponse({'success': False, 'message': 'Invalid status'})
    
    if status == 'all':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(order_status=status)
    
    orders = orders.order_by('-created_at')[:50]
    
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'order_id': f'#ORD-{order.id}',
            'customer': order.user.get_full_name() or order.user.username,
            'email': order.user.email,
            'date': order.created_at.strftime('%d %b %Y'),
            'amount': float(order.total_price),
            'payment_method': order.payment_method,
            'payment_status': 'Paid' if order.payment_status else 'Unpaid',
            'order_status': order.order_status,
        })
    
    return JsonResponse({'success': True, 'orders': data})


# ============================================================
# ============  HOME & PUBLIC VIEWS =========================
# ============================================================

def home(request):
    """Homepage with featured products and categories"""
    products = Product.objects.filter(stock__gt=0)[:8]
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).all()
    
    context = {
        'products': products,
        'categories': categories,
        'total_products': Product.objects.count(),
    }
    
    return render(request, 'home.html', context)


def product_list(request):
    """Product listing page with filters"""
    products = Product.objects.filter(stock__gt=0).select_related('category')
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).all()
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
        'total_products': products.count(),
    }
    
    return render(request, 'product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category, 
        stock__gt=0
    ).exclude(id=product.id)[:4]
    
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })


# ============================================================
# ============  AUTHENTICATION VIEWS ========================
# ============================================================

def register(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        
        if password != confirm:
            messages.error(request, "Passwords don't match")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )
        UserProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('home')
    
    return render(request, 'register.html')


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            
            # Merge session cart with user cart
            session_cart = request.session.get(CART_SESSION_ID, {})
            if session_cart:
                cart, _ = Cart.objects.get_or_create(user=user)
                for product_id, item_data in session_cart.items():
                    product = Product.objects.get(id=product_id)
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart,
                        product=product,
                        defaults={'quantity': item_data['quantity']}
                    )
                    if not created:
                        cart_item.quantity += item_data['quantity']
                        cart_item.save()
                request.session[CART_SESSION_ID] = {}
            
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'login.html')


def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


@login_required
def profile(request):
    """User profile page"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']
        profile.save()
        
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        messages.success(request, "Profile updated!")
        return redirect('profile')
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {
        'profile': profile, 
        'orders': orders
    })


# ============================================================
# ============  CART VIEWS =================================
# ============================================================

CART_SESSION_ID = 'cart'


def get_cart(request):
    """Get cart items for current user/session"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart.items.select_related('product').all(), cart
    else:
        session_cart = request.session.get(CART_SESSION_ID, {})
        cart_items = []
        for product_id, item_data in session_cart.items():
            try:
                product = Product.objects.get(id=product_id)
                cart_items.append({
                    'product': product,
                    'quantity': item_data['quantity'],
                    'total_price': product.final_price * item_data['quantity']
                })
            except Product.DoesNotExist:
                continue
        return cart_items, None


def cart_view(request):
    """Shopping cart page"""
    cart_items, cart_obj = get_cart(request)
    subtotal = sum(
        item.total_price if hasattr(item, 'total_price') else item['total_price'] 
        for item in cart_items
    )
    shipping = 60
    total = subtotal + shipping
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })


def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} items available")
        return redirect('product_detail', slug=product.slug)
    
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            if cart_item.quantity + quantity <= product.stock:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                messages.error(request, f"Cannot add more than {product.stock} items")
                return redirect('cart')
    else:
        cart = request.session.get(CART_SESSION_ID, {})
        current_qty = cart.get(str(product_id), {}).get('quantity', 0)
        if current_qty + quantity <= product.stock:
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] += quantity
            else:
                cart[str(product_id)] = {
                    'quantity': quantity,
                    'price': str(product.final_price)
                }
            request.session[CART_SESSION_ID] = cart
        else:
            messages.error(request, f"Cannot add more than {product.stock} items")
            return redirect('product_detail', slug=product.slug)
    
    messages.success(request, f"{product.name} added to cart!")
    return redirect('cart')


def remove_from_cart(request, product_id):
    """Remove item from cart"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    else:
        cart = request.session.get(CART_SESSION_ID, {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session[CART_SESSION_ID] = cart
    
    messages.success(request, "Item removed from cart")
    return redirect('cart')


def update_cart(request, product_id):
    """Update cart item quantity"""
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    
    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} items available")
        return redirect('cart')
    
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.filter(cart=cart, product_id=product_id).update(quantity=quantity)
    else:
        cart = request.session.get(CART_SESSION_ID, {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity
            request.session[CART_SESSION_ID] = cart
    
    return redirect('cart')


# ============================================================
# ============  CHECKOUT & ORDER VIEWS ======================
# ============================================================

@login_required
def checkout(request):
    """Checkout page"""
    cart_items, cart_obj = get_cart(request)
    
    if not cart_items:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')
    
    subtotal = sum(
        item.total_price if hasattr(item, 'total_price') else item['total_price'] 
        for item in cart_items
    )
    shipping = 60
    total = subtotal + shipping
    
    if request.method == 'POST':
        payment_method = request.POST['payment_method']
        transaction_id = request.POST.get('transaction_id', '')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=subtotal,
            payment_method=payment_method,
            payment_status=(payment_method == 'cod'),
            transaction_id=transaction_id
        )
        
        # Create order items and update stock
        for item in cart_items:
            if hasattr(item, 'product'):
                product = item.product
                quantity = item.quantity
                price = product.final_price
            else:
                product = item['product']
                quantity = item['quantity']
                price = product.final_price
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            
            # Reduce stock
            product.stock -= quantity
            product.save()
        
        # Create payment record for bKash/Nagad/Rocket
        if payment_method != 'cod':
            Payment.objects.create(
                order=order,
                transaction_id=transaction_id,
                method=payment_method,
                amount=total
            )
            messages.info(request, "Payment submitted! Waiting for admin verification.")
        else:
            messages.success(request, "Order placed successfully! (Cash on Delivery)")
        
        # Clear cart
        if request.user.is_authenticated and cart_obj:
            cart_obj.delete()
        else:
            request.session[CART_SESSION_ID] = {}
        
        return redirect('order_detail', order_id=order.id)
    
    # Get user profile for prefill
    profile = UserProfile.objects.get(user=request.user)
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'profile': profile
    })


@login_required
def order_detail(request, order_id):
    """Order details page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    subtotal = order.total_price
    shipping = 60
    total = subtotal + shipping
    
    return render(request, 'order_detail.html', {
        'order': order,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })


@login_required
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def submit_payment(request, order_id):
    """Submit payment information"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        transaction_id = request.POST['transaction_id']
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'transaction_id': transaction_id,
                'method': order.payment_method,
                'amount': order.total_price + 60  # Add shipping
            }
        )
        if not created:
            payment.transaction_id = transaction_id
            payment.save()
        
        order.transaction_id = transaction_id
        order.save()
        
        messages.success(request, "Payment information submitted. Admin will verify soon.")
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'submit_payment.html', {'order': order})


# ============================================================
# ============  CONTEXT PROCESSOR ===========================
# ============================================================

def cart_count(request):
    """Context processor for cart item count"""
    CART_SESSION_ID = 'cart'
    
    if request.user.is_authenticated:
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            count = sum(item.quantity for item in cart.items.all())
        except Exception:
            count = 0
    else:
        cart = request.session.get(CART_SESSION_ID, {})
        count = sum(item.get('quantity', 0) for item in cart.values())
    
    return {'cart_count': count}


# ============================================================
# ============  ADMIN ORDER CANCELLATION API ================
# ============================================================

def admin_cancel_order(request, order_id):
    """User cancel order - real-time update"""
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            
            # Only allow cancellation for pending/confirmed COD or unpaid orders
            if order.order_status not in ['pending', 'confirmed']:
                return JsonResponse({'success': False, 'message': 'Order cannot be cancelled at this stage'})
            
            if order.payment_status and order.payment_method != 'cod':
                return JsonResponse({'success': False, 'message': 'Paid orders cannot be cancelled. Please contact support.'})
            
            order.order_status = 'cancelled'
            order.save()
            
            # Restore product stock
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                product = item.product
                product.stock += item.quantity
                product.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Order #{order.id} cancelled successfully'
            })
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})




# ============================================================
# ============  USER ORDER CANCELLATION ======================
# ============================================================

@login_required
def user_cancel_order(request, order_id):
    """
    Allow users to cancel their own orders in real-time
    - Only pending or confirmed orders
    - Only COD orders or unpaid orders
    - Restores product stock automatically
    """
    if request.method == 'POST':
        try:
            # Ensure user can only cancel THEIR OWN orders
            order = Order.objects.get(id=order_id, user=request.user)
            
            # Check if order can be cancelled based on status
            if order.order_status not in ['pending', 'confirmed']:
                return JsonResponse({
                    'success': False, 
                    'message': f'Order cannot be cancelled at this stage (Status: {order.get_order_status_display()})'
                })
            
            # Check if payment is already verified (except COD)
            if order.payment_status and order.payment_method != 'cod':
                return JsonResponse({
                    'success': False, 
                    'message': 'Paid orders cannot be cancelled online. Please contact customer support.'
                })
            
            # Update order status to cancelled
            order.order_status = 'cancelled'
            order.save()
            
            # Restore product stock - IMPORTANT for inventory
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                product = item.product
                product.stock += item.quantity
                product.save()
            
            # If there was a payment, mark it as refund pending (optional)
            if order.payment_status and order.payment_method == 'cod':
                # COD orders don't need refund
                pass
            
            return JsonResponse({
                'success': True,
                'message': f'Order #{order.id} cancelled successfully',
                'order_id': order.id,
                'status': 'cancelled'
            })
            
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Order not found or you do not have permission to cancel this order'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error cancelling order: {str(e)}'
            })
    
    return JsonResponse({
        'success': False, 
        'message': 'Invalid request method'
    })