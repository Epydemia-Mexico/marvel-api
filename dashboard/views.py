import requests
import hashlib
import json
from django.shortcuts import render
from django.views import View

PRIVATE_KEY = '4ab6289c170bb51224c3249bd639eac6d2f3fdb5'
PUBLIC_KEY = '7c0a8d4895927fcef1f5789e0e125869'
URL_MARVEL = 'https://gateway.marvel.com'


class APICallerView(View):
    URL = None

    def get_query(self, **kwargs):
        ts = 1
        string_to_hash = f'{ts}{PRIVATE_KEY}{PUBLIC_KEY}'
        hashed = hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()
        query = f'?ts={ts}&apikey={PUBLIC_KEY}&hash={hashed}'
        for k,v in kwargs.items():
            query += f'&{k}={v}'
        return query

    def make_request(self, query):
        response = requests.get(URL_MARVEL + self.URL + query)
        data = json.loads(response.content)['data']['results']
        return data


class HomeView(APICallerView):
    URL = '/v1/public/characters'

    def get(self, request):
        template_name = 'index.html'
        if 'name' in request.GET:
            name = request.GET.get('name')
            data = self.make_request(self.get_query(nameStartsWith=name))
        else:
            data = self.make_request(self.get_query())
        return render(request, template_name, dict(data=data))


class ComicsView(APICallerView):
    URL = '/v1/public/comics'

    def get(self, request):
        template_name = 'comic.html'
        if 'search' in request.GET:
            title = request.GET.get('search')
            data = self.make_request(self.get_query(titleStartsWith=title))
        else:
            data = self.make_request(self.get_query())
        return render(request, template_name, dict(data=data))
