from setuptools import setup, find_packages

setup(
    name='wink',
    version='0.0.1',
    description='A general-purpose management system background api',
    author='Mao',
    author_email='mjhxyz@foxmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.3.2',
        'Flask-SQLAlchemy>=3.0.5',
        'cymysql>=0.9.18',
        'Flask-Login>=0.6.2',
        'authlib>=1.2.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
