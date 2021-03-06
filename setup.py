from setuptools import setup, find_packages


setup(
    name='dropapp',
    version='1.0',
    py_modules=[
        'config',
        'dropapp',
        'models',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask-Restless==1.0.0b1',
        'Flask-SQLAlchemy==2.1',
        'Flask==0.10.1',
        'Jinja2==2.8',
        'MarkupSafe==0.23',
        'SQLAlchemy==1.0.12',
        'Werkzeug==0.11.9',
        'biplist==1.0.1',
        'itsdangerous==0.24',
        'libipa',
        'mimerender==0.6.0',
        'python-dateutil==2.5.3',
        'python-mimeparse==1.5.1',
        'six==1.10.0',
    ],
    dependency_links=[
        'git+https://github.com/Tatsh/libipa.git@42555191e4d667d9b8d920200123c1496433428a#egg=libipa',
        'git+https://github.com/jfinkels/flask-restless.git@1.0.0b1#egg=Flask-Restless',
    ]
)
