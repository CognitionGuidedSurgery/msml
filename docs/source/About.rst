About
=====

The medical simulation markup language (MSML) is a flexible XML-based description
for the biomechanical modeling workflow and finite-element based biomechanical models.

MSML helps you to create biomechanical models from tomographic data, export them
to FE solvers and analyze the results. It is very flexible as already existing components
(e.g. segmentation algorithms, meshers) can usually be integrated into the framework by
providing a single additional XML-file.

The main library is written in Python, but we also provide a large collection of useful
C++ operators (e.g. linear tetrahedral and quadratic tetrahedral meshing, mesh size reduction,
error analysis etc.).

Additional information can also be found in the paper:

    S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
    The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
    Medicine Meets Virtual Reality (MMVR) 2014

If you like MSML and use it in academic work, please cite the paper above.

We provide a mailing list: under: https://www.lists.kit.edu/wws/info/msml and post to ``msml@lists.kit.edu``.

Please feel free to ask if you have any problems installing, running or extending MSML.
For bugs and issues you can use the https://github.com/CognitionGuidedSurgery/msml/issues