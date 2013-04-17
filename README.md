swascii
=======

A middleware for Openstack Swift to enable serving of dynamically generated
ASCII art from images stored within the object store.

The middleware should be configured in the pipeline, probably after auths and 
StaticWeb if you have that enabled. Using a filter section like this.

    [filter:swascii]
    use = egg:swascii#middleware

To request ASCII art the usual request is performed for the image object but the
HTTP Accept header should be set to 'text/plain'. An optional w parameter may
be provided to change the ASCII art width from its default of 80 chars.

The scaling can be a bit sketchy at some widths.

	$ curl -D -  -H 'Accept: text/plain;w=40' <AUTH> <URL>
	HTTP/1.1 200 OK
	Content-Length: 820
	Content-Type: text/plain
	Date: Sun, 27 Jan 2013 16:06:11 GMT

	                      YGKMA##8d.        
	                     .      .)A%K/      
	                ifdbmmbYXm)t,  P$#A     
	             !Q**dd,-f+=KbGt  d#WA#M    
	          .LNQP4*|  |   ,N+  Y#$%$W%5   
	        -)5b5NQb.  e    /|  ]%8%#$##%   
	       zXXm~Xb4.   Y-  /,  |%A$###%M#.  
	      4bXPPDDP-    2mj=    %#$$$$$$A%=  
	     XdmP~NNdc            5#8#%$%##W%=  
	    *Q~bD~45T             $$$$$%$%%$$   
	   iN4YNKYdQ.            (#8%$$%%#W%T   
	   5*~PDGXYj     ,       K$W%%#%#A#A    
	   dDKY*b4N-   VW$#%W-   4%A#%##W#A     
	  -D*Qdm*G5   (#%W##$%~  D#A#%#A%M      
	   PbXbNYP]  .#A%$#%A%A  )$8%8$#t       
	   2GQ4XXN-  m$$$$###8#= .$W$#W-        
	   .dQ*~b*   $%%#$###8#M  d$A=          
	    vXG4XK  c%W$8M#%$$$%Km[-            
	     _~~*g  z$$%#$##KKGg.               
	       ]K|    ,-..-,                    

	$ curl -D -  -H 'Accept: text/plain;w=50' <AUTH> <URL>
	HTTP/1.1 200 OK
	Content-Length: 1326
	Content-Type: text/plain
	Date: Sun, 27 Jan 2013 16:06:14 GMT

	                           zAK##$$%%WY\           
	                                .=TbW##K5,        
	                       .v=7+gg/i-.   ,tA%$b       
	                   iLd4N4~fmQ4dP4Gm=   A%A#K      
	                cfmmNK*Y= iY(g5GYQ[   A$##A#K     
	              ]PG4bX5~c  /=   -*4(   M%%%$#A$)    
	            t~4NdY~4X,  vc     Gf   K#A$%$$#%%    
	          =~4bm*4dKf    m     t/   G#M$%%$$#A%|   
	         V*NddmQ*d4    .Kc  .j-   j%8$$#$$%$K#X   
	       .KXNYdQ4mQD     ,QG*Nc    -%K##$#$$$$$#W   
	      -4~45Y4bddQ,       ,-      K###%%%#$$$#%A   
	     -YX*QdK5mmNt               /%8$%$#$%##$M%Y   
	     5K~5DQ4*PQP                4%$$%$%#$%#%W#,   
	    ]*N4KdGbQmmv                %$#%$%%%%#%#%A    
	    dQPKQ~dYQPX                -%A%%%%$#%$#8%-    
	   ,bdD*XP*N4K!     \~G~7-     i#K$%#%%#%#K$~     
	   =DGPDN5XG4X     A%#$$$#m    =%W#%###$$A$)      
	   vGKX~YN5**7    W#8MKKK8%A   !#W##%%#WA#v       
	   /mQPYG5~bmi   *#A$#$%#$A$f  .%A#%##8#K.        
	   ,4QDD*4*dD   .#K$%$%#%%%%8   8$$#8$$5          
	    GGD5QYmbY   ~%W$#$%###$8$=  )$8%$W_           
	    _45Pb~NQY   W#$$##$$$#$#$A   #$Ae             
	     YYY5X4*_  .%W##%$##%%KWA%jtK8|               
	      (4GG*X.  f#A%#%%##%###%$KY.                 
	       =bbQ*   iWWA$$%$KKKPL-                     
	         ~5*                                      

