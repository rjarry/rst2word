# rst2word's setup.py
from distutils.core import setup
setup(
    name = "rst2word",
    version = "0.6.0",
    license = "MIT",
    platforms = ["Windows"],
    requires = ["docutils (>=0.7)", "PyWin32"],

    description = "A Word writer for docutils",
    long_description = open('README.rst').read(),
    author = "Robin Jarry",
    author_email = "robin.jarry@gmail.com",
    url = "http://github.com/robin-jarry/rst2word",
    download_url = "http://github.com/robin-jarry/rst2word",
    keywords = ["docutils", "rst", "reStructuredText", "word"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: Beta",
        "Environment :: Windows",
        'Intended Audience :: End Users/Desktop',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT",
        'Operating System :: Microsoft :: Windows',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Document Generation",
    ],
    packages = ["rst2wordlib"],
    package_dir = {'': 'src'},
    package_data = {'rst2wordlib': ['templates/rst2word.dot', 'templates/rst2word.dotx']},
    data_files = [
        ('rst2word/templates', ['templates/rst2word.dot', 'templates/rst2word.dotx'])
    ],
    scripts = ['src/scripts/rst2word.cmd', 'src/scripts/rst2word.py']
)

