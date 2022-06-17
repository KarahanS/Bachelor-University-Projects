import os
from pathlib import Path

from settings import settings

class FileHandler:

    def __init__(self):
        self.f = None

    def create_initial_file(self):
        """Creates the initial file
        for a type.

        Args:
            type_name (str): name of the type. File is created
                with the same name.
            record_data_size (int): number of bytes needed to store
                a single record of the type.
        """
        self.add_page(0)
        
    def add_page(self, page_index):

        if page_index >= settings.MAX_PAGE_INDEX:
            raise Exception("File is out of space. Can not add more records")

        active = self.get_page_is_active(page_index)
        self.seek_page(page_index)

        if active == b"1": 
            raise Exception("Tried to create a page at an index where a page already exists.")
        elif active == b"0": # activate soft deleted page
            self.f.write(b"1")

            for offset in self.record_offset_iterator(page_index):
                active = self.read_offset(offset, 1)
                if active not in [b"0", b"1"]:
                    raise Exception("Something went wrong when activating a soft deleted page. Unrecognized character:", active)
                self.write_offset(offset, b"0")

        elif active == b'': # page doesn't exist
            self.f.write(b"1")

            n_filled_slots = 0
            self.f.write(n_filled_slots.to_bytes(4, 'big'))

            n_slots = self.page_settings["n_records_per_page"]
            self.f.write(n_slots * (b"0%s\n" % (self.page_settings["record_data_size"] * b" ")))
            self.f.write(b"X" * self.page_settings["wasted_space"]) # empty space
        else:

            raise Exception("Something went wrong when adding a page. Unrecognized character:", active)

    def delete_page(self, page_index):
        active = self.get_page_is_active(page_index)
        if active == b"1":
            page_offset = self.get_page_offset(page_index)
            self.write_offset(page_offset, b"0")

            # TODO: Decide in what situation a page is removed from the end of the file
        elif active == b"0":
            raise Exception("Something went wrong when deleting a page. Page is already soft deleted.")
        elif active == b"":
            raise Exception("Something went wrong when deleting a page. Page doesn't exist.")
        else:
            raise Exception("Something went wrong when deleting a page. Unrecognized character:", active)

    def split_page(self, page_index, threshold):
        """Loads the page whose index is provided with
        page_index, identifies the records whose primary
        key is lower than the threshold are identified and
        their records are removed from the original page.
        They are then added to the new page.
        """
        active, n_records, slot_activities, record_data_list = self.read_page(page_index, False)
        next_page_index = self.get_next_available_page_index()
        self.add_page(next_page_index)
        for slot_active, record_data, offset in zip(slot_activities, record_data_list, self.record_offset_iterator(page_index)):
            if slot_active and record_data[0] >= threshold:
                self.write_offset(offset, b"0") # deactive slot
                self.write_record(next_page_index, record_data)

    def merge_pages(self, receiving_page_index, deleted_page_index):
        """Reads the to-be-deleted page, deletes it. Then adds the records
        to the receiving page.
        """
        active, n_records, slot_activities, record_data_list = self.read_page(deleted_page_index)
        self.delete_page(deleted_page_index)
        for record_data in record_data_list:
            self.write_record(receiving_page_index, record_data)

    def get_next_available_page_index(self):
        index = 0
        while True:
            active = self.read_offset(self.get_page_offset(index), 1)
            if active in [b"", b"0"]:
                return index
            index += 1

    def read_page(self, page_index, ignore_deleted_records=True):
        content = self.read_offset(self.get_page_offset(page_index), settings.PAGE_SIZE)
        active = content[0] == 49 # 49 is "1" in ascii
        n_records = int.from_bytes(content[1:5], "big") 
        body_content = content[settings.HEADER_SIZE:]
        record_size = self.page_settings["record_size"]
        record_data_list = [body_content[offset:offset+record_size] for offset in range(0, len(body_content),record_size)][:-1]
        
        if ignore_deleted_records:
            record_data_list = [data for data in record_data_list if data[0] == 49] # remove availability

        slot_activities = [data[0] == 49 for data in record_data_list]
        record_data_list = [data[1:] for data in record_data_list] # remove availability

        def extract_values(record_data):
            values = []
            for dtype in self.page_settings["dtypes"]:
                if dtype == "int":
                    values.append(int.from_bytes(record_data[:4], "big"))
                    record_data = record_data[4:]
                elif dtype == "str":
                    values.append(record_data[:settings.MAX_STR_LENGTH].decode("ascii").strip())
                    record_data = record_data[settings.MAX_STR_LENGTH:]
            return values


        record_data_list = list(map(extract_values, record_data_list))
                
        return active, n_records, slot_activities, record_data_list

    def read_record(self, page_index, primary_key):
        active, n_records, slot_activities, record_data_list = self.read_page(page_index)
        for record_data in record_data_list:
            if record_data[0] == primary_key:
                return record_data

    def write_record(self, page_index, values):
        for offset in self.record_offset_iterator(page_index):
            active = self.read_offset(offset, 1)
            if active == b"0":
                record_data = self.encode_record(values)
                self.write_offset(offset, b"1" + record_data)
                return

    def delete_record(self, page_index, primary_key):
        for offset in self.record_offset_iterator(page_index):
            primary_key_dtype = self.page_settings["dtypes"][0]
            if primary_key_dtype == "str":
                key = self.read_offset(offset+1, settings.MAX_STR_LENGTH).decode("ascii").strip()
            elif primary_key_dtype == "int":
                key = int.from_bytes(self.read_offset(offset+1, 4), "big")
            else:
                raise Exception("Unrecognized dtype:", primary_key_dtype)

            if key == primary_key:
                self.write_offset(offset, b"0")

                return


    # Mount file

    def __get_file_path(self, type_name):
        return os.path.join(settings.FILE_FOLDER_PATH, type_name + ".bin")

    def delete_file(self):
        file_path = self.__get_file_path(self.type_name)
        self.dismount_file()
        os.remove(file_path)

    def mount_file(self, type_name, page_settings):
        self.type_name = type_name
        self.page_settings = page_settings
        file_path = self.__get_file_path(type_name)
        Path(file_path).touch() # make sure that the file exists before reading it.
        if self.f:
            self.f.close()
        self.f = open(file_path, "rb+")

    def dismount_file(self):
        self.f.close()
        self.page_settings["record_data_size"] = None
        self.type_name = None

    def get_page_offset(self, page_index):
        return page_index * settings.PAGE_SIZE

    def get_page_is_active(self, page_index):
        page_offset = self.get_page_offset(page_index)
        return self.read_offset(page_offset, 1)

    # Move file pointer

    def seek_page(self, page_index):
        page_offset = self.get_page_offset(page_index)
        self.f.seek(page_offset)
    
    def read_offset(self, offset, byts):
        self.f.seek(offset)
        return self.f.read(byts)

    def write_offset(self, offset, byts):
        self.f.seek(offset)
        return self.f.write(byts)

    # Offset iterator

    def record_offset_iterator(self, page_index):
        page_body_offset = self.get_page_offset(page_index) + settings.HEADER_SIZE
        record_size = self.page_settings["record_size"]
        for i in range(self.page_settings["n_records_per_page"]):
            yield page_body_offset
            page_body_offset += record_size

    def encode_record(self, values):
        binary = b""
        for value, dtype in zip(values, self.page_settings["dtypes"]):
            binary += self.binarize_value(value, dtype)
        return binary

    def binarize_value(self, value, dtype):
        if dtype == "str":
            return value.encode("ascii").ljust(settings.MAX_STR_LENGTH)
        elif dtype == "int":
            return value.to_bytes(4, "big")
        else:
            raise Exception("Unrecognized dtype in dtypes:", dtype)

    

if __name__ == "__main__":
    pass