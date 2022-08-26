# sync-obs
simple sync script for raw obs files


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

Files in `source` that are older than `archive_older_than_mins` minutes are zipped in `archive_dir`.

Remove the oldest zip files in `archive_dir` until the `archive_dir` volume is less than `archive_max_fill_fraction` * 100 percent full.

