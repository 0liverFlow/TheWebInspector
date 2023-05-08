<img width="1182" alt="image" src="https://user-images.githubusercontent.com/64969369/236709424-19a345c3-af3e-496a-9045-2e5294b956ad.png">

# TheWebInspector
[![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/) 
![Version 1.0](http://img.shields.io/badge/version-v1.0-orange.svg) ![License](https://img.shields.io/badge/license-MIT-red.svg) <img src="https://img.shields.io/badge/Maintained%3F-Yes-96c40f"> 

## Purpose
TheWebInspector is a Python script that analyzes a webpage's source code. It can be very useful during the HTTP protocol enumeration and provides information such as:
- The website's title and language
- The website's meta tags and comments
- The inputs (hidden inputs, text inputs, password inputs, search inputs, file inputs)
- Display none tags
- Forms

Furthermore, it performs certain file enumeration checking for files such as:
- robots.txt
- sitemap.xml
- phpinfo.php
- wp-login.php
- /admin/cgi-bin

Last but not least, it retrieves information about allowed HTTP methods and certain HTTP response headers such as **Server** and **X-Powered-By**.

## Disclaimer ⚠️
Usage of this script for attacking targets without prior mutual consent is illegal. I am not responsible for any misuse or damage caused by this program. Only use for educational purposes.

## Demonstration
[![asciicast](https://asciinema.org/a/uwTfdgW1o9niMVfKMKlGkE8Z3.svg)](https://asciinema.org/a/uwTfdgW1o9niMVfKMKlGkE8Z3)

## Installation & Usage
TheWebInspector is a cross platform script that works with python **3.x**.
```
git clone https://github.com/0liverFlow/TheWebInspector
cd ./TheWebInspector
pip3 install -r requirements.txt
```
Then you can run it
```
python3.x TheWebInspector.py -u url [--followredirects] [-v]
```
## Important Notes
1. You don't need administrator privileges to run this script.
2. By default, this script doesn't follow redirections. If you want to follow redirections, you need to specify the **--followredirects** option.
3. For more information, you can use the **-v** or **-vv** option.

## Contribution
1. If you noticed any bugs, report me  <a href="https://github.com/0liverFlow/TheWebInspector/issues">here</a> 
2. For any interesting idea, thanks to ping me at <a href="mailto:0liverFlow@proton.me">0liverFlow</a>
