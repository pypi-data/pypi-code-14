import bob.paper.biosig2016

extractor = bob.paper.biosig2016.extractor.SpectralStatistics(
    win_length_ms=256,
    win_shift_ms=10,
    with_mean=True,
    with_std=True,
    mean_removal_flag=False,
)
