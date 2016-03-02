from setuptools import setup

setup(
    name='nao',
    version='0.1',
    py_modules=['nao'],
    install_requires=[
        'Click'
    ],
    entry_points="""
    [console_scripts]
    nao=nao:cli
    """
)
