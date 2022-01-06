import setuptools

req = ["p2pnetwork"]

setuptools.setup(
    name="lutherium",
 
    version="0.0.1",
 
    author="Owen Shaule",
 
    author_email="ow1e3@protonmail.com",
 
    description="Example",

    long_description="NOTE: This is in beta and there is still allot of work to do with this project.",
    long_description_content_type="text/markdown",
 
    url="",
    
    packages=["lutherium"],
 
    install_requires=req,
 
    license="MIT",
 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'luthercli=lutherium.cli:main'
        ]
    },
)
