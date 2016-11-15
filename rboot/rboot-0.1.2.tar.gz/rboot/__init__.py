
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import numpy as np
import lz4
import struct

def bin_to_float(b):
    """ Convert binary string to a float. """
    bf = int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64
    return struct.unpack('>d', bf)[0]

def int_to_bytes(n, minlen=0):  # helper function
    """ Int/long to byte string. """
    nbits = n.bit_length() + (1 if n < 0 else 0)  # plus one for any sign bit
    nbytes = (nbits+7) // 8  # number of whole bytes
    b = bytearray()
    for _ in range(nbytes):
        b.append(n & 0xff)
        n >>= 8
    if minlen and len(b) < minlen:  # zero pad?
        b.extend([0] * (minlen-len(b)))
    return bytearray(reversed(b))  # high bytes first

def float_to_bin(f):
    """ Convert a float into a binary string. """
    ba = struct.pack('>d', f)
    ba = bytearray(ba)  # convert string to bytearray - not needed in py3
    s = ''.join('{:08b}'.format(b) for b in ba)
    return s[:-1].lstrip('0') + s[0] # strip all leading zeros except for last

def compute_probabilities(replacement_idx, a, conditional_binary):
    """ 
    Compute the compressed length of a bit string with 
    number as bit a replacing the number as bit in 
    position replacement_idx
    """
    conditional_binary[replacement_idx] = a
    return len(lz4.compress(''.join(conditional_binary))) #54.65

def get_replacement_dist(replacement_idx,conditional_binary,bit_series):
    # Compute the probability distribution for a specific replacement index over the alphabet of possible replacements realized in the given series
    probabilities = np.array([1./compute_probabilities(replacement_idx, a, conditional_binary) for a in bit_series])
    probabilities = probabilities/probabilities.sum()

    return probabilities

def replacement_bootstrap(series, bootstraps, seed=1978, replacement_percentage=1.0, replace=False, rho=0.25):
    """
    Name: Replacement Bootstrap
    
    Description: An implementation of the replacement bootstrap algorithm for dependent data.

    Parameters:
        series - Real or integer series
        bootstraps - Number of Bootstraps
        seed - Random number seed
        replacement_percentage - The percentage of the original series to replace max(1, 0.01 <= replacement_percentage).
        replace - Sample with or without replacement [True, False]
        rho - Concentration control. rho closer to 0 concentrates bootstraps towards the mean, while rho closer to 1 maximizes variability.
    """
    
    assert 0.0 < rho <= 1.0, "rho must be between 0 and 1"
    assert 0.0 < replacement_percentage, "replacement_percentage must be greater than 0"
    assert 0.0 < bootstraps, "bootstraps must be greater than 0"
    
    # Set the seed
    np.random.seed(int(seed))

    # Get the length of the original real numbered series
    T = series.shape[0]

    # A placeholder for the new bootstrap series
    bootstrap_series = series.copy()

    # Placeholder for bootstraps
    bootstrap_series = np.tile(bootstrap_series,(bootstraps,1))

    # A bit representation of the original series
    bit_series = [float_to_bin(v) for v in series]

    # The bit representation concatenated onto the bit representation to provide a conditional distribution for the compressor. All replacements occur on the first bit representation.
    conditional_binary = np.hstack([bit_series,bit_series])
    conditional_binary = np.tile(conditional_binary,(bootstraps,1))

    # Replacements (also the number of rounds)
    replacements = int(np.max([1,T*replacement_percentage]))

    # The index for replacements
    insertion_points = np.random.choice(T, replacements, replace=replace)

    # Get the number of bootstraps to replace in each round
    sampling_sequence = np.logspace(rho*np.exp(1), np.log(bootstraps), num=int(replacements), base=np.exp(1), endpoint=True, dtype=int)
    sampling_sequence[-1] = bootstraps
    sampling_sequence = sampling_sequence[::-1]

    bootstrap_choices = np.arange(bootstraps)

    for i_sampling, sampling in enumerate(sampling_sequence):
        replacement_idx = insertion_points[i_sampling]

        if i_sampling > 0:
            bootstrap_choices_idx = np.random.choice(sampling_sequence[i_sampling-1], sampling, replace=False)
            bootstrap_choices = bootstrap_choices[bootstrap_choices_idx]
            
            for i_bootstrap_choice in range(sampling):
                probabilities = get_replacement_dist(replacement_idx,conditional_binary[bootstrap_choices][i_bootstrap_choice],bit_series)

                # Draw a replacement according to the learned distribution
                replacement_choice = np.random.choice(T, 1, probabilities.tolist())[0]

                # Replace
                bootstrap_series[i_bootstrap_choice][replacement_idx] = series[replacement_choice]

                # Insert the bit representation into the conditional distribution used by the compressor
                conditional_binary[bootstrap_choices][i_bootstrap_choice][replacement_idx] = bit_series[replacement_choice]
        else:
            probabilities = get_replacement_dist(replacement_idx,conditional_binary[0],bit_series)

            # Draw a replacement according to the learned distribution
            replacement_choices = np.random.choice(T, sampling, probabilities.tolist())

            for i_bootstrap_choice, bootstrap_choice in enumerate(bootstrap_choices):
                    # Replace
                    bootstrap_series[i_bootstrap_choice][replacement_idx] = series[replacement_choices[i_bootstrap_choice]]

                    # Insert the bit representation into the conditional distribution used by the compressor
                    conditional_binary[bootstrap_choices][i_bootstrap_choice][replacement_idx] = bit_series[replacement_choices[i_bootstrap_choice]]
                    
    return bootstrap_series