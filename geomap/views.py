import json
from pathlib import Path
from django.shortcuts import render
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.db.models.functions import Coalesce

from cart.models import Order, Item
from movies.models import Movie, Region, MovieRegionStat


# Create your views here.
def index(request):
    # Import folium lazily and handle missing dependency at runtime.

    return render(request, "geomap/index.html")


def get_regional_trends(request):

    regions_with_high_views = MovieRegionStat.objects.values('region__name').annotate(
        total_views = Sum('views')
    ).filter(total_views__gt=5)

    data = []

    for region_stat in regions_with_high_views:
        region_name = region_stat['region__name']

        if not region_name or region_name.strip() == "":
            continue

        first_order_in_region = Order.objects.filter(
            city__icontains=region_name.split(',')[0]
        ).filter(latitude__isnull = False,
                 longitude__isnull = False).first()

        if first_order_in_region:

            top_movie_stat = MovieRegionStat.objects.filter(
                region__name=region_name
            ).order_by('-views').first()

            top_movie_name = top_movie_stat.movie.name if top_movie_stat else "N/A"
            data.append({
                'name': region_name,
                'total_views': region_stat['total_views'],
                'lat': first_order_in_region.latitude,
                'lng': first_order_in_region.longitude,
                'top_movie': top_movie_name,
            })
    return JsonResponse({'regions':data})

def get_trending_movies_in_bbox(request):
    bbox_str = request.GET.get('bbox')
    if not bbox_str:
        return JsonResponse({'error': 'Bounding box not provided'}, status = 400)

    try:
        west, south, east, north = [float(coord) for coord in bbox_str.split(',')]
    except (ValueError, IndexError):
        return JsonResponse({'error': 'Invalid bounding box format'}, status = 400)


    orders_in_bounds = Order.objects.filter(
        latitude__gte=south,
        latitude__lte=north,
        longitude__gte=west,
        longitude__lte=east
    )

    trending_movies = Item.objects.filter(
        order__in=orders_in_bounds
    ).values('movie__title').annotate(
        view_count=Sum('quantity')
    ).order_by('-view_count')[:2]

    data = [
        {
            'title': movie['movie__title'],
            'view_count': movie['view_count'],
        }
        for movie in trending_movies
    ]

    return JsonResponse({'trending':data})