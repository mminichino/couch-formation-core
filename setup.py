from setuptools import setup, find_packages
import couchformation

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='couchformation',
    version=couchformation.__version__,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/mminichino/couch-formation-core',
    license='Apache License 2.0',
    author='Michael Minichino',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'cloudmgr = couchformation.cli.cloudmgr:main',
            'dbdump = couchformation.cli.dbdump:main'
        ]
    },
    package_data={'couchformation': ['data/*']},
    install_requires=[
        "attrs==23.1.0",
        "boto3==1.34.17",
        "botocore==1.34.17",
        "cryptography>=41.0.7",
        "dnspython>=2.1.0",
        "google-api-core==2.11.1",
        "google-api-python-client==2.98.0",
        "google-auth==2.22.0",
        "google-auth-httplib2==0.1.0",
        "googleapis-common-protos==1.60.0",
        "google-cloud==0.34.0",
        "google-cloud-compute==1.14.0",
        "google-cloud-storage==2.10.0",
        "google-cloud-network-management==1.11.0",
        "Jinja2>=3.0.3",
        "passlib>=1.7.4",
        "pycryptodome>=3.12.0",
        "pytz>=2021.3",
        "pyvmomi>=8.0.0.1.1",
        "requests>=2.31.0",
        "urllib3>=1.26.18",
        "azure-common==1.1.28",
        "azure-core==1.29.6",
        "azure-cli-core==2.56.0",
        "azure-cli-command-modules-nspkg==2.0.3",
        "azure-mgmt-resource==23.0.1",
        "azure-identity==1.14.0",
        "azure.mgmt.network==25.1.0",
        "azure.mgmt.compute==30.1.0",
        "azure-mgmt-core==1.4.0",
        "azure.mgmt.storage==21.1.0",
        "azure.mgmt.subscription==3.1.1",
        "ply>=3.11",
        "pytest==7.4.0",
        "pytest-asyncio==0.21.1",
        "pytest-rerunfailures==12.0",
        "sqlite-utils~=3.11",
        "docker>=5.0.3",
        "paramiko==3.4.0",
        "overrides>=7.4.0",
        "bumpversion>=0.6.0",
        "PyYAML>=5.1",
        "cbcmgr>=2.1.8",
        "pyhostprep>=0.1.52",
        "rsa>=4.9"
    ],
    author_email='info@unix.us.com',
    description='Couchbase Cloud Automation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["couchbase", "devops", "automation"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
