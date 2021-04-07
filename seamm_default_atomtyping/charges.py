        #    # Now get the charges if forcefield has them.
        #    terms = ff.terms
        #    if 'bond charge increment' in terms:
        #        logger.debug('Getting the charges for the system')
        #        neighbors = configuration.bonded_neighbors(as_indices=True)

        #        charges = []
        #        total_q = 0.0
        #        for i in range(configuration.n_atoms):
        #            itype = atom_types[i]
        #            parameters = ff.charges(itype)[3]
        #            q = float(parameters['Q'])
        #            for j in neighbors[i]:
        #                jtype = atom_types[j]
        #                parameters = ff.bond_increments(itype, jtype)[3]
        #                q += float(parameters['deltaij'])
        #            charges.append(q)
        #            total_q += q
        #        if abs(total_q) > 0.0001:
        #            logger.warning(f'Total charge is not zero: {total_q:.4f}')
        #            logger.info(
        #                'Charges from increments and charges:\n' +
        #                pprint.pformat(charges)
        #            )
        #        else:
        #            logger.debug(
        #                'Charges from increments:\n' + pprint.pformat(charges)
        #            )

        #        key = f'charges_{ffname}'
        #        if key not in configuration.atoms:
        #            configuration.atoms.add_attribute(key, coltype='float')
        #        charge_column = configuration.atoms.get_column(key)
        #        charge_column[0:] = charges
        #        logger.debug(f"Set column '{key}' to the charges")
