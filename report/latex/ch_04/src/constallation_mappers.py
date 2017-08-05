
"""

    :return: Baseband signal
"""
    tup = 2  # number of bits in one tuple
    n_d = tup - (np.size(data) % tup)
    data = np.append(data, np.zeros(n_d))  # appends zero to get odd number of bits
    data_2s = data.reshape(-1, tup)  # reshaping the data vector into matrix
    data_2s = data_2s > 0

