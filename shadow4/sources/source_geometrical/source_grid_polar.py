
import numpy
from shadow4.beam.beam import Beam
from shadow4.sources.s4_light_source_base import S4LightSourceBase

class SourceGridPolar(S4LightSourceBase):

    def __init__(self,
                 real_space=[1e-6,0,1e-6],
                 direction_space=[1e-6,1e-6],
                 real_space_points=[100,36],
                 direction_space_points=[1,1],
                 real_space_center=[0,0,0],
                 direction_space_center=[0,1,0],
                 name="Undefined",
                 nrays=0, # not used
                 seed=0, # not used
                 ):
        """
        This defines a grid source, so points starting in a ellipsoid-like volume in real space
        and angularly gridded in X,Z

        :param real_space: the widths of the real_space volume [2a,2b,2c] of the ellipsoid
        :param direction_space: The "angular" aperture [Dx',Dz']
        :param real_space_points: Number of points [Nradial,Nangular]
        :param direction_space_points: Number of points [Nradial',Nangular']
        :param real_space_center: Center in real space in cartesial coordinates [Xc,Yc,Zc]
        :param direction_space_center:  Center in direction space [Vx,Vz] (note that (Vx+Vx_sampled)^2+(Vz+Vz_sampled)^2 < 1)
        :return:
        """

        super().__init__(name=name, nrays=nrays, seed=seed)

        if real_space[1] != 0:
            raise Exception("Finite source depth not yet implemented!") # TODO: implement it!

        self._real_space = real_space
        self._direction_space = direction_space
        self._real_space_points = real_space_points
        self._direction_space_points = direction_space_points
        self._real_space_center = real_space_center
        self._direction_space_center = direction_space_center



    @classmethod
    def initialize_point_source(cls,
                real_space_center=[0.0, 0.0, 0.0],
                direction_space=[1e-6,1e-6],
                direction_space_points=[5,36],
                direction_space_center=[0.0,0.0],
                                ):
        """
        Initializes a point source

        :param real_space_center: Center in real space in cartesial coordinates [Xc,Yc,Zc]
        :param direction_space: Default: [1e-6,1e-6],
        :param direction_space_points: Default: [100,100],
        :param direction_space_center: Default: [0.0,0.0] ),
        :return:
        """
        return SourceGridPolar(real_space=[0,0,0],
                 direction_space=direction_space,
                 real_space_points=[1,1,1],
                 direction_space_points=direction_space_points,
                 real_space_center=real_space_center,
                 direction_space_center=direction_space_center,
                )

    @classmethod
    def initialize_collimated_source(cls,
                real_space=[1e-6,0.0,1e-6],
                real_space_points=[100,36],
                real_space_center=[0.0,0.0,0.0],
                direction_space_center=[0.0,0.0],
                                ):
        """

        :param real_space: Default: [1e-6,0,1e-6]
        :param real_space_points: Default: [100,36]
        :param real_space_center: Default: [0.0,0.0,0.0]
        :param direction_space_center: Default: [0.0,0.0]
        :return:
        """
        return SourceGridPolar(real_space=real_space,
                 direction_space=[0.0,0.0],
                 real_space_points=real_space_points,
                 direction_space_points=[1,1],
                 real_space_center=real_space_center,
                 direction_space_center=direction_space_center,)

    #
    # getters
    #


    def get_number_of_points_real_space(self):
        """
        Returns the total number of points
        :return:
        """
        return self._real_space_points[0] * self._real_space_points[1]

    def get_number_of_points_direction_space(self):
        """
        Returns the total number of points
        :return:
        """
        return self._direction_space_points[0] * self._direction_space_points[1]

    def get_number_of_points(self):
        """
        Returns the total number of points
        :return:
        """
        return self.get_number_of_points_real_space() * self.get_number_of_points_direction_space()


    def get_arrays_real_space(self):
        """
        Returns three arrays with the spatial coordinates 1D arrays
        :return: x,y,z
        """
        radial_ratio = numpy.linspace(0, 1, self._real_space_points[0] )

        angular = numpy.arange(self._real_space_points[1]) / self._real_space_points[1]
        angular *= 2 * numpy.pi


        npoints = self.get_number_of_points_real_space()

        x = numpy.zeros(npoints)
        z = numpy.zeros(npoints)

        i = -1
        for radius_ratio in radial_ratio:
            for angle in angular:
                i += 1
                x[i] = self._real_space[0]/2 * radius_ratio * numpy.cos(angle)
                z[i] = self._real_space[2]/2 * radius_ratio * numpy.sin(angle)
        y = numpy.zeros_like(x)
        return x,y,z

    def get_arrays_direction_space(self):
        """
        Returns two arrays with the direction angles (in fact components of the direction vector)
        :return: xp,zp
        """

        radial_ratio = numpy.linspace(0, 1, self._direction_space_points[0] )

        angular = numpy.arange(self._direction_space_points[1]) / self._direction_space_points[1]
        angular *= 2 * numpy.pi

        npoints = self.get_number_of_points_direction_space() # self._real_space_points[0] * self._real_space_points[1]

        vx = numpy.zeros(npoints)
        vz = numpy.zeros(npoints)

        i = -1
        for radius_ratio in radial_ratio:
            for angle in angular:
                i += 1
                vx[i] = self._direction_space[0]/2 * radius_ratio * numpy.cos(angle)
                vz[i] = self._direction_space[0]/2 * radius_ratio * numpy.sin(angle)

        return vx,vz

        return numpy.array([0]), numpy.array([0])

    def get_volume(self):
        """
        Returns an array (6,npoints) with x,y,z,xp,yp,zp (first index 0,1,2,3,4,5 respectively) with the
        spatial and direction coordinates
        :return: x y z xp yp zp array
        """
        X, Y, Z = self.get_arrays_real_space()
        VX, VZ = self.get_arrays_direction_space()
        print(">>>", X.shape, Y.shape, Z.shape, VX.shape, VZ.shape)

        npoint = self.get_number_of_points()
        V1x = numpy.zeros(npoint)
        V1y = numpy.zeros(npoint)
        V1z = numpy.zeros(npoint)
        V2x = numpy.zeros(npoint)
        V2z = numpy.zeros(npoint)
        V2y = numpy.zeros(npoint)

        ij = -1
        for i in range(self.get_number_of_points_real_space()):
            for j in range(self.get_number_of_points_direction_space()):
                ij += 1
                V1x[ij] = X[i]
                V1y[ij] = Y[i]
                V1z[ij] = Z[i]
                V2x[ij] = VX[j]
                V2z[ij] = VZ[j]

        V1x += self._real_space_center[0]
        V1y += self._real_space_center[1]
        V1z += self._real_space_center[2]
        V2x += self._direction_space_center[0]
        V2z += self._direction_space_center[1]

        try:
            V2y = numpy.sqrt(1 - V2x ** 2 - V2z ** 2)
        except:
            raise Exception('Failed to normalize directions. Try smalled angular width and/or angular center.')

        return numpy.vstack((V1x,V1y,V1z,V2x,V2y,V2z))


    #
    # info
    #
    def info(self):
        """
        Returns an array of strings with info.
        :return:
        """
        txt = ""

        txt += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        txt += "Grid source: \n"
        txt += "Number of points: Nreal_space: %d, Ndirection_space: %d, Total: %d \n"%(
                                                self.get_number_of_points_real_space(),
                                                self.get_number_of_points_direction_space(),
                                                self.get_number_of_points())
        txt += "Gridding in real space:      %d, %d\n"%(self._real_space_points[0],
                                                                self._real_space_points[1])
        txt += "Gridding in direction space: %d, %d \n"%(self._direction_space_points[0],
                                                                self._direction_space_points[1])
        txt += "\n"
        txt += "real_space widths"+repr(self._real_space) + "\n"
        txt += "direction_space widths "+repr(self._direction_space) + "\n"
        txt += "real_space_points "+repr(self._real_space_points) + "\n"
        txt += "direction_space_points "+repr(self._direction_space_points) + "\n"
        txt += "real_space_center "+repr(self._real_space_center) + "\n"
        txt += "direction_space_center "+repr(self._direction_space_center) + "\n"

        txt += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'n"

        return txt


    def get_beam(self,wavelength=1e-10):
        """
        Returns a Beam
        :param wavelength: the photon wavelength in m
        :return:
        """

        rays = numpy.zeros((self.get_number_of_points(),18))
        volume = self.get_volume()
        rays[:, 0] = volume[0,:]
        rays[:, 1] = volume[1,:]
        rays[:, 2] = volume[2,:]
        rays[:, 3] = volume[3,:]
        rays[:, 4] = volume[4,:]
        rays[:, 5] = volume[5,:]
        rays[:,6] = 1.0 # Es
        rays[:,9] = 1   # flag
        rays[:,10] = 2 * numpy.pi / (wavelength * 1e2) # wavenumber
        rays[:,11] = numpy.arange(self.get_number_of_points(),dtype=float) # index

        return Beam.initialize_from_array(rays)


if __name__ == "__main__":
    from srxraylib.plot.gol import plot_scatter, set_qt
    from shadow4tests.compatibility.beam3 import Beam3
    set_qt()

    if True:
        a = SourceGridPolar.initialize_point_source(
                    direction_space        = [2e-3,2e-3],
                    direction_space_points = [20,  5],
                    direction_space_center = [0.0, 0.0] )
        print(a.info())

        beam = a.get_beam()
        plot_scatter(beam.get_column(4) * 1e6, beam.get_column(6) * 1e6, title="Polar grid in direction space")

        beam_shadow3 = Beam3.initialize_from_shadow4_beam( beam )
        # beam_shadow3.write("begin.dat")

        import Shadow
        Shadow.ShadowTools.plotxy(beam_shadow3,4,6)


    #
    #
    if True:
        a = SourceGridPolar.initialize_collimated_source(
            real_space=[2e-6, 0.0, 1e-6],
            real_space_points=[10, 4],
            real_space_center=[0.0, 0.0, 0.0]
        )
        print(a.info())


        beam = a.get_beam()
        plot_scatter(beam.get_column(1)*1e6, beam.get_column(3)*1e6, xrange=[-1,1], yrange=[-1,1],
                     title="Polar grid in real space")

        beam_shadow3 = Beam3.initialize_from_shadow4_beam( beam )
        # beam_shadow3.write("begin.dat")

        import Shadow
        Shadow.ShadowTools.plotxy(beam_shadow3,1,3)
        # #
        #

    if True:
        a = SourceGridPolar(
            real_space=[1e-6, 0.0, 1e-6],
            real_space_points=[2, 4],
            real_space_center=[0.0, 0.0, 0.0],
            direction_space=[2e-6, 2e-6],
            direction_space_points=[5, 5],
            direction_space_center=[0.0, 0.0])

        print(a.info())


        beam = a.get_beam()
        plot_scatter(beam.get_column(1)*1e6, beam.get_column(3)*1e6, xrange=[-1,1], yrange=[-1,1],
                     title="Real space")
        plot_scatter(beam.get_column(4)*1e6, beam.get_column(6)*1e6, xrange=[-1,1], yrange=[-1,1],
                     title="Directions space")

        beam_shadow3 = Beam3.initialize_from_shadow4_beam( beam )
        # beam_shadow3.write("begin.dat")

        import Shadow
        Shadow.ShadowTools.plotxy(beam_shadow3, 1, 3)
        Shadow.ShadowTools.plotxy(beam_shadow3, 4, 6)
        # #
        #