If you’re editing this class, you’re usually doing one of these:

1. **Adding or modifying attributes**
   (Expose new device state that clients can read.)

2. **Updating attribute read/write methods**
   (Control how attribute values are validated, stored, or synchronized with AutoScript.)

3. **Adding or changing internal acquisition helpers**
   (Modify `_acquire_stem_image` or `_acquire_stem_image_advanced`)

4. **Adding or modifying commands**
   (Update input validation, settings retrieval via `DeviceProxy`, orchestration logic, caching behavior, or metadata packaging.)

5. **Adding or changing acquisition settings**
   (Extend what is read from detector devices—e.g., dwell time, resolution, scan region—and ensure they propagate correctly into acquisition helpers.)

6. **Adding a new detector**
   (Add a device property for its address, register it in `_connect_detector_proxies`, ensure naming normalization, and map it correctly in acquisition helpers.)

7. **Changing the transport format**
   (Modify DevEncoded usage, metadata schema, caching policy, or multi-image retrieval semantics.)

8. **Improving robustness**
   (Handle connection failures, missing proxies, AutoScript errors, simulation fallback logic, or state transitions like `FAULT`, `ON`, `OFF`.)
