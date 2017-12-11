# DB BackUp

## Back up

```python
$ db_backup.py [-f <db tables txt> -s <mysql host> -u <mysql user> -p <mysql password> -a <tmp dir> -b <backup server> -d <backup path> -t <target date es. 171201> -c]
```

## Import

```python
$ db_import.py [ -s <mysql host> -u <mysql user> -p <mysql password> -d <backup path> -t <target date es. 171201> ]
```

## Db table config

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
