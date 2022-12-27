from setuptools import setup

setup(
    name='bank',
    version='0.1.0',
    py_modules=['bank'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'bank = app.bank:bank_app',
        ],
    },
)