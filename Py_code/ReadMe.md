###Func: 
* This project is creating a multi-thread crawling spider

###Py-files:
* run_main.py &ensp;  　　:  this file is the execute-file of the project
* miniSpider.py 　　:  this file is to start multi crawling-threads
* configArgs.py 　　:  this file is to load configurations from spider.conf
* Url.py　　　　　&ensp;&ensp;&ensp;:  this file is the class for url
* crawlThread.py　&ensp;&ensp;:  this file is a unit of crawling-thread
* htmlParse.py　　&ensp;&ensp;:  this file is a class for parsing html to extract urls
* log.py　　　　　&ensp;&ensp;&ensp;:  this file is used for logging

###Cfg-files:
* urls　　　　&ensp;:  this file save seed-urls (depth - 0)
 15     
* spider.conf　:  this file save normal configurations for crawling

###Dirs:
 * log　　&ensp;　: this dir is used for saving log-files
 * output　&ensp;&ensp;&ensp;: this dir is used for saving Url-page
 * test　　　: this dir contains all unittest-py
  21
   
### How to run:
  * change into this dir
  * run 'python run_main.py -c spider.conf' or 'python run_main.py'
