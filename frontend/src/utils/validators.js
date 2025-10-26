export function validateObservation(data) {
  const errors = {};

  if (!data.date) {
    errors.date = 'Дата обязательна';
  }

  if (data.ra === undefined || data.ra === null) {
    errors.ra = 'Прямое восхождение обязательно';
  } else if (data.ra < 0 || data.ra > 360) {
    errors.ra = 'Прямое восхождение должно быть от 0 до 360°';
  }

  if (data.dec === undefined || data.dec === null) {
    errors.dec = 'Склонение обязательно';
  } else if (data.dec < -90 || data.dec > 90) {
    errors.dec = 'Склонение должно быть от -90 до 90°';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}
