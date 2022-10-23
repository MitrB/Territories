from line_profiler import LineProfiler
from src.math_functions.math_functions import *
from src.gui.gui import main

lp = LineProfiler(main)
lp.add_function(calculate_delaunay)
lp.add_function(calculate_triangle_pairs)
lp.add_function(find_common_edge)
lp.add_function(make_locally_delaunay)
lp_wrapper = lp(main)
lp_wrapper()
lp.print_stats()
