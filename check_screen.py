import pymupdf

pix = pymupdf.Pixmap('live_ruler_check.png')
print("Image size:", pix.width, pix.height)

# Save a cropped version showing the document window
# If screen is 1920x1080 or 1366x768
w, h = pix.width, pix.height
crop_rect = pymupdf.IRect(0, 0, w, h)
print("Full screenshot captured successfully.")
