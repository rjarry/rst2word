# rst2word's setup.py
from distutils.core import setup
setup(
    name = "rst2word",
    version = "0.4.3",
    license = "MIT",
    platforms = ["Windows"],
    requires = ["docutils (>=0.7)", "win32com"],

    description = "A Word writer for docutils",
    long_description = open('README.txt').read(),
    author = "Robin Jarry",
    author_email = "robin.jarry@gmail.com",
    url = "https://github.com/diabeteman/rst2word",
    download_url = "https://github.com/diabeteman/rst2word",
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
    scripts = ['src/scripts/rst2word.cmd', 'src/scripts/rst2word.py']
)

