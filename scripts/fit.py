import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = "images/mask.jpg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Threshold to create a binary mask
_, binary_mask = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour (assumed to be the white shape)
largest_contour = max(contours, key=cv2.contourArea)

# Use convex hull to approximate a quadrilateral for more robust corner detection
hull = cv2.convexHull(largest_contour)
epsilon = 0.02 * cv2.arcLength(hull, True)
approx_corners = cv2.approxPolyDP(hull, epsilon, True)

# Ensure 4 corners by interpolation or approximation
if len(approx_corners) > 4:
    approx_corners = approx_corners[
        :4
    ]  # Use the first four points (assume sorted by contour tracing)
elif len(approx_corners) < 4:
    print(
        "Approximating to 4 corners is required; padding or corner estimation needed."
    )
    approx_corners = np.vstack(
        [approx_corners, approx_corners[: 4 - len(approx_corners)]]
    )

# Sort the corners for perspective transformation
if len(approx_corners) == 4:
    # Sort the corners to be consistent for perspective transform
    approx_corners = np.array([point[0] for point in approx_corners])
    sorted_corners = sorted(approx_corners, key=lambda x: (x[1], x[0]))

    # Top-left, top-right, bottom-right, bottom-left ordering
    top_left, top_right = sorted(sorted_corners[:2], key=lambda x: x[0])
    bottom_left, bottom_right = sorted(sorted_corners[2:], key=lambda x: x[0])

    # Target points for a perfect square
    max_side = max(
        np.linalg.norm(np.array(top_left) - np.array(top_right)),
        np.linalg.norm(np.array(top_right) - np.array(bottom_right)),
        np.linalg.norm(np.array(bottom_right) - np.array(bottom_left)),
        np.linalg.norm(np.array(bottom_left) - np.array(top_left)),
    )

    square_corners = np.array(
        [[0, 0], [max_side, 0], [max_side, max_side], [0, max_side]], dtype="float32"
    )

    # Perform perspective transformation
    src_corners = np.array(
        [top_left, top_right, bottom_right, bottom_left], dtype="float32"
    )
    matrix = cv2.getPerspectiveTransform(src_corners, square_corners)
    warped_image = cv2.warpPerspective(
        binary_mask, matrix, (int(max_side), int(max_side))
    )

    # Draw the detected square and warped result
    plt.figure(figsize=(15, 7))
    plt.subplot(1, 2, 1)
    plt.imshow(binary_mask, cmap="gray")
    plt.plot(
        approx_corners[:, 0], approx_corners[:, 1], "ro-", label="Detected Corners"
    )
    plt.title("Original with Detected Corners")
    plt.axis("off")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.imshow(warped_image, cmap="gray")
    plt.title("Warped Image (Corrected to Square)")
    plt.axis("off")
    # plt.show()

    # save the figure as an image
    plt.savefig("images/warped_image.jpg")

else:
    print("Failed to approximate the shape to 4 corners.")
