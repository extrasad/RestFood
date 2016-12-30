# coding=utf-8
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='RestFood',
    version='1.0.0',
    license='MIT',
    author='charlyjazz',
    author_email='carlosjazzc1@gmail.com',
    description='restaurant social web',
    packages=find_packages('app'),
    package_dir = {'': 'app'},
    platforms='any',
    install_requires=[
        'django',
        'django-bower==5.2.0',
        'django-material==0.11.0',
        'django-simple-captcha==0.5.3',
        'django-newsletter==0.6',
        'Pillow',
    ],
)
