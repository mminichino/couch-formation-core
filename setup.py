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
    setup_requires=['wheel'],
    entry_points={
        'console_scripts': [
            'cloudmgr = couchformation.cli.cloudmgr:main',
            'dbdump = couchformation.cli.dbdump:main'
        ]
    },
    package_data={'couchformation': ['data/*']},
    install_requires=[
        "attrs==23.1.0",
        "boto3>=1.34.17",
        "botocore>=1.34.17",
        "cryptography>=42.0.7",
        "dnspython>=2.1.0",
        "google-api-core>=2.4.0",
        "google-api-python-client>=2.34.0",
        "google-auth>=2.3.3",
        "google-auth-httplib2>=0.1.0",
        "googleapis-common-protos>=1.54.0",
        "google-cloud>=0.34.0",
        "google-cloud-compute>=1.6.1",
        "google-cloud-storage>=2.10.0",
        "google-cloud-dns>=0.35.0",
        "google-cloud-network-management>=1.5.4",
        "Jinja2>=3.0.0",
        "passlib>=1.7.4",
        "pycryptodome>=3.20.0",
        "pytz>=2021.3",
        "pyvmomi>=8.0.0.1.1",
        "requests>=2.31.0",
        "urllib3>=1.26.16",
        "azure-common>=1.1.28",
        "azure-core>=1.26.1",
        "azure-mgmt-resource>=22.0.0",
        "azure-identity>=1.12.0",
        "azure-mgmt-network>=25.3.0",
        "azure-mgmt-compute>=31.0.0",
        "azure-mgmt-core>=1.3.2",
        "azure-mgmt-dns>=8.1.0",
        "azure-mgmt-privatedns>=1.1.0",
        "ply>=3.11",
        "sqlite-utils~=3.11",
        "docker>=5.0.3",
        "paramiko>=3.4.0",
        "overrides>=7.4.0",
        "PyYAML>=5.1",
        "rsa>=4.9",
        "pywinrm>=0.4.3",
        "aiohttp>=3.9.3",
        "python-certifi-win32>=1.6.1",
        "certifi>=2023.5.7",
        "pyhostprep>=1.0.10",
        "psutil>=5.9.5",
        "six>=1.16.0"
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
