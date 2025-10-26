import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta
import base64
import tempfile
import os
from astropy.time import Time
from astropy.coordinates import get_body_barycentric
from astropy import units as u

class OrbitVisualizer:
    def __init__(self):
        self.fig = None
        self.ax = None
        self.animation = None

    def create_orbit_animation(
        self,
        a: float,               # большая полуось, AU
        e: float,               # эксцентриситет
        i: float,               # наклонение, рад
        Omega: float,           # долгота восходящего узла, рад
        omega: float,           # аргумент перицентра, рад
        M0: float,              # средняя аномалия на эпоху epoch, рад
        epoch: datetime,        # эпоха, на которую задана M0
        close_approach_time: datetime,
        duration_days: int = 730,
        frames: int = 100
    ) -> bytes:
        """
        Создаёт анимацию орбиты объекта и Земли и возвращает её как bytes (GIF).
        """
        fig = None
        try:
            start_date = close_approach_time - timedelta(days=duration_days // 2)
            frame_dates = [
                start_date + timedelta(days=int(duration_days * i / frames))
                for i in range(frames)
            ]
            astropy_times = Time(frame_dates)

            # Положение Земли
            earth_positions = np.array([
                get_body_barycentric('earth', t).xyz.to(u.AU).value for t in astropy_times
            ])

            # Положение объекта
            object_positions = np.array([
                self._position_from_elements(a, e, i, Omega, omega, M0, epoch, t)
                for t in frame_dates
            ])

            # Минимальное расстояние
            distances = np.linalg.norm(earth_positions - object_positions, axis=1)
            min_dist_idx = int(np.argmin(distances))
            min_distance_au = distances[min_dist_idx]

            # Фоновые орбиты
            dense_step = max(1, duration_days // 365)
            dense_dates = [start_date + timedelta(days=d) for d in range(0, duration_days, dense_step)]
            earth_orbit = np.array([
                get_body_barycentric('earth', Time(t)).xyz.to(u.AU).value for t in dense_dates
            ])
            object_orbit = np.array([
                self._position_from_elements(a, e, i, Omega, omega, M0, epoch, t) for t in dense_dates
            ])

            # Кадры с паузой на минимуме
            pause_frames = 10
            extended_indices = []
            for idx in range(frames):
                extended_indices.append(idx)
                if idx == min_dist_idx:
                    extended_indices.extend([idx] * pause_frames)

            # Создаём график
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')

            max_range = max(
                np.max(np.abs(object_orbit)),
                np.max(np.abs(earth_orbit)),
                2.0
            ) * 1.1

            ax.set_xlim([-max_range, max_range])
            ax.set_ylim([-max_range, max_range])
            ax.set_zlim([-max_range / 2, max_range / 2])

            ax.set_xlabel('X (AU)')
            ax.set_ylabel('Y (AU)')
            ax.set_zlabel('Z (AU)')
            ax.set_title(f'Орбиты объекта и Земли\nМин. расстояние: {min_distance_au:.3f} AU')

            ax.plot(earth_orbit[:, 0], earth_orbit[:, 1], earth_orbit[:, 2], 'b-', alpha=0.3, label='Орбита Земли')
            ax.plot(object_orbit[:, 0], object_orbit[:, 1], object_orbit[:, 2], 'r-', alpha=0.3, label='Орбита объекта')
            ax.plot([0], [0], [0], 'yo', markersize=20, label='Солнце')

            earth_point, = ax.plot([], [], [], 'bo', markersize=10)
            object_point, = ax.plot([], [], [], 'ro', markersize=8)
            min_marker, = ax.plot([], [], [], 'g*', markersize=15, label='Мин. расстояние')

            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)

            def animate(idx):
                e_pos = earth_positions[idx]
                o_pos = object_positions[idx]
                earth_point.set_data([e_pos[0]], [e_pos[1]])
                earth_point.set_3d_properties([e_pos[2]])
                object_point.set_data([o_pos[0]], [o_pos[1]])
                object_point.set_3d_properties([o_pos[2]])
                if idx == min_dist_idx:
                    min_marker.set_data([o_pos[0]], [o_pos[1]])
                    min_marker.set_3d_properties([o_pos[2]])
                else:
                    min_marker.set_data([], [])
                    min_marker.set_3d_properties([])
                return earth_point, object_point, min_marker

            animation = FuncAnimation(
                fig, animate, frames=extended_indices,
                interval=100, blit=False, repeat=True
            )

            # Сохраняем в байты
            with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp:
                tmp_path = tmp.name

            animation.save(tmp_path, writer='pillow', fps=10, dpi=80)

            with open(tmp_path, 'rb') as f:
                gif_bytes = f.read()

            os.unlink(tmp_path)
            return gif_bytes

        except Exception as e:
            print(f"Ошибка при создании анимации: {e}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            if fig is not None:
                plt.close(fig)  # Гарантированно закрываем фигуру
                
    def _position_from_elements(
        self,
        a: float,
        e: float,
        i: float,
        Omega: float,
        omega: float,
        M0: float,
        epoch_M0: datetime,
        t: datetime
    ) -> np.ndarray:
        """
        Вычисляет положение объекта в эклиптической системе J2000 на дату t.
        Вход: M0 — средняя аномалия на эпоху epoch_M0.
        Выход: [x, y, z] в AU.
        """
        # Время от эпохи M0 в годах
        dt_seconds = (t - epoch_M0).total_seconds()
        dt_years = dt_seconds / (365.25 * 24 * 3600)

        # Среднее движение (рад/год)
        n = np.sqrt(4 * np.pi**2 / a**3)

        # Средняя аномалия на дату t
        M = M0 + n * dt_years
        M = (M + np.pi) % (2 * np.pi) - np.pi  # нормализация в [-π, π]

        # Решение уравнения Кеплера: M = E - e*sin(E)
        E = M
        for _ in range(10):
            E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))

        # Истинная аномалия
        sin_nu = (np.sqrt(1 - e**2) * np.sin(E)) / (1 - e * np.cos(E))
        cos_nu = (np.cos(E) - e) / (1 - e * np.cos(E))
        nu = np.arctan2(sin_nu, cos_nu)

        # Расстояние до Солнца
        r = a * (1 - e * np.cos(E))

        # Координаты в орбитальной плоскости
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)

        # Матрица поворота к эклиптической системе
        cos_i, sin_i = np.cos(i), np.sin(i)
        cos_Omega, sin_Omega = np.cos(Omega), np.sin(Omega)
        cos_omega, sin_omega = np.cos(omega), np.sin(omega)

        x = x_orb * (cos_omega * cos_Omega - sin_omega * cos_i * sin_Omega) \
            - y_orb * (sin_omega * cos_Omega + cos_omega * cos_i * sin_Omega)
        y = x_orb * (cos_omega * sin_Omega + sin_omega * cos_i * cos_Omega) \
            + y_orb * (cos_omega * cos_i * cos_Omega - sin_omega * sin_Omega)
        z = x_orb * (sin_omega * sin_i) + y_orb * (cos_omega * sin_i)

        return np.array([x, y, z])

    def _animation_to_base64(self) -> str:
        try:
            with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp:
                tmp_path = tmp.name
            self.animation.save(tmp_path, writer='pillow', fps=10, dpi=80)
            with open(tmp_path, 'rb') as f:
                data = f.read()
            os.unlink(tmp_path)
            b64 = base64.b64encode(data).decode('utf-8')
            return f"data:image/gif;base64,{b64}"
        except Exception as e:
            print(f"Ошибка конвертации в base64: {e}")
            return ""