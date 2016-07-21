<font color=blue>**Func:** 
>This project is creating a multi-thread crawling spider

**Py-files:**
>**run_main.py**   :  this file is the execute-file of the project

>**mini_spider.py** :  this file is to start multi crawling-threads

>**config_args.py** :  this file is to load configurations from spider.conf

>**Url.py**        :  this file is the class for url

>**crawl_thread.py**:  this file is a unit of crawling-thread

>**html_parse.py**  :  this file is a class for parsing html to extract urls

>**downloader.py**  :  this file is a class for downloading a page
>**log.py**        :  this file is used for logging

**Cfg-files:**
>**urls**          :  this file save seed-urls (depth - 0)

>**spider.conf**  :  this file save normal configurations for crawling

**Dirs:**
>**log**           : this dir is used for saving log-files

>**output**        : this dir is used for saving Url-page 

>**test**          : this dir contains all unittest-py

**How to run:**
>1: change into this dir
 
>2: run 
```python run_main.py -c spider.conf``` or ```python run_main.py``` <br>

