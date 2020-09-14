# NLP works on the "Grand Débat National" data

In this repository, we stored the code used for :

 * Produce and use a classification model to identify answers associated with the "transport" theme
 * Using lexical resources, extract occurrences of specific words in the text data
 * Extract specific co-occurrences patterns in the "transport" answers

# Requirements

 * Python 3.6+ (If you are on Windows, favor Anaconda installation)
 * Install the packages listed in the `requirements.txt` file. If you are on Linux/MacOS, run the following command : `pip3 install -r requirements.txt`
 * If you are on Linux/MacOS, run the `prepare.sh`, else download and extract the required data in a `data` directory:
    * https://grandeannotation.fr/downloadResults 
    * http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/LA_TRANSITION_ECOLOGIQUE.csv
    * http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/DEMOCRATIE_ET_CITOYENNETE.csv
    * http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/LA_FISCALITE_ET_LES_DEPENSES_PUBLIQUES.csv
    * http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/ORGANISATION_DE_LETAT_ET_DES_SERVICES_PUBLICS.csv
  * Install `Talismane` 
    * Download `Talismane` from here :
        https://github.com/joliciel-informatique/talismane/releases/tag/v5.3.0
    * Download the extra-files at this address : https://github.com/joliciel-informatique/talismane/releases/tag/v5.2.0
        * frenchLanguagePack-5.2.0.zip
        *  talismane-fr-5.2.0.conf
    * Extract the `Talismane` software archive in a directory
    * Copy the extra-files in the `Talismane` software directory

## !! Attention !!

Before using any script, start the Talismane server using the following command:

    cd <talisman_directory>
    java -Xmx6G -Dconfig.file=talismane-fr-5.2.0.conf -jar talismane-core-5.3.0.jar --analyse --sessionId=fr --mode=server --encoding=UTF-8


# Classification model

To identify answers related to "transportation", we produce a classification model using the SVM algorithm. To train our model, we used crowdsourced annotation from the ["Grande Annotation" initiative](https://grandeannotation.fr/).

In order to train the model, run the `train.py` script using the following command:

    python3 train.py data/LA_TRANSITION_ECOLOGIQUE.csv data/results.csv -o # WITH TALISMANE

Once the model is trained, use the following command to classify a dataset from the Grand Débat National : 

    python3 predict <dataset> <dataset_code**>

** Each "Grand Débat National" dataset is associated to a code, here is the association table:

| code | dataset                             |
|------|-------------------------------------|
| 1    | transition_eco                      |
| 2    | democratie_et_citoy                 |
| 3    | fiscalite_et_depense_publique       |
| 4    | organisation_de_etat_et_service_pub |

<br> 

The output file contains the results of the classification. Each line corresponds to a contribution and each column to a question. The rest of the columns corresponds to the author's ID, postal code and the reference ID of the contributions.

The intersection between a row and column corresponds to a boolean that indicate if the answer is associated to the transportation thematic or not.

You can find an output sample in in the `example` directory.

# Measure the number of occurrences of terms associated with transportation

Using the classification output from `predict.py` script, we can count the number of occurrences of specific words. Here, we proposed three lexicons:

 * Transport lexicons
 * Transportation Verb
 * Alteration Verb

To measure the occurrence of the terms from these lexicons (check the `resources/lexiques` directory), run the following command:

    python3 count_terms.py <grand_debat_dataset> <classification_result>

* <grand_debat_dataset> : CSV of a "Grand Débat National" dataset
* <classification_result> : Results using the trained classification model on the same dataset.

# Identify specific patterns representing proposition of contributors

If counting occurrences 

To measure the co-occurrence patterns based on the lexicons (check the `resources/lexiques` directory), use the following command:

    python3 count_coocs.py <grand_debat_dataset> <classification_result> <dataset_code>

 * <grand_debat_dataset> : CSV of a "Grand Débat National" dataset
 * <classification_result> : Results using the trained classification model on the same dataset.