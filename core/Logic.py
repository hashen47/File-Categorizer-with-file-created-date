import os
import shutil
import json
from datetime import datetime



class Categorizer:

    OUTPUT_FOLDER_NAME = "OUTPUT"
    TYPES = ["copy", "move"]


    def __init__(self, src, dst, func, type : int = 0):
        self.type = Categorizer.TYPES[type]
        self.progress = 0 # get the progress value from the gui
        self.finish_items = 0 # the total count that compleatly move or copy
        self.total_items = 0 # the total files and dir count that have to move or copy
        self.update_func = func # the update function of the Gui(Gui class)

        # don't change the below method order
        self.set_type(type)
        self.set_src(src)
        self.set_target(dst)
        self.set_all_files_dirs()
        self.set_target_folder_structure()
        self.create_target_folders()
        self.move_or_copy_files()


    def set_type(self, type):
        """
        set type copy or move
        :param type : int
        :return None
        """
        try:
            index = int(type)

            if index == 0 or index == 1:
                self.type = Categorizer.TYPES[type]
            else:
                raise Exception("Invalid type, it should be either 0 or 1")

        except Exception as e:
            print(e)
            exit()


    def set_src(self, src):
        """
        set src folder 
        :param src : str
        :return None
        """
        try:
            # check if path is exists
            if os.path.exists(src):

                # then check this path is a dir or not
                if os.path.isdir(src):
                    self.src = src 
                else:
                    raise Exception("The given src path is not pointing to a directory")
            else: 
                raise Exception("The given src path to source is invalid")

        except Exception as e:
            print(e)
            exit()


    def set_target(self, dst):
        """
        set target folder (dst/OUTPUT_FOLDER_NAME)
        :param dst : str
        :return None
        """
        try:
            # check if path is exists
            if os.path.exists(dst):

                # then check this path is a dir or not
                if os.path.isdir(dst):
                    self.target = os.path.join(dst, Categorizer.OUTPUT_FOLDER_NAME)
                else:
                    raise Exception("The given dst path is not pointing to a directory")
            else: 
                raise Exception("The given dst path to source is invalid")

        except Exception as e:
            print(e)
            exit()


    def set_all_files_dirs(self):
        """
        get the all files and folders of the src path
        and set it to self.all property
        :return None
        """
        try:
            self.all = list(os.walk(self.src).__next__())
            root, dirs, _ = self.all 

            if Categorizer.OUTPUT_FOLDER_NAME in dirs:
                if os.path.join(root, Categorizer.OUTPUT_FOLDER_NAME) == self.target:
                    self.all[1].remove(Categorizer.OUTPUT_FOLDER_NAME) # delete output folder from the dirs
            
            # set the total tiles and folder counts that hove to move or copy
            self.set_total_items()
            self.update_func(self.progress, self.total_items, self.finish_items)

        except Exception as e:
            print(e)
            exit()

    
    def set_total_items(self):
        """
        set total_items that have to copy
        if any file that in source already exists in the dstination's sub directory
        that file is skip
        :return None
        """
        _, dirs, files = self.all

        for folder in dirs:
            path = os.path.join(self.target, self.get_cdate(folder), folder)
            if not os.path.exists(path):
                    self.total_items += 1

        for file in files:
            path = os.path.join(self.target, self.get_cdate(file), file)
            if not os.path.exists(path):
                    self.total_items += 1


    def get_cdate(self, name):
        """
        return the created date of the given file 
        :params name : str
        :return cdate : str (ex - 2023-04-03)
        """
        try:
            path = os.path.join(self.src, name)
            cdate = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d")
            return cdate

        except FileNotFoundError:
            print(f"{name} file/folder is not exists in the source folder")
            exit()

        except Exception as e:
            print(e)
            exit()


    def set_target_folder_structure(self):
        """
        set target_folder_structure according to the source folder files and folders created date
        :return None
        """
        try:
            self.target_folder_structure = []
            _, dirs, files = self.all

            for d in dirs:
                cdate = self.get_cdate(d)
                if cdate not in self.target_folder_structure:
                    self.target_folder_structure.append(cdate)

            for file in files:
                cdate = self.get_cdate(file)
                if cdate not in self.target_folder_structure:
                    self.target_folder_structure.append(cdate)

        
        except Exception as e:
            print(e)
            exit()


    def create_target_folders(self):
        """
        create target folder structure according to the value of self.target_folder_structure values
        :return None
        """
        try:
            # create the target folder
            if not os.path.exists(self.target):
                os.mkdir(self.target)

            # then create the sub folders
            for folder in self.target_folder_structure:
                path = os.path.join(self.target, folder)
                if not os.path.exists(path):
                    os.mkdir(path)

        except Exception as e:
            print(e)
            exit()

    
    def copy_or_move_print(self, src:str, dst:str) -> None:
        """
        print the file previous path and copy or move path values with some alignments using fstrings
        :param src: str 
        :param dst: str
        :return None
        """
        print(f"{src:<70}   =>        {dst}")


    def move_or_copy_files(self):
        """
        move or copy file in the self.src path to self.target path sub folders
        not replace anything that already exists in the self.target sub folders
        :return None
        """
        try:
            root, dirs, files = self.all

            # copy all the folders of the src to DIRECTORY sub folder
            for folder in dirs:
                if not os.path.exists(os.path.join(self.target, self.get_cdate(folder), folder)):
                    if self.type == "copy":
                        shutil.copytree(os.path.join(root, folder), os.path.join(self.target, self.get_cdate(folder), folder))
                    elif self.type == "move":
                        shutil.move(os.path.join(root, folder), os.path.join(self.target, self.get_cdate(folder)))

                    self.copy_or_move_print(os.path.join(self.src, folder), os.path.join(self.target, self.get_cdate(folder), folder))
                    self.finish_items += 1 
                    self.progress = 100 * self.finish_items / self.total_items
                    self.update_func(int(self.progress), self.total_items, self.finish_items)


            # copy all files to the sub direcotories according to their extension
            for file in files:
                if not os.path.exists(os.path.join(self.target, self.get_cdate(file), file)):
                    if self.type == "copy":
                        shutil.copy(os.path.join(root, file), os.path.join(self.target, self.get_cdate(file)))
                    else:
                        shutil.move(os.path.join(root, file), os.path.join(self.target, self.get_cdate(file)))

                    self.copy_or_move_print(os.path.join(root, file), os.path.join(self.target, self.get_cdate(file), file))
                    self.finish_items += 1 
                    self.progress = 100 * self.finish_items / self.total_items
                    self.update_func(int(self.progress), self.total_items, self.finish_items)

            # set compleated to True
            self.update_func(int(self.progress), self.total_items, self.finish_items, compleated=True)
        
        except Exception as e:
            print(e)
            exit()