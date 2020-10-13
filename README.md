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

| Notebook                 | Description                                | Maintainer   |
|:-------------------------|:-------------------------------------------|:-------------|
| 00) Repository Helpers   | Code for keeping the repository tidy       | Ayrton Bourn |
| 01) EUMETSAT API Wrapper | Development of API wrapper for EUMETSAT    | Ayrton Bourn |
| 02) Data Transformation  | Initial EDA and transformation comparisons | Ayrton Bourn |

<br>
<br>

### Installation/Set-Up

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


