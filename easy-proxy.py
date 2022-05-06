#!/usr/bin/env python

"""
Created by:
Soubhik Sen (sushruta19, <sensoubhik2001@gmail.com>)
Jalpaiguri Government Engineering College
06/05/2022
"""
import os
import sys

def main():
  print("Please run this program as Super User(sudo) or as root user\n")
  print("Enter 1: Set Proxy")
  print("Enter 2: Remove Proxy")
  print("Enter 3: View Proxy")
  print("Enter 4: Restore Default")
  print("Enter 5: Exit")
  choice = int(input("Choice(1/2/3/4/5) : "))
  
  if(choice == 1):
    set_proxy()
    sub_choice = input("Do you want to set proxy to Git as well? (y/n) :")
    if(sub_choice == 'y' or sub_choice == 'Y'):
      set_proxy_git()
    sub_choice = input("Do you want to set proxy to pip? (y/n) :")
    if(sub_choice == 'y' or sub_choice == 'Y'):
      set_proxy_pip()
  elif(choice == 2):
    remove_proxy()
  elif(choice == 3):
    view_proxy()
  elif(choice == 4):
    restore_default()
  else:
    sys.exit()
  print("Exit!")

"""
The following files will be modified -
1) /etc/apt/apt.conf
2) /etc/environment
3) /etc/bash.bashrc

These additional files will be modified if the user wants to -
1) ~/.gitconfig
2) ~/.pip/pip.conf
3) ~/.config/pip/pip.conf
4) /etc/pip.conf
"""
apt_ = r'/etc/apt/apt.conf'
env_ = r'/etc/environment'
bash_= r'/etc/bash.bashrc'
files = [apt_,env_,bash_]

def set_proxy():
  proxy = input("Enter proxy : ")
  port = input("Enter Port : ")
  username = input("Enter Username (press enter if you don't have one) : ")
  password = input("Enter Password (press enter if you don't have one) : ")
  for file in files:
    create_backup(file)
    if is_proxy_present(file):
      remove_proxy(file)
  writeto_apt(proxy,port,username,password)
  writeto_env(proxy,port,username,password)
  writeto_bash(proxy,port,username,password)


