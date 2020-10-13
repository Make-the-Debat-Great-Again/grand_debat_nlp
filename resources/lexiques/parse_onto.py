import pandas as pd
df_onto = pd.read_csv("lucene-export.csv") # EXPORT from PROTEGE CSV ADDON
df_onto.columns
columns_ren = {
    "http://www.w3.org/2004/02/skos/core#prefLabel":"prefLabel",
    "http://www.w3.org/2004/02/skos/core#altLabel":"altLabel"
}
df_onto = df_onto["http://www.w3.org/2004/02/skos/core#prefLabel http://www.w3.org/2004/02/skos/core#altLabel".split()].rename(columns=columns_ren)
df_onto.fillna("",inplace=True)
df_onto["altLabel"] = df_onto.altLabel.apply(lambda x :"|".join([i.strip("\'") for i in x.split("\t")]))
df_onto["prefLabel"] = df_onto.prefLabel.apply(lambda x: x.strip("\'"))
df_onto.to_csv("ontology.csv",sep="\t")