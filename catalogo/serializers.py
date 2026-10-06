from rest_framework import serializers
from .models import Cancion, Playlist

class PlaylistResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'nombre', 'genero']

class PlaylistSerializer(serializers.ModelSerializer):
    num_canciones = serializers.IntegerField(read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'playlist_id', 'nombre', 'genero', 'subgenero', 'num_canciones']

class CancionSerializer(serializers.ModelSerializer):
    #lectura de playlists asociadas a la canción
    playlists = PlaylistResumeSerializer(many=True, read_only=True)

    #Escritura -> el cliente manda solo los ids de las playlists
    playlist_ids = serializers.PrimaryKeyRelatedField(
        source='playlists',
        queryset=Playlist.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Cancion
        fields = [
            'id',
            'spotify_id',
            'titulo', 
            'artista', 
            'album', 
            'popularidad', 
            'duracion_ms', 
            'fecha_lanzamiento', 
            'creada_en', 
            'playlists',
            'playlist_ids'
        ]
        read_only_fields = ['creada_en']

    def validate_popularidad(self, valor):
        if valor > 100 and valor < 0:
            raise serializers.ValidationError("La popularidad va de 0 a 100")
        return valor

