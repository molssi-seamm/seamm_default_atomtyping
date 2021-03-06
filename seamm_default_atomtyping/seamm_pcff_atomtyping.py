# This was in forcefield_step/forcefield.py



    def assign_forcefield(self, P=None):
        """Assign the forcefield to the structure, i.e. find the atom types
        and charges.

        Parameters
        ----------
        P : {str: Any}
            The final values of the parameters.

        Returns
        -------
        None
        """
        # if P is None:
        #     P = self.parameters.current_values_to_dict(
        #         context=seamm.flowchart_variables._data
        #     )

        ff = self.get_variable('_forcefield')
        system_db = self.get_variable('_system_db')
        configuration = system_db.system.configuration

        ffname = ff.current_forcefield
        printer.important(
            __(
                "Assigning the atom types and charges for forcefield "
                f"'{ffname}' to the system",
                indent=self.indent + '    '
            )
        )

        # Atom types
        logger.debug('Atom typing, getting the SMILES for the system')
        smiles = configuration.to_smiles(hydrogens=True)
        logger.debug('Atom typing -- smiles = ' + smiles)
        ff_assigner = seamm_ff_util.FFAssigner(ff)
        atom_types = ff_assigner.assign(smiles, add_hydrogens=False)
        logger.info('Atom types: ' + ', '.join(atom_types))
        key = f'atom_types_{ffname}'
        if key not in configuration.atoms:
            configuration.atoms.add_attribute(key, coltype='str')
        configuration.atoms[key] = atom_types

        # Now get the charges if forcefield has them.
        terms = ff.data['forcefield'][ffname]['parameters']
        if 'bond_increments' in terms:
            logger.debug('Getting the charges for the system')
            neighbors = configuration.bonded_neighbors(as_indices=True)

            charges = []
            total_q = 0.0
            for i in range(configuration.n_atoms):
                itype = atom_types[i]
                parameters = ff.charges(itype)[3]
                q = float(parameters['Q'])
                for j in neighbors[i]:
                    jtype = atom_types[j]
                    parameters = ff.bond_increments(itype, jtype)[3]
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

            key = f'charges_{ffname}'
            if key not in configuration.atoms:
                configuration.atoms.add_attribute(key, coltype='float')
            charge_column = configuration.atoms.get_column(key)
            charge_column[0:] = charges
            logger.debug(f"Set column '{key}' to the charges")

            printer.important(
                __(
                    "Assigned atom types and charges to "
                    f"{configuration.n_atoms} atoms.",
                    indent=self.indent + '    '
                )
            )
        else:
            printer.important(
                __(
                    f"Assigned atom types to {configuration.n_atoms} "
                    "atoms.",
                    indent=self.indent + '    '
                )
            )

    def setup_forcefield(self, P=None):
        """Setup the forcefield for later use.

        Parameters
        ---------
        P : {str: Any}
            The final values of the parameters.

        Returns
        -------
        None
        """
        if P is None:
            P = self.parameters.current_values_to_dict(
                context=seamm.flowchart_variables._data
            )

        if P['forcefield_file'] == 'OpenKIM':
            printer.important(
                __(
                    "Using the OpenKIM potential '{potentials}'",
                    **P,
                    indent=self.indent + '    '
                )
            )
            self.set_variable('_forcefield', 'OpenKIM')
            self.set_variable('_OpenKIM_Potential', P['potentials'])
        else:
            printer.important(
                __(
                    "Reading the forcefield file '{forcefield_file}'",
                    **P,
                    indent=self.indent + '    '
                )
            )

            # Find the forcefield file
            path = pkg_resources.resource_filename(__name__, 'data/')
            ff_file = os.path.join(path, P['forcefield_file'])

            ff = seamm_ff_util.Forcefield(ff_file)
            self.set_variable('_forcefield', ff)

            if P['forcefield'] == 'default':
                printer.important(
                    __(
                        "   Using the default forcefield '{ff}'.",
                        ff=ff.forcefields[0],
                        indent=self.indent + '    '
                    )
                )

                ff.initialize_biosym_forcefield()
            else:
                printer.important(
                    __(
                        "   Using the forcefield '{forcefield}'",
                        **P,
                        indent=self.indent + '    '
                    )
                )

                ff.initialize_biosym_forcefield(P['forcefield'])
