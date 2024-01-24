![workflow_state](https://github.com/hgb-bin-proteomics/MSAnnika_Combine_Results/workflows/msannika_merge/badge.svg)

# MS Annika Combine Results

A script to merge and optionally validate several [MS Annika](https://github.com/hgb-bin-proteomics/MSAnnika)
search results. The main use case would be for merging results from different MS
Annika runs, e.g. combining results from a cleavable and non-cleavable MS Annika
search or combining results from different doublet distances.

## Usage

- Install python 3.7+: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Install requirements: `pip install -r requirements.txt`
- Export MS Annika CSM results from Proteome Discoverer to Microsoft Excel format.
  - **Important:** CSMs should not be filtered! Export all (unvalidated) CSMs including decoy hits!
- Run `python msannika_merge.py filename1.xlsx filename2.xlsx -fdr 0.01` (see below for more examples).
- The script may take a few minutes, depending on the number of CSMs to process.
- Done!

## Examples

`msannika_merge.py` takes one positional and two optional arguments. The first
argument always has to be the filename(s) of the MS Annika CSM result file(s).
You may specify any number of result files! For demonstration purposes we will
use the files supplied in the `/data` folder:
- `DSSO_CSMs.xlsx` contains unvalidated CSMs from a cleavable MS Annika search
using the crosslinker DSSO.
- `ncDSSO_CSMs.xlsx` contains unvalidated CSMs from a non-cleavable MS Annika
search using the crosslinker DSSO.

The following is a valid `msannika_merge.py` call:

```bash
python msannika_merge.py DSSO_CSMs.xlsx ncDSSO_CSMs.xlsx
```

This will merge CSMs from all given files, in this case `DSSO_CSMs.xlsx` and
`ncDSSO_CSMs.xlsx` into a result file called `CSMs_merged.xlsx`. You can also
set a prefix for the generated result file(s) like this:

```bash
python msannika_merge.py DSSO_CSMs.xlsx ncDSSO_CSMs.xlsx -o All_CSMs.xlsx
```

This will merge CSMs from all given files, exactly like the last command, but
the generated result file will now be named `All_CSMs_merged.xlsx`.

If you suppy the optional argument `-fdr` or `--false_discovery_rate` and the
desired FDR as a floating point number, the CSMs will be merged, then validated,
then grouped by sequence and position to crosslinks and those crosslinks will
again be validated for the given FDR. To group CSMs and validate CSMs and
crosslinks the [MS Annika FDR](https://github.com/hgb-bin-proteomics/MSAnnika_FDR)
script is downloaded and used. Validation therefore requires an active internet
connection!

```bash
python msannika_merge.py DSSO_CSMs.xlsx ncDSSO_CSMs.xlsx -fdr 0.01
```

This will merge CSMs from all given files, then validate the merged CSMs for
estimated 1% FDR, then group CSMs to crosslinks and finally validate the
crosslinks for estimated 1% FDR. The following files will be generated:
- `CSMs_merged.xlsx`: The merged CSMs from all given files.
- `CSMs_merged_validated.xlsx`: The merged CSMs that are above the estimated 1%
FDR threshold.
- `Crosslinks.xlsx`: The crosslinks that result from grouping the merged CSMs.
- `Crosslinks_validated.xlsx`: The crosslinks that are above the estimated 1%
FDR threshold.

Note that the following command will produce the same output (FDR values >= 1
will automatically be divided by 100):

```bash
python msannika_merge.py DSSO_CSMs.xlsx ncDSSO_CSMs.xlsx -fdr 1
```

It is also possible to only validate CSMs and not validate crosslinks by adding
the flag `-csms` to the command:

```bash
python msannika_merge.py DSSO_CSMs.xlsx ncDSSO_CSMs.xlsx -fdr 0.01 -csms
```

The following files will be generated:
- `CSMs_merged.xlsx`: The merged CSMs from all given files.
- `CSMs_merged_validated.xlsx`: The merged CSMs that are above the estimated 1%
FDR threshold.
- `Crosslinks.xlsx`: The crosslinks that result from grouping the merged CSMs.

The same also works for crosslinks by adding the flag `-crosslinks` which will
only validate crosslinks but not CSMs:

```bash
python msannika_merge.py DSSO_CSMs.xlsx ncDSSO_CSMs.xlsx -fdr 0.01 -crosslinks
```

The following files will be generated:
- `CSMs_merged.xlsx`: The merged CSMs from all given files.
- `Crosslinks.xlsx`: The crosslinks that result from grouping the merged CSMs.
- `Crosslinks_validated.xlsx`: The crosslinks that are above the estimated 1%
FDR threshold.

## Parameters

```python
"""
DESCRIPTION:
A script to combine results from several MS Annika searches.
USAGE:
msannika_merge.py f [f ...]
                    [-fdr FDR][--false_discovery_rate FDR]
                    [-o PREFIX][--output PREFIX]
                    [-csms][--csms]
                    [-crosslinks][--crosslinks]
                    [-h][--help]
                    [--version]
positional arguments:
  f                     MS Annika result files in Microsoft Excel format (.xlsx)
                        to process. MS Annika result files have to be
                        unvalidated CSMs including decoys!
optional arguments:
  -fdr FDR, --false_discovery_rate FDR
                        False discovery rate to validate results for. Supports
                        both percentage input (e.g. 1) or fraction input (e.g.
                        0.01). By default not set and results will only be
                        merged. Validation requires internet connection because
                        the MS Annika FDR module will be downloaded to calculate
                        FDR.
                        Default: None
  -o PREFIX, --output PREFIX
                        Prefix of the output file(s).
                        Default: None
-csms, --csms
                        Only validate CSMs and not crosslinks.
                        Default: False
-crosslinks, --crosslinks
                        Only validate crosslinks and not CSMs.
                        Default: False
  -h, --help            show this help message and exit
  --version             show program's version number and exit
"""
```

## Function Documentation

If you want to integrate the MS Annika Combine Results process into your own
scripts, you can import the following function as given:

```python
import pandas as pd

cdsso = pd.read_excel("DSSO_CSMs.xlsx")
ncdsso = pd.read_excel("ncDSSO_CSMs.xlsx")

# Merging CSMs
from msannika_merge import merge
all_csms = merge([cdsso, ncdsso])

# The function signature of merge is:
def merge(files: List[str]) -> pd.DataFrame:
    """code omitted"""
    return
```

For validation please use the functions provided in [MS Annika FDR](https://github.com/hgb-bin-proteomics/MSAnnika_FDR).

## Known Issues

[List of known issues](https://github.com/hgb-bin-proteomics/MSAnnika_Combine_Results/issues)

## Citing

If you are using the MS Annika Combine Results script please cite:
```
MS Annika 2.0 Identifies Cross-Linked Peptides in MS2–MS3-Based Workflows at High Sensitivity and Specificity
Micha J. Birklbauer, Manuel Matzinger, Fränze Müller, Karl Mechtler, and Viktoria Dorfer
Journal of Proteome Research 2023 22 (9), 3009-3021
DOI: 10.1021/acs.jproteome.3c00325
```

If you are using MS Annika please cite:
```
MS Annika 2.0 Identifies Cross-Linked Peptides in MS2–MS3-Based Workflows at High Sensitivity and Specificity
Micha J. Birklbauer, Manuel Matzinger, Fränze Müller, Karl Mechtler, and Viktoria Dorfer
Journal of Proteome Research 2023 22 (9), 3009-3021
DOI: 10.1021/acs.jproteome.3c00325
```
or
```
MS Annika: A New Cross-Linking Search Engine
Georg J. Pirklbauer, Christian E. Stieger, Manuel Matzinger, Stephan Winkler, Karl Mechtler, and Viktoria Dorfer
Journal of Proteome Research 2021 20 (5), 2560-2569
DOI: 10.1021/acs.jproteome.0c01000
```

## License

- [MIT](https://github.com/hgb-bin-proteomics/MSAnnika_Combine_Results/blob/master/LICENSE)

## Contact

- [micha.birklbauer@fh-hagenberg.at](mailto:micha.birklbauer@fh-hagenberg.at)
