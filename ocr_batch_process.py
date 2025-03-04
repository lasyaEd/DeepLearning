import os
import Vision
import Foundation
import AppKit
import pandas as pd

# Define the folder containing images
image_folder = "/Users/lasyaedunuri/Documents/AI & Deep Learning/project/Quotes" 
output_csv = "extracted_text.csv"

def extract_text_from_image(image_path):
    """Extracts text from an image using Apple's Vision Framework."""
    image = AppKit.NSImage.alloc().initWithContentsOfFile_(image_path)
    
    if image is None:
        print(f"Error: Could not load image {image_path}")
        return ""

    # Convert NSImage to CGImage
    image_data = image.TIFFRepresentation()
    bitmap = AppKit.NSBitmapImageRep.alloc().initWithData_(image_data)
    cg_image = bitmap.CGImage()

    # Create Vision Request
    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)  # High accuracy

    # Process Image
    handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(cg_image, None)
    success, error = handler.performRequests_error_([request], None)
    
    if not success:
        print(f"Error in OCR processing {image_path}: {error}")
        return ""

    # Extract recognized text
    recognized_text = []
    for observation in request.results():
        recognized_text.append(observation.topCandidates_(1)[0].string())

    return "\n".join(recognized_text)

# Process all images in the folder
data = []
for filename in sorted(os.listdir(image_folder)):  # Sort for consistency
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):  # Process image files only
        image_path = os.path.join(image_folder, filename)
        extracted_text = extract_text_from_image(image_path)
        data.append({"filename": filename, "text": extracted_text})

# Convert results to a Pandas DataFrame
df = pd.DataFrame(data)

# Save extracted text to CSV
df.to_csv(output_csv, index=False)

print(f"✅ Extraction complete! Text saved in {output_csv}")
