Author: Kulunchakov Andrei
GitHub: KuluAndrej

# Multivariate Regression Composer (Python3)

**MVR** is a project for construction and approximation of nonlinear functions to a given data. Nonlinear functions are represented as 
superpositions of primitive functions set up by experts. The generation is done via Genetic Programming (composition of *mutations*, 
*crossovers* and random generations). This process is iterative and each iteration consists of two steps:

- Production of new models. The stored models are participate in *mutations* and *crossovers* producing new elements of the 
corresponding functional space.
- Best models selection. This step embodies *natural selection*. Only the best representatives of current population are passed to 
the next iterations.

The project currently has two purposes.

- Data fitting.

We have a data and need to reveal underlying dependencies between independent variables and dependent ones.

- Time series classification.

We have a bunch of time series and need to extract its structural representation. Namely, we approximate nonlinear functions 
to these time series, represent these functions as labeled trees and extract structural features from these trees. Given features
are attached to corresponding time series.
Resulted representation could be used in tasks of classification, clustering and anomaly detection.

