This a Spotify data pipeline that retrieves the user's recently played songs from the Spotify API, and stores the data in a MongoDB database. The script uses the Python requests library to make an HTTP GET request to the Spotify API, and uses the JSON response to extract the song names, artist names, and played at timestamps. It then creates a pandas DataFrame of the data and stores it in a MongoDB collection called "spotify_songs". The script also includes logging and error handling, and uses a config file to store the user's ID and token for authentication.


Tools used for this projects

* Spotify API
* Python
* MongoDb
* Seaborn
* Matplotlib
* Apache Airflow


Project Architecture

![spotify_achticture](https://user-images.githubusercontent.com/69304233/211586241-3d879985-6499-43bd-969c-6654bd578b78.png)
