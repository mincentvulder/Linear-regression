import numpy as np
from pathlib import Path
import logging
from nptyping import NDArray, Int
from typing import Tuple
from sources.classes import LinearRegression, PlotGraph

logging.basicConfig(level=logging.INFO)


def train_model(dataset: NDArray[(24, 2), Int[64]], model: LinearRegression, plot: bool) -> Tuple[float, float]:

    # initialize condition variables
    cost = model.cost()
    iteration = 1
    converged = False

    while not converged:
        grad0, grad1 = model.gradient_descent()
        model.update_thetas(grad0, grad1)

        new_cost = model.cost()

        if abs(cost - new_cost) <= model.crit_convergence:
            logging.info(f" Converged at iterations: {iteration}")
            converged = True
        cost = new_cost
        iteration += 1
    
        if iteration == model.max_iteration:
            logging.info(' Max iteration exceeded before converging.')
            converged = True
    model.unnormalize_thetas()

    if plot:
        plot_image = PlotGraph()
        plot_image.plot_basic_graph(model.undependent, model.dependent, model.t0, model.t1)
    logging.info(f" final thetas: {model.t0}, {model.t1}")

    return model.t0, model.t1


def initialize_model(max_iteration = 10000, crit_convergence = 0.00001, learning_rate = 0.1, plot = False):

    data_file = Path(Path.cwd()/"data.csv")

    if data_file.exists():
        # extract from csv file.
        dataset = np.genfromtxt(data_file, delimiter=',', skip_header=1, dtype=int)
        price = [x[1] for x in dataset]
        mileage = [x[0] for x in dataset]

        # normalize which the model requires.
        price_n = [(float(i) - min(price)) / (max(price) - min(price)) for i in price]
        mileage_n = [(float(i) - min(mileage)) / (max(mileage) - min(mileage)) for i in mileage]

        # initialize the model with standard values
        model = LinearRegression(price, mileage, price_n, mileage_n, len(dataset), max_iteration, crit_convergence, learning_rate)

        t0, t1 = train_model(dataset, model, plot)
        with open('thetas.csv', 'w') as f:
            f.write(f"{t0},{t1}")
    else:
        logging.error(f"Could not find your dataset, should be stored as such: {Path.cwd()}/data.csv")


if __name__ == "__main__":
    initialize_model()
