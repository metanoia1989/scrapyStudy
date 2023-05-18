#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import psycopg
from psycopg.rows import dict_row 
from . import config

class db_query:
    """Psycopg3 wrapper class"""
    
    def __init__(self):
        self.conn = psycopg.connect(config.POSTGRES_URI, row_factory=dict_row)
 
    def queryAll(self, sql, parameters=None):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, parameters or ())
            return cursor.fetchall()

    def queryOne(self, sql, parameters=None):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, parameters or ())
            return cursor.fetchone()

    def execute(self, sql, parameters=None):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, parameters or ())
            self.conn.commit()

    def close(self):
        self.conn.close()