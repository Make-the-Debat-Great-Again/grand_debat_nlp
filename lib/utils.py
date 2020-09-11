import warnings
import socket
from io import StringIO

import numpy as np
import pandas as pd

from joblib import Parallel,delayed

from tqdm import tqdm


def match_sequences(sequences_to_match, data):
    """
    Return match sequence start,end positions in a data

    Parameters
    ----------
    seq : list
        sequence
    data : list
        data

    """
    N = len(sequences_to_match)
    if N < 1:
        warnings.warn("Sequence Empty")
        return []

    # Converting to numpy arrays
    if isinstance(data, list):
        data = np.asarray(data)
    if isinstance(sequences_to_match, list):
        sequences_to_match = np.array(sequences_to_match)

    sequence_register = np.array(
        [[seq[0], (seq, i, len(seq))] for i, seq in enumerate(sequences_to_match)]) # prefix, (sequence, sequence index, sequence_length)

    prefix_ind = np.where(np.isin(data, sequence_register[:, 0]))[0] # Find token that match a sequence prefix from the prefix register

    results = []
    for idx in prefix_ind:
        mask = np.where(sequence_register[:, 0] == data[idx]) # Find the sequence that has the current token as prefix
        for sequence in sequence_register[mask]: # For every possible sequence, we verify if there is a match
            start, end = idx, idx+sequence[1][-1]
            # If a the whole sequence can be found with the prefix combined with n following tokens (n= sequence length)
            # Then it's a match
            try:
                if (data[start:end].tolist() == sequence[1][0]):
                    results.append([sequence[1][1], start, end])
            except ValueError:
                if (data[start:end].tolist() == sequence[1][0].tolist()):
                    results.append([sequence[1][1], start, end])
    return results

def call_talismane(text,host="0.0.0.0",port=7272):
    """
    Retrieve Talismane output for a text. Notice that Talismane must be initialize in Server mode before calling this function.

    Parameters
    ----------
    text : str
        input text
    host : str, optional
        ip of the machine that host Talismane, by default "0.0.0.0"
    port : int, optional
        port of Talismane in the host machine, by default 7272

    Returns
    -------
    pandas.DataFrame
        Talismane output
    """
    s = socket.socket()
    s.connect((host,port))
    s.sendall("{0}\f\f\f".format(text).encode("utf-8"))
    data =""
    while True:# Talismane send data iteratively (sequence by sequence)
        try:
            response = s.recv(port).decode("utf-8")
            if not response:
                break
            data+= response
        except UnicodeDecodeError:
            continue
    s.close()
    return pd.read_csv(StringIO(data),sep="\t",header=None,names="ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC".split())



def random_string(stringLength=8):
    """
    Generate a random string

    Parameters
    ----------
    stringLength : int, optional
        length of the random string, by default 8

    Returns
    -------
    str
        random string
    """
    strings = [
        ("PasséComposéquitue","Le PasséComposéquitue est un temps génial !"),
        ("123456789","Le PasséComposéquitue est un temps génial !")
    ]
    return "123456789"

def _process_batch(batch):
    """
    Procces a batch of text in Talismane. Basically, we merge a batch of text into one, using a string key to identified texts boundaries after the process.

    Parameters
    ----------
    batch : list of strl
        list of texts

    Returns
    -------
    list of pandas.DataFrame
        Talismane output for each text
    """
    code = " " + random_string(10)+ " "
    data = call_talismane(code.join(batch))
    index = data[data.FORM == "123456789"].index.tolist()
    if len(index)+1 != len(batch):
        print("Error in Parallelisation Resutlts",len(index)+1,len(batch))
        a = [call_talismane(b) for b in batch]
        print("Now:", len(a),len(batch))
        return a
    else:
        return [d.iloc[1:,:] for d in np.split(data,index)]

def parallel_talismane(data ,n_jobs = 4,batch_size=100):
    """
    Allows to process a large amount of textual data by combining batch processing and parallelization.

    Parameters
    ----------
    data : list of str
        list of texts
    n_jobs : int, optional
        number of jobs created, by default 4
    batch_size : int, optional
        size of each batch processed, by default 100

    Returns
    -------
    list of pandas.DataFrame
        Talismane output for each text
    """
    from tqdm import tqdm
    N = len(data)
    if batch_size > N:
        return _process_batch(data)
    res_final = None
    divider = np.ceil(N/batch_size)
    data = np.array_split(data, divider)
    all_res = Parallel(n_jobs=n_jobs,backend="multiprocessing")(delayed(_process_batch)(batch) for batch in data)
    res_final = all_res.pop(0)
    while True:
        if len(all_res)<1:
            break
        res_final.extend(all_res.pop(0))
    return res_final


def extract_lemma_spacy(nlp,df,col,stop_words=[],batch_size=1000,n_threads = 8):
  tokens = []
  lemma = []
  for doc in tqdm(nlp.pipe(df[col].astype('unicode').values, batch_size=batch_size,n_threads=n_threads),total = len(df)):
      if doc.is_parsed:
          tokens.append([n.text for n in doc if not n.text in stop_words])
          lemma.append([n.lemma_ for n in doc if not n.lemma_ in stop_words])
      else:
          # We want to make sure that the lists of parsed results have the
          # same number of entries of the original Dataframe, so add some blanks in case the parse fails
          tokens.append(None)
          lemma.append(None)

  df['tokens'] = tokens
  df['lemma'] = lemma