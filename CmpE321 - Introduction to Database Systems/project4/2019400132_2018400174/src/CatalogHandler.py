import os
import glob
from collections import defaultdict

from utils import to_json, from_json, move_item_within_list
from bplustree import BPlusTree
from settings import settings
from FileHandler import FileHandler

class CatalogHandler:

    def __init__(self, file_handler):
        # loads file and saves it in dictionary
        self.file_handler = file_handler
        
        # Load catalog
        self.catalog = defaultdict(lambda: {"fields":[]})
        catalog_file_handler = self.mount_catalog_file()
        next_available_page = catalog_file_handler.get_next_available_page_index()

        next_information = "primaryKeyIndex"
        all_record_data  = []
        for page_index in range(next_available_page):
            _active, _n_records, _slot_activities, record_data_list = catalog_file_handler.read_page(page_index)
            all_record_data.extend(record_data_list)

        counter = 0
        while counter < len(all_record_data):
            type, information, value = all_record_data[counter]
            counter += 1
            if information == next_information and information == "primaryKeyIndex":
                self.catalog[type]["primary_key_index"] = int(value)
                next_information = "numberOfFields"
            elif information == next_information and information == "numberOfFields":
                for _ in range(int(value)):
                    
                    d = {}
                    type, information, value = all_record_data[counter]
                    d["name"] = value
                    counter += 1
                    
                    
                    type, information, value = all_record_data[counter]
                    d["dtype"] = value
                    counter += 1

                    self.catalog[type]["fields"].append(d)
                next_information = "primaryKeyIndex"
            else:
                raise Exception("Something went wrong when processing the catalog file. next_information:\"%s\", information: \"%s\"" % (next_information, information))
        catalog_file_handler.delete_file()

        self.trees = {}
        for type_name in self.catalog:
            page_settings = self.get_page_settings(type_name)
            tree = from_json(self.__get_tree_path(type_name), page_settings["n_records_per_page"]-1)
            self.trees[type_name] = tree

    def type_exists(self, type_name):
        return type_name in self.get_types()

    def get_types(self):
        return list(self.catalog.keys())

    def get_type_data(self, type_name):
        return self.catalog[type_name]['fields']

    def get_primary_key_index(self, type_name):
        return self.catalog[type_name]['primary_key_index']

    def get_primary_key_dtype(self, type_name):
        return self.get_dtypes(type_name)[self.catalog[type_name]['primary_key_index']]

    def get_dtypes(self, type_name):
        return [f['dtype'] for f in self.catalog[type_name]['fields']]

    def format_input(self, input, dtype):
        return int(input) if dtype=="int" else input

    def encode_input(self, type_name, inputs):
        dtypes = self.get_dtypes(type_name)
        return [self.format_input(*args) for args in zip(inputs, dtypes)]

    def fix_fields_for_record(self, type_name, input_fields):
        """Process the raw fields read from the input.
        Convert all integer fields to integer from string.
        Remove the primary key from the list of fields
        
        Args:
            type_name (str): name of the type
            fields (list:str): List of fields in string format

        Returns:
            tuple. First element is the primary key, second
            element a list of other fields
        """
        input_fields = self.encode_input(type_name, input_fields)
        primary_key_index = self.get_primary_key_index(type_name)
        primary_key = input_fields[primary_key_index]
        del input_fields[primary_key_index]
        record_fields = [primary_key]
        record_fields.extend(input_fields)

        return primary_key, record_fields

    def fix_fields_for_output(self, type_name, record_fields):
        """Record fields are in the order they are
        stored in the database. Therefore the primary
        key is the first item. This may not be the case
        in the input and the output files. This method
        fixes this difference.

        Args:
            type_name (str): name of the type
            fields (list:str/int): List of fields ordered as in
                the database records (primary key is in the
                first index)

        """
        primary_key = record_fields[0]
        del record_fields[0]
        record_fields.insert(self.get_primary_key_index(type_name), primary_key)
        return record_fields
    
    def move_item_within_list(self, l, f, t):
        temp = l[f]
        del l[f]
        
    def calculate_record_data_size(self, dtypes):
        record_data_size = 0
        for dtype in dtypes:
            if dtype == "int":
                record_data_size += 4
            elif dtype == "str":
                record_data_size += 20
            else:
                raise Exception("Unrecognized dtype:", dtype)
        return record_data_size
    
    def get_page_settings(self, type_name):

        record_data_size = self.calculate_record_data_size(self.get_dtypes(type_name))
        record_size = record_data_size + 2
        n_records_per_page = settings.BODY_SIZE // record_size
        return {
            "dtypes": move_item_within_list(self.get_dtypes(type_name), self.get_primary_key_index(type_name), 0),
            "record_data_size": record_data_size,
            "record_size": record_size,
            "n_records_per_page": n_records_per_page,
            "wasted_space": settings.BODY_SIZE - n_records_per_page * record_size
        }
    
    # CHECKS are performed by Definition Handler.
    # Just add the given type
    def add_type(self, type_name, primary_key_index, fields):
        self.catalog[type_name] = {'primary_key_index': int(primary_key_index)-1, 'fields': fields}

        # Create tree file
        page_settings = self.get_page_settings(type_name)
        tree = BPlusTree(page_settings["n_records_per_page"])
        self.trees[type_name] = tree

        self.file_handler.mount_file(type_name, page_settings)
        self.file_handler.add_page(0)

    # CHECKS are performed by Definition Handler
    # Just remove the given type
    def remove_type(self, type_name):

        # TODO: looks bad
        page_settings = self.get_page_settings(type_name)
        self.file_handler.mount_file(type_name, page_settings)
        self.file_handler.delete_file()
        del self.catalog[type_name] # it is guaranteed to exist
        del self.trees[type_name]


    def get_tree(self, type_name):
        return self.trees[type_name]

    def __get_tree_path(self, type_name):
        return os.path.join(settings.TREE_FOLDER_PATH, type_name + ".json")

    def mount_catalog_file(self):
        catalog_file_handler = FileHandler()
        catalog_file_handler.mount_file(settings.CATALOG_TYPE, {
            "dtypes": ["str", "str", "str"],
            "record_data_size": 60,
            "record_size": 62,
            "n_records_per_page": settings.BODY_SIZE // 62,
            "wasted_space": settings.BODY_SIZE - (settings.BODY_SIZE // 62) * 62
        })
        return catalog_file_handler

    def close(self):
        catalog_file_handler = self.mount_catalog_file()
        catalog_file_handler.add_page(0)
        n_records_per_page = catalog_file_handler.page_settings["n_records_per_page"]
        page_index = 0
        record_index = 0

        def write_catalog_record(type_name, information, value):
            nonlocal page_index, record_index
            catalog_file_handler.write_record(page_index, [type_name, information, value])
            record_index += 1
            if record_index == n_records_per_page:
                record_index = 0
                page_index += 1
                catalog_file_handler.add_page(page_index)

        # Purge trees folder
        files = glob.glob(settings.TREE_FOLDER_PATH + "/*.json")
        for f in files:
            os.remove(f)

        for type_name in self.catalog:
            write_catalog_record(type_name, "primaryKeyIndex", str(self.catalog[type_name]["primary_key_index"]))
            fields = self.catalog[type_name]["fields"]
            write_catalog_record(type_name, "numberOfFields", str(len(fields)))
            for i, field in enumerate(fields):
                write_catalog_record(type_name, "field%dname"%i, field["name"])
                write_catalog_record(type_name, "field%ddtype"%i, field["dtype"])
        catalog_file_handler.dismount_file()

        for tree in self.trees:
            tree_path = self.__get_tree_path(tree)
            to_json(tree_path, self.trees[tree])
        