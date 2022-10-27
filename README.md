# sync-obs
simple sync script for syncing raw files from observation sites to a remote server.

``` 
git clone https://github.com/willmorrison1/sync-obs
cd sync-obs
chmod u+rwx *
nano sync_config.json
sudo ./install_service.sh
```

# config example


``` json
{
    "source": "/home/smurobs/FTP/CL61/",
    "destination": "datagate5@gateway.meteo.uni-freiburg.de:/data/CL61/T3250605/",
    "archive_dir": "/home/smurobs/archive/",
    "delete_empty_dirs": true,
    "archive_older_than_mins": 5,
    "archive_max_fill_fraction": 0.48,
    "sync_repeat_time_mins": 5,
    "rsync_opts": "rsync -vv -e 'ssh -oBatchMode=yes' -rt -l -D --compress --compress-level=7 --append-verify --update --no-owner --no-group --no-perms --chmod=ugo=rwX --mkpath"
}

```
# sync-obs logic
Everything in `source` is transferred to `destination` every `sync_repeat_time_mins` minutes.

Files in `source` that are older than `archive_older_than_mins` minutes are zipped and moved to `archive_dir`.

When the `archive_dir` volume is more than `archive_max_fill_fraction` * 100 percent full, remove the oldest zip file.

