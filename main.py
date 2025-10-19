from classes.file_manager import FileManager
from tqdm import tqdm
import os

error_log = []
image_list = []
count = 0

if __name__ == "__main__":
    while True:
        # Ensures clean terminal and validates essential folders
        os.system('cls' if os.name == 'nt' else 'clear')
        folders = FileManager.validate_folders()
        
        # Finds all valid config files in config folder
        config_folder = folders.get("config_folder")
        configs = FileManager.get_configs(config_folder)
        print(f"Found configs: {configs}\n")
        
        # If no configs with proper instructions are found then prompts the user to try again after they've inputted correct configs
        if len(configs) == 0:
            print(f"\nPlease add or make a config file inside {config_folder} before proceeding\nSupported filetypes: .csv, .json, .yaml\nFor data format refer to .\\Readme.md\n")
            input("Press \"Enter\" to try again")
            continue


        # Reads each config files with supported file types and makes
        for file in configs:
            # Tries to read config files, if error is found then list them inside error_log
            try:
                FileManager.read_file(os.path.join(config_folder, file), image_list)
            except ValueError as error:
                error_log.append(f"{error}")
        print(f"\nTotal found instructions: {len(image_list)}\n")
        
        print("BE WARNED: ALL OUTPUT WITH SAME NAME WILL OVERRIDE ONE ANOTHER!\nProcessing Images...")
        # Iterates all detected images and processes them
        for image in tqdm(image_list):
            # Tries to process the image, if error is found then list them inside error_log
            try:
                # Processes images and saves it into output_folder, count the total successful processing
                input_folder = folders.get("input_folder")
                output = image.process_image(input_folder, "watermark.png")
                output_folder = folders.get("output_folder")
                FileManager.save_image(output, image, output_folder)
                count+=1
            # WHen an error occurs, checks for the type of error and appends the error message into error_log list
            except FileNotFoundError as error: # If input file or watermark file not found
                error_log.append(f"Cannot find file specified in {image}\nDetails:\n\t{error}")
            except PermissionError as error: # If folder directory is located in a restricted folder
                error_log.append(f"Specified file cannot be accessed\nDetails:\n\t{error}")
            except ValueError as error: # If any invalid values are found in the process
                error_log.append(f"Invalid value found in {image}\nDetails:\n\t{error}")
            except TypeError as error: # If any input were of invalid typing, ex: Expecting coords as a tuple of int but gets string instead
                error_log.append(f"Attempted processing with invalid type in {image}\nDetails:\n\t{error}")
            except IndexError as error: # The program splits instructions and the degress/coordinate by index, if one does not exist or program tries to access invalid index this error is raised
                error_log.append(f"Tried to access an invalid index value in {image}\nDetails:\n\t{error}")
            except MemoryError as error: # In cases where resize are made ubsurdly high which consumes too much memory
                error_log.append(f"Ran out of memory processing {image}\nDetails:\n\t{error}")
            except Exception as error: # Any other undetected errors will go into here
                error_log.append(f"Unknown error has occurned {image}\nDetails:\n\t{error}")
        print(f"\nTotal Image Processed: {count}/{len(image_list)}")
        
        # Compiles errors inside error_log into a txt file
        with open(".\\images\\logs.txt", "w") as file:
            file.write("\n".join(error_log))
        print("For error logs refer to .\\images\\logs.txt")
        break

