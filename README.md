# Unsupervised Polysemy Assessment

The number of senses of a given word, or polysemy, is a very subjective notion, which varies widely across annotators and resources. We propose a novel method to estimate polysemy, based on simple geometry in the contextual embedding space. Our approach is fully unsupervised and purely data-driven.


![pyramid_illustration](figures/pyramid_illustration_cropped.png "TITLE")


## External Resources

- [WordNet](https://www.nltk.org/howto/wordnet.html)

- [Wikipedia](https://dumps.wikimedia.org/)

- [Ontonotes](https://catalog.ldc.upenn.edu/LDC2013T19) (requires application)

- [WordNet-Domains](http://wndomains.fbk.eu/) (requires application)

- [Deep contextualized word embeddings](https://allennlp.org/elmo)

AllenAI's Embeddings from Language Models (ELMo) and specifically we used the provided command line [tool](https://github.com/allenai/allennlp/blob/master/docs/tutorials/how_to/elmo.md#writing-contextual-representations-to-disk). 

## Cite

```
@article{xypolopoulos2020unsupervised,
    title={Unsupervised Word Polysemy Quantification with Multiresolution Grids of Contextual Embeddings},
    author={Christos Xypolopoulos and Antoine J. -P. Tixier and Michalis Vazirgiannis},
    year={2020},
    eprint={2003.10224},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

## Acknowledgements 

We gratefully acknowledge the support of NVIDIA Corporation with the donation of the Titan V GPU used for this research.
