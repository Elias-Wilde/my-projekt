from my_project.routes.profile import crop_picture_to_square
import os

# unit test
def test_picture_cropping():
    """
    GIVEN a picture

    WHEN the picture isn't a square

    THEN the function crops the img to a square

    """
    given_picture = os.path.join("tests/meta/test_crop_img.jpg")

    # given picture has size of (1080, 810); expected output is (810, 810)
    expected_size = (810, 810)

    output_picture = crop_picture_to_square(given_picture)

    output_size = output_picture.size

    assert expected_size == output_size
