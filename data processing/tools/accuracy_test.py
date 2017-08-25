# Relative error per period (Note: not to use the average of these as this will end up by positives and negatives cancelling each other)
# Relative Error=  (Y_t - X_t)/X_t 
# 
# Mean Absolute Percent Error (MAPE) (%) (Note: Measure the cancelling out effects)
# MAPE=  1/n Summation of (t=1)^n|(Y_t-X_t)/X_t 
# 
# Overall Error (%) (Note: Aggregate accuracy of the duration.)
# Overall Error=  (Summation of (t=1)^n Y_t - Summation of _(t=1)^n X_t )/( Summation of  (t=1)^n X_t )
# 
# Having, X_t being the ground truth at period t, Y_t being the count from the detector at period t and n the number of observed periods.
