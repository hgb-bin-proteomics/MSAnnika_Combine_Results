#!/usr/bin/env python3

# MS ANNIKA COMBINE RESULTS
# 2024 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

# version tracking
__version = "1.0.0"
__date = "2024-01-09"

# REQUIREMENTS
# pip install pandas
# pip install openpyxl

######################

# import packages
import argparse
import pandas as pd

from typing import List

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


def main(argv = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar = "f",
                        dest = "files",
                        help = "Name/Path of the MS Annika result files to process.",
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
                        help = "Name of the output file.",
                        type = str)
    parser.add_argument("--version",
                        action = "version",
                        version = __version)
    args = parser.parse_args(argv)

    merged_df = merge(args.files)

    if args.output is not None:
        merged_df.to_excel(args.output.rstrip(".xlsx") + "_merged.xlsx", sheet_name = "CSMs", index = False)
    else:
        merged_df.to_excel("CSMs_merged.xlsx", sheet_name = "CSMs", index = False)

    if args.fdr is not None:

        print(f"Validating using {args.fdr} FDR...")

        import urllib.request as ur
        msannika_fdr_url = "https://raw.githubusercontent.com/hgb-bin-proteomics/MSAnnika_FDR/master/msannika_fdr.py"
        ur.urlretrieve(msannika_fdr_url, "msannika_fdr.py")

        from msannika_fdr import MSAnnika_CSM_Grouper as grouper
        from msannika_fdr import MSAnnika_CSM_Validator as csm_val
        from msannika_fdr import MSAnnika_Crosslink_Validator as xl_val

        validated_csms = csm_val.validate(merged_df, args.fdr)
        crosslinks = grouper.group(merged_df)
        validated_crosslinks = xl_val.validate(crosslinks, args.fdr)

        if args.output is not None:
            validated_csms.to_excel(args.output.rstrip(".xlsx") + "_merged_validated.xlsx", sheet_name = "CSMs", index = False)
            crosslinks.to_excel(args.output.rstrip(".xlsx") + "_crosslinks.xlsx", sheet_name = "Crosslinkss", index = False)
            validated_crosslinks.to_excel(args.output.rstrip(".xlsx") + "_crosslinks_validated.xlsx", sheet_name = "Crosslinks", index = False)
        else:
            validated_csms.to_excel("CSMs_merged_validated.xlsx", sheet_name = "CSMs", index = False)
            crosslinks.to_excel("Crosslinks.xlsx", sheet_name = "Crosslinks", index = False)
            validated_crosslinks.to_excel("Crosslinks_validated.xlsx", sheet_name = "Crosslinks", index = False)

    print("Done!")

if __name__ == "__main__":
    main()
