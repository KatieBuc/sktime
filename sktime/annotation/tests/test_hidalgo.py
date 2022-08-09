# -*- coding: utf-8 -*-
"""Test for hidalgo segmentation."""
import math

import numpy as np

from sktime.annotation.hidalgo import Hidalgo


def _isclose(list1, list2):
    return all(math.isclose(n1, n2, abs_tol=0.0002) for n1, n2 in zip(list1, list2))


# get model
model = Hidalgo(K=2, Niter=10, sampling_rate=2, seed=None)

# generate dataset
N = 10
N_half = int(N / 2)
np.random.seed(10002)
X = np.zeros((N, 6))

# half the points from one generating regime
for j in range(1):
    X[:N_half, j] = np.random.normal(0, 3, N_half)

# the other half from another
for j in range(3):
    X[N_half:, j] = np.random.normal(2, 1, N_half)


def test_X():
    """Test if innput data is of expected dimension and type."""
    assert isinstance(X, np.ndarray), "X should be a numpy array"
    assert len(np.shape(X)) == 2, "X should be a two-dimensional numpy array"


def test_get_neighbourhood_params():
    """Test for neighbourhood parameter generation."""
    model._get_neighbourhood_params(X)

    mu_check = [
        1.46472,
        5.40974,
        2.46472,
        4.78175,
        1.17461,
        1.95891,
        1.05864,
        1.06313,
        1.85041,
        1.28065,
    ]
    Iin_check = [
        2,
        4,
        7,
        3,
        9,
        4,
        0,
        4,
        7,
        1,
        4,
        9,
        0,
        9,
        3,
        8,
        6,
        9,
        8,
        5,
        9,
        5,
        8,
        9,
        5,
        6,
        7,
        5,
        7,
        4,
    ]
    Iout_check = [
        2,
        4,
        3,
        0,
        1,
        4,
        0,
        1,
        2,
        3,
        9,
        6,
        7,
        8,
        9,
        5,
        8,
        0,
        2,
        8,
        9,
        5,
        6,
        7,
        1,
        3,
        4,
        5,
        6,
        7,
    ]
    Iout_count_check = [2, 1, 1, 2, 5, 4, 2, 4, 3, 6]
    Iout_track_check = [0, 2, 3, 4, 6, 11, 15, 17, 21, 24]

    assert _isclose(model.mu, mu_check)
    assert _isclose(model.Iin, Iin_check)
    assert _isclose(model.Iout, Iout_check)
    assert _isclose(model.Iout_count, Iout_count_check)
    assert _isclose(model.Iout_track, Iout_track_check)


def test_initialise_params():
    """Test for initialise parameters."""
    Iin = [
        2,
        4,
        7,
        3,
        9,
        4,
        0,
        4,
        7,
        1,
        4,
        9,
        0,
        9,
        3,
        8,
        6,
        9,
        8,
        5,
        9,
        5,
        8,
        9,
        5,
        6,
        7,
        5,
        7,
        4,
    ]
    mu = np.array(
        [
            1.46472,
            5.40974,
            2.46472,
            4.78175,
            1.17461,
            1.95891,
            1.05864,
            1.06313,
            1.85041,
            1.28065,
        ]
    )

    model._get_neighbourhood_params(X)
    model.mu = mu
    model.Iin = Iin

    # initialise all other parameers, including randomly generated ones
    V, NN, a1, b1, c1, Z, f1, N_in = model._initialise_params()

    N_check = 10
    V_check = [
        3.67521,
        2.67584,
    ]
    NN_check = [
        6,
        4,
    ]
    d_check = [1.0, 1.0]
    p_check = [0.5, 0.5]
    a1_check = [
        7.0,
        5.0,
    ]
    b1_check = [
        4.67521,
        3.67584,
    ]
    c1_check = [
        7,
        5,
    ]
    Z_check = [
        1,
        0,
        0,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
    ]
    N_in_check = 12
    f1_check = [
        13.0,
        19.0,
    ]
    pp_check = 0.5

    assert model.N == N_check
    assert _isclose(Z, Z_check)
    assert _isclose(V, V_check)
    assert _isclose(NN, NN_check)
    # assert _isclose(d, d_check)
    # assert _isclose(p, p_check)
    assert _isclose(a1, a1_check)
    assert _isclose(b1, b1_check)
    assert _isclose(c1, c1_check)

    assert N_in == N_in_check
    assert _isclose(f1, f1_check)
    # assert pp == pp_check


def test_gibbs_sampling():
    """Tests gibbs sampler for one iteration."""
    model.mu = [
        1.46472,
        5.40974,
        2.46472,
        4.78175,
        1.17461,
        1.95891,
        1.05864,
        1.06313,
        1.85041,
        1.28065,
    ]
    model.Iin = [
        2,
        4,
        7,
        3,
        9,
        4,
        0,
        4,
        7,
        1,
        4,
        9,
        0,
        9,
        3,
        8,
        6,
        9,
        8,
        5,
        9,
        5,
        8,
        9,
        5,
        6,
        7,
        5,
        7,
        4,
    ]
    model.Iout = [
        2,
        4,
        3,
        0,
        1,
        4,
        0,
        1,
        2,
        3,
        9,
        6,
        7,
        8,
        9,
        5,
        8,
        0,
        2,
        8,
        9,
        5,
        6,
        7,
        1,
        3,
        4,
        5,
        6,
        7,
    ]
    model.Iout_count = [2, 1, 1, 2, 5, 4, 2, 4, 3, 6]
    model.Iout_track = [0, 2, 3, 4, 6, 11, 15, 17, 21, 24]
    model.N = 10

    V = [
        3.67521,
        2.67584,
    ]
    NN = [
        6,
        4,
    ]
    d = [1.0, 1.0]
    p = [0.5, 0.5]
    a1 = [
        7.0,
        5.0,
    ]
    b1 = [
        4.67521,
        3.67584,
    ]
    c1 = [
        7,
        5,
    ]
    Z = [
        1,
        0,
        0,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
    ]
    N_in = 12
    f1 = [
        13.0,
        19.0,
    ]
    pp = 0.5
    r = 1

    # random list arg
    sampling = model.gibbs_sampling(
        V,
        NN,
        a1,
        b1,
        c1,
        Z,
        f1,
        N_in,
    )
    sampling_check = [
        1.54721,
        1.1892,
        0.694958,
        0.305042,
        0.8,
        0,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        -18.4875,
        -8.44254,
    ]

    assert _isclose(sampling[:16], sampling_check)


def test_predict():
    """Tests predict for filtering, all iterations."""
    model = Hidalgo(K=2, Niter=10, sampling_rate=2, seed=None)
    fitted_model = model._fit(X)
    actual = fitted_model.predict(X)

    expected = [
        [
            3.04431,
            1.56489,
            0.332044,
            0.667956,
            0.8,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            -18.4604,
            -4.99662,
        ],
        [
            1.81112,
            0.892297,
            0.434086,
            0.565914,
            0.8,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            -18.1564,
            -4.69259,
        ],
    ]

    assert _isclose(fitted_model.sampling[0], expected[0])
    assert _isclose(fitted_model.sampling[1], expected[1])


def test_seed_predict():

    expected = [
        [
            0.72269469,
            3.20993546,
            0.59599049,
            0.40400951,
            0.8,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            -17.9650666,
            -4.50125762,
        ],
        [
            0.85025968,
            2.32993642,
            0.80166206,
            0.19833794,
            0.8,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            -19.21897121,
            -7.78773922,
        ],
    ]

    model = Hidalgo(K=2, Niter=10, sampling_rate=2, seed=1)
    fitted_model = model._fit(X)
    actual = fitted_model.predict(X)

    assert np.allclose(fitted_model.sampling, expected)


# also need to test for estimate_zeta = True AND use_Potts = True
