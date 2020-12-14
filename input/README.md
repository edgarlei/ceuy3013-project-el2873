# CitiBike Data Analysis for Impact of COVID-19 on Trip Duration and Frequency

---

The inputs for this program are retrieved directly from CitiBike from NYC Open Data and are .csv files for each month of each year that is being studied.

To upload the .csv files to GitHub, Git LFS was used.

First, Git LFS needed to be installed.

```python
>>> git lfs install
```

In order to be able to handle the large .csv files, Git LFS was instructed to track that file type.
Because the .csv files already existed and Git LFS does not automatically track retroactively, the
migrate command needed to be used.

```python
>>> git lfs track ".csv"
>>> git lfs migrate import --include="*.csv" --everything
migrate: override changes in your working copy? [Y/n] y
```

To check and make sure that the correct files are being tracked:
```python
>>> git lfs ls-files
```

Finally, the .csv files were pushed to Github.
```python
>>> git push origin master
```
