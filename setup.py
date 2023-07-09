from setuptools import setup, find_packages

setup(
    name='wink',
    version='0.0.1',
    description='A general-purpose management system background api',
    author='Mao',
    author_email='mjhxyz@foxmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.1.2',
        'Flask-SQLAlchemy>=3.0.3',
        'cymysql>=0.9.18',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
