import urllib.request
import os
import platform

from navigate.tools.file_functions import delete_folder


def test_ome_metadata_valid(dummy_model):
    from navigate.model.metadata_sources.ome_tiff_metadata import OMETIFFMetadata

    # First, download OME-XML validation tools
    # new_path = https://downloads.openmicroscopy.org/bio-formats/8.1.0/artifacts/bftools.zip
    # old_path = https://downloads.openmicroscopy.org/bio-formats/6.0.1/artifacts/bftools.zip

    urllib.request.urlretrieve(
        "https://downloads.openmicroscopy.org/bio-formats/8.1.0/artifacts/bftools.zip",
        "bftools.zip",
    )

    # Unzip
    _ = os.popen("tar -xzvf bftools.zip").read()

    # Create metadata
    md = OMETIFFMetadata()

    md.configuration = dummy_model.configuration

    # Write metadata to file
    md.write_xml("test.xml")

    # Validate the XML
    if platform.system() == "Windows":
        output = os.popen("bftools\\xmlvalid.bat test.xml").read()
    else:
        output = os.popen("./bftools/xmlvalid test.xml").read()

    print(output)

    # Delete bftools
    delete_folder("./bftools")
    os.remove("bftools.zip")

    # Delete XML
    os.remove("test.xml")

    assert "No validation errors found." in output
