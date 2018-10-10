#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="django_japanese_standard_bus_info_format",
    version="1.0.0",
    description="標準的なバス情報フォーマットをGeoDjangoで扱えるようにするパッケージ",
    author="Aruneko",
    author_email="aruneko99@gmial.com",
    license="MIT",
    url="https://github.com/aruneko/django-japanese-standard-bus-info-format",
    install_requires=["django"],
    packages=find_packages(),
)
