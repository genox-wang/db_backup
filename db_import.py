import zipfile
import time
import datetime
import re
import os
import sys,getopt

DB_HOST = 'localhost'  # mysql host
DB_USER = 'root'   # mysql user
DB_USER_PASSWORD = 'root'  # mysql password
BACKUP_PATH = '/Users/bill/backup/dbbackup/'  # 本地备份临时文件夹


def import_sql(date_format):
  DATETIME = date_format

  print_success("[MYSQL_IMPORT] CONFIG\nDB_HOST: {0}\nDB_USER: {1}\nDB_USER_PASSWORD: {2}\nBACKUP_PATH: {3}\n".format(DB_HOST, DB_USER, DB_USER_PASSWORD, BACKUP_PATH))
  print_warn("[MYSQL IMPORT] start import sql file by date {0}".format(DATETIME))


  TODAYTMPPATH = os.path.join(BACKUP_PATH, DATETIME)
  zippath = '{0}.zip'.format(TODAYTMPPATH)

  print_warn("[MYSQL IMPORT] unzip file: {0}".format(zippath))
  try:
    z = zipfile.ZipFile(zippath, "r")

    z.extractall(BACKUP_PATH)

    for filename in z.namelist():
      db = re.split('[/.]', filename)[1]
      sql_path = os.path.join(BACKUP_PATH, filename)
      sqlcmd = 'mysql -h {0} -u {1} -p{2} {3} < {4}'.format(DB_HOST, DB_USER, DB_USER_PASSWORD, db, sql_path)
      print_warn("[MYSQL IMPORT] start import: {0}".format(sqlcmd))
      os.system(sqlcmd)
      print_success("[MYSQL IMPORT] complete import: {0}".format(sql_path))
      print_error("[MYSQL IMPORT] remove file: {0}".format(sql_path))
      os.remove(sql_path)
    z.close()
  except IOError:
    print_error("{0} not found".format(zippath))
  pass


# Reset
SHELL_COLOR_OFF="\033[0m"       # Text Reset

# Regular Colors
SHELL_BLACK="\033[0;30m"        # Black
SHELL_RED="\033[0;31m"          # Red
SHELL_GREEN="\033[0;32m"        # Green
SHELL_YELLOW="\033[0;33m"       # Yellow
SHELL_BLUE="\033[0;34m"         # Blue
SHELL_PURPLE="\033[0;35m"       # Purple
SHELL_CYAN="\033[0;36m"         # Cyan
SHELL_WHITE="\033[0;37m"        # White

def print_info(str):
  print('{0}{1}{2}'.format(SHELL_BLUE, str, SHELL_COLOR_OFF))


def print_warn(str):
  print('{0}{1}{2}'.format(SHELL_YELLOW, str, SHELL_COLOR_OFF))

def print_error(str):
  print('{0}{1}{2}'.format(SHELL_RED, str, SHELL_COLOR_OFF))

def print_success(str):
  print('{0}{1}{2}'.format(SHELL_GREEN, str, SHELL_COLOR_OFF))


def main(argv):
  global DB_HOST,DB_USER,DB_USER_PASSWORD,DB_USER_PASSWORD,BACKUP_PATH
  DATETIME =  time.strftime('%y%m%d',time.localtime(time.time() - 24*60*60))
  try:
    opts, args = getopt.getopt(argv,"hs:u:p:d:t:")
  except getopt.GetoptError:
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print ('db_import.py -s <mysql host> -u <mysql user> -p <mysql password> -d <backup path -t <target date es. 171201>')
      sys.exit()
    elif opt == "-s":
      DB_HOST = arg
    elif opt in ("-u"):
      DB_USER = arg
    elif opt in ("-p"):
      DB_USER_PASSWORD = arg
    elif opt in ("-d"):
      BACKUP_PATH = arg
    elif opt in ("-t"):
      DATETIME = arg
  import_sql(DATETIME)
  pass

# print('[MYSQL BACKUP] del folder three days ago')
# folders = glob.glob('{0}*'.format(BACKUP_PATH))
# today = datetime.datetime.now()
# for item in folders:
#     try:
#         foldername = os.path.split(item)[1]
#         day = datetime.datetime.strptime(foldername, "%y%m%d")
#         diff = today - day
#         if diff.days >= 3:
#             shutil.rmtree(item)
#     except:
#         pass
#     
if __name__ == "__main__":
   main(sys.argv[1:])