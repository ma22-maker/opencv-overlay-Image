import cv2

def overlay_image(base_image_path, overlay_image_path, x, y, new_height):
    # Load the base image
    base_image = cv2.imread(base_image_path, cv2.IMREAD_UNCHANGED)
    if base_image is None:
        print("Error: Could not read base image.")
        return
    
    # Load the overlay image
    overlay_image = cv2.imread(overlay_image_path, cv2.IMREAD_UNCHANGED)
    if overlay_image is None:
        print("Error: Could not read overlay image.")
        return
    
    print("Original shape of the overlay image:", overlay_image.shape) 
    print("Shape of the base image:", base_image.shape)
    
    # Resize the overlay image to the specified height while maintaining aspect ratio
    aspect_ratio = overlay_image.shape[1] / overlay_image.shape[0]
    new_width = int(new_height * aspect_ratio)
    overlay_image = cv2.resize(overlay_image, (new_width, new_height))
    
    print("Resized shape of the overlay image:", overlay_image.shape)
    
    # Check if the overlay image has an alpha channel
    if overlay_image.shape[2] == 4:
        # Overlay image has an alpha channel
        overlay_b, overlay_g, overlay_r, overlay_a = cv2.split(overlay_image)
        overlay_mask = cv2.merge((overlay_a, overlay_a, overlay_a))
        inverse_overlay_mask = cv2.bitwise_not(overlay_mask)
    else:
        # Overlay image does not have an alpha channel
        overlay_b, overlay_g, overlay_r = cv2.split(overlay_image)
        overlay_a = None
        overlay_mask = None
        inverse_overlay_mask = None
    
    # Get dimensions of the overlay image
    overlay_height, overlay_width = overlay_image.shape[:2]
    
    # Ensure the overlay does not go out of the base image boundaries
    x = max(0, min(x, base_image.shape[1] - overlay_width))
    y = max(0, min(y, base_image.shape[0] - overlay_height))
    print("prient x,y from the image:", x)
    print("prient x,y from the image:", y)
    # Extract the region of interest (ROI) from the base image
    roi = base_image[y:y + overlay_height, x:x + overlay_width]
    
    # If the overlay has an alpha channel, blend using masks
    if overlay_a is not None:
        if roi.shape[2] == 4:
            roi_b, roi_g, roi_r, roi_a = cv2.split(roi)
        else:
            roi_b, roi_g, roi_r = cv2.split(roi)
            roi_a = None
        
        roi_color = cv2.merge((roi_b, roi_g, roi_r))
        overlay_color = cv2.merge((overlay_b, overlay_g, overlay_r))
        
        roi_color = cv2.bitwise_and(roi_color, inverse_overlay_mask)
        overlay_color = cv2.bitwise_and(overlay_color, overlay_mask)
        blended_color = cv2.add(roi_color, overlay_color)
        
        if roi_a is not None:
            blended_alpha = cv2.add(roi_a, overlay_a)
            blended_result = cv2.merge((blended_color[:, :, 0], blended_color[:, :, 1], blended_color[:, :, 2], blended_alpha))
        else:
            blended_result = cv2.merge((blended_color[:, :, 0], blended_color[:, :, 1], blended_color[:, :, 2]))
    else:
        # If no alpha channel, just overlay the image directly
        overlay_color = cv2.merge((overlay_b, overlay_g, overlay_r))
        blended_result = cv2.addWeighted(roi, 0.5, overlay_color, 0.5, 0)
    
    # Place the blended result back into the base image
    base_image[y:y + overlay_height, x:x + overlay_width] = blended_result
    
    # Display the result
    cv2.imshow('Result', base_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
overlay_image('./Photoes/Wrist.jpg', './Photoes/wwbg.png', 305, 130, 158)
