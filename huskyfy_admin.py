"""
huskyfy_admin.py

Provides a GUI for administrative actions for the huskyfy database

Requirements:
 - Python 3.4+

Usage:
    python huskyfy_admin.py
"""

from admin.application import Application
from pymongo import MongoClient


MONGO_URL = "mongodb://matt:riley@ds053794.mongolab.com:53794/huskyfy"

client = MongoClient(MONGO_URL)
db = client.huskyfy

if __name__ == "__main__":
    app = Application(db)
