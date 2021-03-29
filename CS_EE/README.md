# A Comparison of Principal Component Analysis and Factor Analysis as Dimensionality Reduction and Denoising Techniques for Neural Network Inputs

## About
This is an investigation into two methods of dimensionality reduction: Principal Component Analysis and Factor Analysis.

This investigation was initiated in 2019 as part of the author's International Baccalaureate Computer Science Extended Essay, for submission in March 2021. Due to confidentiality reasons, the full paper will be released in August 2021. 

## Index terms
principal component analysis, factor analysis, dimensionality reduction, noise, machine learning, neural network


## Abstract
The use of dimensionality reduction techniques like principal component analysis (PCA) and factor analysis (FA) is increasingly important as computer scientists are presented with “big data”: high volumes of high-dimensional data collected from everyday life. Big data is the fuel for artificial intelligence, yet noises or less relevant information inherent in large datasets are costly obstacles to machine learning algorithms. Therefore, it is crucial to have effective methods that reduces dimensionality, removes noise, while simultaneously preserving key information.

This investigation is a comparison of PCA and FA in terms of their effectiveness as preprocessing algorithms on neural network inputs, both in the absence and presence of noise. First, the dimensionality reduction characteristics are tested by running a feed-forward neural network that accepts PCA or FA-reduced data as inputs. The network’s performance (i.e., validation accuracy and computational complexity) serves as the metrics for evaluation. Subsequently, the noise removal characteristics are tested by adding different levels of AWGN, speckle, or salt and pepper noise to the dataset, before applying PCA or FA and running the neural network.

Results from the experiment show that PCA performs better in the presence of low levels of noise (regardless of type), while FA performs better in selected scenarios involving high levels of noise. Nevertheless, compared to trials without the use of dimensionality reduction, both PCA and FA sacrifice some degree of accuracy. Computer scientists or future researchers are advised to use the experimental and comparative structure outlined in this investigation to weigh the merits and demerits of applying dimensionality reduction in their specific contexts.


## License

MIT License
Copyright (c) 2021 [Carl Ma](https://github.com/macarl08)

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

**NOTE:** This software depends on other packages that may be licensed under different open source licenses.
