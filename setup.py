import setuptools
import os

def read_file(path):
    with open(path, "r") as fp:
        return fp.read()

def install_requires():
    requirements = read_file(os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")).split("\n")
    requirements = list(filter(lambda s: not not s, map(lambda s: s.strip(), requirements)))

    return requirements

long_description = read_file("README.md")

setuptools.setup(
    name="MSMPstream",
    version="0.7.7",
    author="Maxsspeaker",
    description="A bootstrapper for Roblox and Roblox Studio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://msmp.maxsspeaker.tk",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["MSMPstream=MSMPstream.__main__:main","MSMPdownloader=MSMPstream.__main__:mainDownloader"]
    },
    data_files = [
        ('share/applications', ['MSMPstream/resources/msmp-stream.desktop']),
#        ('share/applications', ['resources/roblox-studio.desktop']),
        ('share/icons/hicolor/512x512/apps', ['MSMPstream/resources/msmp-stream.png']),
##        ('share/icons/hicolor/scalable/apps', ['resources/roblox-player.svg']),
##        ('share/icons/hicolor/scalable/apps', ['resources/roblox-studio.svg'])
    ],
    install_requires=install_requires(),
    python_requires='>=3.10',
)
