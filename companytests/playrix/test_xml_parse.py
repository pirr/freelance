import os
import csv
import xml.etree.ElementTree as ET

from datetime import datetime
from zipfile import ZipFile
from multiprocessing import Process, Queue, Pool
from functools import partial


def csv_writer(csvfile, header):
    writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
    writer.writerow(header)
    return writer


def get_zipfile_names(folder):
    for f in os.listdir(folder):
        if f[-4:] == '.zip':
            yield os.path.join(folder, f)


def get_xml_tree(zip_name):
    zipf = ZipFile(zip_name)

    for xml_file_name in zipf.namelist():
        xml_file = zipf.open(xml_file_name, 'r')
        tree = ET.parse(xml_file)
        yield tree


def get_xml_file(zip_name):
    zipf = ZipFile(zip_name)

    for xml_file_name in zipf.namelist():
        yield zipf.open(xml_file_name, 'r')


def xml_parser(xml_tree):
    var_id = xml_tree.find('.//*[@name="id"]').get('value')
    var_level = xml_tree.find('.//*[@name="level"]').get('value')
    objs = [[var_id, obj.get('name')]
            for obj in xml_tree.iter('object')]
    # objs = []
    # for obj in xml_tree.iter('object'):
    #     objs.append([var_id, obj.get('name')])
    return {'level': (var_id, var_level), 'objs': objs}


def q_xml_parser(q, xml_tree):
    var_id = xml_tree.find('.//*[@name="id"]').get('value')
    var_level = xml_tree.find('.//*[@name="level"]').get('value')
    objs = [[var_id, obj.get('name')]
            for obj in xml_tree.iter('object')]

    q.put({'level': (var_id, var_level), 'objs': objs})


# def writer_levels(level):
    


def xml_iterparse(xml_file):
    for root in xml_file.getroot():
        return root.tag, root.attrib
        # for obj in root.iter('object'):


if __name__ == '__main__':

    st = datetime.now()

    q = Queue()

    p = Pool()

    levels_file = open('level.csv', 'a')
    objects_file = open('objects.csv', 'a')
    writer_levels = csv_writer(levels_file, ['id', 'level'])
    writer_objects = csv_writer(objects_file, ['id', 'name'])

    for zip_file_name in get_zipfile_names('xml_dir'):

        items = map(xml_parser, get_xml_tree(zip_file_name))

        for item in items:
            p.apply_async(writer_levels.writerow, item['level'])
            p.apply_async(writer_objects.writerows(item['objs']))

    print(datetime.now() - st)
    # print(q.get())

    # levels_file = open('level.csv', 'w')
    # objects_file = open('objects.csv', 'w')
    # writer_levels = csv_writer(levels_file, ['id', 'level'])
    # writer_objects = csv_writer(objects_file, ['id', 'name'])

    # for zip_file_name in get_zipfile_names('xml_dir'):

        # print(list(map(xml_iterparse, get_xml_tree(zip_file_name))))

        # for xml_tree in get_xml_tree(zip_file_name):

        # for item in map(xml_parser, get_xml_tree(zip_file_name)):

        #     writer_levels.writerow(item['level'])
        #     writer_objects.writerows(item['objs'])

    # levels_file.close()
    # objects_file.close()
