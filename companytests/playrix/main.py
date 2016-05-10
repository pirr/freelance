import os
from datetime import datetime
from importlib import reload

import lib

from lib.xml_creator import parallel_xml_zipper
from lib.xml_parser import parallel_parser

reload(lib)


if __name__ == '__main__':

    xmlfolder = 'xml_dir'
    results_folder = 'res_dir'
    zip_number = 50
    xml_number = 100

    try:
        os.mkdir(xmlfolder)
    except Exception as e:
        print(e)

    st = datetime.now()

    # parallel_xml_zipper(zip_number, xml_number, xmlfolder)
    parallel_parser(xmlfolder, results_folder)

    print(datetime.now() - st)
