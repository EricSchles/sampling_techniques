import pandas as pd
import code
       
def base_agreement_criteria(sample, df, columns):
    count = 0
    for column in columns:
        if int(sample[column].mode()) == int(df[column].mode()):
            count +=1
    return count

def get_percent_per_value(df, column):
    numerator = df[column].value_counts()
    denominator = df[column].value_counts().sum()
    percentages_per_value = numerator/denominator
    values_per_column = list(percentages_per_value.index)
    percentages_per_column = list(percentages_per_value)
    return dict(zip(values_per_column, percentages_per_column))

def nuanced_agreement_criteria(sample, df, columns):
    column_diffs = {}
    for column in columns:
        sample_value_percents = get_percent_per_value(sample, column)
        df_value_percents = get_percent_per_value(df, column)
        summed_diff_in_percent = 0
        for value in sample_value_percents:
            summed_diff_in_percent += abs(sample_value_percents[value] - df_value_percents[value])
        column_diffs[column] = summed_diff_in_percent
    return column_diffs
    
def generate_representative_sample(df, columns, sample_size=1000, num_iterations=1000, simple=False):
    """
    This function generates a representative random sample based 
    on specific variables in the data set.
    Variables for consideration:
    * Passenger_count
    * Trip_distance
    * Total_amount
    * Tip_amount
    We attempt two methods:
    - Kolmogorov-Smirnov test as a means of selection
    - moment differencing as criteria for representativeness
    If KS happens to every returns a valid sample,
    that means all the distributions are equal for all variables of consideration.
    If the moment differencing method is used, we search for the sample which minimizes
    difference between the first two moments.
    Notice that we only select on moment differences if ks fails for all generated samples.
    """    
    possible_samples = []
    base_agreement_scores = []
    nuanced_agreement_scores = []
    for _ in range(num_iterations):
        sample = df.sample(sample_size)   
        possible_samples.append(sample)
        base_agreement_scores.append(
            base_agreement_criteria(sample, df, columns))
        nuanced_score = nuanced_agreement_criteria(sample, df, columns)
        nuanced_agreement_scores.append(
            sum(list(nuanced_score.values()))
                    
    best_nuanced_score = nuanced_agreement_scores[0]
    best_base_score = base_agreement_scores[0]
    best_sample = possible_samples[0]
    for index, value in enumerate(nuanced_agreement_scores):
        if value < best_nuanced_score:
            best_nuanced_score = value
            best_sample = possible_samples[index]
    # for index, value in enumerate(base_agreement_scores):
    #     if value > best_base_score:
    #         best_base_score = value
    #         best_sample = possible_samples[index]
    return best_sample

def remove_by_index(df, sample):
    return df.drop(sample.index)
    
df = pd.read_csv("PLACE YOUR DATA HERE.csv")

# columns of interest here
columns = []

# training, testing, validation, holdout (not listed)
sample_sizes = [int(len(df)*0.60), int(len(df)*0.15), int(len(df)*0.15)]
samples = []
for index, sample_size in enumerate(sample_sizes):
    if index == 0:
        samples.append(generate_representative_sample(df, columns, sample_size=sample_size, num_iterations=1))
    else:
        samples.append(generate_representative_sample(df, columns, sample_size=sample_size, num_iterations=1))
    df = remove_by_index(df, samples[index])


