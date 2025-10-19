from PIL import Image, ImageFilter
import os

class ImageSpecification():
    """Class containing information about the image
    
    This class is used to store information regarding image name,
    what rotate,resize,crop,past,filter,etc operation to apply,
    and the output file name when operation succeeds
    """
    def __init__(self, file_name: str, operation: str, output_name: str):
        """initializes ImageSpecification

        Args:
            file_name (str): string of file name, must end with the file's type (.jpg, .jpeg, .png, etc)
            operation (str): string of operation to be applied, refer to Readme file for .json, .csv, .yaml format
            output_name (str): string of file name when the file is ready to be saved/outputted
        """
        self._file_name = file_name
        self._operation = operation
        self._output_name = output_name
        
    @property
    def file_name(self):
        return self._file_name
    
    @property
    def operation(self):
        return self._operation
    
    @property
    def output_name(self):
        return self._output_name
    
    @classmethod
    def from_dict(cls, image_dict: dict):
        """Class method of making instances from dictionaries

        Args:
            image_dict (dict): a dictionary which must contain image_name, operation, output_name as its keys

        Returns:
            Object/Instance: creates an instances of the current ImageSpecification class based on information from the dictionary
        """
        file_name = image_dict.get("image_name")
        operation = image_dict.get("operation")
        output_name = image_dict.get("output_name")
        return cls(file_name, operation, output_name)
    
    def __str__(self):
        return f"ImageSpecification(\n\t{self.file_name},\n\t{self.operation},\n\t{self.output_name})"
            
    def process_image(self, input_folder: str, watermark_fname=""):
        """Processes the image based on specifications
        Supported processing:
            - Resized Image
            - Rotated Image
            - Cropped Image
            - Pasted Image
            - Gaussian Blur
            - Contour

        Args:
            input_folder (str): the input folder directory where all source images are stored
            watermark_fname (str, optional): The watermark file name that will be used for pasting over an image. Defaults to None.
            
        Raises:
            IndexError: If the degree of rotation is not specified, ex: expected "rotate_[degrees]" but received only "rotate"
            ValueError: If program asks for a tuple but receives none instead due to incomplete values on operations, or operation read by program is not supported
            
        Returns:
            Image.Image: the Image object generated using python's PIL module

        """
        with Image.open(os.path.join(input_folder, self.file_name)) as img:
            # Splits instructs into 2 entries, first entry is the type of processing to the done, and if 2nd entry exist then that is the details needed
            instructions = self.operation.split("_", 1)
            # Checks for all operations other than rotate
            if len(instructions) == 2 and instructions[0] != "rotate":
                operation, detail = instructions
                #Splits the details (point coordinates) into a tuple of absolute value integers
                converted_details = tuple(map(lambda x: abs(int(x)), detail.split("_"))) or None
            # If details are not found then set to none
            else:
                operation, converted_details = instructions[0], None
            
            # Resize processing
            if operation == "resize":
                img = img.resize(converted_details)
            # Rotate processing
            elif operation == "rotate":
                # Rotation details are handled in its own cluster
                try:
                    # Converts degree details into an absolute value float
                    deg = abs(float(instructions[1]))
                    img = img.rotate(deg)
                except:
                    raise IndexError("No degree of rotation is specified, image processing not ran due to same input and output")
            # Crop processing
            elif operation == "crop":
                if converted_details == None:
                    raise ValueError("Cropping with None results in original image")
                img = img.crop(converted_details)
            # Paste processing
            elif operation == "paste":
                # Opens watermark
                with Image.open(os.path.join(input_folder, watermark_fname)) as watermark:
                    img.paste(watermark, converted_details)
            # Gaussian blur processing
            elif operation == "blur":
                img = img.filter(ImageFilter.GaussianBlur)
            # Contour processing
            elif operation == "contour":
                img = img.filter(ImageFilter.CONTOUR)
            else:
                raise ValueError(f"Invalid type of process, {operation} is not supported")
            
            # Returns output image
            return img