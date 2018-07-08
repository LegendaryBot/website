import setuptools

def read_requirements(filename):
    with open(filename, 'r') as file:
        return [line for line in file.readlines() if not line.startswith('-')]
setuptools.setup(
    name="legendarybot-website",
    version="0.0.1",
    author="Greatman",
    author_email="notyourbusiness@test.com",
    description="LegendaryBot website",
    long_description="LegendaryBot website",
    long_description_content_type="text/markdown",
    url="https://github.com/LegendaryBot/website",
    packages=[
        "lbwebsite"
    ],
    install_requires=read_requirements('requirements.txt'),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)