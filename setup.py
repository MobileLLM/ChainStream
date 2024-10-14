# set up basic requirements for droidbot
from setuptools import setup, find_packages, findall
import os

setup(
    name='chainstream',
    packages=find_packages(include=['chainstream', 'chainstream.runtime']),
    # this must be the same as the name above
    version='0.0.1',
    description='Development framework and runtime system for LLM-based stream agent.',
    author='Yuanchun Li',
    license='CUSTOM',
    author_email='li.yuanchun@foxmail.com',
    url='https://github.com/MobileLLM/ChainStream',  # use the URL to the github repo
    download_url='https://github.com/MobileLLM/ChainStream/tarball/0.0.1',
    keywords=['LLM', 'agent', 'stream', 'development', 'system'],  # arbitrary keywords
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'chainstream=start:main',
        ],
    },
    package_data={
        'chainstream': [os.path.relpath(x, 'chainstream') for x in findall('chainstream/resources/')]
    },
    install_requires=['torch', 'pandas', 'flask', 'flask_cors', 'pillow', 'pydub', 'websocket', 'websocket-client', 'openai'],
)
