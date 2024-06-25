import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_login_history2",
    version="0.0.5",
    author="Henrique da Silva Santos",
    author_email="rique_dev@hotmail.com",
    description="It's easy to use, plug-in django app that once included, stores logins history (with device data, like IP, user-agent, location etc.) of all users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/riquedev/django-login-history2",
    keywords="security, django, login, location, session, ip, authenticate",
    project_urls={
        "Bug Tracker": "https://github.com/riquedev/django-login-history2/issues",
        "Repository": "https://github.com/riquedev/django-login-history2",
    },
    install_requires=[
        'Django>=3.2.13',
        'django_ipware>=4.0.2',
        'requests>=2.31.0',
    ],
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    packages=setuptools.find_packages(exclude=("tests",'django_login_history', "manage.py")),
    include_package_data=True,
    python_requires=">=3.8"
)
