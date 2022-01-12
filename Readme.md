# HPO Term Mapping Tool

## Introduction

The Human Phenotype Ontology (HPO) "provides a standardized vocabulary of phenotypic abnormalities encountered in human disease". Each term in the HPO describes a phenotypic abnormality and the ontology has been made publicly available at https://hpo.jax.org/. The goal of this particular tool is to find abnormalities that could potentially correspond to curated phenotypes. In this project, the phenotype files describe the harmonization of various TOPMed studies on that phenotype, and contain a few fields providing specific descriptions of the phenotype concept. 

## Approach

The initial step is to prepare the HPO data to access the different terms for comparison. Since the HPO is an ontology, the data is tree-structured. However, for the purposes of this project, it would be preferable to access the data in a flattened, non-hierarchical form. Since we are seeking the abnormalities that most closely align with the phenotype, and all the HPO terms are indexed, it is not consequential to treat the data as tree-structured. Instead, all the terms presented in the graph as nodes, are converted into a list containing the nodes. Each node corresponds to a specific HPO term. 

By observing the data contained in each HPO term node, there are two primary types: Descriptors and Traversers. The descriptive fields provide information about the abnormality contained in that specific node, while the traverser fields provide the information required to move across the ontology from that particular node. For the HPO matching objective, the descriptive fields are combined to form a single string document. Since the document is just a combination of the fields, it is not continuous. However, since these will be used in a word embedding model, it does not make a huge difference.

Once this process is carried out over all the nodes in the HPO, the documents are cleaned by converting removing punctuation and converting all the words to lowercase to make comparisons easier. Then, all the words found in all the nodes is recorded, and the TF-IDF score for each word in each corpus is calculated and scored. TF-IDF (Term Frequency - Inverse Document Frequency) is a statistic that reflects how important a certain word is to a document in the collection. For example, in an HPO term recording *Hydrocephalus*, CSF is a much better descriptor word than common words like the, from, of etc. This is reflected in the TF-IDF statistic.

Then, for each of the phenotype files (present in the directory as json files), another document is created from its fields. The information encoded for the phenotype is limited in scope to just the phenotype concept and description fields, as those are the most applicable fields from the harmonization files. Using the steps from above, the document is cleaned and the term frequency is calculated on this document using the model established from the HPO terms. Then, the similarity between this phenotype document and each of the HPO documents is calculated, and the three most similar terms are found as the output. The similarity between the documents is calculated using the Cosine metric.

This process is carried out for all the phenotype files iteratively and a table is created with the following fields. Here is an example of a row in the overall output table:

| Phenotype Concept | Most Similar Term                  | Second Term                                            | Third Term                        |
| ----------------- | ---------------------------------- | ------------------------------------------------------ | --------------------------------- |
| opg               | ('Hyperproteinemia', 'HP:0002152') | ('Abnormal blood glucose concentration', 'HP:0011015') | ('Hypoproteinemia', 'HP:0003075') |

The term columns contain both the name of the HPO term and its index, in the case that further exploration is required.

## Code

The entire process runs within a single script, *hpo_mapping.py* and the output file contains the mapping table and is named *hpo_map_1.txt* with the table in a comma separated format. In order to work with the table, it can be read into the environment and be treated as any normal csv file.

In order to run the script, the following command can be run on the terminal with no additional arguments:

```bash
$ python hpo_mapping.py
```

## Discussion

While the process is carried out for all the phenotypes, there are some categories like demographic phenotypes (race, sex etc.) that would not be applicable to having similar HPO terms. So, the output on these files are expected to be strange, but the process was successful in seeking HPO terms for other clinical phenotype categories. 