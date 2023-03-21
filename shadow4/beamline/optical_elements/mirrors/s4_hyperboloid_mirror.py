import numpy
from syned.beamline.shape import Hyperboloid, HyperbolicCylinder, Convexity, Direction
from shadow4.beam.s4_beam import S4Beam
from shadow4.beamline.s4_optical_element_decorators import SurfaceCalculation, S4HyperboloidOpticalElementDecorator
from shadow4.beamline.optical_elements.mirrors.s4_mirror import S4MirrorElement, S4Mirror, ElementCoordinates

class S4HyperboloidMirror(S4Mirror, S4HyperboloidOpticalElementDecorator):
    def __init__(self,
                 name="Hyperboloid Mirror",
                 boundary_shape=None,
                 surface_calculation=SurfaceCalculation.INTERNAL,
                 is_cylinder=False,
                 cylinder_direction=Direction.TANGENTIAL,
                 convexity=Convexity.UPWARD,
                 min_axis=0.0,
                 maj_axis=0.0,
                 p_focus=0.0,
                 q_focus=0.0,
                 grazing_angle=0.0,
                 # inputs related to mirror reflectivity
                 f_reflec=0,  # reflectivity of surface: 0=no reflectivity, 1=full polarization
                 f_refl=0,  # 0=prerefl file
                 # 1=electric susceptibility
                 # 2=user defined file (1D reflectivity vs angle)
                 # 3=user defined file (1D reflectivity vs energy)
                 # 4=user defined file (2D reflectivity vs energy and angle)
                 file_refl="",  # preprocessor file fir f_refl=0,2,3,4
                 refraction_index=1.0  # refraction index (complex) for f_refl=1
                 ):
        S4HyperboloidOpticalElementDecorator.__init__(self, surface_calculation, is_cylinder, cylinder_direction, convexity,
                                                      min_axis, maj_axis, p_focus, q_focus, grazing_angle)
        S4Mirror.__init__(self, name, boundary_shape, self.get_surface_shape_instance(),
                          f_reflec, f_refl, file_refl, refraction_index)

        self.__inputs = {
            "name": name,
            "boundary_shape": boundary_shape,
            "surface_calculation": surface_calculation,
            "is_cylinder": is_cylinder,
            "cylinder_direction": cylinder_direction,
            "convexity": convexity,
            "min_axis": min_axis,
            "maj_axis": maj_axis,
            "p_focus": p_focus,
            "q_focus": q_focus,
            "grazing_angle": grazing_angle,
            "f_reflec": f_reflec,
            "f_refl": f_refl,
            "file_refl": file_refl,
            "refraction_index": refraction_index,
        }

    def to_python_code(self, **kwargs):
        txt = "\nfrom shadow4.beamline.optical_elements.mirrors.s4_hyerboloid_mirror import S4HyperboloidMirror"
        txt_pre = """
optical_element = S4HyperboloidMirror(name='{name:s}',boundary_shape=None,
    surface_calculation={surface_calculation:d},is_cylinder={is_cylinder:d},cylinder_direction={cylinder_direction:d},
    convexity={convexity:d},min_axis={min_axis:f},maj_axis={maj_axis:f},p_focus={p_focus:f},q_focus={q_focus:f},
    grazing_angle={grazing_angle:f},
    f_reflec={f_reflec:d},f_refl={f_refl:d},file_refl='{file_refl:s}',refraction_index={refraction_index:g})
    """
        txt += txt_pre.format(**self.__inputs)
        return txt

    def apply_geometrical_model(self, beam):
        ccc = self.get_optical_surface_instance()
        footprint, normal = ccc.apply_specular_reflection_on_beam(beam)
        return footprint, normal

class S4HyperboloidMirrorElement(S4MirrorElement):
    def __init__(self,
                 optical_element : S4HyperboloidMirror = None,
                 coordinates : ElementCoordinates = None,
                 input_beam : S4Beam = None):
        super().__init__(optical_element=optical_element if optical_element is not None else S4HyperboloidMirror(),
                         coordinates=coordinates if coordinates is not None else ElementCoordinates(),
                         input_beam=input_beam)
        if not (isinstance(self.get_optical_element().get_surface_shape(), HyperbolicCylinder) or
                isinstance(self.get_optical_element().get_surface_shape(), Hyperboloid)):
            raise ValueError("Wrong Optical Element: only Hyperboloid or Hyperbolic Cylinder shape is accepted")

    def to_python_code(self, **kwargs):
        txt = "\n\n# optical element number XX"
        txt += self.get_optical_element().to_python_code()
        coordinates = self.get_coordinates()
        txt += "\nfrom syned.beamline.element_coordinates import ElementCoordinates"
        txt += "\ncoordinates=ElementCoordinates(p=%g,q=%g,angle_radial=%g)" % \
               (coordinates.p(), coordinates.q(), coordinates.angle_radial())
        txt += "\nfrom shadow4.beamline.optical_elements.mirrors.s4_hyperboloid_mirror import S4HyperboloidMirrorElement"
        txt += "\nbeamline_element = S4HyperboloidMirrorElement(optical_element=optical_element,coordinates=coordinates,input_beam=beam)"
        txt += "\n\nbeam, mirr = beamline_element.trace_beam()"
        return txt


if __name__=="__main__":
    from syned.beamline.shape import Rectangle

    angle_radial = 88.0

    el = S4HyperboloidMirrorElement(optical_element=S4HyperboloidMirror(boundary_shape=Rectangle(),
                                                                        surface_calculation=SurfaceCalculation.INTERNAL,
                                                                        is_cylinder=True,
                                                                        cylinder_direction=Direction.TANGENTIAL,
                                                                        convexity=Convexity.UPWARD,
                                                                        p_focus=20000,
                                                                        q_focus=1000,
                                                                        grazing_angle=numpy.radians(90-angle_radial)),
                                    coordinates=ElementCoordinates(p=20000, q=1000, angle_radial=88.0, angle_azimuthal=0.0))

    print(el.get_optical_element().get_surface_shape())
