
mkdir data
wget https://grandeannotation.fr/downloadResults  -P data


wget http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/LA_TRANSITION_ECOLOGIQUE.csv -P data
wget http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/DEMOCRATIE_ET_CITOYENNETE.csv -P data
wget http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/LA_FISCALITE_ET_LES_DEPENSES_PUBLIQUES.csv -P data
wget http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/ORGANISATION_DE_LETAT_ET_DES_SERVICES_PUBLICS.csv -P data


cd data 
unzip downloadResults
cd ..
rm data/downloadResults
