.. msml documentation master file, created by
   sphinx-quickstart on Thu Dec  5 21:48:12 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to msml's documentation!
================================

About
--------------------------------

Medicine Simulation Markup Language (MSML) let you describe scenes of 3D model
for various simulation tools.  It helps you with various preprocessors for
3D models called Operators and exports for Sofa Framework or Abaqus.

The following workflow:

* Input from CT/MRT
* Describe your Workflow (Transformation, Extraction, etc.)
* Describe your Scene
* Execute msml
  * calls the operators
  * simulate with the given export tool
  * postprocessing the simulation results


MSML was created in the SFB125_ in a coorperation between KIT_ and DKFZ_.

Contents:

.. toctree::
   :numbered:
   :maxdepth: 4
   :glob:

   Installation
   GettingStarted
   advanced_topics
   system_explanation
   Development
   Roadmap
   modules/msml/__init__




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _SFB125: http://cognitionguidedsurgery.de/
.. _KIT: http://his.anthropomatik.kit.edu/
.. _DKFZ: https://www.dkfz.de/en/index.html
