from setuptools import find_packages
from setuptools import setup

install_requires = [
    "flask",
    "flask_mongoengine",
    "bcrypt",
    "flask_pymongo",
    "pytz",
    "flask_classy",
    "gunicorn",
    'sentry-sdk[flask]==0.10.1'
]

setup(
    name="app",
    version="1.0.4",
    url="https://fitr.gq",
    license="None",
    maintainer="CDF",
    maintainer_email="howzitcallum@gmail.com",
    description="Fitness App",
    long_description="Fitness App",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"test": ["pytest", "coverage"]},
    scripts=['./app/init/init_db']
)
