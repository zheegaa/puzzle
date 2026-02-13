from split_image import split_image

image_name = input("File name: ")

split_image(f"images/{image_name}", 5, 5, False, False, output_dir=f"images/{"".join(image_name.split(".")[:-1])}")
# e.g. split_image("bridge.jpg", 2, 2, True, False)
