from kakuro import *
from graphic import *
import graphic
import threading

pre_start_graphic()
Kakuro_problem = Kakuro(graphic.selected_board)

def csp_calc(problem,params, slow=False):
    start = time.time()
    if params['inference'] is None:
        params['inference'] = no_inference
    if params['variable_ordering'] is None:
        params['variable_ordering'] = first_unassigned_variable
    if params['value_ordering'] is None:
        params['value_ordering'] = unordered_domain_values

    assignments = backtracking_search(problem, select_variable=params['variable_ordering'],
                                      order_values=params['value_ordering'], inference=params['inference'], slow=slow)

    end = time.time()
    print("\tSolved in: %.2f" % (end - start), "seconds.")
    print("\tMade", Kakuro_problem.num_assigns, "assignments.\n")


graphic_thread = threading.Thread(target=start_graphic, args=(Kakuro_problem,))
graphic_thread.start()

while not graphic.all_set:
    pass

params = graphic.parameters
csp_thread = threading.Thread(target=csp_calc, args=(Kakuro_problem, params, graphic.slow))
csp_thread.start()


