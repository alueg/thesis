import json
import os
from batch1vsbatch2.demographics_b1b2 import analyze_demographic_differences, analyze_trust_differences, analyze_trust_by_demographics_batch_comparison, analyze_trust_by_demographics
from batch1vsbatch2.visualize_trust import plot_nested_pie

batch1 = 'batch1vsbatch2/data/filtered_batch1.txt'
batch2 = 'batch1vsbatch2/data/filtered_batch2.txt'
combined_batches = 'batch1vsbatch2/data/CombinedBatch.txt'

#DONE
#analyze_trust_differences([combined_batches, batch1, batch2])
#analyze_demographic_differences([batch1, batch2, combined_batches])
#analyze_trust_by_demographics_batch_comparison([batch1, batch2, combined_batches])
#analyze_trust_by_demographics([batch1, batch2, combined_batches])
#analyze_demographic_differences([combined_batches, batch1, batch2])

#plot_nested_pie(combined_batches)
analyze_trust_differences([combined_batches, batch1, batch2])
