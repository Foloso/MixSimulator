#!/usr/bin/python3
import copy
import os
import random
import sys
import threading
import time
import warnings
from datetime import datetime
from math import ceil
from typing import Dict, List

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

import mixsimulator.nevergradBased.Optimizer as opt
from mixsimulator import ElectricityMix
from mixsimulator.agents.Moderator import StoppableThread

# from mixsimulator.Evaluation import EvaluationBudget
from mixsimulator.demand.classic.Demand import Demand

"""
    (0) Functions : Check the thread running in background, plot cost results and generate scenarios
"""


def generate_random_scenario(centrals: List, time_index: int) -> Dict:
    scenario: Dict = {}
    tmp: Dict = {}
    for central in centrals:
        tmp.update({"down": [], "up": []})
        default_proba = random.uniform(0, 0.07)

        for i in range(time_index):
            tmp[np.random.choice(["up", "down"], p=[1 - default_proba, default_proba])].append(i)

        up = []
        down = []
        for i in range(time_index):
            if i in tmp["down"] and (i - 1 not in tmp["down"] or i == 0):
                down.append(i)
            if i - 1 in tmp["down"] and i in tmp["up"]:
                up.append(i)
        tmp["up"] = up
        tmp["down"] = down

        scenario.update({central: tmp.copy()})

    print("scenario: ", scenario)
    event_stack: Dict = {}
    for i in range(time_index):
        for central in scenario.keys():
            if i in scenario[central]["down"]:
                try:
                    event_stack[i].append((central._notify_is_down, central, "down"))
                except:
                    event_stack.update({i: [(central._notify_is_down, central, "down")]})
            elif i in scenario[central]["up"]:
                try:
                    event_stack[i].append((central._notify_is_up, central, "up"))
                except:
                    event_stack.update({i: [(central._notify_is_up, central, "up")]})

    # print(numpy.arange(0, 2))
    # print("scenario: ", event_stack)
    return event_stack


def check_thread_running():
    list_ = []
    while True:
        tmp = threading.enumerate().copy()
        if tmp != list_:
            list_ = tmp
            for thread in list_:
                if thread.is_alive():
                    print("THREAD:  " + thread.name)
        time.sleep(10)


def moving_average(x, w):
    return np.convolve(x, np.ones(w), "valid") / w


def plot_loss(optimum, mode: str = "default", average_wide: int = 0, step: int = 1):
    # set the moving average wide
    if average_wide == 0:
        average_wide = ceil(len(optimum[-1]["coef"]) / 4)

    if mode == "default" or mode == "save" or mode == "best":
        # set Y
        Y_: Dict[str, List[float]] = {}
        Y_["cost"] = []
        Y_["demand_gap"] = []
        for t_i in range(0, len(optimum)):
            Y_["cost"].append(optimum[t_i]["loss"])
            Y_["demand_gap"].append(optimum[t_i]["unsatisfied demand"])

        fig, axs = plt.subplots(1, 2, figsize=(10, 10))

        # data integration
        X = [(i + 1) * step for i in range(0, len(optimum))]
        # smooth_value = moving_average(Y_["cost"],average_wide)
        for n_axs in range(0, 2):
            if n_axs == 0:
                # axs[n_axs].plot(X[(average_wide - 1):], smooth_value, '.-' ,alpha=0.5, lw=2, label="cost")
                axs[n_axs].plot(X, Y_["cost"], ".-", alpha=0.5, lw=2, label="cost")
            else:
                axs[n_axs].plot(X, Y_["demand_gap"], "-*", alpha=0.5, lw=2, label="demand gap")

        # Add execution_time and cost information
        try:
            info = (
                "Final cost: "
                + "{:.3f}".format(optimum[-1]["loss"])
                + " ; run_time: "
                + "{:.3f}".format(optimum[-1]["elapsed_time"])
            )
        except:
            info = "production_cost: " + "{:.3f}".format(optimum[-1]["loss"])
        info += ";Final demand gap: " + "{:.3f}".format(optimum[-1]["unsatisfied demand"])
        plt.annotate(
            info,
            xy=(0.5, 0),
            xytext=(0, 10),
            xycoords=("axes fraction", "figure fraction"),
            textcoords="offset points",
            size=10,
            ha="center",
            va="bottom",
        )

        # plots parametrizations
        for n_axs in range(0, 2):
            axs[n_axs].grid()
            axs[n_axs].yaxis.set_tick_params(length=0)
            axs[n_axs].xaxis.set_tick_params(length=0)
            axs[n_axs].set_xlabel("budgets")
            # axs[n_axs].yaxis.set_major_formatter(StrMethodFormatter("{x}"+units[0]))
            if n_axs == 0:
                axs[n_axs].set_ylabel("cost")
            elif n_axs == 1:
                axs[n_axs].set_ylabel("Demand gap")
            axs[n_axs].legend()

        fig.tight_layout()
        try:
            path = "cost_results_" + datetime.now().strftime("%d_%m_%Y")
            os.makedirs(path)
            name = path + "/" + "opt_" + str(datetime.now().strftime("%H%M%S")) + ".png"
            fig.savefig(name)
            if mode == "default":
                plt.show()

        except OSError:
            warnings.warn("Can't create the directory " + path + " or already exists")
            try:
                name = path + "/" + "opt_" + str(datetime.now().strftime("%H%M%S")) + ".png"
                fig.savefig(name)
                if mode == "default":
                    plt.show()
            except FileNotFoundError:
                name = "opt_" + str(datetime.now().strftime("%H%M%S")) + ".png"
                fig.savefig(name)
                if mode == "default":
                    plt.show()

    elif mode == "None":
        pass
    else:
        warnings.warn("Choose an available option : default, save or None")
        # plt.show()


"""
(1) INITIALIZATION  PARAMS:
        - Configure nevergrad optimizers : argument[1] is opt_name, arg[2] is budget, arg[3] num_worker
        - time index as duration (arg[4]),
        - step of evaluation as step_budget (arg[5]),
        - time_interval as t_i (arg[6]).
"""
opt_name = "OnePlusOne"
budget = 100
num_worker = 1
duration = 24
step_budget = round(budget / 10)
t_i = 1  # time_interval
log_filename = "log.txt"
numb_run = 1

for i in range(1, len(sys.argv)):
    if i == 1:
        opt_name = str(sys.argv[i])
    elif i == 2:
        budget = int(sys.argv[i])
    elif i == 3:
        num_worker = int(sys.argv[i])
    elif i == 4:
        duration = int(sys.argv[i])
    elif i == 5:
        step_budget = int(sys.argv[i])
    elif i == 6:
        t_i = int(sys.argv[i])
    elif i == 7:
        numb_run = int(sys.argv[i])
    elif i == 8:
        log_filename = str(sys.argv[i]) + ".pickle"

for run_ in range(numb_run):
    ### optimizer vim
    thread_checker = StoppableThread(target=check_thread_running, name="thread_checker")
    thread_checker.start()
    opt_ = opt.Optimizer(opt=[opt_name], budget=[budget], num_worker=num_worker)
    """
    (2) Init MixSimulator instance :
        Case one [Default] : "classic" method (see test_classic.py for more use case)
        Case two : "MAS" or Multi Agent System method

        Default parameters :
        ------------------------
        method : string = "classic",    --> method explain above
        carbon_cost : float = 0         --> cost of the CO2 production
        penalisation_cost: float = 1e7  --> penalisation cost when production is more or less than the demand #NEED VERIFICATION
    """

    classic_mix = ElectricityMix().mix(method="classic", carbon_cost=0, penalisation_cost=100)
    mas_mix = ElectricityMix().mix(method="MAS", carbon_cost=0, penalisation_cost=100)

    centrals = mas_mix.get_moderator().get_observable()
    scenario = generate_random_scenario(centrals, duration)

    """
    (3) ONE SHOT optimization by calling the classic approach

    """
    classic_mix.set_data_to("Toamasina")
    demand = Demand()
    demand.set_data_to("Toamasina", delimiter=",")
    classic_mix.set_demand(demand)

    start_time = time.time()
    classic_result = classic_mix.optimizeMix(
        1e10, optimizer=opt_, step=step_budget, penalisation=100, carbon_cost=0, time_index=duration, plot="save"
    ).copy()
    ###
    ### MODIFY RESULTS BASED ON EVENTS
    backup_results = copy.deepcopy(classic_result)
    for t in scenario.keys():
        for event in scenario[t]:
            for position, central in enumerate(classic_mix.get_centrals()):
                if central.get_id() == event[1].get_name():
                    if event[2] == "down":
                        for step_, value in enumerate(classic_result):
                            for ti in range(t, duration):
                                classic_result[step_]["coef"][ti][position] = 0.0
                    elif event[2] == "up":
                        for step_, value in enumerate(classic_result):
                            for ti in range(t, duration):
                                classic_result[step_]["coef"][ti][position] = backup_results[step_]["coef"][ti][
                                    position
                                ]

    for step_, value in enumerate(classic_result):
        classic_result[step_]["cost"] = classic_mix.loss_function(
            classic_result[step_]["coef"], time_interval=t_i, no_arrange=True
        )
    classic_runtime = time.time() - start_time

    ###
    ### print(classic_result)
    ### PLEASE Check this specific plot in the folder "cost_result_....."
    plot_loss(classic_result, step=step_budget, mode="save")

    """
    (4) Simulating the mas platform (Manually)
            1 - First, set params by using set_params method
            2 - Launch the run_optimization method to initiate the simulation
            3 - Add events
            4 - Get the result after all threads done
    """
    start_runtime = time.time()
    mas_mix.get_moderator().set_params(
        1e10, optimizer=opt_, step=step_budget, penalisation=100, carbon_cost=0, time_index=duration, plot="None"
    )
    mas_mix.get_moderator().run_optimization()

    for t in scenario.keys():
        for event in scenario[t]:
            event[0](t)

    ### Waiting method
    while True:
        if len(threading.enumerate()) == 2:
            thread_checker.stop()
            break
    print("SIMULATION DONE")
    mas_runtime = time.time() - start_time

    mas_mix.get_moderator().plotResults(mas_mix.get_moderator().get_results(), mode="save")

    ### PLEASE Check this specific plot in the folder "cost_result_....."
    plot_loss(mas_mix.get_moderator().get_results(), step=step_budget, mode="save")

    log: Dict = {"run_nb": run_}
    log.update(
        {
            "Perf": (
                (classic_result[-1]["loss"] - mas_mix.get_moderator().get_results()[-1]["loss"])
                / classic_result[-1]["loss"]
            )
            * 100,
            "events": scenario,
            "opt_params": classic_mix.get_params(),
            "mas_results": mas_mix.get_moderator().get_results(),
            "classic_results": classic_result,
            "classic_runtime": classic_runtime,
            "mas_runtime": mas_runtime,
        }
    )

    file_ = open(log_filename, "a")
    print(log, file=file_)
    file_.close
