#!/usr/bin/env python3

# easy-proxy.py
# Run the program as Sudo or Root

"""
Created by:
Soubhik Sen (sushruta19, <sensoubhik2001@gmail.com>)
Jalpaiguri Government Engineering College
06/05/2022
"""
"""
The following config_files will be modified -
1) /etc/apt/apt.conf
2) /etc/environment
3) /etc/bash.bashrc
These additional config_files will be modified if the user wants to -
1) ~/.gitconfig
2) ~/.pip/pip.conf
3) ~/.config/pip/pip.conf
4) /etc/pip.conf
"""

#Addresses of configuration files and their backups
# apt_ = r'/etc/apt/apt.conf'
# env_ = r'/etc/environment'
# bash_= r'/etc/bash.bashrc'
apt_ = r'./testing/apt.conf'
env_ = r'./testing/environment'
bash_= r'./testing/bash.bashrc'
config_files = [apt_,env_,bash_] #list of all config files
apt_backup = r'./.easy-proxy_backup/apt.conf.txt'
env_backup = r'./.easy-proxy_backup/environment.txt'
bash_backup = r'./.easy-proxy_backup/bash.bashrc.txt'
config_backups = [apt_backup, env_backup, bash_backup]  #list of all backup config_files

import os      #for creating and finding files and directories
import sys    
import shutil  #for copying files
import getpass #for password input

# main function handles user input
def main():
  print("Please run this program as Super User(sudo) or as root user\n")
  print("Enter 1: Set Proxy")
  print("Enter 2: Remove Proxy")
  print("Enter 3: View Proxy")
  print("Enter 4: Restore Previous version")
  print("Enter 5: Exit")
  choice = int(input("\nChoice(1/2/3/4/5) : "))
  
  if(choice == 1):
    # create backup
    create_backup()
    set_proxy()
    sub_choice = input("\nDo you want to set proxy to Git as well? (y/n) :")
    if(sub_choice == 'y' or sub_choice == 'Y'):
      set_proxy_git()
    sub_choice = input("Do you want to set proxy to pip? (y/n) :")
    if(sub_choice == 'y' or sub_choice == 'Y'):
      set_proxy_pip()
  elif(choice == 2):
    create_backup()
    for config_file in config_files:
      remove_proxy(config_file)
  elif(choice == 3):
    view_proxy()
  elif(choice == 4):
    restore_previous()
  else:
    sys.exit()
  print("\nDone!")

def set_proxy():
  proxy = input("\nEnter proxy : ")
  port = input("Enter Port : ")
  username = input("Enter Username (press enter if you don't have one) : ")
  password = getpass.getpass("Enter Password (press enter if you don't have one) : ")
  if proxy != '': 
    for config_file in config_files:
      remove_proxy(config_file)
      writeto_file(config_file,proxy,port,username,password)
    print("Proxy Set Successfully!")

def writeto_file(config_file, proxy='', port='', username='', password=''):
  with open(config_file,'a') as opened_file:
    if config_file == apt_:
      opened_file.write(
        'Acquire::http::proxy "http://{0}:{1}@{2}:{3}/";'
        .format(username, password,proxy,port)
      )
      opened_file.write(
        '\nAcquire::https::proxy "https://{0}:{1}@{2}:{3}/";'
        .format(username, password, proxy, port)
      )
      opened_file.write(
        '\nAcquire::ftp::proxy "ftp://{0}:{1}@{2}:{3}/";'
        .format(username, password, proxy, port)
      )
      opened_file.write(
        '\nAcquire::socks::proxy "socks://{0}:{1}@{2}:{3}/";'
        .format(username, password, proxy, port)
      )
    elif config_file == env_:
      opened_file.write(
        'http_proxy="http://{0}:{1}@{2}:{3}/"'
        .format(username, password,proxy,port)
      )
      opened_file.write(
        '\nhttps_proxy="https://{0}:{1}@{2}:{3}/"'
        .format(username, password,proxy,port)
      )
      opened_file.write(
        '\nftp_proxy="ftp://{0}:{1}@{2}:{3}/"'
        .format(username, password,proxy,port)
      )
      opened_file.write(
        '\nsocks_proxy="socks://{0}:{1}@{2}:{3}/"'
        .format(username, password,proxy,port)
      )
    elif config_file == bash_:
      opened_file.write(
        'export http_proxy="http://{0}:{1}@{2}:{3}/"'
        .format(username, password,proxy,port)
      )
      opened_file.write(
        '\nexport https_proxy="http://{0}:{1}@{2}:{3}/"'
        .format(username, password,proxy,port)
      )
      opened_file.write(
        '\nexport ftp_proxy="ftp://{0}:{1}@{2}:{3}/"'
        .format(username, password,proxy,port)
      )
      opened_file.write(
        '\nexport socks_proxy="socks://{0}:{1}@{2}:{3}/"'
        .format(username, password,proxy,port)
      )

def remove_proxy(config_file):
  if os.path.isfile(config_file):
    #copies file to a list of line
    with open(config_file,"r") as opened_file:
      lines = opened_file.readlines()

    #writing lines to the file
    with open(config_file,"w") as opened_file:
      for line in lines:
        #lines containing proxy will not be written
        if r'http://' not in line and r'https://' not in line and r'ftp://' not in line and 'socks://' not in line :
          opened_file.write(line)
  
def create_backup():
  if not os.path.isdir(r'./.easy-proxy_backup'):
    os.makedirs(r'./.easy-proxy_backup')
  for i in range(len(config_files)):
    if os.path.isfile(config_files[i]):
      shutil.copy(config_files[i],config_backups[i])
       
def restore_previous():
  #if backup exists
  if os.path.isdir(r'./.easy-proxy_backup'):
    for i in range(len(config_backups)):
      if os.path.isfile(config_backups[i]):
        shutil.copy(config_backups[i],config_files[i])
    print('Successfully restored previous version of configuration files.')
  else: #if backup doesn't exist
    print('No backups found!')

def view_proxy():
  with open(bash_,"r") as opened_file:
    # config file copied to list of lines(strings)
    lines=opened_file.readlines()
    proxy=''
    # Going through each line
    for line in lines:
      if 'http://' in line or 'https://' in line:
        proxy = line[line.rfind('@')+1 : line.rfind(':')]
        if proxy != '':
          print('\nHTTP Proxy\t: {0}'.format(proxy))
          port = line.split('@')[1].split(':')[1].split('/')[0]
          print('Port\t\t: {0}'.format(port))
          username = line.split('://')[1].split(':')[0]
          print('Username\t: {0}'.format(username))
          print('Password\t: '+ line.split(':')[2].split('@')[0])
        break
    if proxy == '':
      print('\nNo Proxy Found!')
    
if __name__ == "__main__":
  main()

"""
gsettings list-recursively | grep 'proxy'
org.gnome.system.proxy.ftp port 0
org.gnome.system.proxy.ftp host ''
org.gnome.system.proxy.socks port 0
org.gnome.system.proxy.socks host ''
org.gnome.system.proxy ignore-hosts ['localhost', '127.0.0.0/8', '::1']
org.gnome.system.proxy use-same-proxy true
org.gnome.system.proxy mode 'manual'
org.gnome.system.proxy autoconfig-url ''
org.gnome.system.proxy.http use-authentication false
org.gnome.system.proxy.http enabled false
org.gnome.system.proxy.http authentication-password ''
org.gnome.system.proxy.http port 8080
org.gnome.system.proxy.http host '172.16.102.28'
org.gnome.system.proxy.http authentication-user ''
com.gexperts.Tilix.Settings set-proxy-env true
org.gnome.evolution.shell.network-config use-http-proxy false
org.gnome.evolution.shell.network-config proxy-type 0
org.gnome.system.proxy.https port 8080
org.gnome.system.proxy.https host '172.16.102.28'
"""