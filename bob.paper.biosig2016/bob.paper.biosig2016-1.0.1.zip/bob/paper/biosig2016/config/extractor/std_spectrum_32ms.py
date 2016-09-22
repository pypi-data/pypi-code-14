import bob.paper.biosig2016


extractor = bob.paper.biosig2016.extractor.SpectralStatistics(
    win_length_ms=32,
    win_shift_ms=10,
    with_mean=False,
    with_std=True,
)

# TODO: provide config files with varying input arguments
