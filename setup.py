import sys

import setuptools


importlib_req = ['importlib'] if sys.version_info < (2,7) else []
argparse_req = ['argparse'] if sys.version_info < (2,7) else []

setup_params = dict(
    name="ircbot",
    description="Simple IRC bot library for Python",
    use_hg_version=True,
    packages=setuptools.find_packages(),
    author="x64x6a",
)



if __name__ == '__main__':
	setuptools.setup(**setup_params)