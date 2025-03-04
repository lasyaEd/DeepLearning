import Vision
import Foundation
import AppKit  # For macOS image handling

def extract_text_from_image(image_path):
    """Extracts text from an image using Apple's Vision Framework."""
    
    # Load Image
    image = AppKit.NSImage.alloc().initWithContentsOfFile_(image_path)
    
    if image is None:
        print("Error: Could not load image.")
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
        print("Error in OCR processing:", error)
        return ""

    # Extract recognized text
    recognized_text = []
    for observation in request.results():
        recognized_text.append(observation.topCandidates_(1)[0].string())

    return "\n".join(recognized_text)

# Example Usage
image_path = "//Users/lasyaedunuri/Documents/AI & Deep Learning/project/Quotes/DC6FD752-33C2-45C4-837A-9FAF5877B287.PNG"  # Update with the actual image path
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:\n", extracted_text)
