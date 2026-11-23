# Survivors

The original n=10 counterexample CNF was SAT. Its complete witness satisfies every original clause. Its distance classes, recovered from the Boolean comparison literals with `inspect_model.py`, are in [distance_classes.txt](runs/n10/distance_classes.txt) and the raw witness is in [model.txt](runs/n10/model.txt).

The first class contains edges 9-0, 0-1, 9-1, 1-2, 2-3 and 1-3. Any realization must make triangles (9,0,1) and (1,2,3) equilateral. The rays from vertex 1 occur in cyclic chain order 2, 3, 9, 0. Both outer sectors, 2-1-3 and 9-1-0, equal 60 degrees. Strict convexity bounds the sum of these two angles and the middle angle 3-1-9 below 180 degrees, hence the middle angle is strictly less than 60 degrees. However, edges 1-3 and 1-9 are shortest-class edges and edge 3-9 lies in the next class. By side-angle ordering in triangle (3,1,9), the angle at 1 is the largest and is strictly greater than 60 degrees. The contradiction rules out that SAT assignment exactly.

The FAN extension encodes this angle argument for every five-vertex pattern. The final n=10 and n=12 CNFs are UNSAT, so those configurations leave no survivors. SAT witnesses from weakened ablation CNFs were kept as controls and carry no geometric verdict.
