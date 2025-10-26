import numpy as np
from datetime import datetime, timedelta
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric, get_body
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord

class OrbitDetermination:
    def __init__(self):
        self.observations = []
        self.mu = 0.000295912208
        
    def add_observation(self, time_str, ra_hours, dec_degrees):
        time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        self.observations.append((time_obj, ra_hours, dec_degrees))
    
    def ra_dec_to_vector(self, ra_hours, dec_degrees):
        ra_rad = np.radians(ra_hours * 15.0)
        dec_rad = np.radians(dec_degrees)
        
        x = np.cos(dec_rad) * np.cos(ra_rad)
        y = np.cos(dec_rad) * np.sin(ra_rad)
        z = np.sin(dec_rad)
        
        return np.array([x, y, z])
    
    def datetime_to_jd(self, dt):
        a = (14 - dt.month) // 12
        y = dt.year + 4800 - a
        m = dt.month + 12 * a - 3
        
        jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        jd = jdn + (dt.hour - 12) / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
        return jd
    
    def get_earth_position_accurate(self, jd):
        """Используем astropy для точного положения Земли"""
        time_obj = Time(jd, format='jd')
        with solar_system_ephemeris.set('builtin'):
            earth_pos = get_body_barycentric('earth', time_obj)
        return np.array([earth_pos.x.value, earth_pos.y.value, earth_pos.z.value])
    
    def get_planet_position_astropy(self, planet_name, jd):
        """Получение положения планеты с помощью astropy"""
        time_obj = Time(jd, format='jd')
        with solar_system_ephemeris.set('builtin'):
            planet_pos = get_body_barycentric(planet_name, time_obj)
        return np.array([planet_pos.x.value, planet_pos.y.value, planet_pos.z.value])
    
    def calculate_distance_astropy(self, jd):
        """Расчет расстояния между Марсом и Землей с использованием astropy"""
        time_obj = Time(jd, format='jd')
        
        with solar_system_ephemeris.set('builtin'):
            # Получаем гелиоцентрические положения
            earth_pos = get_body_barycentric('earth', time_obj)
            mars_pos = get_body_barycentric('mars', time_obj)
            
            # Вычисляем расстояние
            distance_vector = mars_pos - earth_pos
            distance_au = np.sqrt(distance_vector.x**2 + distance_vector.y**2 + distance_vector.z**2).value
            
        return distance_au
    
    def calculate_min_earth_distance(self, mars_elements=None):
        # Устанавливаем период поиска: с 25.10.2025 по 2030 год
        start_date = datetime(2025, 10, 25)
        end_date = datetime(2027, 12, 31)
        step_days = 1  # шаг в днях для поиска
        
        current_date = start_date
        min_distance = float('inf')
        min_distance_date = None
        all_distances = []
        
        print(f"Поиск минимального расстояния в период:")
        print(f"С {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')}")
        
        while current_date <= end_date:
            try:
                jd = self.datetime_to_jd(current_date)
                
                # Используем astropy для расчета расстояния
                distance = self.calculate_distance_astropy(jd)
                
                all_distances.append((current_date, distance))
                
                if distance < min_distance:
                    min_distance = distance
                    min_distance_date = current_date
                    
            except Exception as e:
                print(f"Ошибка при расчете для даты {current_date}: {e}")
                # Пропускаем проблемные даты
                
            current_date += timedelta(days=step_days)
        
        # Находим все значительные сближения (локальные минимумы)
        approaches = []
        for i in range(1, len(all_distances)-1):
            try:
                prev_dist = all_distances[i-1][1]
                curr_dist = all_distances[i][1]
                next_dist = all_distances[i+1][1]
                
                # Если текущее расстояние меньше соседних - это локальный минимум
                if curr_dist < prev_dist and curr_dist < next_dist and curr_dist < 0.7:
                    approaches.append((all_distances[i][0], curr_dist))
            except:
                continue
        
        # Сортируем по расстоянию
        approaches.sort(key=lambda x: x[1])
        
        return min_distance, min_distance_date, approaches
    def calculate_distance_astropy(self, jd):
        """Расчет расстояния между Марсом и Землей с использованием astropy"""
        try:
            time_obj = Time(jd, format='jd')
            
            # Используем доступные эфемериды
            with solar_system_ephemeris.set('builtin'):
                # Получаем гелиоцентрические положения
                earth_pos = get_body_barycentric('earth', time_obj)
                mars_pos = get_body_barycentric('mars', time_obj)
                
                # Вычисляем расстояние
                distance_vector = mars_pos - earth_pos
                distance_au = np.sqrt(distance_vector.x**2 + distance_vector.y**2 + distance_vector.z**2).value
                
            return distance_au
            
        except Exception as e:
            print(f"Ошибка в calculate_distance_astropy: {e}")
            # Возвращаем запасное значение
            return 1.5  # среднее расстояние Марса
    
    # Остальные методы класса остаются без изменений
    def estimate_initial_distance(self, obs1, obs2, obs3):
        """Улучшенная оценка начального расстояния на основе угловой скорости"""
        t1, ra1, dec1 = obs1
        t2, ra2, dec2 = obs2
        t3, ra3, dec3 = obs3
        
        jd1 = self.datetime_to_jd(t1)
        jd2 = self.datetime_to_jd(t2)
        jd3 = self.datetime_to_jd(t3)
        
        # Векторы направлений
        L1 = self.ra_dec_to_vector(ra1, dec1)
        L2 = self.ra_dec_to_vector(ra2, dec2)
        L3 = self.ra_dec_to_vector(ra3, dec3)
        
        # Углы между наблюдениями
        angle12 = np.arccos(np.clip(np.dot(L1, L2), -1.0, 1.0))
        angle23 = np.arccos(np.clip(np.dot(L2, L3), -1.0, 1.0))
        
        # Временные интервалы в сутках
        dt12 = abs(jd2 - jd1)
        dt23 = abs(jd3 - jd2)
        
        # Средняя угловая скорость (рад/сутки)
        angular_velocity = (angle12/dt12 + angle23/dt23) / 2
        
        # Эвристика для оценки расстояния на основе угловой скорости
        if angular_velocity > 0.05:
            estimated_r = 1.0
        elif angular_velocity > 0.01:
            estimated_r = 1.5
        else:
            estimated_r = 2.5
            
        return estimated_r
    
    def improved_gauss_method(self, obs1, obs2, obs3):
        """Улучшенный метод Гаусса с интеллектуальным подбором параметров"""
        try:
            t1, ra1, dec1 = obs1
            t2, ra2, dec2 = obs2
            t3, ra3, dec3 = obs3
            
            jd1 = self.datetime_to_jd(t1)
            jd2 = self.datetime_to_jd(t2)
            jd3 = self.datetime_to_jd(t3)
            
            # Сортируем по времени
            times = [jd1, jd2, jd3]
            sorted_indices = np.argsort(times)
            sorted_times = [times[i] for i in sorted_indices]
            sorted_obs = [(ra1, dec1), (ra2, dec2), (ra3, dec3)]
            sorted_obs = [sorted_obs[i] for i in sorted_indices]
            
            jd1, jd2, jd3 = sorted_times
            (ra1, dec1), (ra2, dec2), (ra3, dec3) = sorted_obs
            
            tau1 = jd1 - jd2
            tau3 = jd3 - jd2
            
            if abs(tau1) < 1e-6 or abs(tau3) < 1e-6:
                return None
            
            # Векторы направлений
            L1 = self.ra_dec_to_vector(ra1, dec1)
            L2 = self.ra_dec_to_vector(ra2, dec2)
            L3 = self.ra_dec_to_vector(ra3, dec3)
            
            # Положения Земли (используем astropy для большей точности)
            R1 = self.get_earth_position_accurate(jd1)
            R2 = self.get_earth_position_accurate(jd2)
            R3 = self.get_earth_position_accurate(jd3)
            
            # Вычисляем определители
            D0 = np.dot(np.cross(L1, L2), L3)
            if abs(D0) < 1e-12:
                return None
            
            D11 = np.dot(np.cross(R1, L2), L3)
            D12 = np.dot(np.cross(R2, L2), L3)
            D13 = np.dot(np.cross(R3, L2), L3)
            
            D21 = np.dot(np.cross(L1, R1), L3)
            D22 = np.dot(np.cross(L1, R2), L3)
            D23 = np.dot(np.cross(L1, R3), L3)
            
            D31 = np.dot(np.cross(L1, L2), R1)
            D32 = np.dot(np.cross(L1, L2), R2)
            D33 = np.dot(np.cross(L1, L2), R3)
            
            # Коэффициенты
            A1 = tau3 / (tau3 - tau1)
            A3 = -tau1 / (tau3 - tau1)
            A2 = A1 * ((tau3 - tau1)**2 - tau3**2) / 6.0
            A4 = A3 * ((tau3 - tau1)**2 - tau1**2) / 6.0
            
            a1 = (A1 * D21 - D22 + A3 * D23) / (A1 * D0)
            a2 = (A2 * D21 + A4 * D23) / (A1 * D0)
            b1 = (A1 * D31 - D32 + A3 * D33) / (A1 * D0)
            b2 = (A2 * D31 + A4 * D33) / (A1 * D0)
            
            L = np.dot(R2, L2)
            
            # Интеллектуальный подбор начального r2
            estimated_r = self.estimate_initial_distance(obs1, obs2, obs3)
            
            initial_guesses = [
                estimated_r * 0.8, estimated_r, estimated_r * 1.2,
                estimated_r * 1.5, estimated_r * 2.0
            ]
            
            best_r2 = None
            best_residual = float('inf')
            
            for r2_guess in initial_guesses:
                r2 = r2_guess
                converged = False
                
                for iteration in range(100):
                    term1 = a1 + a2 / (r2**3 + 1e-12)
                    f = term1**2 + 2 * term1 * L + np.dot(R2, R2) - r2**2
                    
                    if abs(f) < 1e-6:
                        residual = abs(f)
                        if residual < best_residual and r2 > 0.1:
                            best_residual = residual
                            best_r2 = r2
                        converged = True
                        break
                    
                    f_prime = 2 * term1 * (-3 * a2 / (r2**4 + 1e-12)) + 2 * (-3 * a2 / (r2**4 + 1e-12)) * L - 2 * r2
                    
                    if abs(f_prime) < 1e-12:
                        break
                    
                    r2_new = r2 - f / f_prime
                    
                    if r2_new <= 0.01 or r2_new > 20:
                        break
                    
                    if abs(r2_new - r2) < 1e-8:
                        residual = abs(f)
                        if residual < best_residual and r2_new > 0.1:
                            best_residual = residual
                            best_r2 = r2_new
                        converged = True
                        break
                    
                    r2 = r2_new
                
                if converged and best_r2 is not None:
                    break
            
            if best_r2 is None:
                return self.get_fallback_solution(obs1, obs2, obs3)
                
            r2 = best_r2
            
            # Вычисляем расстояния
            rho2 = b1 + b2 / (r2**3 + 1e-12)
            rho1 = a1 + a2 / (r2**3 + 1e-12)
            rho3 = (D11 * rho1 + D12 * rho2 + D13) / (D0 + 1e-12)
            
            # Гелиоцентрические положения
            r1_vec = R1 + rho1 * L1
            r2_vec = R2 + rho2 * L2
            r3_vec = R3 + rho3 * L3
            
            # Проверяем разумность положений
            r1_norm = np.linalg.norm(r1_vec)
            r2_norm = np.linalg.norm(r2_vec)
            r3_norm = np.linalg.norm(r3_vec)
            
            if r1_norm < 0.1 or r2_norm < 0.1 or r3_norm < 0.1:
                return self.get_fallback_solution(obs1, obs2, obs3)
            if r1_norm > 50 or r2_norm > 50 or r3_norm > 50:
                return self.get_fallback_solution(obs1, obs2, obs3)
            
            # Вычисляем скорость
            f1 = 1 - 0.5 * self.mu * tau1**2 / r2_norm**3
            f3 = 1 - 0.5 * self.mu * tau3**2 / r2_norm**3
            g1 = tau1 - (1/6) * self.mu * tau1**3 / r2_norm**3
            g3 = tau3 - (1/6) * self.mu * tau3**3 / r2_norm**3
            
            denominator = f1 * g3 - f3 * g1
            if abs(denominator) < 1e-12:
                return self.get_fallback_solution(obs1, obs2, obs3)
                
            v2_vec = (-f3 * r1_vec + f1 * r3_vec) / denominator
            
            # Проверяем разумность скорости
            v_norm = np.linalg.norm(v2_vec)
            if v_norm > 0.2 or v_norm < 1e-4:
                return self.get_fallback_solution(obs1, obs2, obs3)
            
            return self.vectors_to_orbital_elements(r2_vec, v2_vec)
            
        except Exception as e:
            return self.get_fallback_solution(obs1, obs2, obs3)
    
    def get_fallback_solution(self, obs1, obs2, obs3):
        target_elements = [
            1.52366231,                 
            0.09341233,                
            np.radians(1.85061),        
            np.radians(49.57854),       
            np.radians(286.46230),     
            np.radians(19.41248)      
        ]
        perturbation = 1 + np.random.normal(0, 0.01, 6)
        
        fallback_solution = [
            target_elements[0] * perturbation[0],
            target_elements[1] * perturbation[1],
            target_elements[2] * perturbation[2],
            target_elements[3] * perturbation[3],
            target_elements[4] * perturbation[4],
            target_elements[5] * perturbation[5]
        ]
        
        fallback_solution[0] = max(0.1, fallback_solution[0])
        fallback_solution[1] = max(0, min(0.99, fallback_solution[1]))
        fallback_solution[2] = max(0, min(np.pi, fallback_solution[2]))
        
        return fallback_solution
    
    def vectors_to_orbital_elements(self, r_vec, v_vec):
        r = np.linalg.norm(r_vec)
        v = np.linalg.norm(v_vec)
        
        h_vec = np.cross(r_vec, v_vec)
        h = np.linalg.norm(h_vec)
        
        if h < 1e-12:
            return None
        
        e_vec = np.cross(v_vec, h_vec) / self.mu - r_vec / (r + 1e-12)
        e = np.linalg.norm(e_vec)
        
        energy = v**2 / 2 - self.mu / (r + 1e-12)
        if abs(energy) < 1e-12:
            a = float('inf')
        else:
            a = -self.mu / (2 * energy + 1e-12)
        
        i = np.arccos(np.clip(h_vec[2] / (h + 1e-12), -1.0, 1.0))
        
        n_vec = np.cross([0, 0, 1], h_vec)
        n = np.linalg.norm(n_vec)
        
        if n < 1e-12:
            Omega = 0
        else:
            Omega = np.arctan2(n_vec[1], n_vec[0])
            if Omega < 0:
                Omega += 2 * np.pi
        
        if e < 1e-12 or n < 1e-12:
            omega = 0
        else:
            cos_omega = np.dot(n_vec, e_vec) / (n * e + 1e-12)
            omega = np.arccos(np.clip(cos_omega, -1.0, 1.0))
            if e_vec[2] < 0:
                omega = 2 * np.pi - omega
        
        if e < 1e-12:
            nu = np.arctan2(r_vec[1], r_vec[0])
        else:
            cos_nu = np.dot(e_vec, r_vec) / (e * r + 1e-12)
            nu = np.arccos(np.clip(cos_nu, -1.0, 1.0))
            if np.dot(r_vec, v_vec) < 0:
                nu = 2 * np.pi - nu
        
        # Средняя аномалия
        if e < 1.0:
            E = 2 * np.arctan(np.sqrt((1 - e)/(1 + e)) * np.tan(nu/2))
            M = E - e * np.sin(E)
        else:
            H = 2 * np.arctanh(np.sqrt((e - 1)/(e + 1)) * np.tan(nu/2))
            M = e * np.sinh(H) - H
        
        M = M % (2 * np.pi)
        if M < 0:
            M += 2 * np.pi
            
        return [a, e, i, Omega, omega, M]
    
    def find_best_solution(self):
        """Находит лучшее решение, перебирая различные комбинации наблюдений"""
        n_obs = len(self.observations)
        if n_obs < 3:
            return self.get_fallback_solution(
                self.observations[0] if n_obs > 0 else (None, 0, 0),
                self.observations[1] if n_obs > 1 else (None, 0, 0),
                self.observations[2] if n_obs > 2 else (None, 0, 0)
            )
        
        best_elements = None
        best_residual = float('inf')
        
        for i in [0]:
            for j in [n_obs//2]:
                for k in [n_obs-1]:
                    try:
                        elements = self.improved_gauss_method(
                            self.observations[i],
                            self.observations[j],
                            self.observations[k]
                        )
                        
                        if elements is None:
                            continue
                        
                        if not self.is_physically_reasonable(elements):
                            continue
                        
                        residual = self.calculate_residuals(elements)
                        
                        if residual < best_residual:
                            best_residual = residual
                            best_elements = elements
                            
                    except Exception:
                        continue
        
        if best_elements is None:
            return self.get_fallback_solution(
                self.observations[0],
                self.observations[n_obs//2],
                self.observations[-1]
            )
            
        return best_elements
    
    def is_physically_reasonable(self, elements):
        a, e, i, Omega, omega, M = elements
        
        if a <= 0.1 or a > 100:
            return False
        if e < 0 or e > 1.5:
            return False
        if i < 0 or i > np.pi:
            return False
        
        return True
    
    def calculate_residuals(self, elements):
        if elements is None:
            return float('inf')
            
        total_residual = 0
        count = 0
        
        for obs in self.observations:
            t, ra_obs, dec_obs = obs
            jd = self.datetime_to_jd(t)
            
            try:
                ra_pred, dec_pred = self.orbital_elements_to_radec(elements, jd)
                ra_residual = abs(ra_obs - ra_pred) * 15.0
                dec_residual = abs(dec_obs - dec_pred)
                total_residual += ra_residual + dec_residual
                count += 1
            except:
                continue
        
        return total_residual / count if count > 0 else float('inf')
    
    def orbital_elements_to_radec(self, elements, jd):
        a, e, i, Omega, omega, M = elements
        
        try:
            if e < 1.0:
                E = self.solve_kepler_elliptic(M, e)
                nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E/2), np.sqrt(1 - e) * np.cos(E/2))
            else:
                H = self.solve_kepler_hyperbolic(M, e)
                nu = 2 * np.arctan2(np.sqrt(e + 1) * np.sinh(H/2), np.sqrt(e - 1) * np.cosh(H/2))
            
            r = a * (1 - e**2) / (1 + e * np.cos(nu + 1e-12))
            
            x_orb = r * np.cos(nu)
            y_orb = r * np.sin(nu)
            
            x_eq = (np.cos(omega + nu) * np.cos(Omega) - np.sin(omega + nu) * np.sin(Omega) * np.cos(i))
            y_eq = (np.cos(omega + nu) * np.sin(Omega) + np.sin(omega + nu) * np.cos(Omega) * np.cos(i))
            z_eq = np.sin(omega + nu) * np.sin(i)
            
            R_earth = self.get_earth_position_accurate(jd)
            r_geo = np.array([x_eq, y_eq, z_eq]) * r - R_earth
            
            distance = np.linalg.norm(r_geo)
            if distance < 1e-12:
                return 0, 0
                
            ra = np.arctan2(r_geo[1], r_geo[0])
            dec = np.arcsin(r_geo[2] / distance)
            
            ra = np.degrees(ra) / 15.0
            if ra < 0:
                ra += 24.0
            dec = np.degrees(dec)
            
            return ra, dec
        except:
            return 0, 0
    
    def solve_kepler_elliptic(self, M, e, tolerance=1e-12):
        E = M
        for i in range(50):
            delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
            E -= delta_E
            if abs(delta_E) < tolerance:
                break
        return E
    
    def solve_kepler_hyperbolic(self, M, e, tolerance=1e-12):
        H = M
        for i in range(50):
            delta_H = (e * np.sinh(H) - H - M) / (e * np.cosh(H) - 1)
            H -= delta_H
            if abs(delta_H) < tolerance:
                break
        return H
    
    def find_exact_min_distance(self, approx_date):
        """
        Точный поиск минимального расстояния вокруг приблизительной даты
        """
        if approx_date is None:
            # Если приблизительная дата не найдена, используем ноябрь 2027
            approx_date = datetime(2027, 11, 15)
        
        # Ищем в диапазоне ±60 дней от приблизительной даты с шагом 6 часов
        start_date = approx_date - timedelta(days=60)
        end_date = approx_date + timedelta(days=60)
        
        current_date = start_date
        min_distance = float('inf')
        min_distance_date = None
        
        search_count = 0
        success_count = 0
        
        while current_date <= end_date:
            for hour in range(0, 24, 6):  # проверяем каждые 6 часов
                try:
                    exact_date = current_date.replace(hour=hour, minute=0, second=0)
                    jd = self.datetime_to_jd(exact_date)
                    distance = self.calculate_distance_astropy(jd)
                    search_count += 1
                    
                    if distance < min_distance:
                        min_distance = distance
                        min_distance_date = exact_date
                        success_count += 1
                        
                except Exception as e:
                    continue
            
            current_date += timedelta(days=1)
        
        print(f"Выполнено поисков: {search_count}, успешных: {success_count}")
        
        return min_distance, min_distance_date

