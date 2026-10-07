import pymupdf

doc = pymupdf.open('live_ruler_check.png')
page = doc[0]

# Crop top tabs (y: 50 to 120)
crop_tabs = page.get_pixmap(clip=pymupdf.Rect(0, 50, 1200, 120))
crop_tabs.save('crop_live_tabs.png')

# Crop table Row 1 area (x: 200 to 750, y: 150 to 450)
crop_row1 = page.get_pixmap(clip=pymupdf.Rect(50, 120, 850, 600))
crop_row1.save('crop_live_canvas.png')
print("Cropped successfully!")
