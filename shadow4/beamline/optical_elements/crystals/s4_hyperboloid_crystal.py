from syned.beamline.element_coordinates import ElementCoordinates

from shadow4.beam.s4_beam import S4Beam
from shadow4.beamline.optical_elements.crystals.s4_crystal import S4CrystalElement, S4Crystal
from shadow4.beamline.s4_optical_element_decorators import SurfaceCalculation, S4HyperboloidOpticalElementDecorator
from syned.beamline.shape import Hyperboloid, HyperbolicCylinder, Convexity, Direction

class S4HyperboloidCrystal(S4Crystal, S4HyperboloidOpticalElementDecorator):
    """
    Shadow4 Hyperboloid Crystal Class
    This is a spherically curved perfect crystal in reflection geometry (Bragg), using the diffracted beam.

    Constructor.

    Parameters
    ----------
    name :  str, optional
        A name for the crystal
    boundary_shape : instance of BoundaryShape, optional
        The information on the crystal boundaries.
    material : str, optional
        The crystal material name (a name accepted by crystalpy).
    miller_index_h : int, optional
        The Miller index H.
    miller_index_k : int, optional
        The Miller index K.
    miller_index_l : int, optional
        The Miller index L.
    f_bragg_a : int, optional
        Asymmetric crystal 0:No, 1:Yes.
    asymmetry_angle : float, optional
        For f_bragg_a=1, the asymmetry angle (angle between crystal planes and surface) in rads.
    is_thick : int, optional
        Use thick crystal approximation.
    thickness : float, optional
        For is_thick=0, the crystal thickness in m.
    f_central : int, optional
        Flag for autosetting the crystal to the corrected Bragg angle.
    f_phot_cent : int, optional
        0: setting photon energy in eV, 1:setting photon wavelength in m.
    phot_cent : float, optional
        for f_central=1, the value of the photon energy (f_phot_cent=0) or photon wavelength (f_phot_cent=1).
    f_ext : inf, optional
        Flag for autosetting the crystal surface parameters.
        0: internal/calculated parameters, 1:external/user defined parameters. TODO: delete?
    material_constants_library_flag : int, optional
        Flag for indicating the origin of the crystal data:
        0: xraylib, 1: dabax, 2: preprocessor file v1, 3: preprocessor file v2.
    file_refl : str, optional
        for material_constants_library_flag=2,3, the name of the file containing the crystal parameters.
    min_axis : float, optional
        The hyperbola/hyperboloid minor axis.
    maj_axis : float, optional
        The hyperbola/hyperboloid major axis.
    p_focus : float, optional
        The distance from focus 1 (locus of the source) to the crystal pole.
    is_cylinder : int, optional
        Flag to indicate that the surface has cylindrical symmetry (it is flat in one direction).
    cylinder_direction : int, optional
       For is_cylinder=1, the direction where the surface is flat.
       Use synedDirection.TANGENTIAL (0) or Direction.SAGITTAL (1).
    convexity : int, optional
        The surface is concave (0) or convex (1).
        Use syned Convexity.UPWARD (0) for concave or Convexity.DOWNWARD (1).

    """
    def __init__(self,
                 name="Hyperboloid crystal",
                 boundary_shape=None,
                 material=None,
                 # diffraction_geometry=DiffractionGeometry.BRAGG,  # ?? not supposed to be in syned...
                 miller_index_h=1,
                 miller_index_k=1,
                 miller_index_l=1,
                 asymmetry_angle=0.0,
                 is_thick=0,
                 thickness=0.010,
                 f_central=False,
                 f_phot_cent=0,
                 phot_cent=8000.0,
                 file_refl="",
                 f_bragg_a=False,
                 f_ext=0,
                 material_constants_library_flag=0,  # 0=xraylib, 1=dabax
                                                     # 2=shadow preprocessor file v1
                                                     # 3=shadow preprocessor file v2
                 min_axis=0.0,
                 maj_axis=0.0,
                 p_focus=0.0,
                 is_cylinder=False,
                 cylinder_direction=Direction.TANGENTIAL,
                 convexity=Convexity.UPWARD,
                 ):
        q_focus, grazing_angle = 1.0, 1e-3
        S4HyperboloidOpticalElementDecorator.__init__(self, SurfaceCalculation.EXTERNAL, is_cylinder, cylinder_direction, convexity,
                                                 min_axis, maj_axis, p_focus, q_focus, grazing_angle)

        S4Crystal.__init__(self,
                           name=name,
                           boundary_shape=boundary_shape,
                           surface_shape=self.get_surface_shape_instance(),
                           material=material,
                           # diffraction_geometry=diffraction_geometry,  # ?? not supposed to be in syned...
                           miller_index_h=miller_index_h,
                           miller_index_k=miller_index_k,
                           miller_index_l=miller_index_l,
                           asymmetry_angle=asymmetry_angle,
                           is_thick=is_thick,
                           thickness=thickness,
                           f_central=f_central,
                           f_phot_cent=f_phot_cent,
                           phot_cent=phot_cent,
                           file_refl=file_refl,
                           f_bragg_a=f_bragg_a,
                           f_ext=f_ext,
                           material_constants_library_flag=material_constants_library_flag,
                           )

        self.__inputs = {
            "name": name,
            "boundary_shape": boundary_shape,
            "material": material,
            # "diffraction_geometry": diffraction_geometry,
            "miller_index_h": miller_index_h,
            "miller_index_k": miller_index_k,
            "miller_index_l": miller_index_l,
            "asymmetry_angle": asymmetry_angle,
            "is_thick": is_thick,
            "thickness": thickness,
            "f_central": f_central,
            "f_phot_cent": f_phot_cent,
            "phot_cent": phot_cent,
            "file_refl": file_refl,
            "f_bragg_a": f_bragg_a,
            "f_ext": f_ext,
            "material_constants_library_flag": material_constants_library_flag,
            "min_axis": min_axis,
            "maj_axis": maj_axis,
            "p_focus": p_focus,
            "is_cylinder": is_cylinder,
            "cylinder_direction": cylinder_direction,
            "convexity": convexity,
            }

    def to_python_code(self, **kwargs):
        """
        Auxiliar method to automatically create python scripts.

        Parameters
        ----------
        **kwargs

        Returns
        -------
        str
            Python code.

        """

        txt = "\nfrom shadow4.beamline.optical_elements.crystals.s4_hyperboloid_crystal import S4HyperboloidCrystal"

        txt_pre = """\noptical_element = S4HyperboloidCrystal(name='{name}',
    boundary_shape=None, material='{material}',
    miller_index_h={miller_index_h}, miller_index_k={miller_index_k}, miller_index_l={miller_index_l},
    f_bragg_a={f_bragg_a}, asymmetry_angle={asymmetry_angle},
    is_thick={is_thick}, thickness={thickness},
    f_central={f_central}, f_phot_cent={f_phot_cent}, phot_cent={phot_cent},
    file_refl='{file_refl}',
    f_ext={f_ext},
    material_constants_library_flag={material_constants_library_flag}, # 0=xraylib,1=dabax,2=preprocessor v1,3=preprocessor v2
    min_axis={min_axis:f}, maj_axis={maj_axis:f}, p_focus={p_focus:f}, is_cylinder={is_cylinder:d}, cylinder_direction={cylinder_direction:d}, convexity={convexity:d},
    )"""
        txt += txt_pre.format(**self.__inputs)

        return txt

class S4HyperboloidCrystalElement(S4CrystalElement):
    """
    The Shadow4 hyperboloid crystal element.
    It is made of a S4HyperboloidCrystal and an ElementCoordinates instance. It also includes the input beam.

    Constructor.

    Parameters
    ----------
    optical_element : instance of S4HyperboloidCrystal
        The crystal data.
    coordinates : instance of ElementCoordinates
        The position data.
    input_beam : instance of S4Beam
        The input beam.

    """
    def __init__(self,
                 optical_element : S4HyperboloidCrystal = None,
                 coordinates : ElementCoordinates = None,
                 input_beam : S4Beam = None):
        super().__init__(optical_element=optical_element if optical_element is not None else S4HyperboloidCrystal(),
                         coordinates=coordinates if coordinates is not None else ElementCoordinates(),
                         input_beam=input_beam)

        if not (isinstance(self.get_optical_element().get_surface_shape(), HyperbolicCylinder) or
                isinstance(self.get_optical_element().get_surface_shape(), Hyperboloid)):
            raise ValueError("Wrong Optical Element: only Hyperboloid or Hyperbolic Cylinder shape is accepted")

    def to_python_code(self, **kwargs):
        """
        Auxiliar method to automatically create python scripts.

        Parameters
        ----------
        **kwargs

        Returns
        -------
        str
            Python code.

        """
        txt = "\n\n# optical element number XX"
        txt += self.get_optical_element().to_python_code()
        coordinates = self.get_coordinates()
        txt += "\nfrom syned.beamline.element_coordinates import ElementCoordinates"
        txt += "\ncoordinates = ElementCoordinates(p=%g, q=%g, angle_radial=%g, angle_azimuthal=%g, angle_radial_out=%g)" % \
               (coordinates.p(), coordinates.q(), coordinates.angle_radial(), coordinates.angle_azimuthal(), coordinates.angle_radial_out())
        txt += "\nfrom shadow4.beamline.optical_elements.crystals.s4_hyperboloid_crystal import S4HyperboloidCrystalElement"
        txt += "\nbeamline_element = S4HyperboloidCrystalElement(optical_element=optical_element,coordinates=coordinates,input_beam=beam)"
        txt += "\n\nbeam, mirr = beamline_element.trace_beam()"
        return txt

if __name__ == "__main__":
    c = S4HyperboloidCrystal(
            name="Undefined",
            boundary_shape=None,
            material="Si",
            # diffraction_geometry=DiffractionGeometry.BRAGG, #?? not supposed to be in syned...
            miller_index_h=1,
            miller_index_k=1,
            miller_index_l=1,
            asymmetry_angle=0.0,
            thickness=0.010,
            f_central=False,
            f_phot_cent=0,
            phot_cent=8000.0,
            file_refl="",
            f_bragg_a=False,
            f_ext=0,)
    # print(c.info())
    # print(c.to_python_code())


    ce = S4HyperboloidCrystalElement(optical_element=c)
    print(ce.info())
    print(ce.to_python_code())

    cc = S4HyperboloidCrystalElement()
