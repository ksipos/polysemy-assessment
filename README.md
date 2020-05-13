### What is this repo for?

This repository contains code and data to reproduce the results presented in the paper: **Unsupervised Word Polysemy Quantification with Multiresolution Grids of Contextual Embeddings** (Xypolopoulos et al. 2020). [link to arXiv](https://arxiv.org/abs/2003.10224)

### Method

- The number of senses of a given word, or polysemy, is a very subjective notion, which varies widely across annotators and resources.

- We propose a novel method to estimate polysemy, based on simple geometry in the contextual embedding space. Our approach is fully unsupervised and purely data-driven, which makes it applicable to any language.

- We show through rigorous experiments that our rankings are well correlated (with strong statistical significance) with 6 different rankings derived from famous human-constructed resources such as WordNet, OntoNotes, Oxford, Wikipedia etc., for 6 different standard metrics. We also visualize and analyze the correlation between the human rankings.

- A valuable by-product of our method is the ability to sample, at no extra cost, sentences containing different senses of a given word.

<p align="center">
<img src="https://raw.githubusercontent.com/ksipos/polysemy-assessment/master/figures/pyramid_illustration_cropped.png" alt="" width="750"/>
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/ksipos/polysemy-assessment/master/figures/heatmap.png" alt="" width="450"/>
</p>

### External Resources

- [WordNet](https://www.nltk.org/howto/wordnet.html)
- [Wikipedia](https://dumps.wikimedia.org/)
- [Ontonotes](https://catalog.ldc.upenn.edu/LDC2013T19) (requires application)
- [WordNet-Domains](http://wndomains.fbk.eu/) (requires application)
- [Deep contextualized word embeddings](https://allennlp.org/elmo)

We used AllenAI's Embeddings from Language Models (ELMo) and specifically the command line [tool](https://github.com/allenai/allennlp/blob/master/docs/tutorials/how_to/elmo.md#writing-contextual-representations-to-disk) provided by the authors.

### Cite :thumbsup:

If you use some of the code in this repository, or simply if you want to refer to our paper, please cite:

```BibTeX
@article{xypolopoulos2020unsupervised,
    title={Unsupervised Word Polysemy Quantification with Multiresolution Grids of Contextual Embeddings},
    author={Christos Xypolopoulos and Antoine J. -P. Tixier and Michalis Vazirgiannis},
    year={2020},
    eprint={2003.10224},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

> Xypolopoulos, Christos, Antoine J-P. Tixier, and Michalis Vazirgiannis. "Unsupervised Word Polysemy Quantification with Multiresolution Grids of Contextual Embeddings." arXiv preprint arXiv:2003.10224 (2020).

### Acknowledgements :thumbsup: 

- We thank [Giannis Nikolentzos](https://github.com/giannisnik) for helpful discussions about pyramid matching.

- This work was supported by the [LinTo](https://linto.ai/) project.

- We gratefully acknowledge the support of NVidia Corporation that donated the Titan V GPU used for this research.
