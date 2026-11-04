# Note on omitted stderr captures

The release replay and controls also captured standard error to four files:
`controls.stderr`, `replay.stderr`, and the same two under `initial_documentation/`.
All four were empty (SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855,
the hash of the empty string). They are not published, and they have been removed from
`../SHA256SUMS` and `../MANIFEST.json`. Nothing else changed.
