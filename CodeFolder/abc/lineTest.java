//
//  Test.java
//  
//
//  Created by Joe Geigel on 1/21/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

import java.awt.*;

public class lineTest {
	
	public lineTest () {}	
    
	static public void main(String[] args){
		
		simpleCanvas T = new simpleCanvas(300, 300);
        Rasterizer R = new Rasterizer (300);
        
        T.setColor (0.0f, 0.0f, 0.0f);
		T.clear();
		T.setColor (1.0f, 1.0f, 1.0f);
		
		R.drawLine( 100, 100, 100, 150, T );  /* Vertical */
		R.drawLine( 100, 100, 100, 50, T );   /* Vertical */
		
		R.drawLine( 100, 100, 50, 100, T );   /* Horizontal */
		R.drawLine( 100, 100, 150, 100, T);  /* Horizontal */
		
		R.drawLine( 100, 100, 150, 150, T );  /* + diagonal */
		R.drawLine( 100, 100, 50, 50, T );    /* + diagonal */
		
		R.drawLine( 100, 100, 50, 150, T );   /* - diagonal */
		R.drawLine( 100, 100, 150, 50, T );   /* - diagonal */
		
		R.drawLine( 100, 100, 150, 125, T );  /* shallow + slope */
		R.drawLine( 100, 100, 50, 75, T );    /* shallow + slope */
    
		R.drawLine( 100, 100, 150, 75, T );   /* shallow - slope */
		R.drawLine( 100, 100, 50, 125, T );   /* shallow - slope */
		
		R.drawLine( 100, 100, 125, 150, T );  /* steep + slope */
		R.drawLine( 100, 100, 75, 50, T );    /* steep + slope */
		
		R.drawLine( 100, 100, 125, 50, T );   /* steep - slope */
		R.drawLine( 100, 100, 75, 150, T );   /* steep - slope */
        
        Frame f = new Frame( "line Test" );
        f.add("Center", T);
		f.pack();
		f.setResizable (false);
        f.setVisible(true);
		
	}
        
}
