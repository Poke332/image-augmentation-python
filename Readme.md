# **Image Data Augmentation Project**  
This projects explores the process of creating new images using existing images by usage of python's PIL module. This is a process often used to augment new data for AI by using already existing data to make new data.

#### Project Dependencies: 
> - Pillow
> - PyYAML
> - tqdm

---
###### By Team 13  
###### - Richie Cedrick Adrian (01881250010)  
###### - Jasmine Regina (01881250055)
###### - Ivan Pratama (01881250004)
---
## How to Operate the Program  
### 1. Preparing the Essential Files  
#### 1.1 Preparing Images
All image file supported by Pillow's `Image.open()` method is supported
Save your images inside `.\images\input` folder
__MUST HAVE `watermark.png` FILE IN INPUT FOLDER__
#### 1.2 Preparing Configs
Supported config file types: `.csv .json .yaml`
All config files are saved to: `.\images\config`
#### Config File Format:
Operations follow a certain format:
 - Resize: `resize_x_y`
 - Crop: `crop_x0_y0_x1_y1`
 - Rotate: `rotate_deg`
 - Paste: `paste_x_y`
 - Blur: `blur`
 - Contour: `contour`

For configs you may choose one or more from the following:
##### 1.2.1 CSV Files
The following is the format inside .csv file:  

    image_name,operation,output_name <- Required Header section
    test.jpeg,resize_600_500,test_resize_1.png
    test.jpeg,crop_0_0_100_100,test_crop_1.png
    ...

##### 1.2.2 JSON Files
The following is the format inside .json file: 

    [
        {
            "image_name": "test.jpeg",
            "operation": "resize_600_500",
            "output_name": "test_resize_1.png"
        },
        {
            "image_name": "test.jpeg",
            "operation": "crop_0_0_100_100",
            "output_name": "test_crop_1.png"
        },
        ...
    ]

##### 1.2.3 YAML Files
The following is the format inside .yaml file: 

    - image_name: test.jpeg
      operation: resize_600_500
      output_name: test_resize_1.png
    - image_name: test.jpeg
      operation: crop_0_0_100_100
      output_name: test_crop_1.png
    - ...

### 2. Running the Code:  
Ensure all dependencies are installed:  
>  `pip install -r requirements.txt`  

On root directory terminal run:  
>  `py main.py`  

Processed images are saved inside:
> `.\images\output`  

For error logs are found:
> `.\images\logs.txt`