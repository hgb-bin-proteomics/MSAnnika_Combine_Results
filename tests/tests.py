#!/usr/bin/env python3

# MS ANNIKA COMBINE RESULTS - TESTS
# 2024 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

# test 1
def test1_msannika_merge():

    from msannika_merge import main

    result = main(["DSSO_CSMs.xlsx", "ncDSSO_CSMs.xlsx", "-fdr", "0.01"])

    # check nr of merged CSMs
    assert result["CSMs_merged"].shape[0] == 13985

    # check that all CSMs are unique
    assert result["CSMs_merged"].shape[0] == len(result["CSMs_merged"]["First Scan"].unique().tolist())

    # check that validated CSMs fullfill FDR < 0.01
    import pandas as pd

    def get_decoy_flag(row: pd.Series) -> bool:
        return True if "D" in row["Alpha T/D"] or "D" in row["Beta T/D"] else False

    result["CSMs_merged_validated"]["test_decoy_flag"] = result["CSMs_merged_validated"].apply(lambda row: get_decoy_flag(row), axis = 1)

    assert result["CSMs_merged_validated"][result["CSMs_merged_validated"]["test_decoy_flag"] == True].shape[0] / result["CSMs_merged_validated"][result["CSMs_merged_validated"]["test_decoy_flag"] == False].shape[0] < 0.01

    # check that grouping CSMs to Crosslinks worked
    assert result["Crosslinks"] is not None

    # check nr of validated crosslinks
    assert result["Crosslinks_validated"].shape[0] == 729

    # check that validated Crosslinks fullfill FDR < 0.01
    assert result["Crosslinks_validated"][result["Crosslinks_validated"]["Decoy"] == True].shape[0] / result["Crosslinks_validated"][result["Crosslinks_validated"]["Decoy"] == False].shape[0] < 0.01

# test 2
def test2_msannika_merge():

    from msannika_merge import main

    result = main(["DSSO_CSMs.xlsx", "ncDSSO_CSMs.xlsx", "-fdr", "0.01", "-csms"])

    assert result["CSMs_merged"] is not None

    assert result["CSMs_merged_validated"] is not None

    assert result["Crosslinks"] is not None

    assert result["Crosslinks_validated"] is None

# test 3
def test3_msannika_merge():

    from msannika_merge import main

    result = main(["DSSO_CSMs.xlsx", "ncDSSO_CSMs.xlsx", "-fdr", "0.01", "-crosslinks"])

    assert result["CSMs_merged"] is not None

    assert result["CSMs_merged_validated"] is None

    assert result["Crosslinks"] is not None

    assert result["Crosslinks_validated"] is not None
