from setuptools import setup

setup(
    name='ljon',
    version='0.0.1',
    author='Mihir Singh (@citruspi)',
    author_email='hello@mihirsingh.com',
    description='A no-frills static site generator',
    url='https://github.com/citruspi/ljon',
    classifiers=[
        'License :: Public Domain',
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
    ],
    scripts=[
        'scripts/ljon'
    ],
    packages=['ljon'],
    zip_safe=False,
    include_package_date=True,
    platforms='any'
)
