pmtris
======

Poor Man's Tetris Clone 

Current status: Works, but plenty of bugs.  A rewrite will be coming soon.  I'm going to try to lessen the strain of dealing with 2d/3d arrays(lists).  The rewrite will be OO.  And I'm thinking for farming out the manipulation and searching of 2d/3d arrays to methods.  Ostensibly there only need be code to search a single deminsion array.  And methods can be created for 2d/3d, that simply do recursive calls to the single deminsion code.  The module's methods will be called in a procedural style.  Akin to the likes of Fortran... or, perhaps HP RPL code.  Give yourself a scosh of Laphroaig if you know HP RPL!  i.e: get3d(3,4,1).set3d(6,7,2)

![screenshot](https://github.com/mhearse/pmtris/blob/master/screenshots/pmtris.png)
