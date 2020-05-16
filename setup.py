from setuptools import setup, find_packages

setup(
    name='Edator',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='A python package that runs exploratory data analysis for users',
    long_description=open('README.txt').read(),
    install_requires=['os', 'pandas', 'matplotlib', 'seaborn', 'PySimpleGUI', 'sklearn', 'numpy', 'scipy', 'statsmodels', 'itertools'],
    url='https://https://github.com/kianweelee/Edator',
    download_url= 'https://github.com/kianweelee/Edator/archive/0.1.tar.gz',
    author='Lee Kian Wee',
    author_email='leekianwee@outlook.com'
)