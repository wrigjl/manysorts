# manysorts
several different sorting algorithms with visualization in python/matplotlib

These were written to help visualize several sorting algorithms for a lecture on sorting.

The code is somewhat convoluted to make it visualizable.  It seems that
matplotlib on MacOS doesn't like to be run from a thread, so it runs as
a main thread and the sorting algorithm runs in a subthread.  Coordination
being handled by a Queue.  Also, when using 'blit=True', the programs crash
when the drawing window is closed.  Any suggestions for a fix welcome
(note: blit'n is used because the flicker from blit=False is annoying on
a ChromeCast).
