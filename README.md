# Peko app

## Table of contents
- [Peko app](#peko-app)
  - [Table of contents](#table-of-contents)
  - [General info](#general-info)
  - [Setup](#setup)
  - [App Features](#app-features)
- [Resourses](#resourses)


## General info
This python project provides some basic images filters and basic image meta extraction with a smooth GUI.
![Alt text](images/doc_images/home.png "Peko Home Page")


## Setup
1. install the task requirements
```
pip install -r requirements.txt
```
2. run the script
```
python main.py
```

## App Features
1. Image Meta Extactor
    # extract basic meta data from a selected image
    ![Alt text](images/doc_images/img_meta_before.png)
    ![Alt text](images/doc_images/img_meta_after.png)

2. Peko superNova
    # apply combination of filters to the selected image
     * applied fliters
       * Saturation
       * Contrast
       * Brightness
    ![Alt text](images/doc_images/supermove_home.png)
    ![Alt text](images/doc_images/pekosprnva_before.png)
    ![Alt text](images/doc_images/pekosprnva_after.png)

3. Black&White filter
    # apply black and white filter to the selected image
    ![Alt text](images/doc_images/b&w_before.png)
    ![Alt text](images/doc_images/b&w_after.png)

4. Copyright page
    # copyright page to reserve all the rights to the peko app developers
   ![Alt text](images/doc_images/copyright.png)

# Resourses
* Frames swithing mechanism code -> https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter