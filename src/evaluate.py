import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def mape(actual, predicted):
    """Mean absolute percentage error, ignoring zero-valued actuals."""
    actual, predicted = np.array(actual), np.array(predicted)
    mask = actual != 0
    return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100


def evaluate(actual, predicted, model_name):
    """Return a dict with RMSE, MAE, MAPE for a single model."""
    return {
        "model": model_name,
        "rmse": np.sqrt(mean_squared_error(actual, predicted)),
        "mae": mean_absolute_error(actual, predicted),
        "mape": mape(actual, predicted),
    }


def compare_models(results_list):
    """Print a formatted comparison table from a list of evaluate() dicts."""
    print(f"{'Model':<20} {'RMSE':>10} {'MAE':>10} {'MAPE':>10}")
    for r in results_list:
        print(f"{r['model']:<20} {r['rmse']:>10.6f} {r['mae']:>10.6f} {r['mape']:>9.2f}%")
