from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.RST').read_text(encoding='utf-8')

setup(
    name="pymacros4py",
    version="0.8",
    description=("Macro preprocessor for Python code. Write your macros in Python, "
                 + "even directly in your code. Replacements can be in-place, "
                 + "multi-stage, and recursive. Pure Python, tiny code."),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/HeWeMel/pymacros4py",
    author="Dr. Helmut Melcher",
    author_email='HeWeMel@web.de',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={"pymacros4py": ["py.typed"]},
    # install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    keywords=('macro, preprocessor, python code, replace, in-place'),
    python_requires='>=3.9, <4',
    project_urls={
        'Source': 'https://github.com/hewemel/pymacros4py/',
        'Bug Reports': 'https://github.com/hewemel/pymacros4py/issues',
    },
    license_files='LICENSE',
)