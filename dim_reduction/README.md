# Dimensionality Reduction

Due to the high dimensionality of our input we had to use a PySpark based implementation to reduce it.

## Input

Our input is a list containing the generated ELMo vectors (1024 dimensions).
Each vectors has to be formated following this example:

*word - 0.6579854,1.161026,0.43898278,[...],2.0629232,0.063231304*


## Output

The output is formated as following:

*write,"-8.898457162048345,-0.08643378936279938"*