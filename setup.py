# encoding: utf-8
from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

meta = {}
with open('funcwrap.py', 'rb') as f:
    exec(f.read(), meta, meta)


setup(
    name='funcwrap',
    version=meta['__version__'],
    description='Helps function wrappers/decorators with perfect forwarding',
    author='Thomas Gläßle',
    author_email='thomas@coldfix.de',
    url='https://github.com/coldfix/funcwrap',
    py_modules=['funcwrap'],
    python_requires='>=3.5',
    install_requires=[],
    tests_require='pytest',
    zip_safe=True,
    license='Unlicense',
    license_files=['UNLICENSE'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'License :: Public Domain',
    ],
)
