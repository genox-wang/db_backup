# Import required python libraries
import os
import time
import datetime
import glob
import shutil
import zipfile
import sys,getopt


DB_TABLES_FILE = 'db_tables.txt'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'root'
TMP_PATH = '/Users/bill/backup/dbbackup/'  # 本地备份临时文件夹
CLEAN_TMP_COPLETED = False  # 备份完成删除临时文件

BACKUP_SERVER = 'root@106.14.148.86'  # 备份服务器用户id
BACKUP_PATH = '/root/backup/'  # 备份服务器备份目录

def mysql_backup(date_format):
  DATETIME = date_format
  TODAYTMPPATH = TMP_PATH + DATETIME

  print_success("[MYSQL_IMPORT] CONFIG \nDB_HOST: {0}\nDB_USER: {1}\nDB_USER_PASSWORD: {2}\nBACKUP_PATH: {3}\nDB_TABLE_FILE: {4}\nTMP_PATH: {5}\nCLEAN_TMP_COMPLETE: {6}\nBACKUP_SERVER: {7}\n".format(DB_HOST, DB_USER, DB_USER_PASSWORD, BACKUP_PATH, DB_TABLES_FILE, TMP_PATH, CLEAN_TMP_COPLETED, BACKUP_SERVER))
  
  print_warn("[MYSQL IMPORT] start backup sql by date {0}".format(DATETIME))

  print_info("[MYSQL BACKUP] creating backup folder")
  if not os.path.exists(TODAYTMPPATH):
    os.makedirs(TODAYTMPPATH)

  # Code for checking if you want to take single database backup or assinged multiple backups in DB_TABLES_FILE.
  print_info("[MYSQL BACKUP] checking for databases names file.")
  if os.path.exists(DB_TABLES_FILE):
    print_info("[MYSQL BACKUP] Databases file found...")
    print_info("[MYSQL BACKUP] Starting backup of all dbs listed in file " + DB_TABLES_FILE)

    in_file = open(DB_TABLES_FILE,"r")
    flength = len(in_file.readlines())
    in_file.close()
    p = 1
    dbfile = open(DB_TABLES_FILE,"r")

    dbs = []
    dumptables = {}

    curdb = ""

    while p <= flength:
      line = dbfile.readline()
      if line.startswith(" ") :
        table_name = line.strip()
        if "%y%m%d" in table_name:
          table_name = table_name.replace("%y%m%d", DATETIME)
        if curdb in dumptables:
          dumptables[curdb].append(table_name)
        else:
          dumptables[curdb] = [table_name]
      else:
        curdb = line[:-1]
        dbs.append(curdb)
      p = p + 1
      pass

    print_warn("[MYSQL BACKUP] Dbs prepare backup : {0} ".format(dbs))
    print_warn("[MYSQL BACKUP] Tables prepare backup : {0} ".format(dumptables))

    for db in dbs:
      if db in dumptables:
        for table in dumptables[db]:
          print_warn("[MYSQL BACKUP] start backup : {0}.{1} ".format(db,table))
          # dumpcmd = "mysqldump -h {0} -u {1} -p{2} {3} {4} > {5}/{6}.{7}.sql".format(DB_HOST, DB_USER, DB_USER_PASSWORD, db, table, TODAYTMPPATH, db, table)
          dumpcmd = "sudo docker exec {0} /usr/bin/mysqldump -u {1} -p{2} {3} {4} > {5}/{6}.{7}.sql".format(DB_HOST, DB_USER, DB_USER_PASSWORD, db, table, TODAYTMPPATH, db, table)
          status = os.system(dumpcmd)
          if status != 0:
            print_error("[MYSQL BACKUP] os.system status : {0}".format(status))
          else:
            print_success("[MYSQL BACKUP] complete backup : {0}.{1} ".format(db,table))
          
          
    dbfile.close()

    print_info("[MYSQL BACKUP] Your backups has been created in '" + TODAYTMPPATH + "' directory")

    zippath = '{0}.zip'.format(TODAYTMPPATH)

    print_warn("[MYSQL BACKUP] Zip directory {0} to {1}".format(TODAYTMPPATH, zippath))

    globpath = '{0}/*'.format(TODAYTMPPATH, DATETIME)
    files = glob.glob(globpath)
    f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
      f.write(file, '/{0}/'.format(DATETIME) + os.path.basename(file))
    f.close()
    print_error("[MYSQL BACKUP] Remove directory {0}".format(TODAYTMPPATH))
    shutil.rmtree(TODAYTMPPATH)

    print_warn("[MYSQL BACKUP] start rsyn copy to backup server")
    rsynccmd = 'rsync -avzP -e \'ssh\' {0} {1}:{2}'.format(zippath, BACKUP_SERVER, BACKUP_PATH)
    os.system(rsynccmd)
    print_success("[MYSQL BACKUP] complete rsyn copy to backup server")
    if CLEAN_TMP_COPLETED:
      print_error("[MYSQL BACKUP] Remove tmp zip {0}".format(zippath))
      os.remove(zippath)
  else:
    print_error("{0} not found".format(DB_TABLES_FILE))

  print_success("[MYSQL BACKUP] Backup script completed")
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

# Get PreDay date format
DATETIME =  time.strftime('%y%m%d',time.localtime(time.time() - 24*60*60) )


def main(argv):
  global DB_TABLES_FILE,DB_HOST,DB_USER,DB_USER_PASSWORD,DB_USER_PASSWORD,BACKUP_PATH,TMP_PATH,BACKUP_SERVER,CLEAN_TMP_COPLETED
  DATETIME =  time.strftime('%y%m%d',time.localtime(time.time() - 24*60*60))
  try:
    opts, args = getopt.getopt(argv,"hf:s:u:p:a:b:d:t:c")
  except getopt.GetoptError:
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print ('db_backup.py -f <db tables txt> -s <mysql host> -u <mysql user> -p <mysql password> -a <tmp dir> -b <backup server> -d <backup path> -t <target date es. 171201> -c')
      sys.exit()
    elif opt == "-s":
      DB_HOST = arg
    elif opt in ("-f"):
      DB_TABLES_FILE = arg
    elif opt in ("-u"):
      DB_USER = arg
    elif opt in ("-p"):
      DB_USER_PASSWORD = arg
    elif opt in ("-d"):
      BACKUP_PATH = arg
    elif opt in ("-a"):
      TMP_PATH = arg
    elif opt in ("-b"):
      BACKUP_SERVER = arg
    elif opt in ("-t"):
      DATETIME = arg
    elif opt == "-c":
      CLEAN_TMP_COPLETED = True
      break;
  mysql_backup(DATETIME)
  pass

if __name__ == "__main__":
   main(sys.argv[1:])

