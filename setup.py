#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tikphoto',
    version='1.0.0',
    author='Hussein Al-Sokar',
    author_email='',
    description='TikPhoto - Professional Image Editor for Android',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kjnnzxck-droid/tikphoto',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Android',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: Arabic',
    ],
    python_requires='>=3.9',
    install_requires=[
        'kivy>=2.2.0',
        'opencv-python>=4.8.0',
        'Pillow>=10.0.0',
        'numpy>=1.24.0',
    ],
)
