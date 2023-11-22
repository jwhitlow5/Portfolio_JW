//2020 Jon Whitlow
import ij.*;
import ij.Prefs;
import ij.process.*;
import ij.gui.*;
import java.io.File;
import java.util.ArrayList;
import java.awt.*;
import ij.plugin.*;
import fiji.util.gui.GenericDialogPlus;
import ij.process.*;  
import ij.io.FileSaver;
import inra.ijpb.morphology.*;
import java.io.*;
import ij.io.*;
import javax.swing.*;
import javax.swing.filechooser.*; 

public class CellIFAnalysis implements PlugIn{
	static File dir;
	public String userInputScale = "1.0";
	public String circ = "0";
	public String minSize = "0";
	public int noiseMode = 0; //0 is blur, 1 is unsharp mask
	public String[] noiseProc = {"Apply Canny edge blur before segmentation","Apply unsharp mask prior to segmentation"};
	
	public void run(String arg) {
		GenericDialogPlus gd=new GenericDialogPlus("Immunofluorescence Image Processor");
		loadPrefs();
		
		gd.addStringField("Scale (microns per pixel)",userInputScale);
		gd.addStringField("Particle circularity",circ);
		gd.addStringField("Minimum particle size",minSize);
		gd.addChoice("Blur or unsharp mask noise?",noiseProc,noiseProc[0]);
		gd.showDialog();
		if (gd.wasCanceled()){
			//make sure instance of gdplus is deallocated?
		}else{
	
			userInputScale = gd.getNextString();
			circ = gd.getNextString();
			minSize = gd.getNextString();
			noiseMode = gd.getNextChoiceIndex();
			setPrefs();
		}
		openFiles();
	}

	 void loadPrefs(){
		userInputScale = Prefs.get("my.persistent.scale","1.0");
		circ = Prefs.get("my.persistent.circ","0");
		minSize = Prefs.get("my.persistent.minsize","0");
		String mode = Prefs.get("my.persistent.mode","0");
		if (mode=="0"){
			noiseMode = 0;
		} else {
			noiseMode = 1;
		}
				
		return;
	}
	
	 void setPrefs(){
		Prefs.set("my.persistent.scale", userInputScale);
    	Prefs.set("my.persistent.circ", circ);
    	Prefs.set("my.persistent.minsize", minSize);
   		Prefs.set("my.persistent.mode", noiseMode);
   		Prefs.savePreferences();
   		return;
	}

	
	public void openFiles() {
		JFileChooser fc = null;
		try {fc = new JFileChooser();}
		catch (Throwable e) {IJ.error("This plugin requires Java 2 or Swing."); return;}
		fc.setMultiSelectionEnabled(true);
		if (dir==null) {
			String sdir =OpenDialog.getLastDirectory();// OpenDialog.getDefaultDirectory();
			if (sdir!=null)
				dir = new File(sdir);
		}
		if (dir!=null)
			fc.setCurrentDirectory(dir);
		int returnVal = fc.showOpenDialog(IJ.getInstance());
		if (returnVal!=JFileChooser.APPROVE_OPTION)
			return;
		File[] files = fc.getSelectedFiles();
		if (files.length==0) { // getSelectedFiles does not work on some JVMs
			files = new File[1];
			files[0] = fc.getSelectedFile();
		}
		String path = fc.getCurrentDirectory().getPath()+Prefs.getFileSeparator();
		dir = fc.getCurrentDirectory();
		String maskDir = dir + "/masks/";
		File mDir = new File(maskDir);
		if (!mDir.exists()){
			boolean pointlessVariable = mDir.mkdir();
			if (!pointlessVariable){
				IJ.log("ohno");
			}
		}
		
		//Opener opener = new Opener();
		for (int i=0; i<files.length; i++) {
			
			ImagePlus img = processImg(path + files[i].getName());
		
			if (img!=null){
				try{
					new FileSaver(img).saveAsPng(maskDir+files[i].getName());
				}
				catch (Throwable e) {
						IJ.error("Mask not saved, something's not right with the file directory." +files[i].getName()); 
						return;
				}
				IJ.wait(500);
				closeAllWindowsBehind();
				
		}       
		
		 
	}
	}
	public ImagePlus processImg(String imgFilePath){
		ImagePlus imp = IJ.openImage(imgFilePath);
		String title = imp.getTitle();
		imp.setTitle("ref");
		ImagePlus imp2 = duplicateObject("new",imp);
		imp2.show();
		imp2=convertTo8bit(imp2);
		IJ.run(imp2, "Subtract Background...", "rolling=15 sliding disable");
		if (noiseMode ==0){ //haha
			IJ.run(imp2,"Gaussian Blur...","sigma=1");
		}
		else {
			IJ.run(imp2,"Unsharp Mask...","radius=1 mask=0.6");
		}
		imp2.updateAndDraw();
		IJ.run(imp2,"Invert","");
		imp2.show();
		ImagePlus thresh = duplicateObject("thresh",imp2);
		IJ.run(thresh,"Gaussian Blur...","sigma=1");
		thresh.updateAndDraw();
		thresh=autoThresh(thresh);
		thresh.show();
		IJ.run(thresh, "Invert", "");
		
		ImagePlus threshNew = morph(thresh,0,2);
		threshNew.updateAndDraw();threshNew.show();
		IJ.run(threshNew,"Kill Borders","");
		ImagePlus impnew2 =WindowManager.getCurrentImage();
		IJ.run(impnew2, "3-3-2 RGB", "");
		IJ.run(impnew2, "Distance Transform Watershed", "distances=[Quasi-Euclidean (1,1.41)] output=[32 bits] normalize dynamic=1 connectivity=4");
		ImagePlus impnew3 =WindowManager.getCurrentImage();
		IJ.run(impnew3,"8-bit","");
		//IJ.run(thresh, "Label Size Filtering", "operation=Lower_Than size=40");
		
		impnew3=trimThreshold(impnew3,1);
		impnew3.setTitle(title);
		IJ.run(impnew3,"Set Scale...", "distance=1 known="+userInputScale+" pixel=1 unit=pixel");
		IJ.run(impnew3,"Set Measurements...","area mean min perimeter shape integrated area_fraction redirect=new decimal=1");
		IJ.run(impnew3,"Analyze Particles...","size="+minSize+"-Infinity pixel circularity="+circ+"-1.00 show=Masks clear summarize");
		ImagePlus impMask =WindowManager.getCurrentImage();
		IJ.run(impMask,"Label Boundaries","");
		ImagePlus overLay = WindowManager.getCurrentImage();
		overLay.setTitle("OL");
		IJ.run(imp,"Binary Overlay","reference=[new] binary=[OL] overlay=red");
		ImagePlus impOL = WindowManager.getCurrentImage();
		return impOL;
	}
	
	public ImagePlus morph(ImagePlus imp_old,int proc, int rad){
	//proc= 0  dilation; proc = 1 erosion
		ImageProcessor img = imp_old.getProcessor();
		ImagePlus morphImg;
		if (proc==0){
			ImageProcessor dil  = Morphology.dilation(img,Strel.Shape.OCTAGON.fromDiameter(rad));
			morphImg = new ImagePlus("dilation",dil);
		} else if (proc==1){
			ImageProcessor dil  = Morphology.erosion(img,Strel.Shape.OCTAGON.fromDiameter(rad));
			morphImg = new ImagePlus("erosion",dil);
		} else{
			ImageProcessor dil  = Morphology.closing(img,Strel.Shape.OCTAGON.fromDiameter(rad));
			morphImg = new ImagePlus("closing",dil);
		}
		morphImg.updateAndDraw();
		morphImg.show();
		return morphImg;
	}
	
	public void closeAllWindowsBehind(){
		int[] k= WindowManager.getIDList();
		for (int z=0;z<k.length;++z){
			ImagePlus impt = WindowManager.getImage(k[z]);
			impt.changes=false;
			if (impt!=null){
				closeImage(impt);
				IJ.wait(50);
			}
		}
		return;
	}
	
	public void closeImage(ImagePlus imp) {
		if (imp==null) {
			IJ.noImage();
			return;
		}
		imp.close();
	   
	}
	
	public ImagePlus trimThreshold(ImagePlus imp_1, int lower){
		ImageProcessor ip = imp_1.getProcessor();
		ImagePlus newImp = new ImagePlus(imp_1.getTitle()+" th1-255",ip);
		ip.setThreshold(lower,255, ImageProcessor.NO_LUT_UPDATE);
		newImp.setProcessor(ip);
		newImp.show();
		newImp.updateAndDraw();
		IJ.run(newImp,"Convert to Mask","");
		newImp.updateAndDraw();
		return newImp;
	}
	
	public ImagePlus autoThresh(ImagePlus imp_1){
		ImageProcessor ip_th = imp_1.getProcessor();
		ImagePlus imp = new ImagePlus(imp_1.getTitle()+ " thresh",ip_th);
		imp.show();
		imp.updateAndDraw();
		imp = convertTo8bit(imp);
		imp.updateAndDraw();
		ip_th.setAutoThreshold(AutoThresholder.Method.Otsu, true);
		imp.setProcessor(ip_th);
		IJ.run(imp,"Convert to Mask","");
		imp.updateAndDraw();
		return imp;
	}
	
	public ImagePlus convertTo8bit(ImagePlus imp_1){
		ImagePlus imp = new ImagePlus(imp_1.getTitle()+"8bit",imp_1.getProcessor());
		ImageConverter ic = new ImageConverter(imp);
		ic.convertToGray8();
		imp.updateAndDraw();
		return imp;
	}
	
	public ImagePlus duplicateObject(String title,ImagePlus imp_2){
		ImagePlus temp =WindowManager.getTempCurrentImage();
		WindowManager.setTempCurrentImage(imp_2);
		ImagePlus newWin= imp_2.duplicate();
		newWin.setTitle(title);
		newWin.getProcessor().setColorModel(imp_2.getProcessor().getColorModel());
		WindowManager.setTempCurrentImage(temp);
		return newWin;
	}
	

}
