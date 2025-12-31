"""
DICOM utility functions for tag operations, element extraction, and file manipulation.
"""

import os
import time
import glob
import json
from pathlib import Path
from typing import List
from pydicom import dcmread
from pydicom import datadict


def get_dcm_files(directory: str) -> List[str]:
    """Get all DICOM files in directory recursively."""
    # Normalize path for cross-platform compatibility
    directory = os.path.normpath(directory)
    
    # Try recursive glob first (more efficient)
    try:
        # Use os.path.join for cross-platform path handling
        search_pattern = os.path.join(os.path.realpath(directory), '**', '*.dcm')
        files = glob.glob(search_pattern, recursive=True)
        if files:
            return sorted(files)
    except Exception as e:
        # If recursive glob fails, fall through to non-recursive search
        pass
    
    # Fallback to non-recursive search (also handles subdirectories manually)
    dcm_files = []
    if not os.path.exists(directory):
        return dcm_files
    
    def search_recursive(dir_path: str) -> List[str]:
        """Recursively search for DICOM files."""
        found_files = []
        try:
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path):
                    # Check for common DICOM extensions
                    if item.lower().endswith(('.dcm', '.dicom')):
                        found_files.append(item_path)
                elif os.path.isdir(item_path):
                    # Recursively search subdirectories
                    found_files.extend(search_recursive(item_path))
        except PermissionError:
            # Skip directories we don't have permission to access
            pass
        except Exception:
            # Skip other errors and continue
            pass
        return found_files
    
    dcm_files = search_recursive(directory)
    return sorted(dcm_files)


def generate_unique_id() -> str:
    """
    Generate a unique ID based on current timestamp in nanoseconds.
    
    Returns:
        String representation of timestamp in nanoseconds
    """
    timestamp = time.time_ns()
    timestamp_str = str(timestamp)
    unique_id = timestamp_str
    return unique_id


def update_tags_ds(ds, tag_name: str, value):
    """
    Update a DICOM tag in a dataset.
    
    Args:
        ds: pydicom Dataset object
        tag_name: Name of the tag to update (e.g., "StudyInstanceUID")
        value: Value to set for the tag
    """
    if tag_name == "SpecimenLabelInImage":
        ds.SpecimenLabelInImage = value
    if tag_name == "BurnedInAnnotation":
        ds.BurnedInAnnotation = value
    if tag_name == "StudyInstanceUID":
        ds.StudyInstanceUID = value
    if tag_name == "SeriesInstanceUID":
        ds.SeriesInstanceUID = value
    if tag_name == "DimensionOrganizationType":
        ds.DimensionOrganizationType = value
    if tag_name == "SOPClassUID":
        ds.SOPClassUID = value
    if tag_name == "SOPInstanceUID":
        ds.SOPInstanceUID = value
    if tag_name == "BarcodeValue":
        ds.BarcodeValue = value
    if tag_name == "NumberOfFrames":
        ds.NumberOfFrames = value
    if tag_name == "AccessionNumber":
        ds.AccessionNumber = value
    if tag_name == "ContainerIdentifier":
        ds.ContainerIdentifier = value
    if tag_name == "StudyInstanceUID":
        ds.StudyInstanceUID = value
    if tag_name == "FrameOfReferenceUID":
        ds.FrameOfReferenceUID = value
    if tag_name == "PatientID":
        ds.PatientID = value
    if tag_name == "PatientName":
        ds.PatientName = value
    if tag_name == "PatientBirthDate":
        ds.PatientBirthDate = value
    if tag_name == "InstitutionName":
        ds.InstitutionName = value
    if tag_name == "ReferringPhysicianName":
        ds.ReferringPhysicianName = value
    if tag_name == "DeviceSerialNumber":
        ds.DeviceSerialNumber = value
    
    # Handle private tags
    if tag_name == "30210010":
        if (0x3021, 0x0010) in ds:
            ds[0x3021, 0x0010].value = value
    if tag_name == "30211001":
        if (0x3021, 0x1001) in ds:
            ds[0x3021, 0x1001].value = value
    if tag_name == "30211003":
        if (0x3021, 0x1003) in ds:
            ds[0x3021, 0x1003].value = value
    if tag_name == "30211004":
        if (0x3021, 0x1004) in ds:
            ds[0x3021, 0x1004].value = value
    if tag_name == "00020002":
        if (0x0002, 0x0002) in ds:
            ds[0x0002, 0x0002].value = value
    if tag_name == "00100040":
        if (0x0010, 0x0040) in ds:
            ds[0x0010, 0x0040].value = value
    
    return ds


def update_tags(dcm_file, tag_name, value):
    """
    Update a DICOM tag in a file.
    
    Args:
        dcm_file: Path to DICOM file
        tag_name: Name of the tag to update
        value: Value to set for the tag
    """
    ds = dcmread(dcm_file)
    update_tags_ds(ds, tag_name, value)
    ds.save_as(dcm_file)


def add_tags(dcm_file, tag_name, value):
    """
    Add a new DICOM tag to a file.
    
    Args:
        dcm_file: Path to DICOM file
        tag_name: Name of the tag to add
        value: Value for the tag
    """
    ds = dcmread(dcm_file)
    if tag_name == "SpecimenLabelInImage":
        ds.add_new(0x00480010, 'CS', value)
    if tag_name == "BurnedInAnnotation":
        ds.add_new(0x00280301, 'CS', value)
    if tag_name == "StudyInstanceUID":
        ds.add_new(0x0020, 0x000d, 'UI', value)
    if tag_name == "SeriesInstanceUID":
        ds.add_new(0x0020, 0x000e, 'UI', value)
    if tag_name == "DimensionOrganizationType":
        ds.add_new(0x00209311, 'CS', value)
    ds.save_as(dcm_file)


def remove_tags(dcm_file, tag_name):
    """
    Remove a DICOM tag from a file.
    
    Args:
        dcm_file: Path to DICOM file
        tag_name: Name of the tag to remove
    """
    ds = dcmread(dcm_file)
    if tag_name == "BarcodeValue":
        if (0x2200, 0x0005) in ds:
            del ds[0x2200, 0x0005]
    if tag_name == "PatientSex":
        if (0x0010, 0x0040) in ds:
            del ds[0x0010, 0x0040]
    ds.save_as(dcm_file)


def get_tag_value(dcm_file, tag_name):
    """
    Get a tag value from a DICOM file.
    
    Args:
        dcm_file: Path to DICOM file
        tag_name: Name of the tag to retrieve
        
    Returns:
        Tag value or None
    """
    ds = dcmread(dcm_file)
    if tag_name == "StudyInstanceUID":
        return ds[0x0020, 0x000d].value
    return None


def update_tags_all_files(dir, tag_name, value):
    """
    Update a tag in all DICOM files in a directory.
    
    Args:
        dir: Directory containing DICOM files
        tag_name: Name of the tag to update
        value: Value to set for the tag
    """
    files = get_dcm_files(dir)
    for dcm_file in files:
        update_tags(dcm_file, tag_name, value)


def update_bar_code_file(dcm_file, new_bar_code):
    """
    Update the barcode value in a DICOM file.
    
    Args:
        dcm_file: Path to DICOM file
        new_bar_code: New barcode value
    """
    ds = dcmread(dcm_file)
    ds.BarcodeValue = new_bar_code
    ds.save_as(dcm_file)


def update_bar_code_all_files(dir, new_bar_code):
    """
    Update barcode value in all DICOM files in a directory.
    
    Args:
        dir: Directory containing DICOM files
        new_bar_code: New barcode value
    """
    files = get_dcm_files(dir)
    for dcm_file in files:
        update_bar_code_file(dcm_file, new_bar_code)


def update_image_type_file(dcm_file, new_image_type):
    """
    Update the ImageType tag in a DICOM file.
    
    Args:
        dcm_file: Path to DICOM file
        new_image_type: New ImageType value (e.g., ['DERIVED', 'PRIMARY', 'VOLUME', 'RESAMPLED'])
    """
    ds = dcmread(dcm_file)
    ds.ImageType = new_image_type
    ds.save_as(dcm_file)


def update_dim_org_type(dcm_file, new_dim_org_type):
    """
    Update the DimensionOrganizationType tag in a DICOM file.
    
    Args:
        dcm_file: Path to DICOM file
        new_dim_org_type: New DimensionOrganizationType value
    """
    ds = dcmread(dcm_file)
    ds.DimensionOrganizationType = new_dim_org_type
    ds.save_as(dcm_file)


def is_valid_tag(keyword):
    """
    Check if a DICOM tag keyword is valid.
    
    Args:
        keyword: DICOM tag keyword
        
    Returns:
        True if valid, False otherwise
    """
    if datadict.tag_for_keyword(keyword) is None:
        return False
    return True


def get_dicom_dataset(dcm_file: str, metadata_folder: str, metadata_file_name: str):
    """
    Extract DICOM metadata and save to a text file.
    
    Args:
        dcm_file: Path to DICOM file
        metadata_folder: Directory to save metadata file
        metadata_file_name: Name of the metadata file to create
    """
    try:
        ds = dcmread(dcm_file)
        
        # Create metadata folder if it doesn't exist
        os.makedirs(metadata_folder, exist_ok=True)
        
        # Create metadata file path
        metadata_path = os.path.join(metadata_folder, metadata_file_name)
        
        # Write metadata to file
        with open(metadata_path, 'w') as f:
            f.write(f"DICOM Metadata for: {dcm_file}\n")
            f.write("=" * 80 + "\n\n")
            
            # Write key tags
            key_tags = [
                "PatientID", "PatientName", "StudyInstanceUID", "SeriesInstanceUID",
                "SOPInstanceUID", "Modality", "StudyDate", "SeriesDate",
                "DeviceSerialNumber"
            ]
            
            for tag_name in key_tags:
                if hasattr(ds, tag_name):
                    value = getattr(ds, tag_name)
                    f.write(f"{tag_name}: {value}\n")
            
            # Write all tags
            f.write("\n" + "=" * 80 + "\n")
            f.write("All DICOM Tags:\n")
            f.write("=" * 80 + "\n\n")
            
            for elem in ds:
                f.write(f"{elem.tag} {elem.keyword}: {elem.value}\n")
                
    except Exception as e:
        print(f"Error extracting metadata from {dcm_file}: {e}")


def get_folders(folder_path: str) -> List[str]:
    """
    List all folders in the directory and return the full path.
    
    Args:
        folder_path: Path to directory
        
    Returns:
        List of full paths to subdirectories
    """
    folders = []
    if not os.path.exists(folder_path):
        return folders
    
    for f in os.listdir(folder_path):
        full_path = os.path.join(folder_path, f)
        if os.path.isdir(full_path):
            folders.append(full_path)
    
    return sorted(folders)


def get_image_index(n: int, t: int) -> int:
    """
    Calculate image index based on total count and row index.
    Uses modulo operation to cycle through available images.
    
    Args:
        n: Total number of images/folders
        t: Current row/index
        
    Returns:
        Image index to use
    """
    if t < n:
        return t
    # Recursively evaluate by subtracting n from t
    return get_image_index(n, t - n)


def ds_to_dict(ds):
    """
    Convert a DICOM dataset to a dictionary.
    
    Args:
        ds: pydicom Dataset object
        
    Returns:
        Dictionary representation of the DICOM dataset
    """
    out = {}
    for elem in ds:
        if elem.VR == "SQ":
            out[elem.name] = [ds_to_dict(item) for item in elem.value]
        else:
            out[elem.name] = str(elem.value)
    return out


def get_dicom_elements_file_nested(dcm_file: str, dest_folder: str):
    """
    Extract DICOM elements from a file and save in nested structure.
    
    Args:
        dcm_file: Path to DICOM file
        dest_folder: Destination folder to save extracted elements
    """
    try:
        ds = dcmread(dcm_file)
        
        # Create destination folder if it doesn't exist
        os.makedirs(dest_folder, exist_ok=True)
        
        # Convert dataset to dictionary
        ds_dict = ds_to_dict(ds)
        
        # Create output filename
        base_name = os.path.splitext(os.path.basename(dcm_file))[0]
        output_file = os.path.join(dest_folder, f"{base_name}_elements.json")
        
        # Write to JSON file
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ds_dict, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error processing {dcm_file}: {e}")


def get_dicom_elements_dir(dicom_dir: str, dest_folder: str):
    """
    Extract DICOM elements from all files in a directory.
    
    Args:
        dicom_dir: Directory containing DICOM files
        dest_folder: Destination folder to save extracted elements
    """
    dcm_files = get_dcm_files(dicom_dir)
    
    for dcm_file in dcm_files:
        print(f"Processing DICOM file: {dcm_file}")
        get_dicom_elements_file_nested(dcm_file, dest_folder)


def get_not_deidentified_list(deid_tags, dcm_file, dest_folder):
    """
    Check de-identification status of a DICOM file.
    
    Args:
        deid_tags: List of tag keywords to check for de-identification
        dcm_file: Path to DICOM file
        dest_folder: Destination folder for verification output
        
    Returns:
        List of tags that are not de-identified
    """
    ds = dcmread(dcm_file)
    not_deidentified_list = []
    deidentified_list = []
    not_existing_keys = []
    
    for deidtag in deid_tags:
        try:
            if not ds[deidtag].value or ds[deidtag].value == '':
                deidentified_list.append(f"{deidtag}:{str(ds[deidtag].value)}")
            else:
                not_deidentified_list.append(f"{deidtag}:{str(ds[deidtag].value)}")
        except KeyError:
            not_existing_keys.append(deidtag)
    
    metadata_file_name = os.path.join(dest_folder, os.path.basename(dcm_file) + "_deid_verification.txt")
    os.makedirs(dest_folder, exist_ok=True)
    
    with open(metadata_file_name, "w") as f:
        f.write(f"{dcm_file}\tNot deidentified list: {':'.join(not_deidentified_list)}\n")
        f.write(f"{dcm_file}\tDeidentified list: {':'.join(deidentified_list)}\n")
        f.write(f"{dcm_file}\tTags that do not exist: {':'.join(not_existing_keys)}\n")
    
    return not_deidentified_list


def get_not_deidentified_list_dir(deid_tags, dcm_dir, dest_folder):
    """
    Check de-identification status for all DICOM files in a directory.
    
    Args:
        deid_tags: List of tag keywords to check for de-identification
        dcm_dir: Directory containing DICOM files
        dest_folder: Destination folder for verification output
        
    Returns:
        List of all tags that are not de-identified across all files
    """
    files = get_dcm_files(dcm_dir)
    not_deidentified_list = []
    
    for dcm_file in files:
        result = get_not_deidentified_list(deid_tags, dcm_file, dest_folder)
        not_deidentified_list.extend(result)
    
    return not_deidentified_list


def extract_all_elements(ds, elements, indent=0, attrs=None, path=""):
    """
    Recursively extract all elements from a DICOM dataset.
    
    Args:
        ds: pydicom Dataset object
        elements: List to append formatted element strings
        indent: Current indentation level
        attrs: Optional list of keywords to filter
        path: Current path string for nested elements
    """
    for elem in ds:
        keyword = elem.keyword or elem.tag
        current_path = f"{path}.{keyword}" if path else keyword
        
        if elem.VR == "SQ":
            for i, item in enumerate(elem.value):
                seq_path = f"{current_path}[{i}]"
                elements.append(" " * indent + f"[Sequence Item] {seq_path}")
                extract_all_elements(item, elements, indent + 4, attrs, seq_path)
        else:
            if keyword == "PixelData":
                continue
            if attrs is None or keyword in attrs:
                elements.append(" " * indent + f"{keyword} --> {elem.value}")


def get_dicom_elements_file(file, dest_folder, attrs=None):
    """
    Extract DICOM elements from a file and save as text.
    
    Args:
        file: Path to DICOM file
        dest_folder: Destination folder for output
        attrs: Optional list of keywords to filter
    """
    ds = dcmread(file)
    metadata_file_name = os.path.join(dest_folder, os.path.basename(file) + "_metadata.txt")
    os.makedirs(dest_folder, exist_ok=True)
    
    f = open(metadata_file_name, "w")
    elements = []
    
    for k in ds:
        ele = ds[k]
        if attrs is None:
            print('{} --> {}'.format(k, ele))
            elements.append('{} --> {}'.format(k, ele))
        else:
            if ele.keyword in attrs:
                print('{} --> {}'.format(k, ele))
                elements.append('{} --> {}'.format(k, ele))
    
    f.writelines(f"{e}\n" for e in elements)
    f.close()


def get_dicom_elements_file_nested_text(file, dest_folder, attrs=None):
    """
    Extract DICOM elements from a file with nested structure and save as text.
    
    Args:
        file: Path to DICOM file
        dest_folder: Destination folder for output
        attrs: Optional list of keywords to filter
    """
    ds = dcmread(file)
    metadata_file_name = os.path.join(dest_folder, os.path.basename(file) + "_metadata.txt")
    os.makedirs(dest_folder, exist_ok=True)
    
    elements = []
    
    # Extract file meta information
    if hasattr(ds, 'file_meta'):
        elements.append("[File Meta Information]")
        for elem in ds.file_meta:
            keyword = elem.keyword or elem.tag
            if keyword != "PixelData":
                elements.append(f"{keyword} --> {elem.value}")
    
    # Now extract recursively from main dataset
    elements.append("\n[Dataset]")
    extract_all_elements(ds, elements, indent=0, attrs=attrs)
    
    # Save to file
    with open(metadata_file_name, "w", encoding="utf-8") as f:
        f.writelines(f"{line}\n" for line in elements)
    
    # Optional: also print
    for line in elements:
        print(line)


def get_dicom_dataset_text(file, dest_folder, metadata_file_name=None):
    """
    Save DICOM dataset as text representation.
    
    Args:
        file: Path to DICOM file
        dest_folder: Destination folder for output
        metadata_file_name: Optional custom filename
    """
    ds = dcmread(file)
    
    if metadata_file_name is None:
        metadata_file_path = os.path.join(dest_folder, os.path.basename(file) + "_dataset_metadata.txt")
    else:
        metadata_file_path = os.path.join(dest_folder, metadata_file_name)
    
    os.makedirs(dest_folder, exist_ok=True)
    
    f = open(metadata_file_path, "w")
    f.write(str(ds))
    f.close()

