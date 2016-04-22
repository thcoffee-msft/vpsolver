#!/usr/bin/env python
"""
This code is part of the Arc-flow Vector Packing Solver (VPSolver).

Copyright (C) 2013-2016, Filipe Brandao
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function


def main():
    """Parses 'instance_vbp.mod'"""
    from pympl import PyMPL, Tools, glpkutils

    mod_in = "instance_vbp.mod"
    mod_out = "tmp/instance_vbp.out.mod"
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/instance_vbp.lp"
    glpkutils.mod2lp(mod_out, lp_out, True)
    out, varvalues = Tools.script(
        "glpk_wrapper.sh", lp_out, verbose=True
    )
    sol = parser["VBP_FLOW"].extract(
        lambda varname: varvalues.get(varname, 0),
        verbose=True
    )

    print("")
    print("sol:", sol)
    print("varvalues:", [(k, v) for k, v in sorted(varvalues.items())])
    print("")
    assert varvalues["Z"] == 33  # check the solution objective value

    # exit_code = os.system("glpsol --math {0}".format(mod_out))
    # assert exit_code == 0

if __name__ == "__main__":
    import os
    sdir = os.path.dirname(__file__)
    if sdir != "":
        os.chdir(sdir)
    main()
