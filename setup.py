import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SliPi",
    version="3.0",
    author="Mark Williams",
    author_email="msw4@pdx.edu",
    description="Python 3 hardware accelerated slideshow for the Raspberry Pi using the Pi3d library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thyme676/SliPi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
     install_requires=[
        'Pillow>=5.0',
        'pi3d>=2.0',
        'numpy>=1.16',
        'ruamel.yaml>=0.15'
    ],
)
