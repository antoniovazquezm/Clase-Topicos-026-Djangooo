# catalogo/views.py (reemplaza el contenido completo del archivo)
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db import connection

from .models import Cancion, Playlist


def lista_canciones(request):
    generos = Playlist.objects.values_list('genero', flat=True).distinct().exclude(genero__isnull=True).exclude(genero='') #no entendí por qué? 
    return render(request, "catalogo/lista.html", {"generos": generos})

def detalle_cancion(request, pk):
    return render(request, "catalogo/detalle.html",{"pk": pk})

def detalle_playlist(request, pk):
    return render(request, "catalogo/detalle_playlist.html",{"pk": pk})



# def lista_canciones(request):
#     q = request.GET.get("q", "").strip()
#     genero = request.GET.get("genero", "").strip()

#     canciones = Cancion.objects.prefetch_related("playlists").all()


#     if q:
#         canciones = canciones.filter(Q(titulo__icontains=q) | Q(artista__icontains=q))

#     if genero:
#         canciones = canciones.filter(playlists__genero=genero).distinct()

#     generos = (Playlist.objects.values_list("genero", flat=True).distinct().order_by("genero"))
#     # print("Generos en el csv:", list(generos))
#     #es la consulta que tuve que hacer para ver si se imprimía lo del csv y luego poder hacer bien el <select

#     paginator = Paginator(canciones, 25)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     contexto = {
#         "page_obj": page_obj,
#         "total": canciones.count(),
#         "q": q,
#         "genero": genero,
#         "generos": generos,
#     }
#     # return render(request, "catalogo/lista.html", contexto)
#     respuesta = render(request, "catalogo/lista.html", contexto)
#     print("consultas SQL sin optimizar:", len(connection.queries))
#     return respuesta

# #declaración de IA:
# #no estaba funcionando el <select> de generos, porque olvidé por completo pasar "genero" al contexto...solo declaré y pasé "generos" (la lista de generos) y no el genero seleccionado

# def detalle_cancion(request, pk):
#     cancion = get_object_or_404(Cancion, pk=pk)
#     return render(request, "catalogo/detalle.html", {"cancion": cancion})

# def detalle_playlist(request, pk):
#     playlist = get_object_or_404(Playlist, pk=pk)
#     canciones = playlist.canciones.all().order_by("-popularidad")

#     return render(request, "catalogo/detalle_playlist.html", {"playlist": playlist, "canciones": canciones})