"""
EXPERIMENT REGISTER
"""

def mixsimulator(seed: tp.Optional[int] = None) -> tp.Iterator[Experiment]:
    """MixSimulator of power plants
    Budget 10, 20, ..., 1600.
    Sequential or 30 workers."""
    funcs = [OptimizeMix()]
    seedg = create_seed_generator(seed)
    optims = ["OnePlusOne","NGOpt","NGOptRL","CMA","DE","PSO"]
    if default_optims is not None:
        optims = default_optims
    seq = np.arrange(0,1601,20)
    for budget in seq:
        for num_workers in [1, 30]:
            if num_workers < budget:
                for algo in optims:
                    for fu in funcs:
                        xp = Experiment(fu, algo, budget, num_workers=num_workers, seed=next(seedg))
                        if not xp.is_incoherent:
                            yield xp