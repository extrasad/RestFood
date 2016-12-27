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
    author_web='https://github.com/CharlyJazz',
    description='restaurant social web',
    packages=find_packages('core'),
    package_dir = {'': 'core'},
    platforms='any',
    install_requires=[
        'django',
        'django-bower',
        'django-material',
        'django-simple-captcha',
        'django-newsletter',
        'Pillow',
    ],
)
