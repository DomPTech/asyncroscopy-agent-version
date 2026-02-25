
## Adding a new detector

1. Copy `src/detectors/HAADF.py` to `src/detectors/NEWDET.py` and adjust the attributes for that detector's settings.
2. Add a `device_property` in `Microscope.py`:
   ```python
   newdet_device_address = device_property(dtype=str, default_value="test/detector/newdet")
   ```
3. Register it in `_connect_detector_proxies()`:
   ```python
   "newdet": self.newdet_device_address,
   ```
4. Add acquisition logic in `_acquire_stem_image()` if it differs from HAADF.
5. Add `tests/detectors/test_NEWDET.py` following `test_HAADF.py` as a template.
