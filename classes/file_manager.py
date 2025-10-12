import csv
import json
import yaml
import os
from PIL import Image, ImageFilter

from .image_operation import ImageSpecification
from utils import create_new_image

class FileManager():
    """A Static class made to handle reading different types of file extensions
    Supported file format: .csv, .json, .yaml
    """
    @staticmethod
    def read_file(file_path: str, image_list: str):
        """Reads file from designated file path
        checks file extension for supported file types (.csv, .json, .yaml)

        Args:
            file_path (str): the relative file path containing the csv file
            image_list (str): A list served as container for all created ImageSpecification instances
        """
        with open(file_path, "r") as f_obj:
            # Handles different types of file
            if file_path.endswith(".csv"):
                file = csv.DictReader(f_obj)
            elif file_path.endswith(".json"):
                file = json.load(f_obj)
            elif file_path.endswith(".yaml"):
                file = yaml.safe_load(f_obj)
            else:
                print("Error: File type not supported")

            for file_info in file:
                try:
                    create_new_image(file_info, image_list, file_path)
                except ValueError as error:
                    raise ValueError(error)
    
    @staticmethod
    def validate_folders(root_dir="."):
        """Validates required directories, if directory does not exist creates them
        Checks for images folder as parent folder
        the checks config, input, output folder which are subfolders of images

        Args:
            root_dir (str, optional): the root directory of where the folders are. Defaults to ".".

        Returns:
            dict: dictionary containing the relative folder paths of all required folders and subfolders
        """
        # Gets image folder directory, checks if it exist, if not makes the folder
        image_folder = os.path.join(root_dir, "images")
        if not os.path.exists(image_folder):
            os.makedirs(image_folder, exist_ok=True)
        print(f"Image Folder:{image_folder}")
        
        # Defines the config, input and output subfolders directory
        config_folder = os.path.join(image_folder, "config")
        input_folder = os.path.join(image_folder, "input")
        output_folder = os.path.join(image_folder, "output")
        subfolders = [
            (config_folder, "config"),
            (input_folder, "input"),
            (output_folder, "output")
        ]
        
        # Checks if each subfolder exist, if not makes said folder
        for folder_path, folder_name in subfolders:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
            print(f"{folder_name.capitalize()} Folder: {folder_path}")
        
        # Returns a dictionary containing the directory of each folder
        return {
            "image_folder": image_folder,
            "config_folder": config_folder,
            "input_folder": input_folder,
            "output_folder": output_folder
        }
    
    @staticmethod
    def get_configs(config_path: str):
        """From config path gets all valid configs
        Supported file type: .csv, .json, .yaml

        Args:
            config_path (str): config folder path

        Returns:
            list: list of all files with valid supported extensions
        """
        config_list = os.listdir(config_path)
        valid_configs = []
        for config in config_list:
            _, file_type = config.split(".")
            if file_type in ["csv", "json", "yaml"]:
                valid_configs.append(config)
        return valid_configs
    
    @staticmethod
    def save_image(image: Image.Image, image_specs: ImageSpecification, output_folder: str):
        """Saves generated image to output folder

        Args:
            image (Image.Image): Image object from PIL Library, contains the generated image
            image_specs (ImageSpecification): ImageSpecification instance with the corresponding output name
            output_folder (str): output folder directory
        """
        output_name = image_specs.output_name
        output_path = os.path.join(output_folder, output_name)
        image.save(output_path, optimize=True)
        