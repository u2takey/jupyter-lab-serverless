"""
Setup module for the jupyter-lab-serverless
"""
import setuptools
from setupbase import (
    create_cmdclass, ensure_python, find_packages, get_version
    )

data_files_spec = [(
    'etc/jupyter/jupyter_notebook_config.d',
    'jupyter-config/jupyter_notebook_config.d',
    'jupyter-lab-serverless.json'
),]

cmdclass = create_cmdclass(data_files_spec=data_files_spec)

setup_dict = dict(
    name='jupyter-lab-serverless',
    version=get_version("jupyter-lab-serverless/_version.py"),
    description='Build And Run Serverless Functions in Jupyter Lab.',
    packages=find_packages(),
    cmdclass=cmdclass,
    author          = 'u2takey',
    author_email    = 'u2takey@gmail.com',
    url             = 'https://u2takey.github.com',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'JupyterLab', 'ServerLess'],
    python_requires = '>=3.6',
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'notebook'
    ],
    package_data={'jupyter-lab-serverless':['api/*']},
)

try:
    ensure_python(setup_dict["python_requires"].split(','))
except ValueError as e:
    raise  ValueError("{:s}, to use {} you must use python {} ".format(
                          e,
                          setup_dict["name"],
                          setup_dict["python_requires"])
                     )

setuptools.setup(**setup_dict)
