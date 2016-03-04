## Google Play APKs Analysis

### Setup

* Clone from repo
    
    ```bash
    $ git clone https://github.com/deanboole/googleplay-api.git
    ```

* Create and activate virtual environment
    
    ```bash
    $ virtualenv googleplay-api
    $ cd googleplay-api
    $ source bin/activate
    ```

* Install require modules
    
    ```bash
    $ pip install -r requirements.txt
    ```

* Mongo DB Installation
    
    ```bash
    https://docs.mongodb.org/getting-started/shell/tutorial/install-mongodb-on-ubuntu/
    ```

* Create your dbpath
    
    ```bash
    $ mkdir -p ~/data/db
    ```

* Start mongod with
    
    ```bash
    $ mongod --dbpath ~/data/db
    ```

* Fill in infos
    
    ```bash
    dw_from_gplay/config.py
    dw_from_gplay/db/db.conf (see db.conf.example)
    dw_from_gplay/web.py
    ```

### How to use

* Download apks from googleplay
    ```bash
    $ bash dw_from_gplay/download_from_lists.sh
    ```

* Submit apks to virustotal
    ```bash
    $ python dw_from_gplay/vt.py
    ```

* Launch web interface to review results!
    ```bash
    $ python dw_from_gplay/web.py
    ```


