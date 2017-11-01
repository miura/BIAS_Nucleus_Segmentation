orgName = getTitle();
run("Split Channels");
c1 = "C1-" + orgName;
c2 = "C2-" + orgName;
opt = "area mean centroid perimeter shape integrated limit display redirect=" + c2 + " decimal=3";
run("Set Measurements...", opt);
selectWindow(c1);
for (i =0; i < nSlices; i++){
	setSlice(i+1);
	run("Create Selection");
	run("Make Inverse");
	run("Measure");
}
