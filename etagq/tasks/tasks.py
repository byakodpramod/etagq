from celery.task import task
from dockertask import docker_task
from subprocess import call,STDOUT
import requests
import json
import os, sys
import pandas as pd
from datetime import datetime
import logging
import re
import celeryconfig
from celeryconfig import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT
import sqlalchemy
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DataError
import json

#Default base directory 
basedir="/data/static/"

def parseFile(path, filetype):
    #TODO add required fields to the following lists
    animal_required_fields = []
    location_required_fields = []
    tag_required_fields = ["UUID", "TAG_ID", "TIMESTAMP"]

    df = pd.read_csv(path)
    file_fields = list(df.columns.str.upper())
    if filetype == "animals":
        required_fields = animal_required_fields
    if filetype == "locations":
        required_fields = location_required_fields
    if filetype == "tags":
        required_fields = tag_required_fields
    if not all([column in file_fields for column in required_fields]):
        return ("ERROR", "file does not have all required fields")

    #TODO upsert file data into databse


@task()
def etagDataUpload(local_file,request_data):
    
    """
    This task is associated with the etag-file-upload view.
    The view URl: /api/etag/file-upload/ . Provides a mechanism 
    to upload local file and runs this task. If you are unsure 
    you should go to the upload view to run task.
    etagDataUpload(local_file,request_data)
    args:
        local_file - local filepath (associated with etag-file-upload view
    """
    pg_db = {
    'drivername': 'postgres',
    'username': DB_USERNAME,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'host': DB_HOST,
    'port': DB_PORT
    }

    try:
	engine = create_engine(URL(**pg_db))
   	conn = engine.connect()
    except sqlalchemy.exc.OperationalError as e:
   	logging.error("Error with DB connection (from dspaceq/reports)\n{0}".format(e))
   	return("ERROR: Issue connecting to database, try again in a few minutes")
    
    test_query = """select * from readers;"""
    
    #try:
    results=[]
    res_items = conn.execute(text(test_query)).fetchall()
    #res_items = json.dumps(res_items)
    #loaded_item = json.loads(res_items)
    return json.loads(json.dumps([dict(r) for r in res_items]))
    #excepton sqlalchemy.exc.DataError as e:
    #return {"ERROR": "Could not process supplied dates"}
    
    
    #filetypes = ["animals", "locations", "tags"]
    #filetype = request_data.get('filetype', None)
    #if filetype not in filetypes:
    #    return ("ERROR", "filetype must be one of: animals, locations, tags")
    #parseFile(local_file, filetype)
    #TODO update return to provide results to user
    #return (local_file, request_data)
