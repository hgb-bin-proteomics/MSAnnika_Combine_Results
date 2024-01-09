#!/usr/bin/env python3

# MS ANNIKA COMBINE RESULTS - TESTS
# 2024 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

# test 1
def test1_msannika_merge():

    from msannika_merge import main

    result = main(["DSSO_CSMs.xlsx", "ncDSSO_CSMs.xlsx"])

    assert True
