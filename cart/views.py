from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
        {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    # Only allow POST to finalize a purchase
    if request.method != 'POST':
        return redirect('cart.checkout')

    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if movie_ids == []:
        return redirect('cart.index')

    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    order = Order()
    order.user = request.user
    order.total = cart_total
    # Optional location fields from checkout form
    order.city = (request.POST.get('city') or '')[:120]
    order.state = (request.POST.get('state') or '')[:120]
    order.country = (request.POST.get('country') or '')[:120]
    lat = request.POST.get('latitude')
    lon = request.POST.get('longitude')
    try:
        order.latitude = float(lat) if lat not in (None, '') else None
    except (TypeError, ValueError):
        order.latitude = None
    try:
        order.longitude = float(lon) if lon not in (None, '') else None
    except (TypeError, ValueError):
        order.longitude = None
    order.save()

    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        movie.amount_left -= 1
        item.save()
        movie.save()

    request.session['cart'] = {}
    template_data = {
        'title': 'Purchase confirmation',
        'order_id': order.id,
    }
    return render(request, 'cart/purchase.html', {'template_data': template_data})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if movie_ids == []:
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {
        'title': 'Checkout',
        'movies_in_cart': movies_in_cart,
        'cart_total': cart_total,
    }
    return render(request, 'cart/checkout.html', {'template_data': template_data})
