from rest_framework.views import APIView
import requests
from rest_framework.exceptions import ValidationError
from .view_utils import SearchParams, Coordinates
from django.conf import settings
from urllib.parse import urljoin
from rest_framework.response import Response
from django.http import Http404
from django.core.cache import cache

OPEN_MAP_KEY = settings.OPEN_MAP_KEY
OPEN_MAP_URI = settings.OPEN_MAP_URI


class Search(APIView):
    def CheckQueryParams(self, request):
        place_name = request.query_params.get('placeName', None)
        radius = request.query_params.get('radius', None)
        if place_name is None or radius is None:
            raise ValidationError(
                {'error': 'There was a missing query parameter in your search, please include both place name and radius'})
        return SearchParams(place_name=place_name, radius=radius)

    def GetOpenMapCoordinates(self, place_name):
        response = requests.get(urljoin(OPEN_MAP_URI, 'geoname'), params={
            'apikey': OPEN_MAP_KEY, 'name': place_name})
        rjson = response.json()
        coordinates = Coordinates(lat=rjson['lat'], lon=rjson['lon'])
        return coordinates

    def GetOpenMapSearch(self, coordinates, search_params):
        response = requests.get(urljoin(OPEN_MAP_URI, 'radius'), params={
                                'apikey': OPEN_MAP_KEY, 'lat': coordinates.lat, 'lon': coordinates.lon, 'radius': search_params.radius})
        rjson = response.json()
        if len(rjson['features']) == 0:
            raise Http404('There were no places found in the specified radius around {}'.format(
                search_params.place_name))
        return rjson['features']

    def get(self, request):
        search_params = self.CheckQueryParams(request)
        cache_key = search_params.place_name + search_params.radius
        cached_search = cache.get(cache_key)
        if cached_search is not None:
            return Response(cached_search)
        coordinates = self.GetOpenMapCoordinates(search_params.place_name)
        open_map_search = self.GetOpenMapSearch(coordinates, search_params)
        cache.set(cache_key, open_map_search)
        return Response(open_map_search)


class Details(APIView):
    def GetOpenMapDetails(self, xid):
        response = requests.get(
            urljoin(OPEN_MAP_URI, 'xid/{}'.format(xid)), params={'apikey': OPEN_MAP_KEY})
        return response

    def get(self, request, xid):
        cached_details = cache.get(xid)
        if cached_details is not None:
            return Response(cached_details)
        open_map_details = self.GetOpenMapDetails(xid)
        cache.set(xid, open_map_details)
        return Response(open_map_details)
