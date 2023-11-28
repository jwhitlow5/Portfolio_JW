### 2. Implementing Feedback Loops in Microsphere Production

The challenge of creating double emulsion microspheres involves achieving precise control over a large number of variables such as fluid flow rates and compositions. Traditional methods required cumbersome adjustments based on qualitative observations. I implemented a software-based feedback loop to maximize data throughput by monitoring microsphere dimensions in real time with high speed microscopy. By extracting dimensional data from the output in real time, I was able to adjust my experimental conditions based on immediate feedback responses.


<p align="center"><img width="400" alt="image" src="https://github.com/jwhitlow5/Portfolio_JW/blob/master/Microfluidics/Microscopy/imgs/1.png">
<p align="center">Table displaying variables controlled for stable emulsion preparation

## Custom-Built Microscope for Real-Time Analysis: 
I built a high speed video microscope for acquiring brightfield images of the microspheres at the outlet of the microchannel and captured and processed image data with OpenCV on a Raspberry Pi 4. The use of OpenCV for image segmentation enabled real time analysis of size distribution of microsphere produced in the microchannel. The outcome was a significant enhancement in efficiency, enabling on-the-fly adjustments without the need to pause and manually inspect under a standard microscope.

<p align="center"><img width="600" alt="image" src="https://github.com/jwhitlow5/Portfolio_JW/blob/master/Microfluidics/Microscopy/imgs/2.jpg">


<p align="center"><img width="600" alt="image" src="https://github.com/jwhitlow5/Portfolio_JW/blob/master/Microfluidics/Microscopy/imgs/3.png">

