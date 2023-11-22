# Automated IHC Image Analysis Script

## Background and Purpose
In stem cell research, immunohistochemistry (IHC) is a technique in which cells are stained for different surface or subcellular markers. Our project involved staining stem cells with different fluorescent markers to determine their phenotype during various stages of differentiation. With hundreds of IHC images to analyze, manual analysis was impractical due to time constraints and potential for error. To address this, I wrote a script in Java which automates the quantitative analysis of these images. 

## Objectives
The script was designed to:
- **Enhance Efficiency**: Dramatically reduce the time needed for image analysis, especially for large datasets.
- **Ensure Consistency**: Provide a uniform analysis process, eliminating subjective biases typical of manual analysis.
- **Improve Accuracy**: Increase precision in quantifying and categorizing fluorescent markers.

## Example: Human Pancreatic Beta Cells - PDX-1 staining (marker of insulin expression) 
<img width="241" alt="image" src="https://github.com/jwhitlow5/jw_eng/assets/9408895/b56cb649-6407-428a-ba51-4abcc52d9b15">
<img width="241" alt="image" src="https://github.com/jwhitlow5/jw_eng/assets/9408895/7e1b0301-2ab4-4c24-b710-33277cfc124b">

## Source Code
[ImmunoAnalysis.Java](https://github.com/jwhitlow5/Portfolio_JW/blob/master/IHC-Image-Analysis/ImmunoAnalysis.java)

## Script Functionality
Developed as a plugin for FIJI, the script automates several tasks:
1. **Image Preprocessing**:
   - Noise reduction using Canny edge blur or unsharp mask.
   - Background subtraction to highlight fluorescent markers.
2. **Segmentation and Analysis**:
   - Segments images based on fluorescent markers, categorizing stem cells by phenotype. Image masks are generated for each channel of fluorescence
3. **Customization and Flexibility**:
   - Allows for user input on scale, particle circularity, and minimum particle size.
4. **Batch Processing Capability**:
   - Processes multiple images in a batch, streamlining the workflow.
5. **Output and Saving**:
   - Saves masks of processed images and analysis results for further research.

## Conclusion
This Java-based script for automated IHC image analysis offers significant improvements in data throughput and accuracy for IHC studies. By leveraging Java programming and ImageJ, we have improved the efficiency, consistency, and accuracy of IHC image analysis, leading to more robust scientific discoveries.
