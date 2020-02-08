__author__ = 'Paul Severance'

from setuptools import setup

setup(
    name='sugar-elasticsearch',
    version='0.0.1',
    author='Paul Severance',
    author_email='paul.severance@gmail.com',
    url='https://github.com/sugarush/sugar-elasticsearch',
    packages=[
        'sugar_elasticsearch'
    ],
    description='An asynchronous Elasticsearch proxy with JWT based authentication.',
    install_requires=[
        'sugar-api@git+https://github.com/sugarush/sugar-api@master',
    ]
)
