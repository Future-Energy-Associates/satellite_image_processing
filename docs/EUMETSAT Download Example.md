# EUMETSAT Download Example

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Future-Energy-Associates/satellite_image_processing/master?urlpath=lab%2Ftree%2Fusage_examples%2F00%29%20EUMETSAT%20Download.ipynb)

<br>

This notebook outlines how the `satip` module can be used to download data from EUMETSAT

<br>

### Imports

We will begin by importing the relevant libraries, you can install the latest version of satip using `pip install satip`

```python
from satip import eumetsat as ems

import os
import dotenv
```

<br>

### User Input


```python
data_dir = '../data/raw'
env_vars_fp = '../.env'
metadata_db_fp = '../data/EUMETSAT_metadata.db'
```

<br>

### Authorising API Access

First we'll load the the environment variables and assign the user key and secret


```python
dotenv.load_dotenv(env_vars_fp)

user_key = os.environ.get('user_key')
user_secret = os.environ.get('user_secret')
```

<br>

### Downloading the Data

We have to initialise the DownloadManager, then we can pass date ranges over which all data will be downloaded


```python
start_date = '2020-10-01 00:00'
end_date = '2020-10-01 00:30'

dm = ems.DownloadManager(user_key, user_secret, data_dir, metadata_db_fp)

dm.download_datasets(start_date, end_date)
```


<div><span class="Text-label" style="display:inline-block; overflow:hidden; white-space:nowrap; text-overflow:ellipsis; min-width:0; max-width:15ex; vertical-align:middle; text-align:right"></span>
<progress style="width:60ex" max="6" value="6" class="Progress-main"/></progress>
<span class="Progress-label"><strong>100%</strong></span>
<span class="Iteration-label">6/6</span>
<span class="Time-label">[00:00<00:00, 0.00s/it]</span></div>


<br>

Metadata for each of the files is saved to a database


```python
df_metadata = dm.get_df_metadata()

df_metadata.head()
```

|    |   id | start_date                 | end_date                   | result_time                | platform_short_name   | platform_orbit_type   | instrument_name   | sensor_op_mode   | center_srs_name   | center_position   | file_name                                            |   file_size |   missing_pct | downloaded                 |
|---:|-----:|:---------------------------|:---------------------------|:---------------------------|:----------------------|:----------------------|:------------------|:-----------------|:------------------|:------------------|:-----------------------------------------------------|------------:|--------------:|:---------------------------|
|  0 |    1 | 2020-10-01 00:00:07.767000 | 2020-10-01 00:04:14.060000 | 2020-10-01 00:04:14.060000 | MSG3                  | GEO                   | SEVIRI            | RSS              | EPSG:4326         | 0 9.5             | MSG3-SEVI-MSG15-0100-NA-20201001000414.060000000Z-NA |       99819 |             0 | 2020-10-13 00:24:02.786606 |
|  1 |    2 | 2020-10-01 00:05:07.523000 | 2020-10-01 00:09:13.818000 | 2020-10-01 00:09:13.818000 | MSG3                  | GEO                   | SEVIRI            | RSS              | EPSG:4326         | 0 9.5             | MSG3-SEVI-MSG15-0100-NA-20201001000913.818000000Z-NA |       99819 |             0 | 2020-10-13 00:24:09.229091 |
|  2 |    3 | 2020-10-01 00:10:07.281000 | 2020-10-01 00:14:13.576000 | 2020-10-01 00:14:13.576000 | MSG3                  | GEO                   | SEVIRI            | RSS              | EPSG:4326         | 0 9.5             | MSG3-SEVI-MSG15-0100-NA-20201001001413.576000000Z-NA |       99819 |             0 | 2020-10-13 00:24:15.793064 |
|  3 |    4 | 2020-10-01 00:15:07.040000 | 2020-10-01 00:19:13.336000 | 2020-10-01 00:19:13.336000 | MSG3                  | GEO                   | SEVIRI            | RSS              | EPSG:4326         | 0 9.5             | MSG3-SEVI-MSG15-0100-NA-20201001001913.336000000Z-NA |       99819 |             0 | 2020-10-13 00:24:22.183809 |
|  4 |    5 | 2020-10-01 00:20:08.602000 | 2020-10-01 00:24:14.899000 | 2020-10-01 00:24:14.899000 | MSG3                  | GEO                   | SEVIRI            | RSS              | EPSG:4326         | 0 9.5             | MSG3-SEVI-MSG15-0100-NA-20201001002414.899000000Z-NA |       99819 |             0 | 2020-10-13 00:24:28.338515 |


