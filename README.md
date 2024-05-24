Simple Tile Map Server
=======================

Simple tile map server is a server that stores and serves raster map tiles. Map tiles can be uploaded to the server or provided by a third-party tile map provider.

Disclaimer
------------
The author of the app is not responsible for any damages. Check the Terms of Service of the third-party tile provider to prevent any issues.  

How to use
-----------
- Install dependencies using `pip install -r requirements.txt`
- Rename `app.cfg.sample` to `app.cfg` and configure the app
  - Generate a secret key for Flask ([reference](https://stackoverflow.com/questions/34902378/where-do-i-get-secret-key-for-flask))
  - Configure ProxyFix if needed ([reference](https://werkzeug.palletsprojects.com/en/2.0.x/middleware/proxy_fix/))
- Run the server using `python3 tilemap-server.py` or `gunicorn 'tilemap-server:app'` when using the Gunicorn WSGI server
