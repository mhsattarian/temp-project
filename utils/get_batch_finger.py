from ..fingerprint_simpletest_rpi import save_fingerprint_image

for i in range(10):
  save_fingerprint_image(f'finger-{i+1}.png')

