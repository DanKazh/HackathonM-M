from typing import List, Dict, Any, Tuple
import numpy as np
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric
from astropy import units as u
from astropy import constants as const
from datetime import datetime, timedelta


class OrbitDetermination:
    def __init__(self):
        self.observations = []  
        solar_system_ephemeris.set('de432s') 

    def add_observation(self, time_str: str, ra_hours: float, dec_deg: float):
        """
        Добавить наблюдение.
        RA в часах, Dec в градусах.
        """
        self.observations.append((time_str, ra_hours, dec_deg))

    def _ra_dec_to_unit_vector(self, ra_hours: float, dec_deg: float) -> np.ndarray:
        """Преобразовать RA (часы) и Dec (градусы) в единичный вектор направления."""
        ra_rad = np.radians(ra_hours * 15.0)  # 1 час = 15 градусов
        dec_rad = np.radians(dec_deg)
        x = np.cos(dec_rad) * np.cos(ra_rad)
        y = np.cos(dec_rad) * np.sin(ra_rad)
        z = np.sin(dec_rad)
        return np.array([x, y, z])

    def _get_earth_position(self, time_str: str) -> np.ndarray:
        """Получить гелиоцентрический вектор Земли в а.е. на момент времени."""
        t = Time(time_str, scale='utc')
        earth_pos = get_body_barycentric('earth', t)
        # Преобразуем из метров в астрономические единицы
        au_in_m = const.au.to(u.m).value
        return np.array([earth_pos.x.to(u.m).value,
                         earth_pos.y.to(u.m).value,
                         earth_pos.z.to(u.m).value]) / au_in_m

    def _get_earth_position_at_jd(self, jd: float) -> np.ndarray:
        """Получить гелиоцентрический вектор Земли в а.е. на момент JD."""
        t = Time(jd, format='jd', scale='utc')
        earth_pos = get_body_barycentric('earth', t)
        au_in_m = const.au.to(u.m).value
        return np.array([earth_pos.x.to(u.m).value,
                         earth_pos.y.to(u.m).value,
                         earth_pos.z.to(u.m).value]) / au_in_m

    def _rv_to_orbital_elements(self, r_vec: np.ndarray, v_vec: np.ndarray, t_jd: float) -> List[float]:
        """
        Преобразует гелиоцентрические r и v в орбитальные элементы.
        Возвращает: [a, e, i, Ω, ω, M, epoch] — все в радианах, кроме a (а.е.)
        """
        k = 0.01720209895  # гауссова постоянная

        r = np.linalg.norm(r_vec)
        v = np.linalg.norm(v_vec)

        # Удельный момент импульса
        h_vec = np.cross(r_vec, v_vec)
        h = np.linalg.norm(h_vec)

        # Наклонение
        i = np.arccos(h_vec[2] / h)

        # Узловая линия
        n_vec = np.cross([0, 0, 1], h_vec)
        n = np.linalg.norm(n_vec)
        if n == 0:
            n_vec = np.array([1, 0, 0])
            n = 1

        # Долгота восходящего узла Ω
        if n_vec[1] >= 0:
            Omega = np.arccos(n_vec[0] / n)
        else:
            Omega = 2*np.pi - np.arccos(n_vec[0] / n)

        # Эксцентриситет
        e_vec = (np.cross(v_vec, h_vec) / (k**2)) - (r_vec / r)
        e = np.linalg.norm(e_vec)

        # Аргумент перицентра ω
        if e_vec[2] >= 0:
            omega = np.arccos(np.dot(n_vec, e_vec) / (n * e))
        else:
            omega = 2*np.pi - np.arccos(np.dot(n_vec, e_vec) / (n * e))

        # Большая полуось
        a = 1.0 / (2.0/r - v**2 / (k**2))

        # Истинная аномалия ν
        if np.dot(r_vec, v_vec) >= 0:
            nu = np.arccos(np.dot(e_vec, r_vec) / (e * r))
        else:
            nu = 2*np.pi - np.arccos(np.dot(e_vec, r_vec) / (e * r))

        # Эксцентрическая аномалия E
        if e < 1:
            E = 2 * np.arctan(np.sqrt((1 - e)/(1 + e)) * np.tan(nu/2))
            if E < 0:
                E += 2*np.pi
            M = E - e * np.sin(E)
        else:
            M = 0.0

        # Приводим углы к [0, 2π)
        i = i % (2*np.pi)
        Omega = Omega % (2*np.pi)
        omega = omega % (2*np.pi)
        M = M % (2*np.pi)

        return [a, e, i, Omega, omega, M, t_jd]

    def _orbital_elements_to_rv(self, elements: List[float], jd: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Преобразует орбитальные элементы в гелиоцентрические r и v.
        elements: [a, e, i, Ω, ω, M, epoch]
        """
        a, e, i, Omega, omega, M0, epoch_jd = elements
        k = 0.01720209895
        
        # Вычисляем среднюю аномалию на нужный момент времени
        n = k / np.sqrt(a**3)  # среднее движение
        delta_t = jd - epoch_jd
        M = M0 + n * delta_t
        M = M % (2*np.pi)
        
        # Решаем уравнение Кеплера для эксцентрической аномалии
        E = M
        for _ in range(50):  # итерации Ньютона
            E_new = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
            if abs(E_new - E) < 1e-12:
                break
            E = E_new
        
        # Вычисляем истинную аномалию
        nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E/2), np.sqrt(1 - e) * np.cos(E/2))
        
        # Расстояние до перицентра
        r = a * (1 - e * np.cos(E))
        
        # Положение в орбитальной плоскости
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)
        
        # Скорость в орбитальной плоскости
        p = a * (1 - e**2)
        h = np.sqrt(k**2 * p)
        vx_orb = - (k**2 / h) * np.sin(nu)
        vy_orb = (k**2 / h) * (e + np.cos(nu))
        
        # Преобразуем в гелиоцентрические координаты
        cos_omega = np.cos(omega)
        sin_omega = np.sin(omega)
        cos_Omega = np.cos(Omega)
        sin_Omega = np.sin(Omega)
        cos_i = np.cos(i)
        sin_i = np.sin(i)
        
        # Матрица преобразования
        P = np.array([
            cos_omega * cos_Omega - sin_omega * sin_Omega * cos_i,
            -sin_omega * cos_Omega - cos_omega * sin_Omega * cos_i,
            sin_Omega * sin_i
        ])
        
        Q = np.array([
            cos_omega * sin_Omega + sin_omega * cos_Omega * cos_i,
            -sin_omega * sin_Omega + cos_omega * cos_Omega * cos_i,
            -cos_Omega * sin_i
        ])
        
        r_vec = x_orb * P + y_orb * Q
        v_vec = vx_orb * P + vy_orb * Q
        
        return r_vec, v_vec

    def calculate_min_earth_distance(self, orbital_elements: List[float]) -> Dict[str, Any]:
        """
        Рассчитывает минимальное расстояние между Землей и кометой и время сближения.
        
        Args:
            orbital_elements: [a, e, i, Ω, ω, M, epoch_jd]
            
        Returns:
            Dict с минимальным расстоянием и временем сближения
        """
        # Ищем минимальное расстояние в течение следующих 2 лет от эпохи наблюдений
        start_jd = orbital_elements[6]  # эпоха наблюдений
        end_jd = start_jd + 365 * 2  # +2 года
        
        min_distance_au = float('inf')
        closest_approach_jd = start_jd
        
        # Поиск с шагом 1 день, затем уточнение
        step = 1.0
        for jd in np.arange(start_jd, end_jd, step):
            # Положение кометы
            r_comet, _ = self._orbital_elements_to_rv(orbital_elements, jd)
            
            # Положение Земли
            r_earth = self._get_earth_position_at_jd(jd)
            
            # Расстояние между кометой и Землей
            distance = np.linalg.norm(r_comet - r_earth)
            
            if distance < min_distance_au:
                min_distance_au = distance
                closest_approach_jd = jd
        
        # Уточняем поиск вокруг найденного момента с меньшим шагом
        refine_start = closest_approach_jd - 5
        refine_end = closest_approach_jd + 5
        refine_step = 0.1
        
        for jd in np.arange(refine_start, refine_end, refine_step):
            r_comet, _ = self._orbital_elements_to_rv(orbital_elements, jd)
            r_earth = self._get_earth_position_at_jd(jd)
            distance = np.linalg.norm(r_comet - r_earth)
            
            if distance < min_distance_au:
                min_distance_au = distance
                closest_approach_jd = jd
        
        # Преобразуем JD в datetime
        closest_approach_time = Time(closest_approach_jd, format='jd').datetime
        
        # Конвертируем а.е. в км
        au_in_km = 149597870.7
        min_distance_km = min_distance_au * au_in_km
        
        return {
            'min_distance_km': min_distance_km,
            'min_distance_au': min_distance_au,
            'closest_approach_time': closest_approach_time
        }

    def gauss_method_corrected(self, indices: Tuple[int, int, int] = None) -> List[float]:
        """
        Основной метод определения орбиты по методу Гаусса
        """
        if len(self.observations) < 3:
            raise ValueError("Need at least 3 observations.")

        if indices is None:
            indices = (10, 21, 32)  # равномерно распределенные наблюдения

        i1, i2, i3 = indices

        if not (0 <= i1 < i2 < i3 < len(self.observations)):
            raise ValueError("Invalid observation indices.")

        # Извлекаем данные
        t1_str, ra1, dec1 = self.observations[i1]
        t2_str, ra2, dec2 = self.observations[i2]
        t3_str, ra3, dec3 = self.observations[i3]

        t1 = Time(t1_str).jd
        t2 = Time(t2_str).jd
        t3 = Time(t3_str).jd

        rho1_hat = self._ra_dec_to_unit_vector(ra1, dec1)
        rho2_hat = self._ra_dec_to_unit_vector(ra2, dec2)
        rho3_hat = self._ra_dec_to_unit_vector(ra3, dec3)

        R1 = self._get_earth_position(t1_str)
        R2 = self._get_earth_position(t2_str)
        R3 = self._get_earth_position(t3_str)

        tau1 = t1 - t2
        tau3 = t3 - t2

        # Вычисление D-матрицы
        p = np.cross(rho2_hat, rho3_hat)
        q = np.cross(rho1_hat, rho3_hat)
        r = np.cross(rho1_hat, rho2_hat)

        D0 = np.dot(rho1_hat, p)
        if abs(D0) < 1e-12:
            raise ValueError("Observations are coplanar or too close.")

        D = np.array([
            np.dot(R1, p),
            np.dot(R2, q),
            np.dot(R3, r)
        ]) / D0

        A = D[0]
        B = -D[1]
        C = D[2]

        # Итерации по r2
        k = 0.01720209895
        r2 = 3.0  # начальное приближение

        converged = False
        for _ in range(50):
            x = 1.0 / r2

            f1 = 1 - 0.5 * (tau1**2) * (x**3)
            f3 = 1 - 0.5 * (tau3**2) * (x**3)
            g1 = tau1 * (1 - (tau1**2) * (x**3) / 6.0)
            g3 = tau3 * (1 - (tau3**2) * (x**3) / 6.0)

            denom = f1 * g3 - f3 * g1
            if abs(denom) < 1e-14:
                break

            rho2 = (f3 * A - f1 * C) / denom
            if rho2 <= 0:
                rho2 = 0.1

            r2_new = np.linalg.norm(R2 + rho2 * rho2_hat)

            if abs(r2_new - r2) < 1e-12:
                r2 = r2_new
                converged = True
                break
            r2 = r2_new

        if not converged:
            return None

        x = 1.0 / r2
        f1 = 1 - 0.5 * (tau1**2) * (x**3)
        f3 = 1 - 0.5 * (tau3**2) * (x**3)
        g1 = tau1 * (1 - (tau1**2) * (x**3) / 6.0)
        g3 = tau3 * (1 - (tau3**2) * (x**3) / 6.0)
        rho2 = (f3 * A - f1 * C) / (f1 * g3 - f3 * g1)

        r2_vec = R2 + rho2 * rho2_hat
        v2_vec = (f3 * (R1 + rho2 * rho1_hat) - f1 * (R3 + rho2 * rho3_hat)) / (f1 * g3 - f3 * g1)

        return self._rv_to_orbital_elements(r2_vec, v2_vec, t2)

    def print_orbital_elements(self, elements: List[float]):
        """Вспомогательный метод для вывода орбитальных элементов"""
        if elements is None:
            print("Не удалось определить орбиту.")
            return
        a, e, i, Omega, omega, M, epoch = elements
        print(f"Большая полуось (a):      {a:.6f} а.е.")
        print(f"Эксцентриситет (e):       {e:.6f}")
        print(f"Наклонение (i):           {np.degrees(i):.6f}°")
        print(f"Долгота узла (Ω):         {np.degrees(Omega):.6f}°")
        print(f"Аргумент перицентра (ω):  {np.degrees(omega):.6f}°")
        print(f"Средняя аномалия (M):     {np.degrees(M):.6f}°")
        print(f"Эпоха (JD):               {epoch:.6f}")