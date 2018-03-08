# openCV_or_matlab_that_is_the_question

Testing out background subtraction in python(opencv) and matlab

OG_MOG.m is matlab implementation of the OG gaussian mixture model from http://personal.ee.surrey.ac.uk/Personal/R.Bowden/publications/avbs01/avbs01.pdf

subtractor.py module contains two foreground extractors:
  - the MOG2 model from http://www.zoranz.net/Publications/zivkovic2004ICPR.pdf
  - a K-nearest neighbors approach
  
The OG MOG performs best, both in framerate and foreground extraction, the other two suffer from a lot of salt noise during mask creation.
KNN also suffers from low framerate.

Demo video at: https://www.youtube.com/watch?v=dx9T59AC6cw

TODO:
  X - add youtube demo video links (see video link above)
  - Write instructions on how to use
