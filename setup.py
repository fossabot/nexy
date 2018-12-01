from setuptools import setup, find_packages

setup(
    name='nexy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3',
    install_requires=[
        'Click',
        'urllib3',
        'certifi'
    ],
    entry_points='''
        [console_scripts]
        nexy=nexy.nexy:main
    '''
)
