import os
import csv

from zipfile import ZipFile
from multiprocessing import Pool
from lxml import etree


def parser_xml_in_zip(zipfile_name):

    zipf = ZipFile(zipfile_name)
    data = [list(get_xml_tree(zipf.open(xml_filename)))
            for xml_filename in zipf.namelist()]
    levels = list(map(__get_levels, data))
    objects = list(map(__get_objects, data))

    return levels, objects


def get_xml_tree(xml_file):

    tree = etree.parse(xml_file)

    return tree.iter()


def __get_levels(data):

    return data[1].attrib['value'], data[2].attrib['value'],


def __get_objects(data):

    return [[data[1].attrib['value'], el.attrib['name']]
            for el in data[4:]
            if 'name' in el.attrib]


def get_zipfile_names(folder):

    return (os.path.join(folder, f)
            for f in os.listdir(folder)
            if f[-4:] == '.zip')


def csv_writer(csvfile):

    writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')

    return writer


def parallel_parser(xmlfolder='xml_dir', results_folder='res_dir'):

    try:
        os.mkdir(results_folder)
    except Exception as e:
        print(e)

    zip_names = get_zipfile_names(xmlfolder)

    pool = Pool()

    results_folder = ''.join([results_folder, '/'])

    obj_file = open(results_folder + 'objects.csv', 'a')
    level_file = open(results_folder + 'level.csv', 'a')

    writer_level = csv_writer(level_file)
    writer_objects = csv_writer(obj_file)

    writer_level.writerow(['id', 'level'])
    writer_objects.writerow(['id', 'object_name'])

    # write to file
    [(writer_level.writerows(item[0]),
        [writer_objects.writerows(rows) for rows in item[1]])
     for item in map(parser_xml_in_zip, zip_names)]

    obj_file.close()
    level_file.close()
