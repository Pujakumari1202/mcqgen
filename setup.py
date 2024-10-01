#for install the local package
from setuptools import find_packages,setup

#method
setup(
    name='mcqgenerator',  #all parameters
    version='0.0.1',
    author='puja_kumari',
    author_email='puja.kumari@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dorenv","PyPDF2"],
    packages=find_packages()
)

