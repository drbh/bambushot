import numpy as np
from transformers import SamModel, SamProcessor
from PIL import Image, ImageDraw

model = SamModel.from_pretrained("Zigeng/SlimSAM-uniform-77")
processor = SamProcessor.from_pretrained("Zigeng/SlimSAM-uniform-77")


img_path = "frames/latest_frame_30.jpg"
raw_image = Image.open(img_path).convert("RGB")


# input_points = [[[630, 530]]]
# input_points = [[[430, 530]]]
input_points = [[[230, 530]]]

inputs = processor(
    raw_image,
    #
    input_points=input_points,
    input_labels=[[1]],
    return_tensors="pt",
)
outputs = model(**inputs)

masks = processor.image_processor.post_process_masks(
    outputs.pred_masks.cpu(),
    inputs["original_sizes"].cpu(),
    inputs["reshaped_input_sizes"].cpu(),
)

print("Number of masks:", len(masks))

mask = masks[0][0]
# Print shape to verify dimensions
print("Original mask shape:", mask.shape)

# filter mask to remove noise
mask = mask.detach().cpu().numpy()
mask = mask > 0.99
mask = mask.astype(np.uint8)[0]

# mask_array = (mask.numpy()[0] * 255).astype(np.uint8)  # Take first mask
mask_array = (mask * 255).astype(np.uint8)  # Take first mask
mask_image = Image.fromarray(mask_array, mode="L")

# Print shape after squeeze
print("After squeeze shape:", mask_array.shape)

# Convert to PIL Image
mask_image = Image.fromarray(mask_array, mode="L")

# make sure image is has color channels
mask_image = mask_image.convert("RGB")


# place a red point at the input point
draw = ImageDraw.Draw(mask_image)
draw.ellipse(
    [
        input_points[0][0][0] - 5,
        input_points[0][0][1] - 5,
        input_points[0][0][0] + 5,
        input_points[0][0][1] + 5,
    ],
    fill="red",
)


# Save mask
mask_image.save("images/mask.jpg")
