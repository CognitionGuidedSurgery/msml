.. msml documentation master file, created by
   sphinx-quickstart on Thu Dec  5 21:48:12 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. raw:: html

        <style>h1 {display:none;} .jumbotron h1 {display:block;}</style>

msml - medical simulation markup language
=========================================

.. raw:: html

   <div class="no-display">



.. toctree::

   About
   modules/run-msml
   Installation
   GettingStarted
   examples/index
   advanced/index
   Development
   Roadmap
   Api


.. raw:: html

   </div>
   <div class="jumbotron">
        <div class="container">
        <div class="row">
                 <div class="col-md-5">
                    <img src="_static/msml-logo3d.png" width="350" height="250" />
                 </div>

                 <div class="col-md-7">
                        <!-- <h1>msml</h1> -->


medical simulation markup language

Medicine Simulation Markup Language (MSML) let you describe scenes of 3D model for various simulation tools.  It helps you with various preprocessors for 3D models called Operators and exports for Sofa Framework or Abaqus.

MSML was created in the SFB125_ in a coorperation between KIT_ and DKFZ_.

.. raw:: html

                </div> 
        </div>
        </div>
   </div>

   <div class="container-fluid">
      <div class="row">
        <div class="col-xs-4">
            <h3><a href="/About.html">About</a></h3>
        </div>
        <div class="col-xs-4">
            <h3><a href="/Installation.html">Installation</a></h3>
        </div>
        <div class="col-xs-4">
            <h3><a href="GettingStarted.html">Getting Started</a></h3>
        </div>
      </div>
   </div>

   <div class="container-fluid">
      <div class="row">
        <h3>Features</h3>
        <ul>
            <li>type safety</li>
            <li>automatic conversion between file formats and data types</li>
            <li>parallelism of task</li>
        </ul>
      </div>

      <div class="row">
        <div class="col-xs-4">
            <h3>Pre Processing</h3>
            MSML provides a set of high level <a href="operators/index.html">operators</a> for getting your work done.
            You can define easily your own in <a href="advanced/extendmsml.html#how-to-create-an-operator">C++ or Python</a>.
        </div>
        <div class="col-xs-4">
            <h3>Simulation</h3>
            MSML supports Abaqus, <a href="http://sofa-framework.org">Sofa</a> and <a href="http://hiflow3.org">Hiflow3</a> for running the simulation.
            You can write your own <a href="advanced/extendmsml.html#how-to-create-an-operator">exporter</a> and benefit from the MSML ecosystem.
        </div>
        <div class="col-xs-4">
            <h3>Post Processing</h3>
            You can choose every <a href="operators/index.html">operator</a> to process the simulation results your data.
        </div>
      </div>
   </div>


..  <div>
                            <a href="http://http://his.anthropomatik.kit.edu/">
                              <img src="http://www.arch.kit.edu/downloads/kit_logo_de_farbe_positiv.jpg"
                                height="50" />
                            </a>

                            <a href="http://dkfz.de">
                              <img src="http://www.unit-werbeagentur.de/kunden/dkfz/assets/dkfz_logo_b.jpg"
                                height="50" />
                            </a>
                        </div>


.. _SFB125: http://cognitionguidedsurgery.de/
.. _KIT: http://his.anthropomatik.kit.edu/
.. _DKFZ: https://www.dkfz.de/en/index.html
