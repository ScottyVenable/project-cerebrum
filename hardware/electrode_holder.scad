/*
 * Project Cerebrum: Parametric Electrode Holder
 * For custom active-dry electrodes.
 * 
 * This OpenSCAD script generates a modular socket for 
 * gold-plated spring pins and OPA333 active circuitry.
 */

// Parameters
electrode_diameter = 12; // mm
socket_depth = 15;        // mm
wall_thickness = 2;       // mm
pin_hole_diameter = 2.5;  // mm for spring pin

module electrode_socket() {
    difference() {
        // Main Body
        cylinder(h=socket_depth, d=electrode_diameter + (2 * wall_thickness), $fn=100);
        
        // Internal Cavity
        translate([0, 0, wall_thickness])
            cylinder(h=socket_depth, d=electrode_diameter, $fn=100);
            
        // Pin Hole
        cylinder(h=socket_depth, d=pin_hole_diameter, $fn=50);
        
        // Wire Exit Slot
        translate([electrode_diameter/2, -1, socket_depth-5])
            cube([wall_thickness + 2, 2, 5]);
    }
}

// Render
electrode_socket();
