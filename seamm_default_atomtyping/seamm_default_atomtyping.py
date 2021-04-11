# -*- coding: utf-8 -*-

"""Non-graphical part of the seamm_default_atomtyping step in a SEAMM flowchart
"""

import logging
import pprint  # noqa: F401
import os
import seamm_default_atomtyping
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import rdkit
import rdkit.Chem
import rdkit.Chem.AllChem
import re

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


class SeammDefaultAtomtyping:
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
        parameter_set=None,
        logger=logger,
        **_ignore
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

        self.selected_forcefield = self.forcefield.name

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


    def assign_parameters(self, configuration=None):

        if configuration is None:
            raise TypeError("A configuration must be provided when assigning forcefield parameters")

        printer.important(
            __(
                "Assigning the atom types and charges for forcefield "
                f"'{self.selected_forcefield}' to the system",
            )
        )

        logger.debug('Atom typing, getting the SMILES for the system')
        smiles = configuration.to_smiles(hydrogens=True)
        logger.debug('Atom typing -- smiles = ' + smiles)


        pat3 = re.compile(r'H3\]')
        pat2 = re.compile(r'H2\]')
        pat1 = re.compile(r'(?P<c1>[^[])H\]')

        smiles = pat3.sub(']([H])([H])([H])', smiles)
        smiles = pat2.sub(']([H])([H])', smiles)
        smiles = pat1.sub(r'\g<c1>]([H])', smiles)

        h_subst = None
        for el in ('Rb', 'Cs', 'Fr', 'At'):
            if el not in smiles:
                h_subst = el
                pat4 = re.compile(r'\[H\]')
                smiles = pat4.sub('[{}]'.format(el), smiles)
                logger.debug("Subst SMILES = '{}'".format(smiles))
                break

        molecule = rdkit.Chem.MolFromSmiles(smiles)
        if molecule is None:
            print("There was problem with the SMILES '{}'".format(smiles))
            return

        if h_subst is not None:
            for atom in molecule.GetAtoms():
                if atom.GetSymbol() == h_subst:
                    atom.SetAtomicNum(1)

        # if add_hydrogens:
        #     molecule = rdkit.Chem.AddHs(molecule)
        #     n_atoms = molecule.GetNumAtoms()
        #     logger.debug(
        #         "'{}' has {} atoms with hydrogens added".format(
        #             smiles, n_atoms
        #         )
        #     )
        # else:
        #     n_atoms = molecule.GetNumAtoms()
        #     logger.debug("'{}' has {} atoms".format(smiles, n_atoms))
        n_atoms = molecule.GetNumAtoms()

        atomtypes = ['?'] * n_atoms
        templates = self.forcefield.get_templates()
        for atom_type in templates:
            template = templates[atom_type]
            for smarts in template['smarts']:
                pattern = rdkit.Chem.MolFromSmarts(smarts)

                ind_map = {}
                for atom in pattern.GetAtoms():
                    map_num = atom.GetAtomMapNum()
                    if map_num:
                        ind_map[map_num - 1] = atom.GetIdx()
                map_list = [ind_map[x] for x in sorted(ind_map)]

                matches = molecule.GetSubstructMatches(pattern)
                logger.debug(atom_type + ': ')
                if len(matches) > 0:
                    for match in matches:
                        atom_ids = [match[x] for x in map_list]
                        for x in atom_ids:
                            atomtypes[x] = atom_type
                        tmp = [str(x) for x in atom_ids]
                        logger.debug('\t' + ', '.join(tmp))

        i = 0
        untyped = []
        for atom, atom_type in zip(molecule.GetAtoms(), atomtypes):
            if atom_type == '?':
                untyped.append(i)
            logger.debug("{}: {}".format(atom.GetSymbol(), atom_type))
            i += 1

        if len(untyped) > 0:
            logger.warning(
                'The forcefield does not have atom types for'
                ' the molecule!. See missing_atomtypes.png'
                ' for more detail.'
            )
            #rdkit.Chem.AllChem.Compute2DCoords(molecule)
            #img = rdkit.Chem.Draw.MolToImage(
            #    molecule,
            #    size=(1000, 1000),
            #    highlightAtoms=untyped,
            #    highlightColor=(0, 1, 0)
            #)
            #img.save('missing_atomtypes.png')

            #if self.have_tk:
            #    root = tk.Tk()
            #    root.title('Atom types')
            #    tkPI = ImageTk.PhotoImage(img)
            #    tkLabel = tk.Label(root, image=tkPI)
            #    tkLabel.place(x=0, y=0, width=img.size[0], height=img.size[1])
            #    root.geometry('%dx%d' % (img.size))
            #    root.mainloop()
        else:
            logger.info('The molecule was successfully atom-typed')


        logger.info('Atom types: ' + ', '.join(atomtypes))
        key = f'atomtypes_{self.selected_forcefield}'
        if key not in configuration.atoms:
            configuration.atoms.add_attribute(key, coltype='str')
        configuration.atoms[key] = atomtypes

        # Now get the charges if forcefield has them.
        terms = self.forcefield.data['forcefield'][self.selected_forcefield]['parameters']

        if 'bond_increments' in terms:
            logger.debug('Getting the charges for the system')
            neighbors = configuration.bonded_neighbors(as_indices=True)

            charges = []
            total_q = 0.0
            for i in range(configuration.n_atoms):
                itype = atomtypes[i]
                parameters = self.forcefield.charges(itype)[3]
                q = float(parameters['Q'])
                for j in neighbors[i]:
                    jtype = atomtypes[j]
                    parameters = self.forcefield.bond_increments(itype, jtype)[3]
                    q += float(parameters['deltaij'])
                charges.append(q)
                total_q += q
            if abs(total_q) > 0.0001:
                logger.warning('Total charge is not zero: {}'.format(total_q))
                logger.info(
                    'Charges from increments and charges:\n' +
                    pprint.pformat(charges)
                )
            else:
                logger.debug(
                    'Charges from increments:\n' + pprint.pformat(charges)
                )

            key = f'charges_{self.selected_forcefield}'
            if key not in configuration.atoms:
                configuration.atoms.add_attribute(key, coltype='float')
            charge_column = configuration.atoms.get_column(key)
            charge_column[0:] = charges
            logger.debug(f"Set column '{key}' to the charges")

            printer.important(
                __(
                    "Assigned atom types and charges to "
                    f"{configuration.n_atoms} atoms.",
                )
            )
        else:
            printer.important(
                __(
                    f"Assigned atom types to {configuration.n_atoms} "
                    "atoms.",
                )
            )