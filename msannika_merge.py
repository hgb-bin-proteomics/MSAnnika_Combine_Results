#!/usr/bin/env python3

# MS ANNIKA COMBINE RESULTS
# 2024 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

# version tracking
__version = "1.0.0"
__date = "2024-01-21"

# REQUIREMENTS
# pip install pandas
# pip install openpyxl

######################

"""
DESCRIPTION:
A script to combine results from several MS Annika searches.
USAGE:
msannika_merge.py f [f ...]
                    [-fdr FDR][--false_discovery_rate FDR]
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
  -h, --help            show this help message and exit
  --version             show program's version number and exit
"""

######################

import argparse
import pandas as pd

from typing import List
from typing import Dict

def merge(files: List[str]) -> pd.DataFrame:

    all_csms = dict()
    columns = None

    for f, file in enumerate(files):
        df = pd.read_excel(file)
        if columns is None:
            columns = df.columns.tolist()
        for i, row in df.iterrows():
            spectrum_file = str(row["Spectrum File"])
            scan_nr = int(row["First Scan"])
            score = float(row["Combined Score"])

            if spectrum_file in all_csms:
                if scan_nr in all_csms[spectrum_file]:
                    if all_csms[spectrum_file][scan_nr]["score"] < score:
                        all_csms[spectrum_file][scan_nr] = {"row": row, "score": score}
                else:
                    all_csms[spectrum_file][scan_nr] = {"row": row, "score": score}
            else:
                all_csms[spectrum_file] = {scan_nr: {"row": row, "score": score}}
        print(f"Processed {f + 1} CSM files...")

    rows = list()

    for spectrum_file in all_csms:
        for scan_nr in all_csms[spectrum_file]:
            rows.append(all_csms[spectrum_file][scan_nr]["row"])

    return pd.concat(rows, ignore_index = True, axis = 1, names = columns).T


def main(argv = None) -> Dict[str, pd.DataFrame]:
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar = "f",
                        dest = "files",
                        help = "Name/Path of the MS Annika CSM result files to process.",
                        type = str,
                        nargs = "+")
    parser.add_argument("-fdr", "--false_discovery_rate",
                        dest = "fdr",
                        default = None,
                        help = "FDR for CSM/crosslink validation.",
                        type = float)
    parser.add_argument("-o", "--output",
                        dest = "output",
                        default = None,
                        help = "Prefix of the output file(s).",
                        type = str)
    parser.add_argument("--version",
                        action = "version",
                        version = __version)
    args = parser.parse_args(argv)

    merged_df = merge(args.files)

    result_dict = {"CSMs_merged": merged_df, "CSMs_merged_validated": None,
                   "Crosslinks": None, "Crosslinks_validated": None}

    if args.output is not None:
        merged_df.to_excel(".xlsx".join(args.output.split(".xlsx")[:-1]) + "_merged.xlsx", sheet_name = "CSMs", index = False)
    else:
        merged_df.to_excel("CSMs_merged.xlsx", sheet_name = "CSMs", index = False)

    if args.fdr is not None:

        print("Validating using MS Annika FDR...")

        import urllib.request as ur
        msannika_fdr_url = "https://raw.githubusercontent.com/hgb-bin-proteomics/MSAnnika_FDR/master/msannika_fdr.py"
        ur.urlretrieve(msannika_fdr_url, "msannika_fdr.py")

        from msannika_fdr import MSAnnika_CSM_Grouper as grouper
        from msannika_fdr import MSAnnika_CSM_Validator as csm_val
        from msannika_fdr import MSAnnika_Crosslink_Validator as xl_val

        validated_csms = csm_val.validate(merged_df, args.fdr)
        result_dict["CSMs_merged_validated"] = validated_csms
        crosslinks = grouper.group(merged_df)
        result_dict["Crosslinks"] = crosslinks
        validated_crosslinks = xl_val.validate(crosslinks, args.fdr)
        result_dict["Crosslinks_validated"] = validated_crosslinks

        if args.output is not None:
            validated_csms.to_excel(".xlsx".join(args.output.split(".xlsx")[:-1]) + "_merged_validated.xlsx", sheet_name = "CSMs", index = False)
            crosslinks.to_excel(".xlsx".join(args.output.split(".xlsx")[:-1]) + "_crosslinks.xlsx", sheet_name = "Crosslinks", index = False)
            validated_crosslinks.to_excel(".xlsx".join(args.output.split(".xlsx")[:-1]) + "_crosslinks_validated.xlsx", sheet_name = "Crosslinks", index = False)
        else:
            validated_csms.to_excel("CSMs_merged_validated.xlsx", sheet_name = "CSMs", index = False)
            crosslinks.to_excel("Crosslinks.xlsx", sheet_name = "Crosslinks", index = False)
            validated_crosslinks.to_excel("Crosslinks_validated.xlsx", sheet_name = "Crosslinks", index = False)

    print("Done!")
    return result_dict

if __name__ == "__main__":
    r = main()
