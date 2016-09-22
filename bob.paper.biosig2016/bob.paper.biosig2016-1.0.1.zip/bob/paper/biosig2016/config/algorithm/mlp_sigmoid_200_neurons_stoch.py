import bob.paper.biosig2016

algorithm = bob.paper.biosig2016.algorithm.MLP(
    normalize_features=True,
    mlp_shape=(200, 1),
    batch=False,
    output_activation="sigmoid",
    target=1,
)
