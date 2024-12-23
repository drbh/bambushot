# NOTE THIS FILE IS NOT INTENDED TO BE RUN DIRECTLY
# AND IS JUST FOR REFERENCE TO SHOW HOW THE PLATE WAS DESIGNED
from build123d import (
    Box,
    Mesher,
)

# a 50x50x0.5mm plate
measure_plate = Box(50, 50, 0.5)
exporter = Mesher()
exporter.add_shape(measure_plate, part_number="measure_plate")
exporter.add_code_to_metadata()
exporter.write("measure_plate.3mf")
print("Exporting 3mf file...")
