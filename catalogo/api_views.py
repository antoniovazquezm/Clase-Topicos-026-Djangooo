from django.db.models import Count, Q
from rest_framework import viewsets

from .models import Cancion, Playlist
from .serializers import CancionSerializer, PlaylistSerializer

class CancionViewSet(viewsets.ModelViewSet):
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializer

#aquí no entiendo? O sea lo que tenía en views.py tiene que estar ahora en api? pero por qué la excepcion?
    def get_queryset(self):
        
        queryset = Cancion.objects.all().distinct() #dame todas las canciones en la bd pero que no se repitan

        # 1. Filtro por búsqueda de texto (título o artista)
        search_query = self.request.query_params.get('search') or self.request.query_params.get('q')
        if search_query and search_query.strip():
            query = search_query.strip()
            queryset = queryset.filter(
                Q(titulo__icontains=query) | Q(artista__icontains=query)
            )

        # 2. Filtro por género
        genero = self.request.query_params.get('genero')
        if genero and genero.strip():
            genero_val = genero.strip()
            # Intentamos filtrar por la relación de playlists
            try:
                queryset = queryset.filter(playlists__genero__icontains=genero_val)
            except Exception:
                # Si el related_name no es 'playlists', probamos con 'playlist'
                queryset = queryset.filter(playlist__genero__icontains=genero_val)

        return queryset
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.annotate(num_canciones=Count('canciones')).order_by('nombre')
    serializer_class = PlaylistSerializer