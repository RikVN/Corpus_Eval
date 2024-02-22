# Corpus_Eval

Code for our LREC-COLING 2024 paper about evaluating mono-lingual web-crawled corpora.

## Getting Started

```
git clone https://github.com/RikVN/Corpus_Eval
cd Corpus_Eval
```

Create conda environment and install requirements:

```
conda create -n corpus_eval python=3.9
conda activate corpus_eval
pip install -r requirements.txt
```

## Data ##

The OSCAR, mC4 and CC100 data we download using HuggingFace. We do exact deduplication on document-level. Simply specify the corpus, language and a file to write to:

```
python src/download_data.py -c oscar -l hr -o hr.oscar
```

Note that for large languages this process can take quite a while. For OSCAR, we filter sentence that are labeled as "noisy" and sentences that are in the wrong language.

### MaCoCu

The MaCoCu data needs to be downloaded first before processing. Please check out the [MaCoCu website](https://macocu.eu/) for download locations.

For example, you can download Montenegrin like this:

```
curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1809/MaCoCu-cnr-1.0.xml.zip
unzip MaCoCu-cnr-1.0.xml.zip
```

Then process the file using our Python script. For Serbo-Croatian languages, specify both the Cyrillic and Latin language codes using ``-l hbs_lat hbs_cyr``. Our script automatically transliterates all data to Latin.

You can optionally specify the minimum token length (default 1) and the number of documents you want to keep. Please see line 81 of the Python script for an overview of the meta data columns.

```
python src/process_macocu.py -i MaCoCu-cnr-1.0.xml -o cnr.macocu -l hbs_cyr hbs_lat
```

This saves the texts, but also a lot of meta-data in a tab-separated file. This can be useful information to process the data further. If you just wants the texts, just run:

```
cut -f1 cnr.macocu > cnr.macocu.txt
```

## Annotations

We performed a manual evaluation of the data performed by professional linguists. The annotation files per annotator are in the ``anno`` folder. To rerun our analysis, simply run:

```
python src/analyse_annotations.py
```

This gives you an overview of the annotations per language and per annotator, as well as the inter-annotator agreements.

## Language Model Training

We trained the LMs on TPUs using the instructions in the [LanguageModels](https://github.com/macocu/LanguageModels) repository. Please see the README there for detailed steps.

All the LMs will be released publicly on [MaCoCu's HuggingFace page](https://huggingface.co/MaCoCu/XLMR-MaCoCu-is). For the "combined" setting of all four corpora we also release a model that was trained on 100k steps. This is not discussed in the paper, but is likely a stronger model.

## Language Model Evaluation

We fine-tune our trained LMs on POS, NER, COPA and CB. Fine-tuning scripts are available in the [LanguageModels](https://github.com/macocu/LanguageModels) repository or in the [COPA](https://github.com/RikVN/COPA) repository.

The specific train, dev and test splits we used in our evaluation are hosted here in the ``data`` folder.

### Scatter plot 

The scatterplot in the paper can be recreated like this:

```
python src/scatter.py
```

## Citation

This work was accepted to LREC-COLING 2024. Citation will be available soon.

## Acknowledgements

This work was part of the [MaCoCu](https://macocu.eu/) project. The MaCoCu project has received funding from the European Union’s Connecting Europe Facility 2014-2020 - CEF Telecom, under Grant Agreement No. INEA/CEF/ICT/A2020/2278341. This communication reflects only the authors’ views. The Agency is not responsible for any use that may be made of the information it contains. This research was supported with Cloud TPUs from Google's TPU Research Cloud (TRC).


