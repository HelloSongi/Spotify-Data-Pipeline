
![sportify](https://user-images.githubusercontent.com/69304233/213261140-0929b126-252c-418e-b144-cf2cc1335fd8.png)

- The script is a Airflow DAG that is scheduled to run every day at midnight and it uses the PythonOperator to run the function "spotify_data_pipeline" which pulls data from the Spotify API, logs the data, and inserts it into a MongoDB database.

- The script extracts certain information about each song and stores it in a dictionary, which is then converted into a Pandas Dataframe and added to the MongoDB collection.

- The script also logs any errors that may occur during the execution of the script using the python logging module, which can be used for debugging and troubleshooting purposes.

- Finally, Data analysis/Visualization is handled by the use of matplotlib and seaborn libraries


Tools used for this projects

* Spotify API
* Python
* MongoDb
* Seaborn
* Matplotlib
* Apache Airflow


Project Architecture


