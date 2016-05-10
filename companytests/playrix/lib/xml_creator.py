import lxml.etree
import lxml.builder
import string
import random
import os

from string import ascii_uppercase
from zipfile import ZipFile
from multiprocessing import Pool
from functools import partial


uniq_vals = []
uniq_val = ''.join(random.choice(ascii_uppercase) for i in range(35))


def xml_creator(max_length):

    E = lxml.builder.ElementMaker()
    root = E.root
    var = E.var
    objects = E.objects
    obj = E.object

    objs = [obj(name=string_generator(
        size=random.choice(range(1, max_length))))
        for i in range(1, max_length)]

    the_xml = root(
        var(name='id', value=uniq_id()),
        var(name='level', value=str(random.choice(range(1, 101)))),
        objects(*objs)
    )

    return lxml.etree.tostring(
        the_xml, pretty_print=True, xml_declaration=True)


def string_generator(size=6, chars=string.ascii_uppercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))


def uniq_id():

    while True:
        uniq_val = string_generator(size=15, chars=string.digits)

        if uniq_val not in uniq_vals:
            uniq_vals.append(uniq_val)

            return str(uniq_val)


def create_zip_names(zip_number=50, folder='xml_dir'):
    return [''.join([folder, '/', 'xml_', str(j), '.zip'])
            for j
            in range(zip_number)]


def xml_zipper(zip_name, xml_number=100):

    for k in range(xml_number):
        max_length = random.choice(range(2, 20))
        xml_name = ''.join(['workfile_', str(k), '.xml'])

        with ZipFile(zip_name, 'a') as zf:
            zf.writestr(xml_name, xml_creator(max_length))


def parallel_xml_zipper(zip_number, xml_number, folder):

    pool = Pool()
    zip_names = create_zip_names(zip_number, folder)
    pool.map(partial(xml_zipper, xml_number=xml_number), zip_names)
