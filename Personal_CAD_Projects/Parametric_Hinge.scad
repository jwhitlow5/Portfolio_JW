//Parametric hinge designer
Height = 100; //hinge height
Width = 200; //hinge width
s_Z  = 1;
s_Y = 2; 
threadDiam = 4;        
headDiam = 8;
HeightHeadScrew   = 4;

numberSides=100; //# of sides (screw thread)
headGeometry=100; //# of sides of polygon (screw head)


/////////////////////////////////////////
wThickness = 0;
depth= wThickness == 0  ? Width/3 : wThickness;
W = Width;
H = Height;   
srn = s_Z -1; 

w_x = depth+((W-depth)/2);
w_Z = H/2; 
w_Y = HeightHeadScrew;
srn_width = s_Y-1; 


difference(){
	Base();
	Cut();
}


module Cut(){
	screwBody();
	screwBodyHead();
 	if (srn > 0 || srn_width > 0) {
	base_array_thread();
	base_array();
	}
}


 module screwVol(){
	for ( x = [0 : srn_width] ){
		for ( y = [0 : srn] ){
			union() {
			translate([(W-depth)*x+depth,(H*y)-H,0])cube([W-depth,H,depth]);
			translate([depth,(H*y)-H,(W-depth)*x+depth]) rotate([0,-90,0]) cube([W-depth,H,depth]);
			}
		}
	}
}


module base_array_thread(){
	for ( x = [0 : srn_width] ){
		for ( y = [0 : srn] ){
			translate([w_x+((W-depth)*x),w_Z+((y*H)-H),-W]) cylinder(W*2,0.5*threadDiam,0.5*threadDiam,$fn=numberSides);
			translate([W,w_Z+((y*H)-H),w_x+(W-depth)*x]) rotate([0,-90,0]) cylinder(W*2,0.5*threadDiam,0.5*threadDiam,$fn=numberSides);
		}
	}
}


module base_array(){
	for ( x = [0 : srn_width] ){
		for ( y = [0 : srn] ){
			translate([w_x+((W-depth)*x),w_Z+((y*H)-H),depth-w_Y]) cylinder(W*2,0.5*headDiam,0.5*headDiam,$fn=headGeometry);
			translate([(W*2)+depth-w_Y,w_Z+((y*H)-H),w_x+(W-depth)*x]) rotate([0,-90,0]) cylinder(W*2,0.5*headDiam,0.5*headDiam,$fn=headGeomtry);
		}
	}
}


module Base(){
	union() {
		hinge_volume();
		if (srn > 0 || srn_width > 0) {
		screwVol();
		}
	}
}
module hinge_volume(){
	for ( i = [0 : srn] ){
		union() {
		translate([0,(H*i)-H,0])cube([W,H,depth]);
		translate([depth,(H*i)-H,0]) rotate([0,-90,0]) cube([W,H,depth]);
		}
	}
}

module screwBody(){
	for ( i = [0 : srn] ){
		translate([w_x,w_Z+((i*H)-H),-W]) cylinder(W*2,0.5*threadDiam,0.5*threadDiam,$fn=numberSides);
		translate([W,w_Z+((i*H)-H),w_x]) rotate([0,-90,0]) cylinder(W*2,0.5*threadDiam,0.5*threadDiam,$fn=numberSides);
	}
}

module screwBodyHead(){
	for ( i = [0 : srn] ){
		translate([w_x,w_Z+((i*H)-H),depth-w_Y]) cylinder(W*2,0.5*headDiam,0.5*headDiam,$fn=headGeomtry);
		translate([(W*2)+depth-w_Y,w_Z+((i*H)-H),w_x]) rotate([0,-90,0]) cylinder(W*2,0.5*headDiam,0.5*headDiam,$fn=headGeometry);
	}
}


