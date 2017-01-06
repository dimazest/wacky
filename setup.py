from setuptools import setup, find_packages


setup(
    name='wacky',
    version='0.0.1',
    description='A reader for WaCky corpora.',
    long_description='A reader for WaCky corpora.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
    ],
    author='Dmitrijs Milajevs',
    author_email='dimazest@gmail.com',
    license='MIT license',

    packages=find_packages(),

    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'wacky = wacky.__main__:cli',
        ],
    },
)
