# -*- coding: utf-8 -*-

"""Non-graphical part of the seamm_default_atomtyping step in a SEAMM flowchart
"""

import logging
import pprint  # noqa: F401

import seamm_default_atomtyping
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# In addition to the normal logger, two logger-like printing facilities are
# defined: 'job' and 'printer'. 'job' send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# 'printer' sends output to the file 'step.out' in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('seamm_default_atomtyping')


class SeammDefaultAtomtyping(seamm.Node):
    """
    The non-graphical part of a seamm_default_atomtyping step in a flowchart.

    Attributes
    ----------
    parser : configargparse.ArgParser
        The parser object.

    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : SeammDefaultAtomtypingParameters
        The control parameters for seamm_default_atomtyping.

    See Also
    --------
    TkSeammDefaultAtomtyping,
    SeammDefaultAtomtyping, SeammDefaultAtomtypingParameters
    """

    def __init__(
        self,
        flowchart=None,
        title='seamm_default_atomtyping',
        extension=None,
        logger=logger
    ):
        """A step for seamm_default_atomtyping in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug('Creating seamm_default_atomtyping {}'.format(self))

        self.directory = os.getcwd()
        self.name = self.__class__.__name__

        self.forcefield = seamm.Forcefield(filename="/Users/meliseo/Git/SEAMM2/seamm_default_atomtyping/seamm_default_atomtyping/data/pcff2018.frc")

        self.supported_forcefield = [self.forcefield.name]

    @property
    def version(self):
        """The semantic version of this module.
        """
        return seamm_default_atomtyping.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return seamm_default_atomtyping.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.
        Returns
        -------
        str
            A description of the current step.
        """
        if not P:
            P = self.parameters.values_to_dict()

        text = (
            'Please replace this with a short summary of the '
            'seamm_default_atomtyping step, including key parameters.'
        )

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def assign_parameters(self):
        pass
