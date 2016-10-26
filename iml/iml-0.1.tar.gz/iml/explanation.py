from .visualizers.visualizers import SimpleListVisualizer, AdditiveForceVisualizer

class Explanation:
    def __init__(self, outNames, featureNames, featureEffects, data):
        self.outNames = outNames
        self.featureNames = featureNames
        self.featureEffects = featureEffects
        self.data = data

    def visualize(self, *args):
        visualizer = args[0] if len(args) > 0 else AdditiveForceVisualizer()
        return visualizer.visualize(self.outNames, self.featureNames, self.featureEffects)
