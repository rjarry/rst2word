# rst2word's setup.py
from distutils.core import setup
setup(
    name = "rst2word",
    packages = ["rst2wordlib"],
    scripts=['scripts/rst2word.cmd', 'scripts/rst2word.py'],
    version = "0.3.2",
    description = "A Word writer for docutils",
    author = "Robin Jarry",
    author_email = "robin.jarry@gmail.com",
    url = "https://github.com/diabeteman/rst2word",
    download_url = "https://github.com/diabeteman/rst2word",
    keywords = ["docutils", "rst", "reStructuredText", "word"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6+",
        "Development Status :: Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Document Generation",
        ],
)

