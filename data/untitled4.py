from astropy.io import fits
import numpy as np
from PIL import Image

data = np.squeeze(fits.getdata("51_peg_hst.fits"))

# Reject non-finite and non-positive values
valid = np.isfinite(data) & (data > 0)

# Log transform
log_data = np.zeros(data.shape, dtype=float)
log_data[valid] = np.log10(data[valid])

# Scale valid pixels to 8-bit grayscale
lo, hi = log_data[valid].min(), log_data[valid].max()
image = np.zeros(data.shape, dtype=np.uint8)
image[valid] = ((log_data[valid] - lo) / (hi - lo) * 255).astype(np.uint8)

Image.fromarray(image).save("51_peg_hst_log.tiff")