from setuptools import setup

LONG_DESC = open("README.md").read()

setup(
    name="kadai-gui",
    version="1.0.0a0",
    description="Resizes wallpapers to desired size",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://github.com/slapelachie/kadai-gui",
    author="slapelachie",
    author_email="lslape@slapelachie.xyz",
    license="GPLv2",
    packages=["kadai_gui", "kadai_gui.utils"],
    entry_points={"console_scripts": ["kadai-gtk=kadai_gui.__main__:main_gtk"]},
    install_requires=[],
    zip_safe=False,
)