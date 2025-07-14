Ace Combat 3 Layer Merger for TIM files v1.1
by Dashman

0) What's new?
Basically, this time it works. I had forgotten to apply my initial guesses into the code, stupid me.

1) How to use this thing.

First of all, this is a Java applet. If you don't have Java, install the latest JRE.
Second, this is a command line application. To execute it, you'll need to open up a console/shell window, get to the folder where the program is and execute this:

java -jar ac3lm.jar <TIM_layer1> <TIM_layer2> <output_file>

2) Stuff to note.

* TIM_layer1 and TIM_layer2 are the TIM files that you want to merge into the TIM with two CLUTs (output_file).

* DON'T try to merge TIM files with more than one CLUT, the result won't be pretty.

* This program doesn't support batches, sorry. 

* The file paths are taken relative to the folder where the program is, but I haven't tested it that much so try to have everything in the same folder :P

* No more OR operation. This time it checks the indexed colours of both layers and writes the index that is colour in one layer and transparent on the other, as simple as that.