from distutils.core import setup

setup(
    name='django-generic-confirmation',
    version=__import__('generic_confirmation').__version__,
    description='Deferred forms for the Django webframework',
    author='Arne Brodowski',
    author_email='mail@arnebrodowski.de',
    url='https://github.com/arneb/django-generic-confirmation/',
    packages=(
        'generic_confirmation',
        'generic_confirmation.templatetags',
        'generic_confirmation.tests',
    ),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Framework :: Django',
    ),
)
