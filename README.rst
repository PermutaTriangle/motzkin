#######
motzkin
#######

Motzkin is a Python library for counting and sampling sets of Motzkin paths defined by pattern avoidance.

If you need support, you can join us in our `Discord support server`_.

.. _Discord support server: https://discord.gg/ngPZVT5

Installing
==========

To install Motzkin on your system, run the following after cloning the repository:

.. code-block:: bash

    ./setup.py

It is also possible to install Motzkin in development mode to work on the
source code, in which case you run the following after cloning the repository:

.. code-block:: bash

    ./setup.py develop
    

Using Motzkin
#############

The motzkin library is built on top of the comb_spec_searcher module. To find a specification for a set of pattern avoiding Motzkin paths we first create a MotzkinSpecificationFinder.

.. code-block:: python

    >>> from motzkin import MotzkinSpecificationFinder

We initialise the MotzkinSpecificationFinder with the patterns.

.. code-block:: python

    >>> patterns = ["UUHD", "DDHU"]
    >>> msf = MotzkinSpecificationFinder(patterns)

The MotzkinSpecificationFinder is a CombinatorialSpecificationFinder from the comb_spec_searcher module and as such we can use those underlying methods. To find the specification call the auto_search method.

.. code-block:: python

    >>> specification = msf.auto_search()
    [I 210316 10:15:17 comb_spec_searcher:585] Auto search started Tue, 16 Mar 2021 10:15:17
        Initialising CombSpecSearcher for the combinatorial class:
        Av(UDUHD, UUDHD, UUHDD)
        Looking for recursive combinatorial specification with the strategies:
        Inferral: 
        Initial: Remove known letters.
        Verification: verify atoms
        Set 1: A path is empty, starts with H, or starts with U, pattern insertions
        
    [I 210316 10:15:19 base:235] Specification detected.
    [I 210316 10:15:19 base:241] Minimizing for 0 seconds.
    [I 210316 10:15:19 base:247] Found specification with 22 rules.
    [I 210316 10:15:19 comb_spec_searcher:698] Creating a specification.
    [I 210316 10:15:19 comb_spec_searcher:524] Specification built Tue, 16 Mar 2021 10:15:19
        Time taken: 0:00:01
        CSS status:
            Total time accounted for: 0:00:01
                                                                Number of
                                                                applications    Time spent    Percentage
            ------------------------------------------------  --------------  ------------  ------------
            is empty                                                     205       0:00:01           90%
            verify atoms                                                  96       0:00:00            0%
            Remove known letters.                                         87       0:00:00            0%
            get specification                                             16       0:00:00            4%
            A path is empty, starts with H, or starts with U              39       0:00:00            0%
            pattern insertions                                            39       0:00:00            3%
        ClassDB status:
            Total number of combinatorial classes found is 116
        Queue status (currently on level 5):
            Queue              Size
            ---------------  ------
            working               8
            current (set 1)      10
            next                 11
            The size of the current queues at each level: 1, 3, 14, 29, 25
        RuleDB status:
                                                    Total number
            ---------------------------------------  --------------
            Combinatorial rules                                 107
            Equivalence rules                                    28
            Combintorial rules up to equivalence                 95
            Strategy verified combinatorial classes               3
            Verified combinatorial classes                       60
            combinatorial classes up to equivalence              73
            Called find equiv path 16 times, for total time of 0.0 seconds.
        
        Memory Status:
            ------------  --------
            OS Allocated  55.9 MiB
            CSS            442 KiB
            ClassDB        327 KiB
            ClassQueue      20 KiB
            RuleDB          91 KiB
            ------------  --------
        Specification found has 29 rules

The specification returned is a CombinatorialSpecification from the comb_spec_searcher module. To view these you can either print specification for a string representation or use the show method to visualise the specification in a proof tree format. 

.. code-block:: python

    >>> print(specification)
    A combinatorial specification with 29 rules.
    --------------
    0 -> (1, 2, 3)
    A path is empty, starts with H, or starts with U
    Av(UDUHD, UUDHD, UUHDD)  =  {λ}  +  AvH(UDUHD, UUDHD, UUHDD)∩Co(H)  +  AvU(λ-UHD, UDUD-HUD, UUDD-HUD, UDUDH-UD, UDUHD-λ, UUDDH-UD, UUDHD-λ, UUHDD-λ)∩Co(UD-λ)
    -------
    1 -> ()
    is atom
    {λ}
    -----------
    2 -> (4, 0)
    Remove known letters.
    AvH(UDUHD, UUDHD, UUHDD)∩Co(H)  =  {H}  x  Av(UDUHD, UUDHD, UUHDD)
    -------
    4 -> ()
    is atom
    {H}
    -----
    3 = 5
    The paths avoid or contain UDUDH-λ but only the child at index 0 is non-empty, then The paths avoid or contain UUDDH-λ but only the child at index 0 is non-empty
    AvU(λ-UHD, UDUD-HUD, UUDD-HUD, UDUDH-UD, UDUHD-λ, UUDDH-UD, UUDHD-λ, UUHDD-λ)∩Co(UD-λ)  =  AvU(λ-UHD, UDUD-HUD, UUDD-HUD, UDUDH-λ, UDUHD-λ, UUDDH-UD, UUDHD-λ, UUHDD-λ)∩Co(UD-λ)  =  AvU(λ-UHD, UDUD-HUD, UUDD-HUD, UDUDH-λ, UDUHD-λ, UUDDH-λ, UUDHD-λ, UUHDD-λ)∩Co(UD-λ)
    -----------
    5 -> (6, 7)
    The paths avoid or contain λ-HUD
    AvU(λ-UHD, UDUD-HUD, UUDD-HUD, UDUDH-λ, UDUHD-λ, UUDDH-λ, UUDHD-λ, UUHDD-λ)∩Co(UD-λ)  =  AvU(λ-HUD, λ-UHD, UDUDH-λ, UDUHD-λ, UUDDH-λ, UUDHD-λ, UUHDD-λ)∩Co(UD-λ)  +  AvU(λ-UHD, UDUD-λ, UUDD-λ)∩Co(λ-HUD)∩Co(UD-λ)
    ---------------
    6 -> (8, 9, 10)
    Remove known letters.
    AvU(λ-HUD, λ-UHD, UDUDH-λ, UDUHD-λ, UUDDH-λ, UUDHD-λ, UUHDD-λ)∩Co(UD-λ)  =  {UD}  x  Av(UDH, UHD)  x  Av(HUD, UHD)
    -------
    8 -> ()
    is atom
    {UD}
    ----------------
    9 -> (1, 11, 12)
    A path is empty, starts with H, or starts with U
    Av(UDH, UHD)  =  {λ}  +  AvH(UDH, UHD)∩Co(H)  +  AvU(λ-H, UDH-λ, UHD-λ)∩Co(UD-λ)
    ------------
    11 -> (4, 9)
    Remove known letters.
    AvH(UDH, UHD)∩Co(H)  =  {H}  x  Av(UDH, UHD)
    -----------------
    12 -> (8, 13, 13)
    Remove known letters.
    AvU(λ-H, UDH-λ, UHD-λ)∩Co(UD-λ)  =  {UD}  x  Av(H)  x  Av(H)
    -----------------
    13 -> (1, 14, 15)
    A path is empty, starts with H, or starts with U
    Av(H)  =  {λ}  +  ∅  +  AvU(λ-H, H-λ)∩Co(UD-λ)
    --------
    14 -> ()
    is empty
    ∅
    -----------------
    15 -> (8, 13, 13)
    Remove known letters.
    AvU(λ-H, H-λ)∩Co(UD-λ)  =  {UD}  x  Av(H)  x  Av(H)
    -----------------
    10 -> (1, 16, 17)
    A path is empty, starts with H, or starts with U
    Av(HUD, UHD)  =  {λ}  +  AvH(HUD, UHD)∩Co(H)  +  AvU(λ-HUD, λ-UHD, H-UD, HUD-λ, UHD-λ)∩Co(UD-λ)
    -------------
    16 -> (4, 18)
    Remove known letters.
    AvH(HUD, UHD)∩Co(H)  =  {H}  x  Av(UD)
    -----------------
    18 -> (1, 19, 20)
    A path is empty, starts with H, or starts with U
    Av(UD)  =  {λ}  +  AvH(UD)∩Co(H)  +  ∅
    -------------
    19 -> (4, 18)
    Remove known letters.
    AvH(UD)∩Co(H)  =  {H}  x  Av(UD)
    --------
    20 -> ()
    is empty
    ∅
    -------
    17 = 21
    The paths avoid or contain H-λ but only the child at index 0 is non-empty
    AvU(λ-HUD, λ-UHD, H-UD, HUD-λ, UHD-λ)∩Co(UD-λ)  =  AvU(λ-HUD, λ-UHD, H-λ)∩Co(UD-λ)
    -----------------
    21 -> (8, 13, 10)
    Remove known letters.
    AvU(λ-HUD, λ-UHD, H-λ)∩Co(UD-λ)  =  {UD}  x  Av(H)  x  Av(HUD, UHD)
    ----------------
    7 -> (8, 18, 22)
    Remove known letters.
    AvU(λ-UHD, UDUD-λ, UUDD-λ)∩Co(λ-HUD)∩Co(UD-λ)  =  {UD}  x  Av(UD)  x  Av(UHD)∩Co(HUD)
    -------
    22 = 23
    A path is empty, starts with H, or starts with U but only the child at index 1 is non-empty
    Av(UHD)∩Co(HUD)  =  AvH(UHD)∩Co(HUD)
    -------------
    23 -> (4, 24)
    Remove known letters.
    AvH(UHD)∩Co(HUD)  =  {H}  x  Av(UHD)∩Co(UD)
    ------------------
    24 -> (25, 26, 27)
    A path is empty, starts with H, or starts with U
    Av(UHD)∩Co(UD)  =  ∅  +  AvH(UHD)∩Co(H)∩Co(UD)  +  AvU(λ-HUD, λ-UHD, UDH-UD, UHD-λ)∩Co(UD-λ)
    --------
    25 -> ()
    is empty
    ∅
    -------------
    26 -> (4, 24)
    Remove known letters.
    AvH(UHD)∩Co(H)∩Co(UD)  =  {H}  x  Av(UHD)∩Co(UD)
    -------
    27 = 28
    The paths avoid or contain UDH-λ but only the child at index 0 is non-empty
    AvU(λ-HUD, λ-UHD, UDH-UD, UHD-λ)∩Co(UD-λ)  =  AvU(λ-HUD, λ-UHD, UDH-λ, UHD-λ)∩Co(UD-λ)
    -----------------
    28 -> (8, 13, 10)
    Remove known letters.
    AvU(λ-HUD, λ-UHD, UDH-λ, UHD-λ)∩Co(UD-λ)  =  {UD}  x  Av(H)  x  Av(HUD, UHD)

    >>> specification.show()
    [I 210316 10:15:19 specification_drawer:520] Opening specification in browser
    [I 210316 10:15:23 specification_drawer:506] specification html file removed

As we now have a CombinatorialSpecification we can utilise the underlying methods for counting and randomly sampling this set of Motzkin paths. 

To count we could either find the generating function or use the specification as a recurrence.

.. code-block:: python

    >>> specification.get_genf()
    [I 210316 10:15:19 specification:351] Computing initial conditions
    [I 210316 10:15:19 specification:325] Computing initial conditions
    [I 210316 10:15:19 specification:353] The system of 29 equations
        root_func := F_0:
        eqs := [
        F_0 = F_1 + F_2 + F_3,
        F_1 = 1,
        F_2 = F_0*F_4,
        F_3 = F_5,
        F_4 = x,
        F_5 = F_6 + F_7,
        F_6 = F_10*F_8*F_9,
        F_7 = F_18*F_22*F_8,
        F_8 = x**2,
        F_9 = F_1 + F_11 + F_12,
        F_10 = F_1 + F_16 + F_17,
        F_11 = F_4*F_9,
        F_12 = F_13**2*F_8,
        F_13 = F_1 + F_14 + F_15,
        F_14 = 0,
        F_15 = F_13**2*F_8,
        F_16 = F_18*F_4,
        F_17 = F_21,
        F_18 = F_1 + F_19 + F_20,
        F_19 = F_18*F_4,
        F_20 = 0,
        F_21 = F_10*F_13*F_8,
        F_22 = F_23,
        F_23 = F_24*F_4,
        F_24 = F_25 + F_26 + F_27,
        F_25 = 0,
        F_26 = F_24*F_4,
        F_27 = F_28,
        F_28 = F_10*F_13*F_8
        ]:
        count := [1, 1, 2, 4, 9, 18, 37]:
    [I 210316 10:15:19 specification:354] Solving...
    [I 210316 10:15:27 specification:365] Checking initial conditions for: (-4*x**5 + 6*x**4 - x**3*sqrt(1 - 4*x**2) - 3*x**3 + x*sqrt(1 - 4*x**2) - x - sqrt(1 - 4*x**2) + 1)/(2*x**2*(x**4 - 4*x**3 + 6*x**2 - 4*x + 1))
    (-4*x**5 + 6*x**4 - x**3*sqrt(1 - 4*x**2) - 3*x**3 + x*sqrt(1 - 4*x**2) - x - sqrt(1 - 4*x**2) + 1)/(2*x**2*(x**4 - 4*x**3 + 6*x**2 - 4*x + 1))

    >>> print([specification.count_objects_of_size(i) for i in range(10)])
    [1, 1, 2, 4, 9, 18, 37, 69, 131, 231]

We can also generate the paths in the set. These can be visualised using the ascii_plot method.

.. code-block:: python 

    >>> for path in specification.generate_objects_of_size(5):
            print(path.ascii_plot())
            print(path)
    _____
    HHHHH
    ___/\
    HHHUD
    __/\_
    HHUDH
       _ 
    __/ \
    HHUHD
    _/\__
    HUDHH
    _/\/\
    HUDUD
      _  
    _/ \_
    HUHDH
      __ 
    _/  \
    HUHHD
      /\ 
    _/  \
    HUUDD
    /\___
    UDHHH
    /\/\_
    UDUDH
     _   
    / \__
    UHDHH
     _   
    / \/\
    UHDUD
     __  
    /  \_
    UHHDH
     /\  
    /  \_
    UUDDH
     ___ 
    /   \
    UHHHD
     _/\ 
    /   \
    UHUDD
    /\_/\
    UDHUD

To randomly sample we simply use the random_sample_object_of_size method.

.. code-block:: python 

    >>> path = specification.random_sample_object_of_size(10)
    >>> print(path.ascii_plot())
       /\     
     _/  \/\  
    /       \_
    >>> print(path)
    UHUUDDUDDH

