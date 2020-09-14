import pandas as pd
from .utils import match_sequences


def get_question_with_transport_data(df, df_transport_classification, question):
    mask = df_transport_classification[question].astype(bool)
    return df[question][mask]


def match_lexique_to_responses_texts(texts_lemmas, lexique_dataframe, return_pos=False):
    matched_ = [match_sequences(lexique_dataframe.word.apply(str.split).values, lem) for lem in texts_lemmas]
    if not return_pos:
        matched_ = [[mi[0] for mi in m] for m in matched_]
    return matched_


def load_lexique(filename):
    lexique = pd.read_csv(filename)
    return lexique


def count_occurrences(matching_results, lexique_dataframe=None, binary=False, min_support=5, col="word"):
    count_ = {}
    for m in matching_results:
        visited = set([])
        for mi in m:
            if isinstance(lexique_dataframe, pd.DataFrame):
                mi = lexique_dataframe[col].values[mi]
            if not mi in count_: count_[mi] = 0

            if not binary or (binary and (not mi in visited)):
                count_[mi] += 1
                visited.add(mi)
    if min_support > 1:
        for k in list(count_.keys()):
            if count_[k] < min_support:
                del count_[k]
    return count_
