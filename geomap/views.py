import json
from pathlib import Path
from django.shortcuts import render


# Create your views here.
def index(request):
    # Import folium lazily and handle missing dependency at runtime.
    try:
        import folium
    except ModuleNotFoundError:
        msg = (
            "<div class='alert alert-warning' role='alert'>"
            "Folium is not installed. Install it with "
            "<code>pip install folium</code> to view the map."
            "</div>"
        )
        return render(request, "geomap/index.html", {"map": msg})
    m = folium.Map(location = [20, 0], zoom_start = 3, min_zoom = 3, max_zoom = 10, max_bounds= True)
    geojson_path = Path(__file__).resolve().parent / "custom.geo.json"
    with open(geojson_path, mode="r", encoding="utf-8") as f:
        countries = json.load(f)
    folium.GeoJson(countries,
                     name = "Countries", 
                     tooltip= folium.GeoJsonTooltip(fields = ["formal_en"], aliases = ["Country:"]),
                     style_function=lambda feature: {'fillColor': 'yellow', 'color': 'yellow', 'weight': 0.1,'fillOpacity': 0.3, 'stroke': False},
                    highlight_function = lambda x: {'fillColor': 'white', 'color': 'white', 'weight': 0.5, 'stroke': False},
                    zoom_on_click= True,

                    ).add_to(m)
    
    map_html = m._repr_html_()
    return render(request, "geomap/index.html", {"map": map_html})

