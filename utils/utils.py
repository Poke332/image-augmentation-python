from classes import ImageSpecification

def create_new_image(image_dict: dict, image_list: list, file_name:str):
    """Function tasked with creating new images using ImageSpecification from_dict method

    Args:
        image_dict (dict): Image dictionary containing all the required keys (image_name, operation, output_name)
        image_list (list): A list served as container for all created ImageSpecification instances
    """
    try:
        new_image = ImageSpecification.from_dict(image_dict)
        image_list.append(new_image)
    except ValueError as error:
        raise ValueError(f"Error: Failed to create Image object, {error}\nDetails:\n\tInvalid config format on {file_name}\n\t{image_dict}")