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

Additional information can also be found in the `paper <http://www.ncbi.nlm.nih.gov/pubmed/24732543>`_:

    S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
    The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
    Medicine Meets Virtual Reality (MMVR) 2014

or as bibtex::

    @Article{Suwelack2014,
      Title                    = {The medical simulation markup language - simplifying the biomechanical modeling workflow},
      Author                   = {Stefan Suwelack and Markus Stoll and Sebastian Schalck and Nicolai Schoch and Rüdiger Dillmann and Rolf Berndl and Vincent Heuveline and Stefanie Speidel},
      Journal                  = {Studies in Health Technology and Informatics},
      Year                     = {2014},
      Month                    = {April},
      Pages                    = {396-400},
      Volume                   = {196},
      Abstract                 = {Modeling and simulation of the human body by means of continuum mechanics
                                  has become an important tool in diagnostics, computer-assisted interventions
                                  and training. This modeling approach seeks to construct patient-specific
                                  biomechanical models from tomographic data. Usually many different tools
                                  such as segmentation and meshing algorithms are involved in this workflow.
                                  In this paper we present a generalized and flexible description for
                                  biomechanical models. The unique feature of the new modeling language is
                                  that it not only describes the final biomechanical simulation, but also the
                                  workflow how the biomechanical model is constructed from tomographic data.
                                  In this way, the MSML can act as a middleware between all tools used in the
                                  modeling pipeline. The MSML thus greatly facilitates the prototyping of
                                  medical simulation workflows for clinical and research purposes.
                                  In this paper, we not only detail the XML-based modeling scheme, but also
                                  present a concrete implementation. Different examples highlight the
                                  flexibility, robustness and ease-of-use of the approach.},
      Keywords                 = {MSML, medical markup lanuage, simulation, workflow},

    }





If you like MSML and use it in academic work, please cite the paper above.
