#!/usr/bin/python3

from cryptography.fernet import Fernet
import cryptography
import os

key = None
fernet = None

try:
  if os.stat("fernet-key.key").st_size == 0:
    raise Exception("No Key")
  
  key_file = open("fernet-key.key", "r")
  key = bytes(key_file.read(), encoding="ascii")
  # print(base64_encoded_bytes)
  fernet = Fernet(key)
  key_file.close()
except:
  print("Error to fernet key: invalid token")
  confirm = input("You need to clear all the data, it can not be decrypt. Confirm to clear data (y/n)").lower()
  if confirm == "y":
    file = open("password.txt", "w")
    file.close()
    key = Fernet.generate_key()
    fernet = Fernet(key)
    key_file = open("fernet-key.key", "w")
    # print(key.decode())
    key_file.write(key.decode())
    key_file.close()
  else:
    quit()


def run():
  while True:
    mode = input("\nType a mode for view or add usernames and passwords (view, add) press q to quit?\n: ").lower()

    if mode == "q":
      break

    if mode == "view":
      view()
    elif mode == "add":
      add()
    else:
      print("\n---- Please type the valid options. ----")

def view():
  with open("password.txt", "r") as f:
    print("\n-----------------------------\n")
    for line in f.readlines():
      data = line.rstrip()
      [application, username, encrypted] = data.split("|:|")
      password = fernet.decrypt(encrypted.encode(), ttl=None).decode()
      # print(username, password)
      format_string = f"\tapplication: {application}\n\tusername: {username}\n\tpassword: {password}"
      print(format_string)
      print("\n-----------------------------\n")

def add():
  application = input("Type a website domain or application name for the account: ")
  username = input("Type a username: ")
  password = input("Type a password: ")
  encrypted = fernet.encrypt(password.encode()).decode()
  # print(encrypted)

  with open("password.txt", "a") as f:
    format_string = f"{application}|:|{username}|:|{encrypted}\n"
    f.write(format_string)
  
  print("Account added!")

if __name__ == "__main__":
  run()