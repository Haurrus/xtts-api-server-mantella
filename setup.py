from setuptools import setup, find_packages

setup(
    name='xtts_api_server',
    version='0.1.0',
    description='Mantella XTTS API Server',
    author='xyz',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'PyAudio==0.2.14',
        'requests==2.31.0',
        'pyttsx3==2.90',
        'stream2sentence==0.2.2',
        'fastapi>=0.104.1',
        'loguru',
        'pydantic==2.9.2',
        'pydub',
        'python-dotenv',
        'torch==2.7',
        'torchaudio==2.7',
        'uvicorn',
        'cutlet',
        'fugashi[unidic-lite]',
        'coqui-tts==0.26.2',
        'transformers==4.51.3',
        'uuid',
        'spacy==3.7.4'
    ],
    entry_points={
        'console_scripts': [
            'xtts_api_server=xtts_api_server.__main__:run_server',
        ],
    },
)
