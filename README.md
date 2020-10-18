# README

This repository contains the code necessary for retrieving, transforming and storing EUMETSAT data

<br>

Goals:

- [ ] Entire EUMETSAT SEVIRI RSS archive available as one big Zarr array (tens of TBytes) in Google Public Datasets bucket, spatially reprojected, and saved in a very space-efficient way.
- [ ] Automatic job to update archive on GCP from EUMETSAT's new API once a day.
- [ ] Documentation.  Possibly user-editable.  (source on GitHub, maybe?)
- [ ] A few example Jupyter Notebooks showing how to load the data, train simple ML model, and compute metrics.

<br>

To Do:

- [x] Create scraper for the new EUMETSTAT data service
- [ ] Test transform options
- [ ] Move the metadata db to BigQuery

<br>

Questions:

* What metadata is relevant and should be stored for each EUMETSAT dataset?
* What was the conclusion of comparing EUMETSAT file formats?
* What is explore y offset investigating?

<br>
<br>

### Overview

| Name                 | Directory      |   Number | Description                                 | Maintainer   |
|:---------------------|:---------------|---------:|:--------------------------------------------|:-------------|
| Repository Helpers   | development    |       00 | Code for keeping the repository tidy        | Ayrton Bourn |
| EUMETSAT API Wrapper | development    |       01 | Development of the API wrapper for ems      | Ayrton Bourn |
| Data Transformation  | development    |       02 | Intial EDA and transformation comparisons   | Ayrton Bourn |
| EUMETSAT Download    | usage_examples |       00 | Guidance for using the ems download manager | Ayrton Bourn |

<br>
<br>

### Installation/Set-Up

* Should streamline this an also create a batch script - need mac equivalents

```
git clone
conda env create -f environment.yml
conda activate sat_image_processing
```

We'll also install Jupyter lab interactive plotting for matplotlib

See the [jupyter-matplotlib docs for more info](https://github.com/matplotlib/jupyter-matplotlib).  The short version is to run these commands from within the `sat_image_processing` env:

```
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib
```

<br>

### Publishing to PyPi

To publish the `satip` module to PyPi simply run the following from the batch_scripts directory

```bash
pypi_publish <anaconda_dir>
```

Where `<anaconda_dir>` is the path to your anaconda directory - e.g. C:\Users\Ayrto\anaconda3

When prompted you should enter your PyPi username and password

After this you will be able to install the latest version of satip using `pip install satip`

<br>

### General Notes

Good video on documentation that we should try to incorporate ideas from - https://youtu.be/wEt_8twQctQ
