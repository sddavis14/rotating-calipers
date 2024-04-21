# Rotating Calipers
Computational geometry project for CSC591 at NCSU


By Varun & Spencer

## Minimum Area Bounding Rectangle
The minimum area bounding rectangle problem is concerned with finding the smallest possible rectangle that encloses a 
point set. Rotating calipers can be employed to solve this problem in linear time. The graphic in [1] provides a concise
illustration of the algorithm.

<p align="center">
    <img src="min_area_rect.png" width="300">
</p>

First, the convex hull of the point set is computed. Then, two sets of "calipers" are initialized with axis-aligned 
orientation, anchored to anti-podal points. Next, the calipers are rotated by the smallest angle to the next convex hull 
edge. This process is continued until the rectangles are rotated up to 90 degrees, and finally the minimum area 
rectangle is selected.


To execute the demo, run
```
python3 minimum_area_rectangle_demo.py
```
Click points in the rectangular drawing window and press enter to run the algorithm. The demo will display the tested 
rectangles along with their area. After rotating the calipers 90 degrees, the minimum area rectangle is selected and 
displayed.

## Diameter of Convex Polygon

As before, initially the convex hull of the point set is computed. A single pair of calipers are aligned with x axis in opposite directions and anchored to anti-podal points. Again, the calipers are rotated by the smallest angle to the next convex hull edge such that at least one of the calipers reaches a new vertex, forming a new anti-podal pair. Everytime a new pair is created, the distance between the pair is stored. The calipers are rotated until they reach their initial starting point and the pair with the largest distance form the diameter of the polygon.

To execute the demo, run

```
python3 diameter_demo.py
```
Click points in the rectangular drawing window and press enter to run the algorithm. The demo will measure and show the distance between all pairs that occur. Once the algorithm is complete, the diameter and its length are shown.

## Maximum Distance between two Convex Polygons

The process of finding the maximum distance between two convex polygons is similar to that of finding the diameter of a convex polygon. The difference is that each caliper is placed on different polygons. As before, the calipers are rotated until they reach their initial starting point and the pair with the largest distance is the largest distance between the two convex polygons.

To execute the demo, run

```
python3 maxdist.py
```
Click points in the rectangular drawing window and press enter to create the first convex polygon. Repeat the process to create the second convex polygon and press enter to run the algorithm. The demo will measure and show the distance between all pairs that occur. Once the algorithm is complete, the diameter and its length are shown.

## Citations

[1] https://web.cs.swarthmore.edu/~adanner/cs97/s08/pdf/calipers.pdf

[2] https://www-cgrl.cs.mcgill.ca/~godfried/publications/maxdist2.pdf
