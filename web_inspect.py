import sys
import random
import subprocess
import platform

from rich import print as printc
import requests
from bs4 import BeautifulSoup as bsoup, Comment

class WebInspect:
    def __init__(self, url, follow_redirects):
        if url.startswith('http'):
            self.origin_url = url[:-1] if url.endswith('/')  else url
            self.redirected_url = ""
            try:
                if follow_redirects:
                    redirected_url = requests.get(url, headers={'User-agent': self.get_user_agent(), 'Referer': '/'.join(url.split('/')[:3])}, allow_redirects=True).url
                    self.redirected_url = redirected_url[:-1] if redirected_url.endswith('/')  else redirected_url
                    if self.redirected_url and self.redirected_url != self.origin_url:
                        self.base_url = '/'.join(self.redirected_url.split('/')[:3])
                        command = ['curl','-A', 'Mozilla/5.0', '-e', self.base_url, '-s', self.redirected_url]
                        self.headers = {'User-agent': self.get_user_agent(), 'Referer': self.base_url}
                else:
                    self.base_url =  '/'.join(self.origin_url.split('/')[:3])
                    command = ['curl','-A', 'Mozilla/5.0', '-e', self.base_url, '-s', self.origin_url]
                    self.headers = {'User-agent': self.get_user_agent(), 'Referer': self.base_url}
                self.response = subprocess.check_output(command, universal_newlines=True)
                self.soup = bsoup(self.response, 'html.parser')
            except (subprocess.CalledProcessError, requests.exceptions.ConnectionError) as e:
                printc("[red3][-][/red3] An error occured!")
                printc(f"[gold1][!][/gold1] Here are some recommendations to fix the issue!")
                printc(f"[gold1][1][/gold1] Make sure you are connected to the Internet!")
                printc(f"[gold1][2][/gold1] Make sure that {url} is correct!")
                printc(f"[gold1][3][/gold1] Make sure that the protocol (http[s]) specified is correct!")
                printc(f"\n[red3][-][/red3] If the error is still occuring, thanks to report it at https://github.com/0liverFlow/TheWebInspector/issues!")           
                printc(f"[red3][-][/red3] For that, thanks to report the issue using the error description below ↓ ")
                sys.exit(printc(f"{e}"))
        else:
            sys.exit(printc("[red1 b][-][/red1 b] Incorrect URL format (ex: http[s]://example.com"))

    @staticmethod
    def get_running_os():
        return platform.platform().split('-')[0]

    @staticmethod   
    def is_installed(program, running_os):
        if "linux" in running_os.lower() or "macos" in running_os.lower():
            try:
                subprocess.check_output(["which", program])
                return True
            except subprocess.CalledProcessError:
                return False
        elif "windows" in running_os.lower():
            try:
                subprocess.check_output(["where", program])
                return True
            except subprocess.CalledProcessError:
                return False
        else:
           return None

    @staticmethod
    def get_user_agent() -> str:
        # Generate a random user-agent
        with open('db/user_agents.db') as f:
            user_agents = f.readlines()
            return random.choice(user_agents)[:-1]

    @staticmethod    
    def determine_elapsed_time(start_time, end_time):
        elapsed_time = end_time - start_time
        hours = minutes = 0
        seconds = elapsed_time
        if elapsed_time >= 3600 :
            hours = elapsed_time // 3600
            elapsed_time = elapsed_time % 3600 #elapsed_time - (hours * 3600)
        if elapsed_time >= 60 :
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
        return hours, minutes, seconds

    @staticmethod
    def format_time(hours, minutes, seconds):
        #Set hour.s format
        time_format=str() if not hours else str(hours) + 'h:'
        #Set minute format 
        time_format += str(minutes) + 'min:' if minutes else ''        
        return time_format + str(seconds)[:5] + 's'

    def get_language(self):
        # Returns the language used by the website
        try:
            webpage_language = self.soup.find('html')['lang']
            self.language = webpage_language
        except KeyError:
            self.language = "N/A"

    def get_title(self):
        try:
            webpage_title = self.soup.find('head').find('title').string
            self.title = webpage_title
        except AttributeError:
            self.title = "N/A"
    
    def get_comments(self):
        webpage_comments = self.soup.find_all(string=lambda text: isinstance(text, Comment))
        if len(webpage_comments):
            self.comments = webpage_comments
        else:
            self.comments = "N/A"
    
    def get_meta_tags(self):
        webpage_meta_tags = self.soup.find('head').find_all("meta")
        if len(webpage_meta_tags):
            self.meta_tags = webpage_meta_tags
        else:
            self.meta_tags = "N/A"
    
    def get_inputs(self):
        webpage_text_inputs = self.soup.find_all("input", type="text")
        webpage_password_inputs = self.soup.find_all("input", type="password")
        webpage_file_inputs = self.soup.find_all("input", type="file")
        webpage_email_inputs = self.soup.find_all("input", type="email")
        webpage_hidden_inputs = self.soup.find_all("input", type="hidden")
        webpage_search_inputs = self.soup.find_all("input", type="search")
        if len(webpage_text_inputs):
            self.text_inputs = webpage_text_inputs
        else:
            self.text_inputs = "N/A"
        if len(webpage_password_inputs):
            self.password_inputs = webpage_password_inputs
        else:
            self.password_inputs = "N/A"
        if len(webpage_file_inputs):
            self.file_inputs = webpage_file_inputs
        else:
            self.file_inputs = "N/A"
        if len(webpage_search_inputs):
            self.search_inputs = list(set(webpage_search_inputs))
        else:
            self.search_inputs = "N/A"
        if len(webpage_email_inputs):
            self.email_inputs = webpage_email_inputs
        else:
            self.email_inputs = "N/A"
        if len(webpage_hidden_inputs):
            self.hidden_inputs = list(set(webpage_hidden_inputs))
        else:
            self.hidden_inputs = "N/A"
    
    def get_display_none_tags(self):
        display_none_tags = self.soup.find_all(style=lambda style_attribute: style_attribute and 'display:none' in style_attribute)
        if len(display_none_tags):
            self.display_none = display_none_tags
        else:
            self.display_none = "N/A"

    def get_forms(self):
        forms = self.soup.find_all("form")
        if len(forms):
            self.forms = forms
        else:
            self.forms = "N/A"
    
    def get_allowed_methods(self, target_url):
        allowed_methods = requests.options(target_url, headers=self.headers, allow_redirects=False)
        if allowed_methods.status_code == 200:
            try:
                if allowed_methods.headers["Allow"]:
                    self.allowed_methods = allowed_methods.headers["Allow"]
                else:
                    self.allowed_methods = "N/A"
            except KeyError:
                self.allowed_methods = "N/A"
        else:
            self.allowed_methods = "N/A"
    
    def check_secured_http_response_headers(self, target_url):
        secured_http_response_headers = [
            "Content-Security-Policy",
            "X-XSS-Protection",
            "X-Frame-Options",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Feature-Policy"
        ]
        self.unset_secured_http_response_headers = list()
        self.juicy_headers = dict()
        response = requests.get(target_url, headers=self.headers, allow_redirects=False)
        if response.status_code == 200:
            http_response_headers = response.headers
            for secure_http_response_header in secured_http_response_headers:
                if secure_http_response_header not in http_response_headers:
                    self.unset_secured_http_response_headers.append(secure_http_response_header)

            juicy_headers = ["Server", "X-Powered-By"]
            for http_response_header in http_response_headers:
                if http_response_header in juicy_headers:
                    self.juicy_headers[http_response_header] = http_response_headers[http_response_header]
    
    def get_robots_txt(self):
        response_robots_txt = requests.get(self.base_url + '/robots.txt', headers=self.headers, allow_redirects=False)
        if response_robots_txt.status_code == 200:
            response_robots_txt_rules = response_robots_txt.text.split("\n")
            if len(response_robots_txt_rules):
                self.robots_txt = response_robots_txt_rules
            else:
                self.robots_txt="Robots.txt file empty!"
        else:
            self.robots_txt = "N/A"

    def get_sitemap_xml(self):
        response_sitemap_xml = requests.get(self.base_url + '/sitemap.xml', headers=self.headers, allow_redirects=False)
        if response_sitemap_xml.status_code == 200:
            response_sitemap_xml_content = response_sitemap_xml.text.split()
            if len(response_sitemap_xml_content):
                self.sitemap_xml = response_sitemap_xml_content
            else:
                self.sitemap_xml="Sitemap file empty!"
        else:
            self.sitemap_xml = "N/A"

    def get_phpinfo(self):
        # Checking phpinfo file
        phpinfo_url = self.base_url + '/phpinfo.php'
        phpinfo_response = requests.get(phpinfo_url, headers=self.headers, allow_redirects=False)
        if phpinfo_response.status_code == 200:
            self.phpinfo = phpinfo_response.url
        else:
            self.phpinfo = "N/A"
           
    def get_cgidir(self):
        default_cgidirs = ['/admin/cgi-bin', '/cgi-bin/admin', '/cgi-bin']
        for cgidir in default_cgidirs:
            cgidir_url = self.base_url + cgidir
            cgidir_response = requests.get(cgidir_url, headers=self.headers, allow_redirects=False)
            if cgidir_response.status_code == 200:
                self.cgidir = cgidir_response.url
                break
        else:
            self.cgidir = "N/A"
