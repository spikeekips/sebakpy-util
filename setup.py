from setuptools import setup, find_packages


long_description = None
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sebak',
    version='0.1.0',
    description='base library for SEBAK',
    author='Spike^ekipS',
    author_email='spikeekips@gmail.com',
    url='https://github.com/spikeekips/sebakpy-util',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    py_modules=['sebak'],
    package_dir={'': './src'},
    packages=find_packages('./src'),
    install_requires=(
        'stellar-base>=0.1.9',
        'rlp>=1.0.3',
        'base58>=1.0.2',
    ),
)
