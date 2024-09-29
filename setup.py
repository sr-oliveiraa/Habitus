from setuptools import setup, find_packages

setup(
    name='monitor_sistema',
    version='0.1',
    packages=find_packages(),  # Isso vai automaticamente encontrar o diretório 'monitor_sistema'
    install_requires=[
        'psutil',
        'GPUtil',
        'ping3',
        'speedtest-cli',
    ],
    entry_points={
        'console_scripts': [
            'monitor-sistema=monitor_sistema.cli:main',  # Certifique-se de que isso aponta para a função 'main' em cli.py
        ],
    },
)
