# sync-obs
simple sync script for syncing raw files from observation sites to a remote server.


# config

``` json
{
    "source": "/home/pi/ircam/OUT/",
    "destination": "web@urbisphere.uni-freiburg.de:data/PI-160/",
    "archive_dir": "/home/pi/ircam/archive/",
    "delete_empty_dirs": true,
    "archive_older_than_mins": 5,
    "archive_max_fill_fraction": 0.9,
    "sync_repeat_time_mins": 5
}
```

Everything in `source` is transferred to `destination` every `sync_repeat_time_mins` minutes.

Files in `source` that are older than `archive_older_than_mins` minutes are zipped and moved to `archive_dir`.

When the `archive_dir` volume is more than `archive_max_fill_fraction` * 100 percent full, remove the oldest zip file.

