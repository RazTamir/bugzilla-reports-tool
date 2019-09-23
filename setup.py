"""A setuptools-based script for installing Bugzilla Report Tools."""
from setuptools import find_packages, setup

setup(
    name='Bugzilla Report Tools',
    author='Raz Tamir',
    author_email='ratamir@redhat.com',
    version='0.0.1',
    packages=find_packages(include=['reporttools', 'reporttools.*']),
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'gspread',
        'oauth2client',
        'python-bugzilla',
    ],

    include_package_data=True,
    license='GPLv3',
    description=(
        'Create a Quality dashboard for your product and send'
        ' (weekly) reports with bug status.'),
    package_data={'': ['LICENSE']},
    url='https://github.com/RazTamir/bugzilla-reports-tool',
)
