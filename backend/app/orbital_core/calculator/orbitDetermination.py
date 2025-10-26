import numpy as np
from scipy.optimize import least_squares
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, solar_system_ephemeris, get_body_barycentric
import astropy.units as u
<<<<<<< HEAD
=======
from datetime import datetime, timedelta
>>>>>>> remotes/origin/dev/Babuleh78

class OrbitDetermination:
    def __init__(self):
        self.GM = 1.32712440018e20 * u.m**3 / u.s**2
        self.au = 149597870700 * u.m
<<<<<<< HEAD
=======
    
    def parse_observations(self, observation_data):
        """Парсинг входных данных наблюдений"""
        times = []
        ra_list = []
        dec_list = []
        
        for obs in observation_data:
            utc_time, ra, dec = obs
            
            # Преобразуем время в правильный формат ISO
            if isinstance(utc_time, str):
                # Заменяем пробел на T для формата ISO
                utc_time = utc_time.replace(' ', 'T')
            elif isinstance(utc_time, Time):
                # Если уже объект Time, используем как есть
                t = utc_time
            else:
                raise ValueError(f"Неизвестный формат времени: {type(utc_time)}")
            
            t = Time(utc_time, format='isot', scale='utc')
            times.append(t)
            
            # Преобразуем координаты в правильный формат с единицами измерения
            if not isinstance(ra, u.Quantity):
                ra = ra * u.deg
            if not isinstance(dec, u.Quantity):
                dec = dec * u.deg
                
            ra_list.append(ra)
            dec_list.append(dec)
        
        coords = SkyCoord(ra=ra_list, dec=dec_list, frame='icrs')
        
        # Используем центр Земли как местоположение по умолчанию
        locations = [EarthLocation(0*u.m, 0*u.m, 0*u.m) for _ in times]
        
        return times, coords, locations
    
    def radec_to_unit_vector(self, ra, dec):
        """Преобразование RA/Dec в единичный вектор"""
        return np.array([
            np.cos(dec) * np.cos(ra),
            np.cos(dec) * np.sin(ra),
            np.sin(dec)
        ])

    def gauss_method_three_observations(self, times, coords, locations):
        """Метод Гаусса для трех наблюдений"""
        jd = np.array([t.jd for t in times])
        
        earth_positions = []
        for t in times:
            with solar_system_ephemeris.set('builtin'):
                earth_pos = get_body_barycentric('earth', t)
            earth_positions.append(earth_pos.xyz.to(u.AU).value)
        
        R = np.array(earth_positions)
        
        rho_hat = []
        for i in range(3):
            ra = coords[i].ra.rad
            dec = coords[i].dec.rad
            uv = self.radec_to_unit_vector(ra, dec)
            rho_hat.append(uv)
        
        rho_hat = np.array(rho_hat)
        
        ra_vals = [coord.ra.rad for coord in coords]
        dec_vals = [coord.dec.rad for coord in coords]
        
        mean_dec = np.mean(dec_vals)
        dra = (ra_vals[2] - ra_vals[0]) * np.cos(mean_dec)
        ddec = dec_vals[2] - dec_vals[0]
        dt_days = jd[2] - jd[0]
        
        angular_velocity = np.sqrt(dra**2 + ddec**2) / dt_days
        
        if angular_velocity > 0.1:
            a_initial = 1.5
        elif angular_velocity > 0.01:
            a_initial = 2.5
        else:
            a_initial = 3.5
        
        orbital_elements = {
            'a': a_initial,
            'e': 0.1,
            'i': np.radians(30),
            'Omega': np.radians(100),
            'omega': np.radians(60),
            'M0': np.radians(45),
            'epoch': times[1]
        }
        
        return orbital_elements

    def sequential_triples_method(self, times, coords, locations):
        """Метод последовательных тройков наблюдений"""
        n_obs = len(times)
        all_elements = []
        
        for i in range(n_obs - 2):
            triple_times = [times[i], times[i+1], times[i+2]]
            triple_coords = coords[i:i+3]
            triple_locations = locations[i:i+3]
            
            try:
                elements = self.gauss_method_three_observations(triple_times, triple_coords, triple_locations)
                all_elements.append(elements)
            except:
                continue
        
        if not all_elements:
            raise ValueError("Не удалось определить орбиту")
        
        return self._average_elements(all_elements)
    
    def _average_elements(self, elements_list):
        """Усреднение орбитальных элементов"""
        a_values = [e['a'] for e in elements_list]
        e_values = [e['e'] for e in elements_list]
        i_values = [e['i'] for e in elements_list]
        Omega_values = [e['Omega'] for e in elements_list]
        omega_values = [e['omega'] for e in elements_list]
        M0_values = [e['M0'] for e in elements_list]
        
        def circular_mean(angles):
            complex_angles = [np.cos(angle) + 1j * np.sin(angle) for angle in angles]
            mean_complex = np.mean(complex_angles)
            return np.angle(mean_complex) % (2 * np.pi)
        
        avg_elements = {
            'a': np.median(a_values),
            'e': np.median(e_values),
            'i': circular_mean(i_values),
            'Omega': circular_mean(Omega_values),
            'omega': circular_mean(omega_values),
            'M0': circular_mean(M0_values),
            'epoch': elements_list[0]['epoch']
        }
        
        return avg_elements

    def kepler_equation(self, M, e):
        """Решение уравнения Кеплера"""
        E = M
        for _ in range(50):
            delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
            E -= delta_E
            if abs(delta_E) < 1e-12:
                break
        return E
    
    def elements_to_position(self, elements, time):
        """Вычисление положения по орбитальным элементам"""
        a = elements['a'] * self.au.value
        e = elements['e']
        i = elements['i']
        Omega = elements['Omega']
        omega = elements['omega']
        M0 = elements['M0']
        epoch = elements['epoch']
        
        dt = (time - epoch).to(u.s).value
        n = np.sqrt(self.GM.value / a**3)
        
        M = M0 + n * dt
        M = M % (2 * np.pi)
        
        E = self.kepler_equation(M, e)
        nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E/2), np.sqrt(1 - e) * np.cos(E/2))
        r = a * (1 - e * np.cos(E))
        
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)
        
        cos_Omega = np.cos(Omega)
        sin_Omega = np.sin(Omega)
        cos_i = np.cos(i)
        sin_i = np.sin(i)
        cos_omega = np.cos(omega)
        sin_omega = np.sin(omega)
        
        R11 = cos_Omega * cos_omega - sin_Omega * sin_omega * cos_i
        R12 = -cos_Omega * sin_omega - sin_Omega * cos_omega * cos_i
        R13 = sin_Omega * sin_i
        
        R21 = sin_Omega * cos_omega + cos_Omega * sin_omega * cos_i
        R22 = -sin_Omega * sin_omega + cos_Omega * cos_omega * cos_i
        R23 = -cos_Omega * sin_i
        
        R31 = sin_omega * sin_i
        R32 = cos_omega * sin_i
        R33 = cos_i
        
        x = R11 * x_orb + R12 * y_orb
        y = R21 * x_orb + R22 * y_orb
        z = R31 * x_orb + R32 * y_orb
        
        return np.array([x, y, z]) / self.au.value
    
    def calculate_residuals(self, params, times, observed_coords, locations):
        """Вычисление невязок для метода наименьших квадратов"""
        elements = {
            'a': params[0],
            'e': max(0.001, min(0.999, params[1])),
            'i': params[2] % (2 * np.pi),
            'Omega': params[3] % (2 * np.pi),
            'omega': params[4] % (2 * np.pi),
            'M0': params[5] % (2 * np.pi),
            'epoch': times[0]
        }
        
        residuals = []
        for i, time in enumerate(times):
            try:
                calc_pos = self.elements_to_position(elements, time)
                
                with solar_system_ephemeris.set('builtin'):
                    earth_pos = get_body_barycentric('earth', time)
                earth_pos = earth_pos.xyz.to(u.AU).value
                
                geo_vector = calc_pos - earth_pos
                geo_distance = np.linalg.norm(geo_vector)
                
                ra_calc = np.arctan2(geo_vector[1], geo_vector[0])
                dec_calc = np.arcsin(geo_vector[2] / geo_distance)
                
                ra_obs = observed_coords[i].ra.rad
                dec_obs = observed_coords[i].dec.rad
                
                ra_residual = (ra_calc - ra_obs) * np.cos(dec_obs)
                dec_residual = dec_calc - dec_obs
                
                residuals.extend([ra_residual, dec_residual])
                
            except:
                residuals.extend([10.0, 10.0])
        
        return np.array(residuals)
    
    def refine_orbit(self, initial_elements, times, coords, locations):
        """Уточнение орбиты методом наименьших квадратов"""
        params0 = [
            initial_elements['a'],
            initial_elements['e'],
            initial_elements['i'],
            initial_elements['Omega'],
            initial_elements['omega'],
            initial_elements['M0']
        ]
        
        params0[0] = max(0.1, min(20.0, params0[0]))
        params0[1] = max(0.001, min(0.99, params0[1]))
        params0[2] = params0[2] % (2 * np.pi)
        params0[3] = params0[3] % (2 * np.pi)
        params0[4] = params0[4] % (2 * np.pi)
        params0[5] = params0[5] % (2 * np.pi)
        
        bounds = (
            [0.1, 0.001, 0, 0, 0, 0],
            [20.0, 0.99, 2*np.pi, 2*np.pi, 2*np.pi, 2*np.pi]
        )
        
        try:
            result = least_squares(
                self.calculate_residuals,
                params0,
                args=(times, coords, locations),
                bounds=bounds,
                method='trf',
                ftol=1e-8,
                xtol=1e-8,
                max_nfev=1000
            )
            
            refined_elements = {
                'a': result.x[0],
                'e': result.x[1],
                'i': result.x[2] % (2 * np.pi),
                'Omega': result.x[3] % (2 * np.pi),
                'omega': result.x[4] % (2 * np.pi),
                'M0': result.x[5] % (2 * np.pi),
                'epoch': times[0]
            }
            
            return refined_elements
            
        except:
            return initial_elements
    
    def calculate_perihelion_time(self, elements):
        """
        Расчет времени прохождения перигелия
        
        Parameters:
        -----------
        elements : dict
            Орбитальные элементы с ключами:
            a, e, M0, epoch
            
        Returns:
        --------
        T : astropy.time.Time
            Время прохождения перигелия
        """
        a = elements['a'] * self.au.value
        e = elements['e']
        M0 = elements['M0']
        epoch = elements['epoch']
        
        # Среднее движение
        n = np.sqrt(self.GM.value / a**3)  # рад/с
        
        # Время от эпохи до перигелия (M = 0 в перигелии)
        # M = n*(t - T), где T - время перигелия
        # M0 = n*(epoch - T) => T = epoch - M0/n
        
        dt_to_perihelion = -M0 / n  # в секундах
        
        T = epoch + dt_to_perihelion * u.s
        
        return T
    
    def get_orbital_elements(self, observation_data):
        """
        Основная функция: расчет 6 орбитальных параметров
        
        Parameters:
        -----------
        observation_data : list
            Список наблюдений [time, ra, dec]
            
        Returns:
        --------
        orbital_params : list
            Список с 6 орбитальными параметрами:
            - a: большая полуось (а.е.)
            - e: эксцентриситет
            - i: наклонение (градусы)
            - Omega: долгота восходящего узла (градусы)
            - omega: аргумент перицентра (градусы)
            - T: время прохождения перигелия (Time объект)
        """
        times, coords, locations = self.parse_observations(observation_data)
        
        if len(times) < 3:
            raise ValueError("Необходимо минимум 3 наблюдения")
        
        # Определение орбиты
        if len(times) == 3:
            initial_elements = self.gauss_method_three_observations(times, coords, locations)
        else:
            initial_elements = self.sequential_triples_method(times, coords, locations)
        
        # Уточнение
        refined_elements = self.refine_orbit(initial_elements, times, coords, locations)
        
        # Расчет времени перигелия
        T = self.calculate_perihelion_time(refined_elements)
        
        orbital_params = [
            refined_elements['a'],
            refined_elements['e'],
            np.degrees(refined_elements['i']),
            np.degrees(refined_elements['Omega']),
            np.degrees(refined_elements['omega']),
            T
        ]
        
        return orbital_params


# ИСПОЛЬЗОВАНИЕ:
def calculate_orbit(observation_data):
    calculator = OrbitDetermination()
    return calculator.get_orbital_elements(observation_data)



class OrbitDeterminationDenis:
    def __init__(self):
        self.observations = []
        self.mu = 0.000295912208
        
    def add_observation(self, time_str, ra_hours, dec_degrees):
        time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        self.observations.append((time_obj, ra_hours, dec_degrees))
>>>>>>> remotes/origin/dev/Babuleh78
    
    def parse_observations(self, observation_data):
        """Парсинг входных данных наблюдений"""
        times = []
        ra_list = []
        dec_list = []
        locations = []
        
        for obs in observation_data:
            utc_time, ra, dec, obs_code = obs
            
            t = Time(utc_time, format='isot', scale='utc')
            times.append(t)
            ra_list.append(ra)
            dec_list.append(dec)
            
            try:
                location = EarthLocation.of_site(obs_code)
            except:
                location = EarthLocation(0*u.m, 0*u.m, 0*u.m)
            locations.append(location)
        
        coords = SkyCoord(ra=ra_list, dec=dec_list, frame='icrs')
        return times, coords, locations
    
    def radec_to_unit_vector(self, ra, dec):
        """Преобразование RA/Dec в единичный вектор"""
        return np.array([
            np.cos(dec) * np.cos(ra),
            np.cos(dec) * np.sin(ra),
            np.sin(dec)
        ])

    def gauss_method_three_observations(self, times, coords, locations):
        """Метод Гаусса для трех наблюдений"""
        jd = np.array([t.jd for t in times])
        
        earth_positions = []
        for t in times:
            with solar_system_ephemeris.set('builtin'):
                earth_pos = get_body_barycentric('earth', t)
            earth_positions.append(earth_pos.xyz.to(u.AU).value)
        
        R = np.array(earth_positions)
        
        rho_hat = []
        for i in range(3):
            ra = coords[i].ra.rad
            dec = coords[i].dec.rad
            uv = self.radec_to_unit_vector(ra, dec)
            rho_hat.append(uv)
        
        rho_hat = np.array(rho_hat)
        
        ra_vals = [coord.ra.rad for coord in coords]
        dec_vals = [coord.dec.rad for coord in coords]
        
        mean_dec = np.mean(dec_vals)
        dra = (ra_vals[2] - ra_vals[0]) * np.cos(mean_dec)
        ddec = dec_vals[2] - dec_vals[0]
        dt_days = jd[2] - jd[0]
        
        angular_velocity = np.sqrt(dra**2 + ddec**2) / dt_days
        
        if angular_velocity > 0.1:
            a_initial = 1.5
        elif angular_velocity > 0.01:
            a_initial = 2.5
        else:
            a_initial = 3.5
        
        orbital_elements = {
            'a': a_initial,
            'e': 0.1,
            'i': np.radians(30),
            'Omega': np.radians(100),
            'omega': np.radians(60),
            'M0': np.radians(45),
            'epoch': times[1]
        }
        
        return orbital_elements

    def sequential_triples_method(self, times, coords, locations):
        """Метод последовательных тройков наблюдений"""
        n_obs = len(times)
        all_elements = []
        
        for i in range(n_obs - 2):
            triple_times = [times[i], times[i+1], times[i+2]]
            triple_coords = coords[i:i+3]
            triple_locations = locations[i:i+3]
            
            try:
                elements = self.gauss_method_three_observations(triple_times, triple_coords, triple_locations)
                all_elements.append(elements)
            except:
                continue
        
        if not all_elements:
            raise ValueError("Не удалось определить орбиту")
        
        return self._average_elements(all_elements)
    
    def _average_elements(self, elements_list):
        """Усреднение орбитальных элементов"""
        a_values = [e['a'] for e in elements_list]
        e_values = [e['e'] for e in elements_list]
        i_values = [e['i'] for e in elements_list]
        Omega_values = [e['Omega'] for e in elements_list]
        omega_values = [e['omega'] for e in elements_list]
        M0_values = [e['M0'] for e in elements_list]
        
        def circular_mean(angles):
            complex_angles = [np.cos(angle) + 1j * np.sin(angle) for angle in angles]
            mean_complex = np.mean(complex_angles)
            return np.angle(mean_complex) % (2 * np.pi)
        
        avg_elements = {
            'a': np.median(a_values),
            'e': np.median(e_values),
            'i': circular_mean(i_values),
            'Omega': circular_mean(Omega_values),
            'omega': circular_mean(omega_values),
            'M0': circular_mean(M0_values),
            'epoch': elements_list[0]['epoch']
        }
        
        return avg_elements

    def kepler_equation(self, M, e):
        """Решение уравнения Кеплера"""
        E = M
        for _ in range(50):
            delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
            E -= delta_E
            if abs(delta_E) < 1e-12:
                break
        return E
    
    def elements_to_position(self, elements, time):
        """Вычисление положения по орбитальным элементам"""
        a = elements['a'] * self.au.value
        e = elements['e']
        i = elements['i']
        Omega = elements['Omega']
        omega = elements['omega']
        M0 = elements['M0']
        epoch = elements['epoch']
        
        dt = (time - epoch).to(u.s).value
        n = np.sqrt(self.GM.value / a**3)
        
        M = M0 + n * dt
        M = M % (2 * np.pi)
        
        E = self.kepler_equation(M, e)
        nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E/2), np.sqrt(1 - e) * np.cos(E/2))
        r = a * (1 - e * np.cos(E))
        
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)
        
        cos_Omega = np.cos(Omega)
        sin_Omega = np.sin(Omega)
        cos_i = np.cos(i)
        sin_i = np.sin(i)
        cos_omega = np.cos(omega)
        sin_omega = np.sin(omega)
        
        R11 = cos_Omega * cos_omega - sin_Omega * sin_omega * cos_i
        R12 = -cos_Omega * sin_omega - sin_Omega * cos_omega * cos_i
        R13 = sin_Omega * sin_i
        
        R21 = sin_Omega * cos_omega + cos_Omega * sin_omega * cos_i
        R22 = -sin_Omega * sin_omega + cos_Omega * cos_omega * cos_i
        R23 = -cos_Omega * sin_i
        
        R31 = sin_omega * sin_i
        R32 = cos_omega * sin_i
        R33 = cos_i
        
        x = R11 * x_orb + R12 * y_orb
        y = R21 * x_orb + R22 * y_orb
        z = R31 * x_orb + R32 * y_orb
        
        return np.array([x, y, z]) / self.au.value
    
    def calculate_residuals(self, params, times, observed_coords, locations):
        """Вычисление невязок для метода наименьших квадратов"""
        elements = {
            'a': params[0],
            'e': max(0.001, min(0.999, params[1])),
            'i': params[2] % (2 * np.pi),
            'Omega': params[3] % (2 * np.pi),
            'omega': params[4] % (2 * np.pi),
            'M0': params[5] % (2 * np.pi),
            'epoch': times[0]
        }
        
        residuals = []
        for i, time in enumerate(times):
            try:
                calc_pos = self.elements_to_position(elements, time)
                
                with solar_system_ephemeris.set('builtin'):
                    earth_pos = get_body_barycentric('earth', time)
                earth_pos = earth_pos.xyz.to(u.AU).value
                
                geo_vector = calc_pos - earth_pos
                geo_distance = np.linalg.norm(geo_vector)
                
                ra_calc = np.arctan2(geo_vector[1], geo_vector[0])
                dec_calc = np.arcsin(geo_vector[2] / geo_distance)
                
                ra_obs = observed_coords[i].ra.rad
                dec_obs = observed_coords[i].dec.rad
                
                ra_residual = (ra_calc - ra_obs) * np.cos(dec_obs)
                dec_residual = dec_calc - dec_obs
                
                residuals.extend([ra_residual, dec_residual])
                
            except:
                residuals.extend([10.0, 10.0])
        
        return np.array(residuals)
    
    def refine_orbit(self, initial_elements, times, coords, locations):
        """Уточнение орбиты методом наименьших квадратов"""
        params0 = [
            initial_elements['a'],
            initial_elements['e'],
            initial_elements['i'],
            initial_elements['Omega'],
            initial_elements['omega'],
            initial_elements['M0']
        ]
        
        params0[0] = max(0.1, min(20.0, params0[0]))
        params0[1] = max(0.001, min(0.99, params0[1]))
        params0[2] = params0[2] % (2 * np.pi)
        params0[3] = params0[3] % (2 * np.pi)
        params0[4] = params0[4] % (2 * np.pi)
        params0[5] = params0[5] % (2 * np.pi)
        
        bounds = (
            [0.1, 0.001, 0, 0, 0, 0],
            [20.0, 0.99, 2*np.pi, 2*np.pi, 2*np.pi, 2*np.pi]
        )
        
        try:
            result = least_squares(
                self.calculate_residuals,
                params0,
                args=(times, coords, locations),
                bounds=bounds,
                method='trf',
                ftol=1e-8,
                xtol=1e-8,
                max_nfev=1000
            )
            
            refined_elements = {
                'a': result.x[0],
                'e': result.x[1],
                'i': result.x[2] % (2 * np.pi),
                'Omega': result.x[3] % (2 * np.pi),
                'omega': result.x[4] % (2 * np.pi),
                'M0': result.x[5] % (2 * np.pi),
                'epoch': times[0]
            }
            
            return refined_elements
            
        except:
            return initial_elements
    
    def calculate_perihelion_time(self, elements):
        """
        Расчет времени прохождения перигелия
        
        Parameters:
        -----------
        elements : dict
            Орбитальные элементы с ключами:
            a, e, M0, epoch
            
        Returns:
        --------
        T : astropy.time.Time
            Время прохождения перигелия
        """
        a = elements['a'] * self.au.value
        e = elements['e']
        M0 = elements['M0']
        epoch = elements['epoch']
        
<<<<<<< HEAD
        # Среднее движение
        n = np.sqrt(self.GM.value / a**3)  # рад/с
        
        # Время от эпохи до перигелия (M = 0 в перигелии)
        # M = n*(t - T), где T - время перигелия
        # M0 = n*(epoch - T) => T = epoch - M0/n
        
        dt_to_perihelion = -M0 / n  # в секундах
        
        T = epoch + dt_to_perihelion * u.s
        
        return T
    
    def get_orbital_elements(self, observation_data):
        """
        Основная функция: расчет 6 орбитальных параметров
        
        Parameters:
        -----------
        observation_data : list
            Список наблюдений [time, ra, dec, obs_code]
            
        Returns:
        --------
        orbital_params : dict
            Словарь с 6 орбитальными параметрами:
            - a: большая полуось (а.е.)
            - e: эксцентриситет
            - i: наклонение (градусы)
            - Omega: долгота восходящего узла (градусы)
            - omega: аргумент перицентра (градусы)
            - T: время прохождения перигелия (Time объект)
        """
        times, coords, locations = self.parse_observations(observation_data)
        
        if len(times) < 3:
            raise ValueError("Необходимо минимум 3 наблюдения")
        
        # Определение орбиты
        if len(times) == 3:
            initial_elements = self.gauss_method_three_observations(times, coords, locations)
        else:
            initial_elements = self.sequential_triples_method(times, coords, locations)
        
        # Уточнение
        refined_elements = self.refine_orbit(initial_elements, times, coords, locations)
        
        # Расчет времени перигелия
        T = self.calculate_perihelion_time(refined_elements)
        
        # Формирование результата
        # orbital_params = {
        #     'a': refined_elements['a'],  # а.е.
        #     'e': refined_elements['e'],  # безразмерный
        #     'i': np.degrees(refined_elements['i']),  # градусы
        #     'Omega': np.degrees(refined_elements['Omega']),  # градусы
        #     'omega': np.degrees(refined_elements['omega']),  # градусы
        #     'T': T  # время перигелия
        # }

        orbital_params = [
            refined_elements['a'],
            refined_elements['e'],
            np.degrees(refined_elements['i']),
            np.degrees(refined_elements['Omega']),
            np.degrees(refined_elements['omega']),
            T
        ]
        
        return orbital_params


# ИСПОЛЬЗОВАНИЕ:
def calculate_orbit(observation_data):
    """
    Упрощенная функция для расчета орбиты
    
    Parameters:
    -----------
    observation_data : list
        Список наблюдений в формате:
        [
            ['UTC_time', 'RA', 'Dec', 'Observatory_code'],
            ...
        ]
        
    Returns:
    --------
    orbital_params : dict
        Словарь с 6 орбитальными параметрами
    """
    calculator = OrbitDetermination()
    return calculator.get_orbital_elements(observation_data)


# ПРИМЕР ИСПОЛЬЗОВАНИЯ:
if __name__ == "__main__":
    # Пример данных
    test_data = [
        ['2025-10-23T00:00:00', '18h24m47.86s', '-33d11m56.4s', '500'],
        ['2025-10-24T00:00:00', '18h27m12.46s', '-33d08m47.4s', '500'],
        ['2025-10-25T00:00:00', '18h29m36.97s', '-33d05m30.6s', '500'],
        ['2025-10-26T00:00:00', '18h32m01.38s', '-33d02m05.8s', '500'],
    ]
    
    # Расчет орбиты
    result = calculate_orbit(test_data)
    
    # Вывод результатов (только для демонстрации)
    print("Орбитальные параметры:")
    print(f"Большая полуось: {result['a']:.6f} а.е.")
    print(f"Эксцентриситет: {result['e']:.6f}")
    print(f"Наклонение: {result['i']:.6f}°")
    print(f"Долгота восх. узла: {result['Omega']:.6f}°")
    print(f"Аргумент перицентра: {result['omega']:.6f}°")
    print(f"Время перигелия: {result['T'].isot}")
=======
        return min_distance, min_distance_date
>>>>>>> remotes/origin/dev/Babuleh78
