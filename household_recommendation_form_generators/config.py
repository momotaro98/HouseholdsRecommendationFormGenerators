import os


class Config:
    HOST = 'localhost'
    DBNAME = 'generator-db'
    USER = os.environ.get('GENE_USER')
    PASSWORD = os.environ.get('GENE_PASSWORD')
