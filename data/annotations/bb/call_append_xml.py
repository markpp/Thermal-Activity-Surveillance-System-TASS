"""
Sample script to convert an csv annotation file into a xml file.
"""


import os
import sys
sys.path.append('../../../data processing/tools/')
from append_xml import merge_2, merge


def merge_three():

    #ALL
    # train
    merge('training/2015-09-02-12-44_bb_all.xml', 'training/2015-09-28-12-39_bb_all.xml', 'training/2016-08-08-11-00_bb_all.xml', 'training/')
    # test
    merge('testing/2015-09-30-06-23_bb_all.xml', 'testing/2015-10-05-15-56_bb_all.xml', 'testing/2016-08-09-14-58_bb_all.xml', 'testing/')
    
    #MTB
    # train
    merge('training/2015-09-02-12-44_bb_mtb.xml', 'training/2015-09-28-12-39_bb_mtb.xml', 'training/2016-08-08-11-00_bb_mtb.xml', 'training/')
    # test
    merge('testing/2015-09-30-06-23_bb_mtb.xml', 'testing/2015-10-05-15-56_bb_mtb.xml', 'testing/2016-08-09-14-58_bb_mtb.xml', 'testing/')

    #PED
    # train
    merge('training/2015-09-02-12-44_bb_ped.xml', 'training/2015-09-28-12-39_bb_ped.xml', 'training/2016-08-08-11-00_bb_ped.xml', 'training/')
    # test
    merge('testing/2015-09-30-06-23_bb_ped.xml', 'testing/2015-10-05-15-56_bb_ped.xml', 'testing/2016-08-09-14-58_bb_ped.xml', 'testing/')

def merge_two():

    #ALL
    # train
    merge_2('training/2015-09-02-12-44_bb_all.xml', 'training/2015-09-28-12-39_bb_all.xml', 'training/')
    # test
    merge('testing/2015-09-30-06-23_bb_all.xml', 'testing/2015-10-05-15-56_bb_all.xml', 'testing/2016-08-09-14-58_bb_all.xml', 'testing/')
    
    #MTB
    # train
    merge_2('training/2015-09-02-12-44_bb_mtb.xml', 'training/2015-09-28-12-39_bb_mtb.xml', 'training/')
    # test
    merge('testing/2015-09-30-06-23_bb_mtb.xml', 'testing/2015-10-05-15-56_bb_mtb.xml', 'testing/2016-08-09-14-58_bb_mtb.xml', 'testing/')

    #PED
    # train
    merge_2('training/2015-09-02-12-44_bb_ped.xml', 'training/2015-09-28-12-39_bb_ped.xml', 'training/')
    # test
    merge('testing/2015-09-30-06-23_bb_ped.xml', 'testing/2015-10-05-15-56_bb_ped.xml', 'testing/2016-08-09-14-58_bb_ped.xml', 'testing/')


if __name__ == '__main__':
    """Main function for executing the run script.

    """
    merge_three()
