import cv2
import numpy as np

def detect_qr_finder_patterns(image):
    threshold = image
    # Divide the image into a grid of equally sized regions
    height, width = threshold.shape
    rows, cols = np.meshgrid(np.arange(0, height, height // 50), np.arange(0, width, width // 50))
    regions = np.dstack((cols.ravel(), rows.ravel())).reshape(-1, 1, 2)

    # Define the expected pattern of alternating black and white regions with a 1:1:3:1:1 ratio
    pattern = [1, 1, 3, 1, 1]

    # Scan each row of the grid horizontally, looking for the pattern
    matches = []
    for row in regions:
        # Skip every other row for performance reasons
        if row[0][1] % 2 != 0:
            continue

        # Initialize variables to track the pattern
        pattern_index = 0
        last_pixel = 0
        run_length = 0

        # Scan horizontally from left to right
        for pixel in threshold[row[0][1], row[0][0]:]:
            if pixel == last_pixel:
                run_length += 1
            else:
                if pattern_index < len(pattern):
                    # Check if the run length matches the expected pattern
                    if abs(run_length - pattern[pattern_index] * (row[0][1] % 4 == 0 or pattern_index == 2)) < pattern[pattern_index] // 2:
                        pattern_index += 1
                        if pattern_index >= len(pattern):
                            # Pattern found, record the location and orientation
                            center_x = row[0][0] - (pattern[2] - 1) // 2
                            center_y = row[0][1] - (pattern[2] - 1) // 2
                            matches.append((center_x, center_y, row[0][1] % 4))
                            break
                run_length = 1
                last_pixel = pixel
                pattern_index = 0

    # Group similar matches together
    grouped_matches = []
    for match in matches:
        print("Match")
        found = False
        for grouped_match in grouped_matches:
            if abs(match[0] - grouped_match[0]) < 10 and abs(match[1] - grouped_match[1]) < 10:
                # Matches are considered similar if they are within 10 pixels of each other
                found = True
                grouped_match[2].append(match[2])
                break
        if not found:
            grouped_matches.append([match[0], match[1], [match[2]]])

    # Find the center of each finder pattern
    finder_pattern_centers = []
    for match in grouped_matches:
        center_x = int(sum([x for x in match[::2]]) / len(match[::2]))
        center_y = int(sum([y for y in match[1::2]]) / len(match[1::2]))
        finder_pattern_centers.append((center_x, center_y))
        print(f"({center_x}, {center_y})")

    # Draw rectangles

frame = cv2.imread("test.png", cv2.IMREAD_GRAYSCALE)  
frame = cv2.bitwise_not(frame)
detect_qr_finder_patterns(frame)
cv2.imshow("Filtering Circular Blobs Only", frame)

cv2.waitKey(0)

# Show blobs
cv2.destroyAllWindows()