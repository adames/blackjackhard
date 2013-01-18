try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

config = {
        'description': 'My Project',
        'author': 'Adames',
        'download_url': 'URL to get it at.',
        'author_email': 'adames.hodelin@gmail.com',
        'version': '0.1',
        'install_requires': ['nose'],
        'packages': ['NAME'],
        'scripts': [],
        'name': 'projectname'
}

setup(**config)
