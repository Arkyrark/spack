# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


class PyShapely(PythonPackage):
    """Manipulation and analysis of geometric objects in the Cartesian plane.
    """

    homepage = "https://github.com/Toblerity/Shapely"
    url      = "https://pypi.io/packages/source/S/Shapely/Shapely-1.7.0.tar.gz"
    git      = "https://github.com/Toblerity/Shapely.git"

    maintainers = ['adamjstewart']
    import_modules = [
        'shapely', 'shapely.geometry', 'shapely.algorithms',
        'shapely.examples', 'shapely.speedups', 'shapely.vectorized',
    ]

    version('master', branch='master')
    version('1.7.0', sha256='e21a9fe1a416463ff11ae037766fe410526c95700b9e545372475d2361cc951e')
    version('1.6.4.post2', sha256='c4b87bb61fc3de59fc1f85e71a79b0c709dc68364d9584473697aad4aa13240f')
    version('1.6.4', sha256='b10bc4199cfefcf1c0e5d932eac89369550320ca4bdf40559328d85f1ca4f655')

    depends_on('python@3.5:', when='@1.8:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@1.7:', type=('build', 'run'))
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('geos')
    depends_on('geos@3.3:', when='@1.3:')
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-cov', type='test')

    # https://github.com/Toblerity/Shapely/pull/891
    patch('https://github.com/Toblerity/Shapely/commit/98f6b36710bbe05b4ab59231cb0e08b06fe8b69c.patch',
          sha256='4984cd0590beb5091f213948a953f70cea08ea11c5db1de07ba98c19e3d13f06')

    @when('^python@3.7:')
    def patch(self):
        # Python 3.7 changed the thread storage API, precompiled *.c files
        # need to be re-cythonized
        if os.path.exists('shapely/speedups/_speedups.c'):
            os.remove('shapely/speedups/_speedups.c')
        if os.path.exists('shapely/vectorized/_vectorized.c'):
            os.remove('shapely/vectorized/_vectorized.c')

    def setup_build_environment(self, env):
        env.set('GEOS_CONFIG',
                join_path(self.spec['geos'].prefix.bin, 'geos-config'))

    def test(self):
        # Tests fail when 'geos' library not found in usual search directories
        # python('-m', 'pytest')
        pass
