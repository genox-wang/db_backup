# DB BackUp

## Back up

根据配置文件备份数据库表，压缩发送到备份服务器

- db table file 备份库表配置文件 默认 'db_tables.txt'
- db host 默认 'localhost'
- db user 默认 'root'
- db password 默认 'root'
- tmp path 本地备份临时文件夹 默认 '/Users/bill/backup/dbbackup/'  
- c  备份完成删除临时文件 默认 false 
- backup server 备份服务器 默认 'root@106.14.148.86'  
- backup path 备份服务器备份目录 默认 '/root/backup/'
- target date 备份目标日期  默认 UTC时间昨天 格式 y%m%d

```python
$ python3 db_backup.py [-f <db tables file> -s <db host> -u <db user> -p <db password> -a <tmp path> -b <backup server> -d <backup path> -t <target date es. 171201> -c]
```

## Import

指定日期的备份数据入库

- db host 默认 'localhost'
- db user 默认 'root'
- db password 默认 'root'
- backup path 备份服务器备份目录 默认 '/root/backup/'
- target date 备份目标日期  默认 UTC时间昨天 格式 y%m%d

```python
$ python3 db_import.py [ -s <db host> -u <db user> -p <db password> -d <backup path> -t <target date es. 171201> ]
```

## Db table config

配置文件格式

```
<db name>
  <table name>
  <hd table name>_%y%m%d
```

Example
```
sobering_subscription
  ss_alarm
  ss_ad_source_offer
  ss_request_log_%y%m%d
  ss_postback_log_%y%m%d
```
