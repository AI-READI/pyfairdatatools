import pydicom


def shared_functional_group_sequence(dataset, x):
    """
    Create the shared functional group sequence in the dataset.

    This function constructs the shared functional group sequence for a DICOM dataset,
    populating it with anatomical, reference, orientation, and pixel measurement information.

    Args:
        dataset (pydicom.Dataset): The DICOM dataset to which the functional groups are added.
        x (list): List containing data for constructing the functional groups.
    """
    anatomy_region_seq = pydicom.Sequence()
    anatomic_region_item = pydicom.Dataset()
    anatomic_region_item.CodeValue = ["T-AA610"]
    anatomic_region_item.CodingSchemeDesignator = ["SRT"]
    anatomic_region_item.CodeMeaning = ["Retina"]
    anatomy_region_seq.append(anatomic_region_item)

    frame_anatomic_seq = pydicom.Sequence()
    frame_anatomic_item = pydicom.Dataset()
    frame_anatomic_item.AnatomicRegionSequence = anatomy_region_seq
    frame_anatomic_seq.append(frame_anatomic_item)

    purpose_of_reference_seq = pydicom.Sequence()
    purpose_of_reference_item = pydicom.Dataset()
    purpose_of_reference_item.CodeValue = ["121311"]
    purpose_of_reference_item.CodingSchemeDesignator = ["DCM"]
    purpose_of_reference_item.CodeMeaning = ["Localizer"]
    purpose_of_reference_seq.append(purpose_of_reference_item)

    referenced_image_seq = pydicom.Sequence()
    referenced_image_item = pydicom.Dataset()
    referenced_image_item.ReferencedSOPClassUID = (
        x[0]["52009229"].value[0]["00081140"].value[0]["00081150"].value
    )
    referenced_image_item.ReferencedSOPInstanceUID = (
        x[0]["52009229"].value[0]["00081140"].value[0]["00081155"].value
    )
    referenced_image_item.PurposeOfReferenceCodeSequence = purpose_of_reference_seq
    referenced_image_seq.append(referenced_image_item)

    plane_orientation_seq = pydicom.Sequence()
    plane_orientation_item = pydicom.Dataset()
    plane_orientation_item.ImageOrientationPatient = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    plane_orientation_seq.append(plane_orientation_item)

    pixel_measures_seq = pydicom.Sequence()
    pixel_measures_item = pydicom.Dataset()
    pixel_measures_item.SliceThickness = (
        x[0]["52009229"].value[0]["00289110"].value[0]["00180050"].value
    )
    pixel_measures_item.PixelSpacing = (
        x[0]["52009229"].value[0]["00289110"].value[0]["00280030"].value
    )
    pixel_measures_seq.append(pixel_measures_item)

    shared_func_groups_seq = pydicom.Sequence()
    dataset.SharedFunctionalGroupsSequence = shared_func_groups_seq
    shared_func_item = pydicom.Dataset()
    shared_func_item.FrameAnatomySequence = frame_anatomic_seq
    shared_func_item.ReferencedImageSequence = referenced_image_seq
    shared_func_item.PlaneOrientationSequence = plane_orientation_seq
    shared_func_item.PixelMeasuresSequence = pixel_measures_seq
    shared_func_groups_seq.append(shared_func_item)


def per_frame_functional_groups_sequence(dataset, x):
    """
    Create the per-frame functional groups sequence in the dataset.

    This function constructs the per-frame functional groups sequence for a DICOM dataset,
    populating it with per-frame content, reference, ophthalmic, and position information.

    Args:
        dataset (pydicom.Dataset): The DICOM dataset to which the functional groups are added.
        x (list): List containing data for constructing the functional groups.
    """
    per_frame_functional_groups_seq = pydicom.Sequence()
    repeat = len(x[0]["52009230"].value)

    for i in range(repeat):
        frame_content_seq = pydicom.Sequence()
        frame_content_item = pydicom.Dataset()
        frame_content_item.FrameAcquisitionDateTime = (
            x[0]["52009230"].value[i]["00209111"].value[0]["00189074"].value
        )
        frame_content_item.FrameReferenceDateTime = (
            x[0]["52009230"].value[i]["00209111"].value[0]["00189151"].value
        )
        frame_content_item.StackID = (
            x[0]["52009230"].value[i]["00209111"].value[0]["00209056"].value
        )
        frame_content_item.InStackPositionNumber = (
            x[0]["52009230"].value[i]["00209111"].value[0]["00209057"].value
        )
        frame_content_item.DimensionIndexValues = (
            x[0]["52009230"].value[i]["00209111"].value[0]["00209157"].value
        )
        frame_content_seq.append(frame_content_item)

        purpose_of_reference_seq = pydicom.Sequence()
        purpose_of_reference_item = pydicom.Dataset()
        purpose_of_reference_item.CodeValue = ["121311"]
        purpose_of_reference_item.CodingSchemeDesignator = ["DCM"]
        purpose_of_reference_item.CodeMeaning = ["Localizer"]
        purpose_of_reference_seq.append(purpose_of_reference_item)

        ophthalmic_frame_location_seq = pydicom.Sequence()
        ophthalmic_frame_location_item = pydicom.Dataset()
        ophthalmic_frame_location_item.ReferencedSOPClassUID = (
            x[0]["52009230"].value[i]["00220031"].value[0]["00081150"].value
        )
        ophthalmic_frame_location_item.ReferencedSOPInstanceUID = (
            x[0]["52009230"].value[i]["00220031"].value[0]["00081155"].value
        )
        ophthalmic_frame_location_item.ReferenceCoordinates = (
            x[0]["52009230"].value[i]["00220031"].value[0]["00220032"].value
        )
        ophthalmic_frame_location_item.OphthalmicImageOrientation = (
            x[0]["52009230"].value[i]["00220031"].value[0]["00220039"].value
        )
        ophthalmic_frame_location_item.PurposeOfReferenceCodeSequence = (
            purpose_of_reference_seq
        )
        ophthalmic_frame_location_seq.append(ophthalmic_frame_location_item)

        plane_position_seq = pydicom.Sequence()
        plane_position_item = pydicom.Dataset()
        try:
            value = x[0]["52009230"].value[i]["00209113"].value[0]["00200032"].value
        except KeyError:
            value = []
        plane_position_item.ImagePositionPatient = value
        plane_position_seq.append(plane_position_item)

        per_frame_functional_groups_item = pydicom.Dataset()
        per_frame_functional_groups_item.FrameContentSequence = frame_content_seq
        per_frame_functional_groups_item.PlanePositionSequence = plane_position_seq
        per_frame_functional_groups_item.OphthalmicFrameLocationSequence = (
            ophthalmic_frame_location_seq
        )
        per_frame_functional_groups_seq.append(per_frame_functional_groups_item)

    dataset.PerFrameFunctionalGroupsSequence = per_frame_functional_groups_seq
