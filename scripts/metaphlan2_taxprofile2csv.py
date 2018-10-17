#!/usr/bin/env python

from __future__ import print_function
import argparse

import pandas as pd

TAXLEVELS = {'k': 'kingdom',
             'p': 'phylum',
             'c': 'class',
             'o': 'order',
             'f': 'family',
             'g': 'genus',
             's': 'species',
             't': 'subtype'}


def main():
    ''' Converts the taxonomic profile output of MetaPhlAn2 into a proper table
        by parsing the clade name column into two columns, one column for
        taxonomic rank and one for the taxonomic unit.
    '''
    # Read tax profile
    taxprofile = pd.read_csv(Args['input'], sep='\t',
                             engine='python',
                             skiprows=1, skipfooter=1)
    # Separate taxonomic rank and unit from each other
    taxprofile[['rank', 'unit']] = taxprofile['#clade_name'].\
            str.split("|").str[-1].\
            str.extract(r"([a-z])\_\_([A-Z[a-z0-9_]+)")
    taxprofile['rank'].replace(TAXLEVELS, inplace=True)
    # Add sample name
    taxprofile['sample'] = open(Args['input']).readline().rstrip().split("\t")[-1]
    # Write to file
    taxprofile[['sample', 'rank', 'unit', 'relative_abundance', 'coverage',
                'average_genome_length_in_the_clade',
                'estimated_number_of_reads_from_the_clade']].\
        to_csv(Args['output'], sep="\t", index=False)


# Argument parser
Parser = argparse.ArgumentParser(description='Converts the taxonomic profile ' +
                                 'produced by MetaPhlAn2 into a table by ' +
                                 'splitting the clade name into rank and ' +
                                 'unit and adding the sample name as a ' +
                                 'column.')
Parser.add_argument('-i', '--input', required=True,
                    help='taxonomic profile produced by MetaPhlAn2')
Parser.add_argument('-o', '--output', required=True,
                    help='CSV file')
Args = vars(Parser.parse_args())

if __name__ == '__main__':
    main()
