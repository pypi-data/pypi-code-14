import uuid
import subprocess
from numpy import concatenate
from sklearn.metrics import roc_curve, auc

class PerformanceStats(object):

    """Methods for computing performance statistics."""

    @classmethod
    def pAUC(self, y_true, y_score, fpr_cutoff):
        """ Calculate partial Area Under ROC (pAUC).
    
        Computes a pAUC value given a specified false positive rate (FPR) 
        cutoff. It is important to note that the exact pAUC cannot be computed.
        The accuracy of the calculation depends on the resolution of data 
        points produced by an intermediary ROC curve. The FPR data point 
        closest to and greater than the cutoff specified will be used for 
        interpolation to determine the pAUC at the specified FPR cutoff.
    
        Args:
            y_true: Array-like of true binary class labels in range {0, 1} or 
                {-1, 1} corresponding to y_score. The larger value represents 
                the positive class.

            y_score: Array-like of target scores with higher scores indicating
                more confidence in the positive class.

            fpr_cutoff: A float specifying the FPR cutoff to use in computing 
                the pAUC. Must be in the interval (0,1).
    
        Returns:
            A float representing the pAUC value.
    
        Raises:
            AssertionError: The ROC curve does not contain a point near enough to
                the specified FPR cutoff.

            AssertionError: The FPR cutoff is not in the interval (0,1)
        """
        error_msg = "FPR cutoff must be in (0,1)"
        assert fpr_cutoff > 0.0 and fpr_cutoff < 1.0
        fpr, tpr, trash = roc_curve(y_true, y_score, drop_intermediate=False)
        index_low = len([1 for i in fpr if i < fpr_cutoff])-1
        index_high = index_low + 1
        #Get interpolated TPR value from FPR cutoff
        if index_low == -1:  #No ROC data points lower than cutoff
            x0 = fpr[0]
            x1 = fpr[1]
            y0 = tpr[0]
            y1 = tpr[1]
            #Apply line derived from two closest points from FPR cutoff
            tpr_cutoff = fpr_cutoff*((y1-y0)/(x1-x0)) + ((x1*y0-x0*y1)/(x1-x0))
            #Segment full ROC to get partial ROC
            fpr = [0.0] + [fpr_cutoff]
            tpr = [0.0] + [tpr_cutoff]
        elif index_high == len(fpr):  #No ROC data points higher than cutoff
            x0 = fpr[index_low-1]
            x1 = fpr[index_high-1]
            y0 = tpr[index_low-1]
            y1 = tpr[index_high-1]
            #Apply line derived from two closest points from FPR cutoff
            tpr_cutoff = fpr_cutoff*((y1-y0)/(x1-x0)) + ((x1*y0-x0*y1)/(x1-x0))
            #Segment full ROC to get partial ROC
            fpr = concatenate((fpr,[fpr_cutoff]), axis=1)
            tpr = concatenate((tpr, [tpr_cutoff]), axis=1)
        else: 
            x0 = fpr[index_low]
            x1 = fpr[index_high]
            y0 = tpr[index_low]
            y1 = tpr[index_high]
            #Apply line derived from two closest points from FPR cutoff
            tpr_cutoff = fpr_cutoff*((y1-y0)/(x1-x0)) + ((x1*y0-x0*y1)/(x1-x0))
            #Segment full ROC to get partial ROC
            fpr = concatenate((fpr[:index_high],[fpr_cutoff]), axis=1)
            tpr = concatenate((tpr[:index_high], [tpr_cutoff]), axis=1)
        return auc(fpr,tpr)/fpr_cutoff

