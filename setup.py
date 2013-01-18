try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

config = {
        'description': 'This is my simple blackjack program',
        'author': 'Adames',
        'download_url': 'https://github.com/Adames/blackjackhard',
        'author_email': 'adames.hodelin@gmail.com',
        'version': '0.1',
        'install_requires': ['nose'],
        'packages': ['blackjackHARD'],
        'scripts': [],
        'name': 'blackjackHARD'
}

setup(**config)
