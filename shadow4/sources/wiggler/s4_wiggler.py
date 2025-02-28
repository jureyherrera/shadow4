import numpy
from syned.storage_ring.magnetic_structures.wiggler import Wiggler
import scipy.constants as codata

class S4Wiggler(Wiggler):
    def __init__(self,
                 magnetic_field_periodic=1, # 0=external, 1=periodic
                 file_with_magnetic_field="", # useful if magnetic_field_periodic=0
                 K_vertical=10.0, period_length=0.1, number_of_periods=10, # syned Wiggler pars: useful if magnetic_field_periodic=1
                 emin=1000.0,               # Photon energy scan from energy (in eV)
                 emax=2000.0,               # Photon energy scan to energy (in eV)
                 ng_e=11,                    # Photon energy scan number of points
                 ng_j=20,                    # Number of points in electron trajectory (per period) for internal calculation only
                 flag_emittance=0,           # when sampling rays: Use emittance (0=No, 1=Yes)
                 shift_x_flag=0,        # Shift x? 0:No, 1:Half excursion, 2:min, 3:max, 4:value at y=0, 5:user value
                 shift_x_value=0.0,     # for shift_x_flag=5, the x value
                 shift_betax_flag=0,    # Shift x'? 0:No, 1:Half excursion, 2:min, 3:max, 4:value at y=0, 5:user value
                 shift_betax_value=0.0, # for shift_betax_flag=5, the x' value
                 epsi_dx=0.0, # distance from waist X
                 epsi_dz=0.0, # distance from waist Z
                 ):

        self._magnetic_field_periodic = magnetic_field_periodic
        self._file_with_magnetic_field = file_with_magnetic_field

        super().__init__(K_vertical=K_vertical, K_horizontal=0.0,
                        period_length=period_length, number_of_periods=number_of_periods)

        # Photon energy scan
        self._EMIN            = emin   # Photon energy scan from energy (in eV)
        self._EMAX            = emax   # Photon energy scan to energy (in eV)
        self._NG_E            = ng_e   # Photon energy scan number of points

        # other specific inputs
        self._NG_J            = ng_j       # Number of points in electron trajectory (per period)
        self._FLAG_EMITTANCE  =  flag_emittance # Yes  # Use emittance (0=No, 1=Yes)

        self._shift_x_flag      = shift_x_flag
        self._shift_x_value     = shift_x_value
        self._shift_betax_flag  = shift_betax_flag
        self._shift_betax_value = shift_betax_value

        self._EPSI_DX           = epsi_dx
        self._EPSI_DZ           = epsi_dz

    def info(self,debug=False):

        txt = ""
        # txt += "-----------------------------------------------------\n"

        if self._magnetic_field_periodic:  # conventional wiggler
            txt += "Input Wiggler parameters: \n"
            txt += "        period: %f m\n"%self.period_length()
            txt += "        number of periods: %d\n"%self.number_of_periods()
            txt += "        K-value: %f\n"%self.K_vertical()

            # txt += "-----------------------------------------------------\n"

            txt += "Wiggler length: %f m\n"%(self.period_length()*self.number_of_periods())
            K_to_B = (2.0 * numpy.pi / self.period_length()) * codata.m_e * codata.c / codata.e
            txt += "Wiggler peak magnetic field: %f T\n"%(K_to_B*self.K_vertical())

        else: # magnetic field from file
            txt += "Input Wiggler parameters: \n"
            txt += "        from external magnetic field: %s \n" % self._file_with_magnetic_field

        # txt += "-----------------------------------------------------\n"
        txt += "Grids: \n"
        if self._NG_E == 1:
            txt += "        photon energy %f eV\n"%(self._EMIN)
        else:
            txt += "        photon energy from %10.3f eV to %10.3f eV\n"%(self._EMIN,self._EMAX)
        txt += "        number of energy points: %d\n"%(self._NG_E)
        txt += "        number of points for the trajectory: %d\n"%(self._NG_J)

        txt += "\n\n"
        txt += "        distance from waist X: %f m\n" % (self._EPSI_DX)
        txt += "        distance from waist Z: %f m\n" % (self._EPSI_DZ)
        # txt += "-----------------------------------------------------\n"

        return txt

    def get_flag_emittance(self):
        return self._FLAG_EMITTANCE

    def set_energy_monochromatic(self,emin):
        """
        Sets a single energy line for the source (monochromatic)
        :param emin: the energy in eV
        :return:
        """
        self._EMIN = emin
        self._EMAX = emin
        self._NG_E = 1


    def set_energy_box(self,emin,emax,npoints=None):
        """
        Sets a box for photon energy distribution for the source
        :param emin:  Photon energy scan from energy (in eV)
        :param emax:  Photon energy scan to energy (in eV)
        :param npoints:  Photon energy scan number of points (optinal, if not set no changes)
        :return:
        """

        self._EMIN = emin
        self._EMAX = emax
        if npoints != None:
            self._NG_E = npoints


    def get_energy_box(self):
        """
        Gets the limits of photon energy distribution for the source
        :return: emin,emax,number_of_points
        """
        return self._EMIN,self._EMAX,self._NG_E

    def set_electron_initial_conditions(self,shift_x_flag=0,shift_x_value=0.0,shift_betax_flag=0,shift_betax_value=0.0):
        self._shift_x_flag      = shift_x_flag
        self._shift_x_value     = shift_x_value
        self._shift_betax_flag  = shift_betax_flag
        self._shift_betax_value = shift_betax_value

    def set_electron_initial_conditions_by_label(self,
                                        position_label="no_shift", # values are: no_shift, half_excursion, minimum, maximum, value_at_zero, user_value
                                        velocity_label="no_shift", # values are: no_shift, half_excursion, minimum, maximum, value_at_zero, user_value
                                        position_value=0.0,
                                        velocity_value=0.0,
                                        ):
        self._shift_x_value = 0.0
        self._shift_betax_value = 0.0

        if position_label == "no_shift":
            self._shift_x_flag = 0
        elif position_label == "half_excursion":
            self._shift_x_flag = 1
        elif position_label == "minimum":
            self._shift_x_flag = 2
        elif position_label == "maximum":
            self._shift_x_flag = 3
        elif position_label == "value_at_zero":
            self._shift_x_flag = 4
        elif position_label == "user_value":
            self._shift_x_flag = 5
            self._shift_x_value = position_value
        else:
            raise Exception("Invalid value for keyword position_label")

        if velocity_label == "no_shift":
            self._shift_betax_flag = 0
        elif velocity_label == "half_excursion":
            self._shift_betax_flag = 1
        elif velocity_label == "minimum":
            self._shift_betax_flag = 2
        elif velocity_label == "maximum":
            self._shift_betax_flag = 3
        elif velocity_label == "value_at_zero":
            self._shift_betax_flag = 4
        elif velocity_label == "user_value":
            self._shift_betax_flag = 5
            self._shift_betax_value = velocity_value
        else:
            raise Exception("Invalid value for keyword velocity_label")

    def to_python_code(self):
        script_template = """
        
#magnetic structure
from shadow4.sources.wiggler.s4_wiggler import S4Wiggler
source = S4Wiggler(
    magnetic_field_periodic  = {magnetic_field_periodic},  # 0=external, 1=periodic
    file_with_magnetic_field = "{file_with_magnetic_field}",  # used only if magnetic_field_periodic=0
    K_vertical        = {K_vertical},  # syned Wiggler pars: used only if magnetic_field_periodic=1
    period_length     = {period_length}, # syned Wiggler pars: used only if magnetic_field_periodic=1
    number_of_periods = {number_of_periods},  # syned Wiggler pars: used only if magnetic_field_periodic=1
    emin              = {emin},  # Photon energy scan from energy (in eV)
    emax              = {emax},  # Photon energy scan to energy (in eV)
    ng_e              = {ng_e},  # Photon energy scan number of points
    ng_j              = {ng_j} , # Number of points in electron trajectory (per period) for internal calculation only
    epsi_dx           = {epsi_dx},  # distance to waist in X [m]
    epsi_dz           = {epsi_dZ} , # distance to waist in Z [m]
    flag_emittance    = {flag_emittance}, # Use emittance (0=No, 1=Yes)
    shift_x_flag      = {shift_x_flag}, # 0="No shift", 1="Half excursion", 2="Minimum", 3="Maximum", 4="Value at zero", 5="User value"
    shift_x_value     = {shift_x_value}, # used only if shift_x_flag=5
    shift_betax_flag  = {shift_betax_flag}, # 0="No shift", 1="Half excursion", 2="Minimum", 3="Maximum", 4="Value at zero", 5="User value"
    shift_betax_value = {shift_betax_value},#  used only if shift_betax_flag=5
    )"""


        script_dict = {
            "magnetic_field_periodic"  : self._magnetic_field_periodic ,
            "file_with_magnetic_field" : self._file_with_magnetic_field,
            "K_vertical"               : self.K_vertical()       ,
            "period_length"            : self.period_length()    ,
            "number_of_periods"        : self.number_of_periods(),
            "emin"                     : self._EMIN            ,
            "emax"                     : self._EMAX            ,
            "ng_e"                     : self._NG_E            ,
            "ng_j"                     : self._NG_J            ,
            "epsi_dx"                  : self._EPSI_DX,
            "epsi_dz"                  : self._EPSI_DZ,
            "flag_emittance"           : self._FLAG_EMITTANCE  ,
            "shift_x_flag"             : self._shift_x_flag     ,
            "shift_x_value"            : self._shift_x_value    ,
            "shift_betax_flag"         : self._shift_betax_flag ,
            "shift_betax_value"        : self._shift_betax_value,
        }

        script = script_template.format_map(script_dict)

        return script

if __name__ == "__main__":

    from srxraylib.plot.gol import set_qt
    set_qt()

    e_min = 5000.0 # 70490.0 #
    e_max = 100000.0 # 70510.0 #
    e_min = 70490.0 #
    e_max = 70510.0 #
    NRAYS = 5000
    use_emittances=True



    wigFile = "xshwig.sha"
    inData = ""

    nPer = 5 # 50
    nTrajPoints = 501
    ener_gev = 6.04
    per = 0.040
    kValue = 7.85
    trajFile = "tmp.traj"
    shift_x_flag = 0
    shift_x_value = 0.0
    shift_betax_flag = 0
    shift_betax_value = 0.0


    sw = S4Wiggler(magnetic_field_periodic=1, # 0=external, 1=periodic
                 file_with_magnetic_field="", # useful if magnetic_field_periodic=0
                 K_vertical=10.0, period_length=0.1, number_of_periods=10, # syned Wiggler pars: useful if magnetic_field_periodic=1
                 emin=1000.0,               # Photon energy scan from energy (in eV)
                 emax=2000.0,               # Photon energy scan to energy (in eV)
                 ng_e=11,                    # Photon energy scan number of points
                 ng_j=20,                    # Number of points in electron trajectory (per period) for internal calculation only
                 flag_emittance=0,           # when sampling rays: Use emittance (0=No, 1=Yes)
                 shift_x_flag=0, shift_x_value=0.0, shift_betax_flag=0, shift_betax_value=0.0,) # ele)
    print(sw.info())

    sw = S4Wiggler(magnetic_field_periodic=0, # 0=external, 1=periodic
                 file_with_magnetic_field="magnetic_field.dat", # useful if magnetic_field_periodic=0
                 K_vertical=10.0, period_length=0.1, number_of_periods=10, # syned Wiggler pars: useful if magnetic_field_periodic=1
                 emin=1000.0,               # Photon energy scan from energy (in eV)
                 emax=2000.0,               # Photon energy scan to energy (in eV)
                 ng_e=11,                    # Photon energy scan number of points
                 ng_j=20,                    # Number of points in electron trajectory (per period) for internal calculation only
                 flag_emittance=0,           # when sampling rays: Use emittance (0=No, 1=Yes)
                 shift_x_flag=0, shift_x_value=0.0, shift_betax_flag=0, shift_betax_value=0.0,) # ele)
    print(sw.info())

    print(sw.to_python_code())

    # #
    # # syned
    # #
    # syned_wiggler = Wiggler(K_vertical=kValue,K_horizontal=0.0,period_length=per,number_of_periods=nPer)
    #
    #
    # syned_electron_beam = ElectronBeam(energy_in_GeV=6.04,
    #              energy_spread = 0.0,
    #              current = 0.2,
    #              number_of_bunches = 400,
    #              moment_xx=(400e-6)**2,
    #              moment_xxp=0.0,
    #              moment_xpxp=(10e-6)**2,
    #              moment_yy=(10e-6)**2,
    #              moment_yyp=0.0,
    #              moment_ypyp=(4e-6)**2 )
    #
    # sourcewiggler = SourceWiggler(name="test",syned_electron_beam=syned_electron_beam,
    #                 syned_wiggler=syned_wiggler,
    #                 flag_emittance=use_emittances,
    #                 emin=e_min,emax=e_max,ng_e=10, ng_j=nTrajPoints)
    #
    #
    #
    # print(sourcewiggler.info())
    #
    #
    # rays = sourcewiggler.calculate_rays(NRAYS=NRAYS)
    #
    # plot_scatter(rays[:,1],rays[:,0],title="trajectory",show=False)
    # plot_scatter(rays[:,0],rays[:,2],title="real space",show=False)
    # plot_scatter(rays[:,3],rays[:,5],title="divergence space")

