import numpy
from shadow4.syned.shape import Conic, Plane
from shadow4.beamline.optical_elements.crystals.s4_crystal import S4CrystalElement, S4Crystal
from shadow4.syned.element_coordinates import ElementCoordinates
from shadow4.optical_surfaces.s4_conic import S4Conic

from shadow4.beamline.s4_optical_element import S4ConicOpticalElement

from syned.beamline.optical_elements.crystals.crystal import DiffractionGeometry

class S4PlaneCrystal(S4Crystal, S4ConicOpticalElement):
    def __init__(self,
                 name="Plane crystal",
                 boundary_shape=None,
                 # surface_shape=None,
                 material=None,
                 diffraction_geometry=DiffractionGeometry.BRAGG,  # ?? not supposed to be in syned...
                 miller_index_h=1,
                 miller_index_k=1,
                 miller_index_l=1,
                 asymmetry_angle=0.0,
                 thickness=0.010,  ###########################
                 f_central=False,
                 f_phot_cent=0,
                 phot_cent=8000.0,
                 file_refl="",
                 f_bragg_a=False,
                 # a_bragg=0.0,
                 f_johansson=False,
                 r_johansson=1.0,
                 f_mosaic=False,
                 spread_mos=0.4 * numpy.pi / 180,
                 f_ext=0,
                 ):

        S4ConicOpticalElement.__init__(self, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0])
        S4Crystal.__init__(self,
                           name=name,
                           boundary_shape=boundary_shape,
                           surface_shape=Conic(conic_coefficients=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0]),
                           material=material,
                           diffraction_geometry=diffraction_geometry,  # ?? not supposed to be in syned...
                           miller_index_h=miller_index_h,
                           miller_index_k=miller_index_k,
                           miller_index_l=miller_index_l,
                           asymmetry_angle=asymmetry_angle,
                           thickness=thickness,  ###########################
                           f_central=f_central,
                           f_phot_cent=f_phot_cent,
                           phot_cent=phot_cent,
                           file_refl=file_refl,
                           f_bragg_a=f_bragg_a,
                           # a_bragg=0.0,
                           f_johansson=f_johansson,
                           r_johansson=r_johansson,
                           f_mosaic=f_mosaic,
                           spread_mos=spread_mos,
                           f_ext=f_ext,
                           )

class S4PlaneCrystalElement(S4CrystalElement):
    def __init__(self, optical_element=None, coordinates=None):
        super().__init__(optical_element if optical_element is not None else S4Crystal(),
                         coordinates if coordinates is not None else ElementCoordinates())
        if not isinstance(self.get_optical_element().get_surface_shape(), Conic):
            raise ValueError("Wrong Optical Element: only Conic shape is accepted")



    def apply_crystal_diffraction(self, beam):
        surface_shape = self.get_optical_element().get_surface_shape()

        ccc = S4Conic.initialize_from_coefficients(surface_shape.get_conic_coefficients())

        oe = self.get_optical_element()

        if oe._diffraction_geometry == DiffractionGeometry.BRAGG and oe._asymmetry_angle == 0.0:
            beam_mirr, normal = ccc.apply_crystal_diffraction_bragg_symmetric_on_beam(beam)
        else:
            raise Exception(NotImplementedError)

        return beam_mirr, normal


if __name__ == "__main__":
    c = S4PlaneCrystal(
            name="Undefined",
            boundary_shape=None,
            material="Si",
            diffraction_geometry=DiffractionGeometry.BRAGG, #?? not supposed to be in syned...
            miller_index_h=1,
            miller_index_k=1,
            miller_index_l=1,
            asymmetry_angle=0.0,
            thickness=0.010, ###########################
            f_central=False,
            f_phot_cent=0,
            phot_cent=8000.0,
            file_refl="",
            f_bragg_a=False,
            # a_bragg=0.0,
            f_johansson=False,
            r_johansson=1.0,
            f_mosaic=False,
            spread_mos=0.4*numpy.pi/180,
            f_ext=0,)
    # print(c.info())


    ce = S4PlaneCrystalElement(optical_element=c)
    print(ce.info())