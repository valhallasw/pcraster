Source code management
======================
Git is used for source code management of the PCRaster source code.

Branching
---------
Branches are created for these reasons:

* Work on a bug.
* Work on a feature.
* Separate release(d) code from development (work in progress, unstable) code.

For ease of finding branches, most (all?) branches are stored in a hierarchy. Branches are categorized in the folowing `namespaces`: ``bug``, ``feature``, ``release``.

Release branches
^^^^^^^^^^^^^^^^

.. graphviz::

   digraph G {
       rankdir="LR";
       node[width=0.1, height=0.1, shape=point];
       edge[fontsize=10, arrowhead=none];

       // master branch. -------------------------------------------------------
       edge[color=black, fontcolor=black, weight=10000];
       "master_1" -> "master_2" [label="master"];
       "master_2" -> "master_3" -> "master_4" -> "master_5" -> "master_6";

       // Main branches. -------------------------------------------------------
       edge[color=red, fontcolor=red, weight=1000];

       // 1 main branch.
       "master_2" -> "1_1" [label="release/1"];
       "1_1" -> "1_2" -> "1_3" -> "1_4";

       // 2 main branch.
       "master_4" -> "2_1" [label="release/2"];
       "2_1" -> "2_2" -> "2_3" -> "2_4";

       // Sub-branches. --------------------------------------------------------
       edge[color=blue, fontcolor=blue, weight=100];

       // 1.0 sub branch.
       "1_1" -> "1.0_1" [label="release/1.0"];
       "1.0_1" -> "1.0_2" -> "1.0_3" -> "1.0_4" -> "1.0.5";

       // 1.1 sub branch.
       "1_2" -> "1.1_1" [label="release/1.1"];
       "1.1_1" -> "1.1_2" -> "1.1_3";

       // 2.0 sub branch.
       "2_1" -> "2.0_1" [label="release/2.0"];
       "2.0_1" -> "2.0_2" -> "2.0_3";

       // Patch-branches. ------------------------------------------------------
       edge[color=green, fontcolor=green, weight=1];

       // 1.0.x patch branches.
       "1.0_1" -> "1.0.0_1" [label="release/1.0.0"];
       "1.0_3" -> "1.0.1_1" [label="release/1.0.1"];
       "1.0_4" -> "1.0.2_1" [label="release/1.0.2"];

       // 1.1.x patch branches.
       "1.1_2" -> "1.1.0_0" [label="release/1.1.0"];

       // 2.0.x patch branches.
       "2.0_1" -> "2.0.0_1" [label="release/2.0.0"];
   }


The branch called ``master`` is the branch in which all code changes that need to be in a future release are merged. Future release branches are spawned off of the master branch.

Once development of new features that `include public API changes` has finished, a main release branch (version `x`) is spawned off of the ``master`` branch. Main release branches are named after their version number and stored under ``release``, like ``release/1``.

Once development of new features that `don't include public API changes` has finished, a sub release branch (version `x.y`) is spawned off of the main release branch. Sub release branches are named like ``release/1.0``.

Once a sub release branch is ready to be released, a patch release branch (version `x.y.z`) is spawned off of the sub-release branch. Patch release branches are named like ``release/1.0.0``.

.. important::

   After the release, a final release branch is *never* changed again.

Fix a bug
^^^^^^^^^
TODO

Add a feature
^^^^^^^^^^^^^
TODO

.. Bugs are fixed in main and sub release branches and ported to the ``master`` branch.
   
   A new final release branch (``release/1.0.1``) is spawned off of the main release branch (``release/1.0``) again, and contains the bug fixes made to it since the previous release.
   
   A new main release branch (``release/1.1``) is spawned off of the main

