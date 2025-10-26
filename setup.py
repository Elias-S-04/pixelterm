from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pixelterm",
    version="0.1.0",
    author="Elias-S-04",
    author_email="eliaslvsrs@gmail.com",
    description="Terminal-based pixel graphics library with GitHub integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Elias-S-04/pixelterm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Terminals",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="terminal graphics pixel art github heatmap visualization",
    install_requires=[
        "requests>=2.25.0",
        "pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "pixelterm-github=pixelterm.githubmap:main",
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
