# CreativeSidescroller-

This is a simple python game that follows the guidelines below: 
## Animation Stuff
spritesheets (so the player is running, for example). Also, do this without using the spritesheet from the notes (you can easily find others all over the web).
Note that you cannot submit an image file with hw9. So you have to load your spritesheet using a URL. If you want to use a local image, then use one of the many free image sharing services (such as Imgur, Flickr, among many others) to place the image online so you and the graders can all load that image using a URL.
modes (at least a splash screen, main screen, and actually helpful help screen)
sidescrolling (of course) -- in that the game actually requires sidescrolling in order to win.
a custom cursor (image) following the mouse using mouseMoved. You can easily find images for this all over the web, or design your own!
the ability to drag-and-drop some objects in the game using the mouse

## OOPy Stuff
At least 3 well-chosen and well-designed top-level classes of objects (something like Player, Object, Enemy) and at least 2 well-chosen and well-designed subclasses (something like FastEnemy and SillyEnemy). So that's 5 total classes at minimum. Also, the inheritance needs to be done appropriately -- inheriting rather than copying code, etc.
At least one use of a set or dictionary whose keys are instances of one of your classes (thus showing that you understand how to use __eq__ and __hash__). For example, you might have a set of monsters that are currently frozen and cannot move.

## General Gameplay
The game should be simple, but fun and engaging.
It should be playable, in that someone can walk up and use it without knowing anything special about it. They may have to read a help screen, though.
If it makes sense at all, it should also be winnable and losable. If it is point-based, for example, then you can win if you get a certain number of points, and you can lose if you get below some number of points.
superhelp: if the user (or grader) presses 'S' (shift-s), then they should get superhelp. This should print to the console (unlike literally everything else, that must be in the canvas). It should print everything the player/grader needs to play the game, and also to grade it and be sure it complies fully with this spec.

