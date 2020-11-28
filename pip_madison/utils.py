import collections
from operator import itemgetter

import configparser
import os
import platform
import re
import sys
from pySystem import System
import bs4
import requests

from pip_madison._cli_util import os_to_re, pyversion_to_re
if len(sys.argv) > 1 and sys.argv[1] not in ["help","madison"]:
    sys.argv.insert(1,"madison")

def star_credentials_url(s):
    return re.sub("://([^/]*)@","://*****@",s)
def distinct_list(L):
    seen = set()
    return [i for i in L if i not in seen and not seen.add(i)]

def get_default_index_url():
    result = System().pip.install("-h")
    return re.search("\(default\s*([^\s\)]*)\)",result.split("\n  -i, --index-url")[1]).group(1)

def get_index_urls():
    result=System().pip.config.list()
    results = distinct_list(re.findall("index-url\s*='(.*)'\n",result))
    if "global.index-url=" not in result:
        default = get_default_index_url()
        results.append(default)
    return results



def get_extra_index_url(cfgPath=None):
    ## ON WINDOWS this file goes in C:\Users\<<USERNAME>>\AppData\Roaming\pip\pip.ini !!!!!
    ## ON Linux this file goes in /home/<<USERNAME>>/.config/pip/pip.conf !!!!!
    ## ON Mac $HOME/Library/Application Support/pip/pip.conf  **OR** $HOME/.config/pip/pip.conf
    #                                                                IFF folder pip is not in 'Application Support'
    if cfgPath is None:
        if platform.system() == "Windows":
            cfgPath = os.path.expanduser("~/AppData/Roaming/pip/pip.ini")
        elif platform.system() == "Linux":
            cfgPath = os.path.expanduser("~/.config/pip/pip.conf")
        elif platform.system() == "Darwin":
            cfgPath = os.path.expanduser("~/Library/Application Support/pip/pip.conf")
            if not os.path.exists(os.path.expanduser("~/Library/Application Support/pip")):
                cfgPath = os.path.expanduser("~/.config/pip/pip.conf")
    p = configparser.ConfigParser()
    p.read(cfgPath)
    return p['global'].get('extra-index-url')
def make_regex(package_name,py=None,os=None,endswith=".*"):
    endswith = endswith.replace(".", "\\.")
    pattern = "%s-(?P<ver>(?P<major>\d+)\.(?P<minor>\d+)\.?(?P<build>\d+)?)" % package_name.replace("_", "[-_]")
    endings = endswith.split("|")
    alt_endings = []
    if "\\.tar\\.gz" in endings:
        alt_endings.append("\\.tar\\.gz")
        endings.remove("\\.tar\\.gz")
    if "\\.zip" in endings:
        alt_endings.append("\\.zip")
        endings.remove("\\.zip")

    if len(endings):
        pattern2 = ".*-(?P<py>%s[^-]*?)" % pyversion_to_re(py)
        pattern2 += ".*-(?P<os>%s)" % os_to_re(os)
        pattern += "(?:%s)?" % pattern2
    return pattern + "(?P<ext>%s)" % endswith

def filename_parser_factory(packagename,py=None,os=None,endswith=".*"):
    regex = make_regex(packagename,py,os,endswith)
    def __inner(filename):
        match = re.match(regex,filename,re.I)
        # print("RE:",filename,regex)
        if not match:
            return None

        default_data = {"major":-1,"minor":-1,"build":-1,'os':'any','py':'any'}
        default_data.update(match.groupdict())
        ver_list = [int(-1 if x is None else x) for x in itemgetter("major","minor","build")(default_data)]
        return {"list": ver_list, 'package_name': packagename,
                   'ver': default_data.get('ver', "??????"),
                   'os': default_data['os'] or "any",
                   'py': default_data['py'] or "any",
                   'fname': filename,
                   'error': 'false'}
    return __inner
def get_available_versions_files_and_urls(package_url, py=None,os=None,endswith=".tar.gz"):
    endswith=endswith.replace(".","\\.")
    package_index, package_name = filter(None, package_url.rsplit("/", 2))
    mapper = filename_parser_factory(package_name,py,os,endswith)
    page = bs4.BeautifulSoup(requests.get(package_url).content, features="html.parser")
    def map_it(L):
        for a in L:
            result = mapper(a)
            if not result:
              continue
            result.update({'uri': a.attrs['href'],'index-url':package_index})
            yield result

    data = sorted(map_it(page.find_all("a")), key=lambda x: x['list'], reverse=True)
    return data

def get_latest_package_details(package_url,endswith=".tar.gz"):
    data = get_available_versions_files_and_urls(package_url,endswith)[0]
    if data:
        return data[0]

