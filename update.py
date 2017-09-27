# Author: Sun Yufei

import urllib.request
import os
import shutil

HOSTS_URL = 'https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts'

LOCAL_PATH = os.environ['windir'] + '\\System32\\drivers\\etc\\hosts'


def main():
    '''Main Function'''
    # Download hosts file
    if(os.path.exists('hosts')):
        os.remove('hosts')
    try:
        urllib.request.urlretrieve(HOSTS_URL, 'hosts')
    except Exception:
        print('网络连接失败')
    # Backup old hosts file
    try:
        if(os.path.exists(LOCAL_PATH + '.bak')):
            os.remove(LOCAL_PATH)
        else:
            shutil.copyfile(LOCAL_PATH, LOCAL_PATH + '.bak')
        # Move new file to system
        shutil.move('hosts', LOCAL_PATH)
        # Update dns cache
        os.system('ipconfig /flushdns')
    except Exception:
        print('请使用管理员权限运行')


if __name__ == '__main__':
    main()
