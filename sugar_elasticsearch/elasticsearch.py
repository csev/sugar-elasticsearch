import os

import aiohttp
from sanic import Blueprint
from sanic.response import json, text

from sugar_api import webtoken, scope, preflight, CORS


class Elasticsearch(object):

    __host__ = os.getenv('SUGAR_ELASTICSEARCH_URI', 'http://localhost:9200')
    __methods__ = [ 'HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE' ]

    @classmethod
    def set_host(cls, uri):
        cls.__host__ = uri

    @classmethod
    def get_host(cls):
        return cls.__host__

    @classmethod
    def resource(cls, *args, **kargs):

        if not len(args) > 0:
            args = [ 'elasticsearch' ]

        bp = Blueprint(*args, **kargs)

        @bp.options('/elasticsearch')
        async def options(*args, **kargs):
            return preflight(methods=cls.__methods__)

        @bp.options('/elasticsearch/<index>')
        async def options(*args, **kargs):
            return preflight(methods=cls.__methods__)

        @bp.options('/elasticsearch/<index>/<path:path>')
        async def options(*args, **kargs):
            return preflight(methods=cls.__methods__)

        @bp.route('/elasticsearch', methods=cls.__methods__)
        @webtoken
        @scope({ 'elasticsearch.administrator': True })
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        @bp.route('/elasticsearch/<index>', methods=cls.__methods__)
        @webtoken
        @scope({ 'elasticsearch.administrator': True, 'elasticsearch.index': '$index' })
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        @bp.route('/elasticsearch/<index>/<path:path>', methods=cls.__methods__)
        @webtoken
        @scope({ 'elasticsearch.administrator': True, 'elasticsearch.index': '$index' })
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        return bp

    @classmethod
    async def handler(cls, request, index='', path='', token=None):
        uri = f'{cls.__host__}/{index}/{path}' # Elasticsearch collapses // to /
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession() as session:
            async with session.request(request.method, uri, data=request.body, headers=headers) as response:
                try:
                    return json(await response.json(), headers={
                        'Access-Control-Allow-Origin': CORS.get_origins()
                    })
                except aiohttp.ContentTypeError:
                    return text(await response.text(), headers={
                        'Access-Control-Allow-Origin': CORS.get_origins()
                    })
