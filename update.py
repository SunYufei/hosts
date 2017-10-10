"""
    Date: 2017/10/10
"""
import re
import urllib.request
import os
import zipfile
import shutil
import time

HTML = 'https://laod.cn/hosts/2017-google-hosts.html'
LOCAL_PATH = os.environ['windir'] + '\\System32\\drivers\\etc\\hosts'
DOWN_PAGE = 'https://iiio.io/download/'


def download_file():
    """ Download Hosts File """
    req = urllib.request.urlopen(DOWN_PAGE)
    html = req.read().decode('UTF-8')
    dates = re.findall(re.compile(r'<a href=".*">([0-9]*/)</a>'), html)
    date = dates[len(dates) - 1]
    req = urllib.request.urlopen(DOWN_PAGE + date)
    html = req.read().decode('UTF-8')
    file_link = re.search(re.compile(r'<a href="(.*)">Windows系列跟苹果系列.zip</a>'), html).group(1)
    urllib.request.urlretrieve(DOWN_PAGE + date + file_link, 'hosts.zip')


def get_password():
    """ Get zip file password """
    req = urllib.request.urlopen(HTML)
    html = req.read().decode('UTF-8')
    return re.search(re.compile(r'解压密码：(.*)</span>'), html).group(1)


def move_file():
    """ Replace current hosts file """
    zip_file = zipfile.ZipFile('hosts.zip')
    zip_file.extractall(pwd=bytes(get_password(), encoding='UTF-8'))
    zip_file.close()
    os.remove('hosts.zip')
    try:
        # Backup hosts file
        if os.path.exists(LOCAL_PATH + '.bak'):
            os.remove(LOCAL_PATH)
        else:
            shutil.copyfile(LOCAL_PATH, LOCAL_PATH + '.bak')
        # Move new file to system
        shutil.move('hosts', LOCAL_PATH)
        # Update dns cache
        os.system('ipconfig /flushdns')
    except Exception:
        print('请使用管理员权限运行')


def main():
    """ Main Function """
    download_file()
    move_file()
    time.sleep(2)


if __name__ == '__main__':
    main()
