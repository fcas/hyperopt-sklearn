from hpsklearn.components._base import validate

from hyperopt.pyll import scope
from hyperopt import hp

from sklearn import gaussian_process
import typing


@scope.define
def sklearn_GaussianProcessClassifier(*args, **kwargs):
    return gaussian_process.GaussianProcessClassifier(*args, **kwargs)


@validate(params=["optimizer"],
          validation_test=lambda param: isinstance(param, str) and param == "fmin_l_bfgs_b",
          msg="Invalid parameter '%s' with value '%s'. Value must be 'fmin_l_bfgs_b' or callable.")
@validate(params=["multi_class"],
          validation_test=lambda param: isinstance(param, str) and param in ["one_vs_rest", "one_vs_one"],
          msg="Invalid parameter '%s' with value '%s'. Value must be in ['one_vs_rest', 'one_vs_one'].")
def gaussian_process_classifier(name: str,
                                kernel=None,
                                optimizer: typing.Union[str, callable] = None,
                                n_restarts_optimizer: int = None,
                                max_iter_predict: int = None,
                                warm_start: bool = False,
                                copy_X_train: bool = True,
                                random_state=None,
                                multi_class: str = None,
                                n_jobs: int = 1):
    """
    Return a pyll graph with hyperparameters that will construct
    a sklearn.gaussian_process.GaussianProcessClassifier model.

    Args:
        name: name | str
        kernel: kernel instance
        optimizer: optimizer for kernel parameter optimization | str, callable
        n_restarts_optimizer: number of restarts optimizer | int
        max_iter_predict: maximum number of iterations for prediction | int
        warm_start: reuse previous fit solution | bool
        copy_X_train: store persistent copy of training data | bool
        random_state: random seed for center initialization | int
        multi_class: how multi class problems are handled | str
        n_jobs: number of CPUs to use | int
    """
    def _name(msg):
        return f"{name}.gaussian_process_classifier_{msg}"

    hp_space = dict(
        kernel=kernel,
        optimizer="fmin_l_bfgs_b" if optimizer is None else optimizer,
        n_restarts_optimizer=hp.pchoice(_name("n_restarts_optimizer"), [(0.5, 0), (0.10, 1), (0.10, 2), (0.10, 3),
                                                                        (0.10, 4), (0.10, 5)])
        if n_restarts_optimizer is None else n_restarts_optimizer,
        max_iter_predict=max_iter_predict or scope.int(hp.uniform(_name("max_iter_predict"), 75, 225)),
        warm_start=warm_start,
        copy_X_train=copy_X_train,
        random_state=hp.randint(_name("random_state"), 5) if random_state is None else random_state,
        multi_class=multi_class or hp.choice(_name("multi_class"), ["one_vs_rest", "one_vs_one"]),
        n_jobs=n_jobs
    )
    return scope.sklearn_GaussianProcessClassifier(**hp_space)
