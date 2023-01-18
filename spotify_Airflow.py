import pymongo
import logging as logger
import pandas as pd
import requests
import json
from matplotlib import pyplot as plt
import seaborn as sns
import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'me',
    'start_date': datetime(2022, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('spotify_data_pipeline', default_args=default_args, schedule_interval='0 0 * * *')

logger.basicConfig(filename = 'AuditLogger.log',
                 filemode = 'w',
                  level = logger.INFO,
                  format = '%(asctime)s -%(levelname)s -%(message)s'
                 )

def spotify_data_pipeline():
    # Connect to MongoDB
    connection_string = "mongodb+srv://<PASSWORD>@spotifypipeline.lpaenzh.mongodb.net/test"
    client = pymongo.MongoClient(connection_string)

    # Isolate the database 'mydb' which will be used to store Spotify data
    db = client.mydb

    # Creating a Spotify collection
    collection = db.spotify_songs

    USER_ID = '31mqqbbqlvjqnibevcyrqpnitxga20'
    TOKEN = 'BQBDUzKVGjv1GeUdtrl4PUvyYGIj6GZ8uyuhABh2WFBG_pB8LXvxAACIvKMeOHSmcRLq4ZzlRkLjE9FTwlnM_JyT-gvCrz19V_n32G8clrP-sj-VIBZnWcoOVv7tZBNMx7FOZavSATSbWppZXo6KQ0CD-ei6G4CydU3j7OLJ0wTFfw6gGuy7S9p2yu35PBYIm66UIw0W'

    headers = dict([("Accept", "application/json"),
        ("Content-Type", "application/json"),
        ("Authorization", "Bearer {token}".format(token = TOKEN))])

    today = datetime.datetime.now()
    last_15_days = today - datetime.timedelta(days=15)
    last_15_days_unix_timestamp = int(last_15_days.timestamp()) * 1000
    last_15_days_unix_timestamp 
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=last_15_days_unix_timestamp), headers=headers)
    try:
        logger.info('+' * 35)
        logger.info('Making HTTP Request to Spotify API')
        r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=last_15_days_unix_timestamp), headers=headers)
        if ('401' in str(r) == True):
            raise Exception('HTTP 401 Unathorized Error')
    except Exception as e:
        logger.error('{}'.format(e))
        
    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    for song in data['items']:
    song_names.append(song['track']['name'])
    artist_names.append(song['track']['artists'][0]['name'])
    played_at_list.append(song['played_at'][0:10])
    
    song_dict = {
      'song_name': song_names,
      'artist_name': artist_names,
      'played_at': played_at_list
    }
    
  songs_df = pd.DataFrame(song_dict, columns=['song_name', 'artist_name', 'played_at'])

  #tranforming and manipulation data
  songs_df['played_at'] = pd.to_datetime(songs_df['played_at']).dt.strftime('%d/%m/%y')
  songs_df['song_name'] = songs_df['song_name'].astype('str')
  songs_df['artist_name'] = songs_df['artist_name'].astype('str')
  songs_df

  #upload and storing data to MongoDB
  db.spotify_songs.insert_many(songs_df.to_dict('records'))
  songs_df['identify'] = 1
  songs_df = songs_df.drop(['artist_name', 'played_at'], axis = 1)
  songs_df = songs_df.groupby('song_name').size()

  #data analysis using matplotlib and seaborn
  plt.figure(figsize=(15,8))
  sns.barplot(y = songs_df.index, x =songs_df.values)
        
        
spotify_data_pipeline_task = PythonOperator(
    task_id='spotify_data_pipeline',
    python_callable=spotify_data_pipeline,
    dag=dag)
    
    
spotify_data_pipeline_task
