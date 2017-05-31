"""
Module contains a set of functions which produce binary sequences either pseudo-random
or deterministic. Algorithms are developed based on the book *Spread Spectrum Systems for
GNSS and Wireless Communications* by Jack K. Holmes.

Returned binary sequences are numpy arrays of the type *bool*.
"""
import numpy as np

def ssrg(init_reg, fb_reg, **args):

    """
    The function generates a binary sequence using structure of the *simple shift register generator*
    -- SSRG -- with M-bit shift register. The generator is in a Fibonacci form. The length of the shift
    register *M* is defined by the length of the register *init_reg* or *fb_reg*. Both are suppose to
    be of the same length.

    :param init_reg: M-bit initialization sequence in the shift register. NumPy array *bool*.
    :param fb_reg: M-bit Numpy *bool* array which defines feedbacks of the shift register. Log *1* means a feedback exists for an appropriate bit of the register.
    :param args: optional set of arguments

    +-------------+-------------+----------+-------------------------------------------+
    | Key word    | Possible    | Default  | Description                               |
    |             | values      |          |                                           |
    +=============+=============+==========+===========================================+
    | n_bits      | positive    |          |                                           |
    |             | integers    |     7    | length of the output sequence in bits     |
    +-------------+-------------+----------+-------------------------------------------+
    | verbosity   | boolean T/F | *False*  |  *False* - nothing to be printed,         |
    |             |             |          |  *True* - the state of the shift register |
    |             |             |          |  is being printed  for each cycle         |
    +-------------+-------------+----------+-------------------------------------------+

    :return: a binary sequence of the length 'n-bits' (default 7 bits) -- the output code.

    **Example:**

    See, how to use the function to produce a 7-bits output sequence by the 3-bits SSRG with the feedback from the output of
    the first and the second bit of the shift register. The register is initialized by one log. *1* at
    the first bit (*numpy-array's element [0]*):

    >>> import numpy as np
    >>> import PRN_bitstream as prn
    >>> init = np.array ([1,0,0])
    >>> fb = np.array ([0,1,1])
    >>> out_seq = prn.ssrg(init,fb)

    Another example producing the output sequence with length of 50 bits and states of the shift register
    printed for each step:

    >>> import numpy as np
    >>> import PRN_bitstream as prn
    >>> init = np.array ([1,0,0,0,0,0])
    >>> fb = np.array   ([0,1,1,0,1,0])
    >>> out_seq = prn.ssrg(init,fb,n_bits=50,verbosity=True)

    """
    if 'n_bits' in args:
        n_bits = int(args['n_bits'])
    else:
        n_bits = 7

    if 'verbosity' in args:
        verbosity = bool(args['verbosity'])
    else:
        verbosity = False

    #  Output register
    x=np.zeros([n_bits])
    #  Shift register
    shft_reg = init_reg
    nob = len(shft_reg)
    #  Feedback registers - bit '1' means -> FB is connected
    #  defined as an input argument fb_reg
    for i1 in range (0,n_bits-1):
        in1 = int(np.dot(shft_reg,fb_reg)%2)
        x[i1] = shft_reg[nob-1]
        shft_reg = np.roll(shft_reg,1)
        shft_reg[0] = in1
        if verbosity:
            print('For i=',i1,'shift register:',shft_reg,'output:',x)
    return (x.astype(bool))

def gold_seq(x1, x2, **args):
    """
    The function generates *Gold's binary sequence* using two 10-bits SSRGs *G1* and *G2* when
    each of which generates a *maximal length sequence* of the length *N = 2^10 - 1*.
    * G1 = x^10 + x^3
    * G2 = x^10 + x^9 + x^8 + x^6 + x^3 + x^2
    Both of the registers are initialized by a sequence *[1 1 1 1 1 1 1 1 1 1]*.

    The output sequence is an exclusive *OR* result of the G1 output and delayed G2 output. The
    delayed G2 output is obtained by the exclusive *OR* of the selected positions of the two taps
    defined by input arguments **x1** and **x2**.

    All the structure is developed according to the GPS standards -- *Interface Control
    Document IS-GPS-200H* -- C/A code.

    :param x1: the first selected position from the *G2*
    :param x2: the second selected position from the *G2*
    :param args: optional set of arguments

    +-------------+-------------+----------+---------------------------------------------------+
    | Key word    | Possible    | Default  | Description                                       |
    |             | values      |          |                                                   |
    +=============+=============+==========+===================================================+
    | no_bits     | positive    |          |  number of bits generated for one period, full    |
    |             | integers    |   1023   |  period of the Gold's code contains 1023 bits     |
    +-------------+-------------+----------+---------------------------------------------------+
    | no_periods  | positive    |          |  number of periods of the code                    |
    |             | integers    |   1      |  being generated                                  |
    +-------------+-------------+----------+---------------------------------------------------+
    | verbosity   | boolean T/F | *False*  |  *False* - nothing to be printed,                 |
    |             |             |          |  *True* - the state of the shift register         |
    |             |             |          |  and feedbacks is being printed  for each cycle   |
    +-------------+-------------+----------+---------------------------------------------------+

    :return: a binary sequence of the length 'no_bits' x 'no_periods' -- the Gold's code.

    **Example:**

    Gold's sequence generator being used to generate a PRN code of the satellite SV1. Returned is one
    period with a full length of 1023 bits. Generator in a silence mode (*verbosity*=False):

    >>> import PRN_bitstream as prn
    >>> out_seq = prn.gold_seq(2,6)

    And the same but 30 periods are generated in row:

    >>> import PRN_bitstream as prn
    >>> out_seq = prn.gold_seq(2,6,no_periods = 30)

    Another example producing a PRN code of the satellite SV2. Returned is only a fragment of the period,
    first 100 bits of the code. Generator provides text output for each of the cycles to check internal
    state of its registers and feedbacks:

    >>> import PRN_bitstream as prn
    >>> out_seq = prn.gold_seq(3,7,no_bits = 100, verbosity = True)
    """

    if 'verbosity' in args:
        verbosity = bool(args['verbosity'])
    else:
        verbosity = False

    if 'no_bits' in args:
        no_bits = int(args['no_bits'])
    else:
        no_bits = 1023

    if 'no_periods' in args:
        no_periods = int(args['no_periods'])
    else:
        no_periods = 1

    # Output register
    x = np.zeros([no_periods * no_bits])
    # Maximum-length sequence generators:
    #  Shift registers
    shft_reg_1 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    shft_reg_2 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    #  Feedback registers - bit '1' means -> FB is connected
    fbck_reg_1 = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 1])
    fbck_reg_2 = np.array([0, 1, 1, 0, 0, 1, 0, 1, 1, 1])

    if verbosity == 1:
        print('G1: ', shft_reg_1, 'G2: ', shft_reg_2)

    for i1 in range(0, no_periods * no_bits):
        g1 = shft_reg_1[9]
        g2 = (shft_reg_2[x1 - 1] + shft_reg_2[x2 - 1]) % 2
        x[i1] = (g1 + g2) % 2

        in1 = np.dot(shft_reg_1, fbck_reg_1) % 2
        in2 = np.dot(shft_reg_2, fbck_reg_2) % 2

        shft_reg_1 = np.roll(shft_reg_1, 1)
        shft_reg_1[0] = in1

        shft_reg_2 = np.roll(shft_reg_2, 1)
        shft_reg_2[0] = in2

        # g1  = shft_reg_1 [9]
        # g2  = ( shft_reg_2[x1] + shft_reg_2[x2] ) % 2
        # x[i1] = ( g1 + g2 ) % 2

        if verbosity == 1:
            print('G1:', shft_reg_1, 'G2:', shft_reg_2, 'g2a:', shft_reg_2[x1], 'g2b:', shft_reg_2[x2], 'g2out:', g2,
                  'g1out:', g1, 'out:', x[i1])

    return (x.astype(bool))
