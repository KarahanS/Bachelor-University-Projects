
from logging import FileHandler
import sys
import re
from settings import settings
from Loader import InputLoader
from Writer import LogWriter, OutputWriter
from CatalogHandler import CatalogHandler
from FileHandler import FileHandler

if __name__ == "__main__":

    input_file_name, output_file_name = sys.argv[1:3]

    fileHandler   = FileHandler()
    catalogHandler = CatalogHandler(fileHandler)

    # IO
    inputLoader  = InputLoader(input_file_name)
    outputWriter = OutputWriter(output_file_name)
    logWriter = LogWriter(settings.LOGFILE_NAME)

    # Do stuff here. Structure:
    # Load Config, Run Program, Write Config

    def search(primary_key, type_name):
        primary_key = catalogHandler.format_input(primary_key, catalogHandler.get_primary_key_dtype(type_name))
        tree = catalogHandler.get_tree(type_name)
        page_index = tree.search(primary_key)
        if page_index != None:
            record_data = fileHandler.read_record(page_index, primary_key)
            record_data = catalogHandler.fix_fields_for_output(type_name, record_data)
            outputWriter.write_fields(record_data)
            logWriter.write(line, True)
        else:
            logWriter.write(line, False)

    for tokens, line in inputLoader.line_iterator():
            
        if tokens[1] == "type": # definition language operations

            if tokens[0] == "create":
                type_name = tokens[2]
                if catalogHandler.type_exists(type_name):
                    logWriter.write(line, False)
                else:
                    n_fields  = tokens[3]
                    primary_key_index = tokens[4]
                    fields = []
                    for field in range(int(n_fields)):
                        offset = 5 + field*2
                        field = {"name": tokens[offset], "dtype": tokens[offset+1]}
                        fields.append(field)
                    catalogHandler.add_type(type_name, primary_key_index, fields)
                    logWriter.write(line, True)
            elif tokens[0] == "delete":
                type_name = tokens[2]
                if catalogHandler.type_exists(type_name):
                    catalogHandler.remove_type(type_name)
                    logWriter.write(line, True)
                else:
                    logWriter.write(line, False)
            elif tokens[0] == "list":
                types = catalogHandler.get_types()
                outputWriter.write_types(types)

                if(types): logWriter.write(line, True)
                else: logWriter.write(line, False)
            else:
                raise Exception("Undefined operation:", tokens[0])

        elif tokens[1] == "record": # manipulation language operations
            type_name = tokens[2]
            if catalogHandler.type_exists(type_name):
                tree = catalogHandler.get_tree(type_name)
                fileHandler.mount_file(type_name, catalogHandler.get_page_settings(type_name))
                primary_key_index = catalogHandler.get_primary_key_index(type_name)

                if tokens[0] == "create":
                    fields    = tokens[3:]
                    primary_key, record_fields = catalogHandler.fix_fields_for_record(type_name, fields)
                    success = tree.insert(primary_key, record_fields, fileHandler)
                    logWriter.write(line, success)

                elif tokens[0] == "delete":
                    primary_key = tokens[3]
                    primary_key = catalogHandler.format_input(primary_key, catalogHandler.get_primary_key_dtype(type_name))
                    success = tree.delete(primary_key, fileHandler)
                    logWriter.write(line, success)


                    
                elif tokens[0] == "update":
                    fields    = tokens[4:]
                    primary_key, record_fields = catalogHandler.fix_fields_for_record(type_name, fields)
                    page_index = tree.search(primary_key)
                    if page_index == None: # record not found
                        logWriter.write(line, False)
                    else:                    
                        fileHandler.delete_record(page_index, primary_key)
                        fileHandler.write_record(page_index, record_fields)
                        logWriter.write(line, True)
                elif tokens[0] == "search":
                    primary_key = tokens[3]
                    search(primary_key, type_name)
                elif tokens[0] == "list":
                    page_indexes = tree.leaf_nodes()
                    if len(page_indexes) > 0:
                        for page_index in page_indexes:
                            _active, _n_records, _slot_activities, record_data_list = fileHandler.read_page(page_index)
                            for record_data in sorted(record_data_list):
                                record_data = catalogHandler.fix_fields_for_output(type_name, record_data)
                                outputWriter.write_fields(record_data)
                        logWriter.write(line, True)
                    else:
                        logWriter.write(line, False)

                elif tokens[0] == "filter":
                    primary_key, condition, key = re.split("([<>=])", tokens[3])
                    key = catalogHandler.format_input(key, catalogHandler.get_primary_key_dtype(type_name))
                    if condition == "=":
                        search(key, type_name)
                    elif condition == ">":
                        page_indexes = tree.filter(2, key)
                        if len(page_indexes) > 0:
                            for page_index in sorted(page_indexes):
                                _active, _n_records, _slot_activities, record_data_list = fileHandler.read_page(page_index)
                                for record_data in sorted(record_data_list):
                                    if record_data[0] <= key:
                                        continue
                                    record_data = catalogHandler.fix_fields_for_output(type_name, record_data)
                                    outputWriter.write_fields(record_data)
                            logWriter.write(line, True)
                        else:
                            logWriter.write(line, False)

                    elif condition == "<":
                        page_indexes = tree.filter(1, key)
                        if len(page_indexes) > 0:
                            for page_index in sorted(page_indexes):
                                _active, _n_records, _slot_activities, record_data_list = fileHandler.read_page(page_index)
                                for record_data in sorted(record_data_list):
                                    if record_data[0] >= key:
                                        continue
                                    record_data = catalogHandler.fix_fields_for_output(type_name, record_data)
                                    outputWriter.write_fields(record_data)
                            logWriter.write(line, True)
                        else:
                            logWriter.write(line, False)

                    else:
                        raise Exception("Undefined condition:", condition)
                else:
                    raise Exception("Undefined operation:", tokens[0])
            else:
                logWriter.write(line, False)                    
        else:
            raise Exception("Undefined operation type:", tokens[1])
        
        # outputWriter.helper(tokens)
        # logWriter.write(line, True)




    
    outputWriter.close()
    logWriter.close()
    catalogHandler.close()
